

###
###  The Scirpt that glues them all together 
###

import pandas as pd
from datetime import date
import os
from os import path 
import time

ROOT = "/home/vamber/ML_stock/"


big_lock = ROOT + "/Pipeline/BIG_LOCK_OPEN"
small_lock = ROOT + "/Pipeline/SMALL_LOCK_OPEN"

def exec_cmd(cmd):
    res = os.system(cmd)
    if res != 0:
        print(cmd + "failed to run, Aborting ")
        os.makedirs(small_lock)
        raise Exception("above cmd can failed")

def main():

    
    if not path.exists(big_lock):
        print("BIG_LOCK is not open, pipeline can not begin")
        exit()
    if not path.exists(small_lock):
        print("SMALL_LOCK is not open, pipeline can not begin")
        exit()

    print("Pipeline starts in 5 seconds")
    for i in range(0,5):
        print(5-i)
        time.sleep(1)


    os.rmdir(small_lock)

    ##
    ## creating the log file for future debugging purpose
    ##
    today = str(date.today())
    pipeline_log_dir = ROOT + "/Data/Log/Pipeline_Log/"
    if not path.exists(pipeline_log_dir):
        os.makedirs(pipeline_log_dir)
    today_log = pipeline_log_dir + "/" + today + ".txt"


    os.chdir("/home/vamber/ML_stock")

    start_time = time.time()
    #the week day case
    if pd.Timestamp(today).dayofweek <= 4:
        exec_cmd("/bin/python3 /home/vamber/ML_stock/Download/download_main.py weekdays" + " >> " + today_log)
        exec_cmd("/bin/python3 /home/vamber/ML_stock/ML_Models/ml_model_main.py weekdays" + " >> " + today_log)
        exec_cmd("/bin/python3 /home/vamber/ML_stock/Experts/expert_main.py" + " >>  " + today_log)
        end_time = time.time()
        duration = str(round( (end_time - start_time)/60 , 2))
        exec_cmd(" /bin/python3 /home/vamber/ML_stock/Email/main.py weekdays " + duration)
    
    
    #satuday case
    elif pd.Timestamp(str(today)).dayofweek == 5:
        exec_cmd("/bin/python3 /home/vamber/ML_stock/ReLearn/main.py" + " >> " + today_log )
        exec_cmd("/bin/python3 /home/vamber/ML_stock/Download/download_main.py weekend" + " >> " + today_log)
        exec_cmd("/bin/python3 /home/vamber/ML_stock/ML_Models/ml_model_main.py weekend" + " >> " + today_log)
        end_time = time.time()
        duration = str(round( (end_time - start_time)/60 , 2))
        exec_cmd(" /bin/python3 /home/vamber/ML_stock/Email/main.py weekend " + duration)



    os.makedirs(small_lock)

    ##
    ## Add code here to shut down the VM
    exec_cmd(" sudo systemctl poweroff ")



if __name__ == "__main__":
    main()