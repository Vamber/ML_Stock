


from pytrends.request import TrendReq
import datetime as DT
from Utils.write_error_to_Log import write_download_error_msg_to_Log
from Utils.lst_of_proxies import get_random_lst_of_proxy_for_google_trend
from datetime import date

#####
#
# Description regarding to details of this function 
#
# This function here downloads the raw data for a keyword's google trend 
#
# The returned value from the function is a dataset (panda csv), not a number
#
# It downloads the trend (time (every hour) vs relative popularity score) relating to a keyword for the last 7 days 
#
#      The Time-Zone is CST (california) and the poluarity score is only for United State
#
#      This function has a relatively high chance of failure, because Google could modify it's http request API
#      Therefore, in case of failure, check with Pipy website to update the pytrends lib
#
####


###
# Raw Feature Downloader Function
###


def get_dataset_google_trend_score_for_keyword_helper(keyword, date):

  year_month_day_lst = date.split("-")
  year = int(year_month_day_lst[0])
  month = int(year_month_day_lst[1])
  day = int(year_month_day_lst[2])
  to_day = DT.date(year, month, day)
  from_day = to_day - DT.timedelta(days=6)


  keyword_lst = [keyword]

  
  try:
      pytrends = TrendReq(hl='en-US', tz=360,
                          timeout=(10,25),
			                    retries=5, 
                          backoff_factor=0.1,
			                    requests_args={'verify':True},
                          proxies=get_random_lst_of_proxy_for_google_trend()
                          )
      


      #pytrends.build_payload(keyword_lst, cat=0, timeframe="today 7-d", geo='US', gprop='')

      df = pytrends.get_historical_interest(keyword_lst, 
                                      year_start=from_day.year,
                                      month_start=from_day.month,
                                      day_start=from_day.day,
                                      hour_start=0,
                                      year_end=to_day.year,
                                      month_end=to_day.month,
                                      day_end=to_day.day,
                                      hour_end=23,
                                      geo="US", #it was US before
                                      gprop='',
                                      sleep=1
                                      )
      return df 

  except:
    return None




###
# the pytrend libaray is inconsistent with getting data, so we give it five attempts
# if it fails after five attempts, then we write it
###
def get_dataset_google_trend_score_for_keyword(stock_NASDAQ_code, date, keyword):
  df = None
  attempts = 5
  while ((df is None) and attempts > 0):
    df = get_dataset_google_trend_score_for_keyword_helper(keyword, date)
    attempts -= 1


  if df is None or df.empty:
    write_download_error_msg_to_Log(date, stock_NASDAQ_code, "get_dataset_google_trend_score_for_keyword" , keyword)
    return None

  else:
    return df



###
# this function is an useful helper function for computing the correlation between a kw's trend vs the stock price
#
# for example, if you are interestinted in the correlation between Bitcoin and Nvidia for the last two years, prior to 
#
# deciding if you should use bitcoin as a predictor for Nvidia 
#
###

def get_dataset_google_trend_score_for_keyword_in_last_3m(keyword):
  keyword_lst = [keyword]
  #try:
  try:
      pytrends = TrendReq(hl='en-US', tz=360,
                          timeout=(10,25),
			                    retries=5, 
                          backoff_factor=0.1,
			                    requests_args={'verify':True},
                          proxies=get_random_lst_of_proxy_for_google_trend(), 
                          
                          )
      


      #pytrends.build_payload(keyword_lst, cat=0, timeframe="today 7-d", geo='US', gprop='')

      pytrends.build_payload(keyword_lst, timeframe = "today 3-m", geo="US")
      df = pytrends.interest_over_time()
      return df 

  #except:
  except:
    return None



def get_related_kw(keyword):
  keyword_lst = [keyword]

  try:
      pytrends = TrendReq(hl='en-US', tz=360,
                          timeout=(10,25),
			                    retries=5, 
                          backoff_factor=0.1,
			                    requests_args={'verify':True},
                          proxies=get_random_lst_of_proxy_for_google_trend(), 
                          
                          )
      


      #pytrends.build_payload(keyword_lst, cat=0, timeframe="today 7-d", geo='US', gprop='')

      pytrends.build_payload(keyword_lst, timeframe = "today 3-m", geo="US")
      df_dic = pytrends.related_queries()
      df_top = df_dic[keyword]["top"]
      return list(df_top["query"])

  except:
    return []

