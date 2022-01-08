#
#  Whenever you see a file is called something like ....strategy.py
#  It is used for turning raw_features into processed features
#  No function in this file can establish socket connection (basicaly, can not use internet)
#
##




###
#This function just check if one particular is some variation of any word in lst_of_keyword
# for example, it would return true, if word = Nvidia's, and lst_of_keyword = ["NVIDIA", "GPU"]
###
def contained_by_keyword(word, lst_of_keyword):
	augmented_lst_of_keyword = []
	for keyword in lst_of_keyword:
		augmented_lst_of_keyword.append(keyword.lower())
	word = word.lower()
	for w in augmented_lst_of_keyword:
		if w in word:
			return True

###
# This functions check if a sentence mentions any keyword
###
def sentence_contains_keyword(sentence, lst_of_keyword):
	split_sentence = sentence.split(" ")
	for word in split_sentence:
		if contained_by_keyword(word, lst_of_keyword):
			return True


# Notice here I am importing from the absolute path when I am actually using a lib from the same directory 
# this could be bad engineering
from Utils.sentiment_model_2_func import evaluate_sentiment_score_for_a_sentence


def eval_sentiment_score_for_title(title):
	
	return round(evaluate_sentiment_score_for_a_sentence(title), 1)


####
# Refine a long setence to the portions where it just from its keyword
####
def refine_sentence_by_keywords(sentence, lst_of_keyword):
	min_setence_length = 5

	split_sentence = sentence.split(" ")
	key_word_first_appeared_index = 0
	for word in split_sentence:
		if contained_by_keyword(word, lst_of_keyword) :
			break
		key_word_first_appeared_index += 1

	refined_sentence = split_sentence[key_word_first_appeared_index:]

	if len(refined_sentence) >= min_setence_length:
		return ' '.join(refined_sentence)




def eval_sentiment_score_for_desc(desc, lst_of_keyword):
	refined_desc = refine_sentence_by_keywords(desc, lst_of_keyword)
	print(refined_desc)
	if refined_desc:
		return evaluate_sentiment_score_for_a_sentence(refined_desc)
	else:
		return 0.0



##
#The resulting lst only contains sentences starting with keyword
##
def refine_lst_of_sentence_by_keywords(lst_of_sentence, lst_of_keyword):
        results = []
        for sentence in lst_of_sentence:
                s = refine_sentence_by_keywords(sentence, lst_of_keyword)
                if s:
                        results.append(s)
        return results


def eval_sentiment_score_vector_for_lst_of_sentence(lst_of_sentence):
	return [evaluate_sentiment_score_for_a_sentence(s) for s in lst_of_sentence]



