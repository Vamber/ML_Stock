##################################################################################################
# 
# The premise of this File is turn different libarary into Logical and explicit function
# All the News relative Data retrival happens here 
#
##################################################################################################

from Utils.write_error_to_Log import write_download_error_msg_to_Log

from pygooglenews import GoogleNews

from Utils.lst_of_proxies import get_random_proxy_for_google_news

import datetime as DT

import pandas as pd

def get_news_metadata_df_from_a_keyword_on_a_particular_date_helper(keyword, date):

    try:
            year_month_day_lst = date.split("-")
            year = int(year_month_day_lst[0])
            month = int(year_month_day_lst[1])
            day = int(year_month_day_lst[2])
            day = DT.date(year, month, day)
            next_day = day + DT.timedelta(days=1)
            next_day = str(next_day)
            gn = GoogleNews(lang = 'en', country = 'US')

            #The intitle option force the keyword to be in the title of news, when searched
            s = gn.search("intitle:" + keyword, 
                from_= date, 
                to_ = next_day, 
                proxies=get_random_proxy_for_google_news())

            lst_news_data = s["entries"]
            numeber_of_news_found = len(lst_news_data)


            ######
            # so sometimes, for stock which aren't too relevant, it's totally possible that there --
            # is just no news about that stock. In this case, we just set "null" for those features, rather than having a 
            # empty data_frame
            ######
            if numeber_of_news_found == 0:
                one_row = {}
                one_row["title"] = "null"
                one_row["link"] = "null"
                one_row["published"] = "null"
                one_row["source"] = "null"
                one_row["total_news_today"] = 0
                
                df = pd.DataFrame([one_row])
                return df
            #############################################################################################


            refined_data = []

            for news in lst_news_data:
                one_row = {}
                one_row["title"] = news["title"]
                one_row["link"] = news["link"]
                one_row["published"] = news["published"]
                one_row["source"] = news["source"]["title"]
                one_row["total_news_today"] = numeber_of_news_found
                refined_data.append(one_row)

            df = pd.DataFrame(refined_data)

            return df
	

    except:
            return None


###
# 
###
#Handles Error and write to Log
def get_news_metadata_df_from_a_keyword_on_a_particular_date(stock_NASDAQ_code, date, keyword):

	data = get_news_metadata_df_from_a_keyword_on_a_particular_date_helper(keyword,date)

	if data is None:
		write_download_error_msg_to_Log(date, stock_NASDAQ_code, "get_news_metadata_df_from_a_keyword_on_a_particular_date" , keyword)
		return None

	else:
		return data






		





# THis function turns a particular article's url into a list of very small piece of sentence 

from bs4 import BeautifulSoup
import requests
def turn_article_url_into_list_of_sentence(url):

	link = url
	try:
		r = requests.get(link, verify=True, timeout=10) # 10 seconds
	except:
		r = 0
      
	if r == 0:
		return []

	soup = BeautifulSoup(r.text, 'html.parser')
	results = soup.find_all('p')
	text = [res.text for res in results]
	words = ' '.join(text).split()
	ARTICLE = ' '.join(words)
	ARTICLE = ARTICLE.replace(', ', '. ').replace("\n", ". ").split(". ")
	return ARTICLE














