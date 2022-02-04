
from ML_Models.ml_model_generator_hypervisor import ml_model_generator_hypervisor

from ML_Models.svm_svc_rbf import svm_svc_rbf_generator

from os import sys



def main():
    H = ml_model_generator_hypervisor([svm_svc_rbf_generator])
    cmd_arg = sys.argv
    if cmd_arg[1] == "weekend":
        print("running iterative 5d sim on all stocks")
        H.run_iterative_5d_sim_on_all_stocks()
        print("training and saving all ml models")
        H.train_and_save_all_ml_model_generator()
    else:
        print("Today is a weekday, each model will start making prediction")
        H.create_daily_prediction()


if __name__ == "__main__":
    main()