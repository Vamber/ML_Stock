



#########################################################################################
#
# The files turns the sentiment model into a logical function that's ready to be used
# The reason why this function exists as its own file is because we want this entire_software to
# more modulized, 
# Basically, whenever a better sentiment model from Hugging Face Transformers, it can be swapped in here
# without modifying a whole a lot of code
#
#########################################################################################





### basic imports to make the Neural Nets Functional 
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import warnings
warnings.filterwarnings("ignore")

import os

dirname = os.path.dirname(__file__)

Path  =  os.path.join(dirname, "HF_Transformers/mbart_large-financial_phrasebank")

# Let's load the model and the tokenizer 

tokenizer = AutoTokenizer.from_pretrained(Path)
model = AutoModelForSequenceClassification.from_pretrained(Path) 



def evaluate_sentiment_score_for_a_sentence(sentence):

	tokens = tokenizer.encode(sentence, return_tensors = "pt")

	sentiment_vector = model(tokens).logits.detach().numpy()[0] #it's a two D tensor apparently

	negative = round(sentiment_vector[0],2)

	neutral = round(sentiment_vector[1],2)

	positive =  round(sentiment_vector[2],2)
    
    #the sentiment vector has three elements, however, the negativity and positivity of a setenence
    #is not evaluated into a positive/negative number, but rather as a big/small absolute value
    #therefore, the final step here actually does the conversion.

    #for example, a very negative news "Tesla stock sucks ", would get the tensor [3,2,-1]
    #and we will make this function just return -3, to indicated to bad sentiment 

	if  neutral > positive and neutral > negative:
		return 0    
	if negative > positive :
		return -negative

	else:
		return positive

