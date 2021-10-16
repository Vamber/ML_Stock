##################################################################################################
# 
# The premise of this File is turn different libarary into Logical and explicit function
# All the News relative Data retrival happens here 
#
##################################################################################################

from GoogleNews import GoogleNews

from Utils.write_error_to_Log import write_download_error_msg_to_Log





###
# Raw Feature Downloader Function
###
# The function takes in the data in the form of Year Month Date 2021-07-09
# However, the original google news APi takes in form Month/Date/Year, so a conversion is needed
def get_all_news_metadata_from_a_keyword_on_a_particular_date_helper(keyword, date):

	try:
	#doing the Date conversion
		year_month_day_lst = date.split("-")
		year = year_month_day_lst[0]
		month = year_month_day_lst[1]
		day = year_month_day_lst[2]

		date = month + "/" + day + "/" + year
		searcher = GoogleNews(start = date, end = date)
		searcher.search(keyword)
		meta_data = searcher.result()
		return meta_data

	except:
		return None


#Handles Error and write to Log
def get_all_news_metadata_from_a_keyword_on_a_particular_date(stock_NASDAQ_code, date, keyword):

	data = get_all_news_metadata_from_a_keyword_on_a_particular_date_helper(keyword,date)

	if data == [] or data is None:
		write_download_error_msg_to_Log(date, stock_NASDAQ_code, "get_all_news_metadata_from_a_keyword_on_a_particular_date" , keyword)
		return None

	else:
		return data














###
# @Raw_feature_downloader Function
###
#get the number of news article pubushed about a certain keyword  
def get_the_number_of_news_published_pertaining_to_the_keyword_helper(keyword, date):
        #doing the Date conversion
	try:

		year_month_day_lst = date.split("-")
		year = year_month_day_lst[0]
		month = year_month_day_lst[1]
		day = year_month_day_lst[2]
		
		date = month + "/" + day + "/" + year
		searcher = GoogleNews(start = date, end = date)
		searcher.search(keyword)
		count = searcher.total_count()
		return count

	except:

		return None

#Handles the error and write to Log
def get_the_number_of_news_published_pertaining_to_the_keyword(stock_NASDAQ_code, date, keyword):
	
	
	count = get_the_number_of_news_published_pertaining_to_the_keyword_helper(keyword,date)

	if count is None:
		write_download_error_msg_to_Log(date, stock_NASDAQ_code, "get_the_number_of_news_published_pertaining_to_the_keyword", keyword)
		#This thing returns 0 if an error occurs
		return None
	
	
	else:
		
		return count 


		

















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














