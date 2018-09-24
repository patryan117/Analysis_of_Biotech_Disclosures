import numpy as np
import pandas as pd
import os
import time

dir_path = os.path.dirname(os.path.realpath(__file__))

#TODO set so that the creating loop doesnt take from the hard coded list, but parses from the /data/ folder
#TODO add segment to collect data that creates an interger feature for stock splits (holding the split ratio), and does one of two options:
    # manipulates the investment in accordance with the split
    # does not allow the algorithm to trade the date before or after the stock split

# TODO create a major loop that runs through the cartesian product (all possible window and std_threshold combos) and stoes as tuples in a list (combo list)
# TODO Create a plotly script that will take the "combo list" and create a plotly
# note, the number of tuples in the list will be sd_options * window options.  color = scale (red = positive, green = negative) (size = magnitude)



def main():

    start_time = time.time()

    w_tup = (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)   # trailing_sd window
    k_tup = (.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5)  # standard_dev sampling window

    base_investment = 100
    combo_list = (generate_cartesian_product(w_tup, k_tup))

    # start for loop to create combo list...
    print(generate_cartesian_product(w_tup, k_tup))
    # create_close_delta_feature(1, 10, base_investment)



    print("\n--- %s seconds ---" % (time.time() - start_time))


def create_close_delta_feature(k, w, p):

    cum_sum = 0
    event_count = 0
    max_sum = 0

    for i in micro_cap_list:

        df = pd.read_csv(dir_path + "\\data\\" + i +".csv")
        df.columns = map(str.lower, df.columns)
        df = df.dropna()

        df["close_delta"] = (df["close"]) / (df["close"].shift)(1) - 1
        df["rolling_std"] = df["close_delta"].rolling(w).std()
        df["daily_k_stds"] = df["close_delta"] / df["rolling_std"]
        df['event_flag'] = np.where(df['daily_k_stds'] <= -k, 1, 0)
        df["return"] = (p / (df["close"]) * (df["close"].shift)(-1))*df['event_flag']
        df["net_return"] = (df["return"] - p) * df['event_flag']



        cum_sum = cum_sum + (df["net_return"].sum())
        event_count += (df["event_flag"].sum())

        if (df["net_return"].sum()) > max_sum:
            max_sum = (df["net_return"].sum())


        if i == "MDWD":
            df.to_csv("trouble.csv")

        print(i, " : ", (df["net_return"].sum()))
        # print(df)

    print("\n")
    print("Max Sum: ", max_sum)
    print("Event_Count: ", event_count)
    print("Total Vested (Pre-Return): ", event_count  * p )
    print("Total portfolio return: ", cum_sum)
    print("Average portfolio return: ", cum_sum/event_count)






def generate_cartesian_product(a,b):


    temp = []

    for t1 in a:
        for t2 in b:
            temp += [(t1, t2),]

    return temp


global  micro_cap_list
micro_cap_list = [ "ALDX", "BLRX", "CRMD", "KDMN", "KALV", "KMDA", "MDGL", "MGEN", "PTGX", "RETA", "TRVN", "CDTX", \
                   "MTNB", "NBRV", "KIN", "XOMA", "CMRX", "CTRV", "NNVC", "CDXS", "PFNX", "ATNM", "AGLE", "AFMD", \
                   "ALRN", "AVEO", "BPTH", "BTAI",  "CBMG", "DFFN", "ECYT", "FBIO", "GALT", \
                   "GNPX", "GTXI", "IMDZ", "IMGN", "IMMP", "INFI", "KURA", "LPTX", "MEIP", "MRTX", "NK", "ONS", \
                   "PIRS", "RNN", "SLS", "SRNE", "STML", "SNSS",  "TCON", "TRIL", "VBLT", "VSTM",  \
                   "ZYME", "ZYNE", "AVXL", "AXSM", "NTEC", \
                   "OVAS", "RDHL", "PLX", "GNMX", "CAPR", "GEMP", "SELB", "CALA", "ADMA", "ASNS", "CFRX", "DVAX", \
                   "SGMO", "SMMT", "MTFB", "SPRO", "AMPE", "ABUS", "ARWR", "CNAT", "DRNA", "GLMD", "VTL", "ALNA", \
                   "CBAY", "SYN", "BCLI", "EDGE", "MNOV", "OVID", "FLKS", "DRRX", "ABEO", "AKTX", "LIFE", "CATB", \
                   "CPRX", "CHMA", "EIGR", "FATE", "NVLN", "RGLS", "RCKT", "SBBP", "QURE", "XENE", "ATHX", "PRQR",\
                   "PULM", "VRNA", "ARCT", "GLYC", "NYMX", "SPHS", "URGN", "GNCA", "SBPH", "VVUS", \
                   "ZFGN", "OBSV", "PTN"]



if __name__ == "__main__":
    main()