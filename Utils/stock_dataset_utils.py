

#############################################################
#
# Download historical data for a stock into a Panda Table
# 
#
#############################################################


import yfinance as yf
from Utils.write_error_to_Log import write_download_error_msg_to_Log
from datetime import datetime



####
# @Raw_feature_downloader
####

def get_historical_dataset_for_a_stock_helper(stock_NASDAQ_code):

	try:
		stock = yf.Ticker(stock_NASDAQ_code)
		hist = stock.history(period = "5y")
		return  hist

	except:
		return None

def get_historical_dataset_for_a_stock(stock_NASDAQ_code):
	
	

	dataset = get_historical_dataset_for_a_stock_helper(stock_NASDAQ_code)
	if dataset.empty or dataset is None:
		#to be honest, today's date doesn't really matter, since this function downloads the entire historical data set for this stock
		# also the keyword is null, because the function doesn't take in any extra argument
		today = datetime.today().strftime('%Y-%m-%d')
		write_download_error_msg_to_Log(today, stock_NASDAQ_code, "get_historical_dataset_for_a_stock", "null")
		return None

	else:
		return dataset
	


def get_dataset_for_a_stock_for_last_year(stock_NASDAQ_code):

	try:
		stock = yf.Ticker(stock_NASDAQ_code)
		hist = stock.history(period = "1y")
		return  hist

	except:
		return None
