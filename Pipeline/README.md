

# Pipeline

## Goal
Pipline is the final module that ties everything together, it automates downloading features, training_modol, makeing daily selection, deciding which portfolio of stocks to buy. 
#

## Concepts
### BIG_LOCK_OPEN
since the GCP machine will be turned on and off automatically. (Ideally the VM turns on every 2 AM on weekdays) and (2 AM on satuday) and (never turns on Sunday). BIG_LOCK_OPEN is a file under ROOT + /Pipeline/, if this file is not found, then the pipeline would not run. This is useful for maintainance purposes, if we are mannually trying to insert new stocks to stock_and_features.csv, then the first thing to do is remove BIG_LOCK_OPEN. The big lock can only be opened or closed by Vamber.

#

### SMALL_LOCK_OPEN
The SMALL_LCOK_OPEN fundction as a BIG_LOCK_OPEN, which means the pipeline would not run if it is missing. The SMALL_LOCK_OPEN is removed by the pipeline once it does decides to run, and restored after it finishes. The reason why we need a small_lock is to prevent a process from carrying over until the next day. For example, suppose a really long training process happened on the weekend, and it was so long it is still runing on Monday morning. But the pipeline for Monday would want to start, and therefore we need this SMALL_LOCK_OPEN to protect the process from Satuday. 

#

### Weekdays vs Weekend
On weekdays: download features -> reading serialized ml_models -> make predictions
On Saturday:          Relearn features -> download features -> run_5d_iter_sim -> train and serialize model


# CronTab

### Every 2 AM
The GCP console will turn on the VM everyday 2 AM, and the there will be a cronjob from the VM (not gcp console) to run the  pipeline. Note, the cron-job will attemp to run the pipeline every minute between 2 AM to 2:30 AM. However, only one Pipline will run due to the protection of SMALL_LOCK.  Therefore it's perfect fine to ssh into the machine around 10 AM, persay, when the pipeline would not run, and perform and maintainance work. 

