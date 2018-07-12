#This Formula Is an Iteration of the Simple Formula which Removes Bitcoin and Ethereum
import matplotlib.pyplot as plt
from lxml import html
import requests
from re import sub
from decimal import Decimal
import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from numpy import arange

#The initial value of the Index which is appended to the datapoints of the Index
c = 100
datapoints = []
datapoints.append(c)
#All of this code is an HTML scraper as this was the only way to get weekly percentage changes
#and Market Cap data. Hopefully, this index will be able to interact with our backend and pull
#that information directly
url = 'https://coinmarketcap.com/historical/'
urend = ['20170604','20170611','20170618','20170625','20170702','20170709',
'20170716','20170723','20170730','20170806','20170813','20170820','20170827',
'20170903','20170910','20170917','20170924','20171001','20171008','20171015',
'20171022','20171029','20171105','20171112','20171119','20171126','20171203',
'20171210','20171217','20171224','20171231','20180107','20180114','20180121',
'20180128','20180204','20180211','20180218','20180225','20180304','20180311',
'20180318','20180325','20180401','20180408','20180415','20180422','20180429',
'20180506','20180513','20180520','20180527','20180603','20180610','20180617',
'20180624','20180701','20180708']
dates = [datetime.datetime(2017, 05, 28)]
for num in urend:
	dates.append(datetime.datetime(int(num[0:4]),int(num[4:6]),int(num[6:8])))
#This is basically scraping the CoinMarketCap weekly snapshot html
for x in urend:
	page = requests.get(url + x)
	tree = html.fromstring(page.content)
	tic = tree.xpath('//td[@class="text-left col-symbol"]/text()')
	MC = tree.xpath('//td[@class="no-wrap market-cap text-right"]/text()')
	PC = tree.xpath('//td[@data-timespan="7d"]/text()')
	inc = 0
	teth = False
	#So the one thing we don't care about is stablecoins so this right here is to filter out stablecoins
	#perhaps it will be easier to do this because in our api we have types which has 'stablecoin' in it
	while not teth:
		if tic[inc] == 'USDT':
			teth = True
		else:
			inc = inc + 1
	MC100 = []
	PC100 = []
	count = 0
	#The inputs are then sanitized and placed into the weekly top 100 Market Caps for coins and their 
	#corresponding percentage changes
	while count < 102:
		if count != inc:
			MC100.append(Decimal(sub(r'[^\d.]', '', MC[count])))
			if '%' not in PC[count]:
				PC100.append(0)
			if '>' in PC[count]:
				PC100.append(9)
			else:
				PC100.append(Decimal(PC[count].strip('%'))/100)
		count = count + 1
	#This is the creative part that matters. Every week, or an arbitrary amount of time can be changed
	#based on coin data, we obtain a multiplier by factoring in percentage changes of the top 100 coins
	#weighted by market cap. This time, we removed the first two or Bitcoin and Ethereum.
	tMC = 0
	inc2 = 2
	while inc2 < 101:
		tMC = tMC + MC100[inc2]
		inc2 = inc2 + 1
	multiplier = 1
	count2 = 2
	while count2 < 101:
		div = MC100[count2]/tMC
		weight = 1 + (PC100[count2] * div)
		multiplier = multiplier*weight
		count2 = count2 + 1
	c = c * multiplier
	print(x)
	datapoints.append(c)
plt.plot(dates, datapoints, '-')
plt.title('1 Year Weekly CryptoCurrency Index Minus BTC & ETH')
plt.ylabel('Index Value')
plt.xlabel('Date')
plt.show()
