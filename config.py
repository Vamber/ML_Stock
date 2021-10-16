############################################################################
#
# This file imports all logical-functions needed for the rest of this project
# 
#
# 1. All date format are consistent for the function Year Month Day 2018/12/01
# 
#
#
# 2. Import Hugging Face Transformers as logical function that's ready to be used. (After Line 100)
#
#
#
#
############################################################################








#from Utils.summarization_model_2_func import summarize_a_paragraph_into_a_sentence

#from Utils.sentiment_model_2_func import evaluate_sentiment_score_for_a_sentence


from Utils.google_news_utils import get_all_news_metadata_from_a_keyword_on_a_particular_date

from Utils.google_news_utils import get_the_number_of_news_published_pertaining_to_the_keyword

from Utils.google_news_utils import turn_article_url_into_list_of_sentence

from Utils.sentiment_scoring_strategy import eval_sentiment_score_for_title

from Utils.sentiment_scoring_strategy import eval_sentiment_score_for_desc

from Utils.google_trends_utils import get_dataset_google_trend_score_for_keyword

from Utils.stock_dataset_utils import get_historical_dataset_for_a_stock

#from Utils.sentiment_scoring_strategy import refine_lst_of_sentence_by_keywords

#from Utils.sentiment_scoring_strategy import eval_sentiment_score_vector_for_lst_of_sentence

company = "Netflix"

keyword = "Nvidia"

code = "NFLXERR"

date = "2023-1-5"



A = get_all_news_metadata_from_a_keyword_on_a_particular_date(code, date, keyword)
print(A)



B = get_dataset_google_trend_score_for_keyword(code, date, keyword)
print(B)

C = get_the_number_of_news_published_pertaining_to_the_keyword(code, date, keyword)
print(C)

D = get_historical_dataset_for_a_stock(code)
print(D)



print(str(v) + " " + "RTX 3090")
#dataset = get_historical_dataset_for_a_stock("NVDA")
#print(dataset)
#print(v)
#print(c)
h = get_the_number_of_news_published_pertaining_to_the_keyword("NVDA", "Nvidia", "2021-07-18")
print(h)









