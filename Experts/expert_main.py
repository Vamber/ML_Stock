

from Experts.expert_vamber import expert_vamber
from Experts.expert_nasdaq_fellow import expert_nasdaq_fellow
from datetime import date 



def main():
    expert_lst = [expert_vamber, expert_nasdaq_fellow]
    for expert in expert_lst:
        E = expert()
        print(E.name + "instantiated ")
        print(E.name + " creating today's stock selection")
        selection = E.create_today_stock_selection()
        E.save_today_stock_selection(selection)
        print("simulating wealth")
        E.simulate_wealth()
        print("DONE")


if __name__ == "__main__":
    main()