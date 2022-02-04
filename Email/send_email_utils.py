
import smtplib
import os
from datetime import date
import pandas as pd
from os import path
import numpy as np

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
ROOT = "/home/vamber/ML_stock/"



def send_msg_to_receiver(msg, receiver_email):

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        email = EMAIL_ADDRESS
        pswd = EMAIL_PASSWORD
        smtp.login(email, pswd)

        subject = "[ML_STOCK] Daily Status  " + str(date.today())
        body = msg
    
        msg = f'Subject: {subject} \n\n {body}'

        smtp.sendmail(email, receiver_email, msg)



##
## for each expert, print out the stocks was chosen
## and the money delta from the last 5 work days
def get_expert_msg(expert_class):
    E = expert_class()
    df_dir = E.daily_dir
    today = str(date.today())
    stock_selection_df = pd.read_csv(df_dir + "/" + today + "/" + "stock_selection_lst.csv")
    msg = " \n\n"
    msg += "From " + E.name + " :"
    msg += "The following are stocks pick on today "
    msg += "\n\n"
    msg += str(stock_selection_df)
    msg += "\n\n"

    df_dir = E.work_dir
    wealth_df = pd.read_csv(df_dir + "/" + "wealth.csv")
    wealth_df = wealth_df.set_index("date")
    wealth_df = wealth_df.iloc[ min(5, len(wealth_df)) * -1  : , :]
    msg += "\n"
    msg += str(wealth_df)
    msg += "\n" * 5

    return msg

def get_yesterday(date):
    return str(pd.Timestamp(date) - pd.Timedelta(1)).split(' ')[0]


##
## get relearn msg, it finds the most relean msg, in case the training part takes more than a day

def get_relearn_msg():
    most_recent_day = str(date.today())
    relearn_dir = ROOT + "Data/Log/ReLearn/"
    while (not path.exists(relearn_dir + most_recent_day + ".txt")):
        most_recent_day = get_yesterday(most_recent_day)
    file_path = relearn_dir + most_recent_day + ".txt"
    
    with open(file_path, "r") as f:
        lines = f.readlines()

    msg = "Features ReLearned during the Weekend"
    msg += "\n\n"
    for l in lines:
        msg += l 

    msg += "\n" * 3
    return msg


##
## get the average historical accuracy after running iterative_5d_training

def get_ml_model_prediction_status():
    df_dir = ROOT + "/Data/ML_Models/Daily_Prediction/"

    most_recent_day = str(date.today())
    while (not path.exists(df_dir + most_recent_day)):
        most_recent_day = get_yesterday(most_recent_day)

    recent_df_dir = df_dir + most_recent_day + "/"

    ret_stock_lst = []
    #
    hist_acc_df = pd.read_csv(recent_df_dir + "hist_acc_df.csv")
    hist_acc_df["avg_acc"] = hist_acc_df.iloc[:, 2:].apply(np.mean, axis=1)
    hist_acc_df = hist_acc_df[["Nasdaq_code", "avg_acc"]]
    hist_acc_df = hist_acc_df.sort_values(by="avg_acc", ascending=False)

    msg = ""
    msg += "\n\n"
    msg += "The following is the accuracy benchmark : " + '\n\n'
    msg += str(hist_acc_df)

    hist_recall_df = pd.read_csv(recent_df_dir + "hist_recall_df.csv")
    hist_recall_df["avg_recall"] = hist_recall_df.iloc[:, 2:].apply(np.mean, axis=1)
    hist_recall_df = hist_recall_df[["Nasdaq_code", "avg_recall"]]
    hist_recall_df = hist_recall_df.sort_values(by="avg_recall")

    msg += "\n\n"
    msg += "The following is the recall benchmark : " + "\n\n"
    msg += str(hist_recall_df)
    msg += "\n"*5

    return msg

#msg = get_expert_msg(expert_vamber)

#msg = get_ml_model_prediction_status()

#print(msg)

#send_smg_to_receiver(msg, "vamber@berkeley.edu")