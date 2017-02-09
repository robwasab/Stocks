from yahoo_finance import Share
from pprint import pprint
import datetime
import pickle
import time
import sys

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

name = sys.argv[0]
args = sys.argv[1:]

if len(args) > 0:
	stock_name = args[0]
	delta = 7
	if len(args) > 1:
		delta = int(args[1])
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
	except Exception as e:
		print e
		print '%sError:%s %s does not exist.'%(RED+UNDERLINE+BOLD, ENDC, stock_name)

else:
	print "%sUsage:\n%s stock_sym [another_stock_sym [another_stock_sym ...]]"%(RED+UNDERLINE,ENDC+BLUE+BOLD+'python '+name+ENDC)
