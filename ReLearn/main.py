
from ReLearn.relearn_trend_kw import get_n_stocks_with_lowest_acc_and_highest_recall

from ReLearn.relearn_trend_kw import relearn_features_for_stock






def main():

    stocks_to_relearn_lst = get_n_stocks_with_lowest_acc_and_highest_recall(2)
    for stock in stocks_to_relearn_lst:
        relearn_features_for_stock(stock)


if __name__ == "__main__":
    main()

    