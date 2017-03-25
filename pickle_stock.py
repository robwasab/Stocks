import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from yahoo_finance import Share
from pprint import pprint
import numpy as np
import datetime
import pickle
import time
import sys
import pdb

HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[36m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
UNDERLINE = '\033[4m'

def pickle_stock(stock_name, delta):
	stop_date = time.strftime('%Y-%m-%d')
	convert = datetime.datetime.strptime(stop_date, '%Y-%m-%d') - datetime.timedelta(delta)
	start_date = datetime.datetime.strftime(convert, '%Y-%m-%d')
	try:
		stock = Share(stock_name)
		print 'Downloading %s from %s to %s'%(stock_name, start_date, stop_date)

		histo = stock.get_historical(start_date, stop_date)
		filename = '[%s][%d][%s]'%(stock_name.ljust(4), delta, stop_date)
		print filename
		outpu = open(filename, 'wb')
		pickle.dump(histo, outpu)
		outpu.close()
		return True
	except Exception as e:
		print e
		print '%sError:%s %s does not exist.'%(RED+UNDERLINE+BOLD, ENDC, stock_name)
		return False

def plot_stock(filename):
	try:
		fobj = open(filename, 'r')
		data = pickle.load(fobj)
		close_prices = []
		open_prices = []
		adj_close = []
		volumes = []
		dates = []
		high = []
		low = []
		for day in data:
			close_prices.append(float(day['Close']))
			open_prices.append(float(day['Open']))
			adj_close.append(float(day['Adj_Close']))
			volumes.append(int(day['Volume']))
			dates.append(datetime.datetime.strptime(day['Date'], '%Y-%m-%d'))
			high.append(float(day['High']))
			low.append(float(day['Low']))

		ax = plt.gca()
		years = mdates.YearLocator()   # every year
		months = mdates.MonthLocator()  # every month
		yearsFmt = mdates.DateFormatter('%m-%d\n%Y')

		# format the ticks
		ax.xaxis.set_major_locator(months)
		ax.xaxis.set_major_formatter(yearsFmt)
		ax.xaxis.set_minor_locator(months)

		plt.subplot(211)
		plt.plot(dates, close_prices)
		plt.subplot(212)
		plt.plot(dates, volumes, '.')
		plt.show()

		return True
	except Exception as e:
		print e
		return False

def usage():
	name = sys.argv[0]
	print UNDERLINE+CYAN+'Usage:'+ENDC+' python ' + name + ' ' + UNDERLINE + CYAN + 'stock symbol' + ENDC

if __name__ == '__main__':
	args = sys.argv[1:]
	name = args[0]

	if len(args) < 1:
		print RED+UNDERLINE+BOLD+'Error:'+ENDC+' Not enough arguments'
		usage()
		sys.exit(-1)

	downloaded = plot_stock(name)

	if not downloaded:
		if len(args) > 0:
			stock_name = name
			delta = 7
			if len(args) > 1:
				delta = int(args[1])
			ok = pickle_stock(stock_name, delta)
			if not ok:
				usage()
