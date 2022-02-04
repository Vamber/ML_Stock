

from Utils.trend_kw_2_stock_price_corr_utils import find_corr_between_stock_price_and_trend_kw

from Utils.google_trends_utils import get_related_kw

import sys

###
###
### This is also a critically important module, it takes an Nasdaq_code and a defulat trend kw
### it find automatically finds another 5 related word r0, r1, ... r4. And for each related word
### it then finds another 3 related kw if possible r0rr0 , r0rr2, r1rr0, r1rr2 .. r4rr2
###
### now we have a pretty big lst of keyword, what we need to do find the best one that shows correlations with nasdaqcode
### using a weighted sum of 3 correlation heuristic computed by find_corr_between_stock_price_and_trend_kw
###
###


# I know there is some room for optimization since the stock_price data is pulled 15 times, kinda unnesssery 
def good_trend_kw_filter(Nasdaq_code, trend_kw, enable_print=False):
    
    full_kw_candidate_lst = []
    related_kw_lst = get_related_kw(trend_kw)

    #append the default one first
    full_kw_candidate_lst.append(trend_kw)

    #sometimes the related keyword could be many, but we only use the top five
    for i in range(0, min(5, len(related_kw_lst))):
        related_kw = related_kw_lst[i]
        if related_kw not in full_kw_candidate_lst:
            full_kw_candidate_lst.append(related_kw)
            #handling 2 order related kw
            related_to_related_kw_lst = get_related_kw(related_kw)
            for j in range(0, min(3, len(related_to_related_kw_lst))):
                related_to_related_kw = related_to_related_kw_lst[j]
                if related_to_related_kw not in full_kw_candidate_lst:
                    full_kw_candidate_lst.append(related_to_related_kw)

    

    #now the addition to full_kw_candiate_lst is complete 
    #time to compute their correlation score
    kw_corr_map = {}

    for kw in full_kw_candidate_lst:
        corr_vec = find_corr_between_stock_price_and_trend_kw(Nasdaq_code, kw)
        corr_score = abs(corr_vec[0])*1 + abs(corr_vec[1])*3 + abs(corr_vec[2])*10
        kw_corr_map[kw] = corr_score

    kw_corr_map = sorted(kw_corr_map.items(), key=lambda x: x[1], reverse=True)

    if enable_print:
        for kw, corr_val in kw_corr_map:
            print(kw + "   " + str(round(corr_val,2) ) )

    return kw_corr_map




def main():
    cmd_args = list(sys.argv)
    stock = cmd_args[1]
    starting_kw = cmd_args[2]
    good_trend_kw_filter(stock, starting_kw, enable_print=True)

if __name__ == "__main__":
    main()