
from os import sys

from Email.send_email_utils import send_msg_to_receiver
from Email.send_email_utils import get_expert_msg
from Email.send_email_utils import get_ml_model_prediction_status
from Email.send_email_utils import get_relearn_msg
from Experts.expert_nasdaq_fellow import expert_nasdaq_fellow



from Experts.expert_vamber import expert_vamber


receiver = ["vamber@berkeley.edu"]

def main():
    msg = "GREETINGS, hopefully I made some $$$ for you !" + "\n\n"
    cmd_arg = sys.argv
    duration = cmd_arg[2]
    msg += "Entire pipeline today took : " + duration + " minutes"
    if cmd_arg[1] == "weekend":
        msg += get_relearn_msg()
        msg += get_ml_model_prediction_status()
    elif cmd_arg[1] == "weekdays":
        expert_lst = [expert_vamber, expert_nasdaq_fellow]
        for expert in expert_lst:
            msg += get_expert_msg(expert)

    for r in receiver:
        send_msg_to_receiver(msg, r)
    



if __name__ == "__main__":
    main()
