
import pandas as pd
import os
import numpy as np
import plotly
import plotly.offline
import plotly.graph_objs as go
import os

class backtest():

    def __init__ (self, strategy=1, index_name="XBI"):

        self.strategy = strategy
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.investment = 100
        self.strategy_name = "Strategy" + str(self.strategy)
        # self.k_tup = [0, 0.25, 0.5, 0.75,  1, 1.25,  1.5, 1.75,  2, 2.25,  2.5, 2.75,  3]
        # self.w_tup = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]   # trailing_sd window
        self.k_tup = [0,  1,  2,  3]
        self.w_tup = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,]  # trailing_sd window
        self.transaction_cost = 0.25
        self.index_name = index_name
        self.index_df = self.get_transformed_index_data()

        self.micro_cap_list = ["ALDX", "BLRX", "KDMN", "KALV", "KMDA", "MDGL", "PTGX", "RETA", "TRVN", "CDTX", \
                          "MTNB", "NBRV", "KIN", "XOMA", "CMRX", "CTRV", "NNVC", "CDXS", "PFNX", "ATNM", "AGLE", "AFMD", \
                          "ALRN", "AVEO", "BTAI", "ECYT", "FBIO", "GALT", \
                          "GNPX", "GTXI", "IMDZ", "IMGN", "IMMP", "INFI", "KURA", "LPTX", "MEIP", "MRTX", "NK", "ONS", \
                          "PIRS", "RNN", "SLS", "SRNE", "STML", "SNSS", "TRIL", "VBLT", "VSTM", \
                          "ZYME", "ZYNE", "AXSM", "NTEC", "NERV", \
                          "TENX", "KRYS", "MNKD", "NEPT", "ADVM", "AGTC", "IMMY", "OCUL", "OHRP", "OPHT", \
                          "OVAS", "RDHL", "PLX", "GNMX", "GEMP", "SELB", "CALA", "ADMA", "ASNS", "CFRX", "DVAX", \
                          "SGMO", "SMMT", "MTFB", "SPRO", "AMPE", "ABUS", "ARWR", "CNAT", "DRNA", "GLMD", "VTL", "ALNA", \
                          "CPRX", "CHMA", "EIGR", "FATE", "NVLN", "RGLS", "RCKT", "SBBP", "QURE", "XENE", "ATHX",
                          "PRQR", \
                          "PULM", "VRNA", "ARCT", "GLYC", "NYMX", "SPHS", "URGN", "GNCA", "SBPH", "VVUS", \
                          "ZFGN", "OBSV"]

        self.strategy_output = self.generate_net_return_spread()

    def print_index_df(self):
        print(self.index_df)

    def generate_net_return_spread(self):

        combo_list = (self.generate_cartesian_product(self.w_tup, self.k_tup))
        counter = 0
        w_list = []
        k_list = []
        net_return_list = []

        # index_df creation line should be here, so it doesnt need to be created for each investment simulation
        for i in combo_list:
            counter += 1
            cur_w = i[0]
            cur_k = i[1]
            net_return = self.calc_cum_return(cur_w, cur_k)
            w_list.append(cur_w)
            k_list.append(cur_k)
            net_return_list.append(net_return)

            print("****************************************", len(combo_list) - counter,
                  "Calculations Remaining ****************************************\n")

        return [tuple(w_list), tuple(k_list), tuple(net_return_list)]

    def create_scatterplot(self):

        std_trailing_window = self.strategy_output[0]
        std_threshold = self.strategy_output[1]
        net_returns = self.strategy_output[2]

        print(std_trailing_window)
        print(std_threshold)
        print(net_returns)

        scaled_net_returns = []  # scale down return
        minmax_return = max(max(net_returns), abs(min(net_returns)))

        for x in net_returns:
            y = x / minmax_return
            scaled_net_returns.append(abs(y) * 30)

        max_val = max(max(net_returns), abs(min(net_returns)))

        print(std_trailing_window)
        print(std_threshold)
        print(net_returns)

        trace0 = go.Scatter(
            x=std_trailing_window,
            y=std_threshold,
            text=net_returns,
            mode='markers',
            marker=dict(
                color=net_returns,
                size=scaled_net_returns,
                showscale=True,
                cmax=max_val,
                cmin=(-max_val),
            )
        )

        data = [trace0]

        layout = go.Layout(title=str(
            "Net-Return Spread (" + "Strategy " + str(self.strategy) + ", Index = " + self.index_name + ", Transaction Cost = $" + str(
                self.transaction_cost) + ")"),
                           xaxis=dict(title='Rolling σ Window Length'),
                           yaxis=dict(title='σ Threshold'),
                           hovermode='closest'
                           )
        plotly.offline.plot({"data": data, "layout": layout})

    def generate_cartesian_product(self, a,b):

        temp = []
        for t1 in a:
            for t2 in b:
                temp += [(t1, t2),]

        return temp

    def get_transformed_index_data(self):

        df = pd.read_csv(self.dir_path + "\\index_csvs\\" + self.index_name + ".csv")
        print("index_name: ", self.index_name)
        df.columns = map(str.lower, df.columns)
        df = df.dropna()
        df["index_close_delta"] = (df["close"]) / (df["close"].shift)(1) - 1
        df = df.dropna()
        return (df)

    def calc_cum_return(self, w, k):


        if self.strategy == 1:

            cum_sum = 0
            event_count = 0
            index_delta_dict = self.index_df.set_index('date').to_dict()['close']


            for i in self.micro_cap_list:

                stock_df = pd.read_csv(self.dir_path + "\\stock_csvs\\" + i +".csv")
                stock_df.columns = map(str.lower, stock_df.columns)
                stock_df = stock_df.dropna()
                stock_df = stock_df.drop(columns=['low', 'high', 'adj close', 'volume'])
                stock_df['index_close'] = stock_df['date'].map(index_delta_dict)
                stock_df = stock_df.rename(index=str, columns={"close": "stock_close", "open": "stock_open"})
                stock_df["index_close_delta"] = ((stock_df["index_close"] - (stock_df["index_close"].shift)(1)) / (stock_df["index_close"].shift)(1))
                stock_df["stock_close_delta"] = (((stock_df["stock_close"]) - (stock_df["stock_close"].shift)(1)) / (stock_df["stock_close"].shift)(1))
                stock_df["net_close_delta"] = ((stock_df["stock_close_delta"]) - stock_df["index_close_delta"])
                stock_df["ncd_rolling_std"] = stock_df["net_close_delta"].rolling(w).std()  #add shift(1) before rolling to not include that rows day in the calculation
                stock_df["ncd_rolling_mean"] = stock_df["net_close_delta"].rolling(w).mean()
                stock_df["ncd_daily_k_stds"] = stock_df["net_close_delta"] / stock_df["ncd_rolling_std"]
                stock_df['mu_-_k_*_sd'] = ( stock_df["ncd_rolling_mean"] - (k*stock_df["ncd_rolling_std"]))
                stock_df['event_flag'] = np.where(stock_df['net_close_delta'] <( stock_df["ncd_rolling_mean"] - (k*stock_df["ncd_rolling_std"])), 1, 0)

                stock_df["return"] = ((self.investment / stock_df["stock_close"]) * stock_df["stock_open"].shift(-1))*stock_df['event_flag']
                stock_df["net_return"] = (stock_df["return"] - self.investment - self.transaction_cost) * stock_df['event_flag']
                stock_df["roi"] = (stock_df["net_return"] / self.investment)
                cum_sum = cum_sum + (stock_df["net_return"].sum())
                event_count += (stock_df["event_flag"].sum())
                print(i, " : ", (stock_df["net_return"].sum()))

            print("\n")
            print("Stock Name: ", i)
            print("Trailing Window: ", w)
            print("STD Threshold: ", k)
            print("Total portfolio return: ", cum_sum)

            return cum_sum


        if self.strategy == 2:

            cum_sum = 0
            event_count = 0
            index_delta_dict = self.index_df.set_index('date').to_dict()['close']

            for i in self.micro_cap_list:

                stock_df = pd.read_csv(self.dir_path + "\\stock_csvs\\" + i + ".csv")
                stock_df.columns = map(str.lower, stock_df.columns)
                stock_df = stock_df.dropna()
                stock_df = stock_df.drop(columns=['low', 'high', 'adj close', 'volume'])
                stock_df['index_close'] = stock_df['date'].map(index_delta_dict)
                stock_df = stock_df.rename(index=str, columns={"close": "stock_close", "open": "stock_open"})
                stock_df["index_close_delta"] = ((stock_df["index_close"] - (stock_df["index_close"].shift)(1)) / (stock_df["index_close"].shift)(1))
                stock_df["stock_close_delta"] = (((stock_df["stock_close"]) - (stock_df["stock_close"].shift)(1)) / (stock_df["stock_close"].shift)(1))
                stock_df["net_close_delta"] = ((stock_df["stock_close_delta"]) - stock_df["index_close_delta"])
                stock_df["ncd_rolling_std"] = stock_df["net_close_delta"].rolling(w).std()
                stock_df["ncd_rolling_mean"] = stock_df["net_close_delta"].rolling(w).mean()
                stock_df["ncd_daily_k_stds"] = stock_df["net_close_delta"] / stock_df["ncd_rolling_std"]
                stock_df['mu_-_k_*_sd'] = (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))

                stock_df['event_flag'] = np.where(stock_df['net_close_delta'] < (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"])), 1, 0)
                stock_df["return"] = ((self.investment / stock_df["stock_close"]) * stock_df["stock_close"].shift(-1)) *  stock_df['event_flag']
                stock_df["net_return"] = (stock_df["return"] - self.investment - self.transaction_cost) * stock_df['event_flag']
                stock_df["roi"] = (stock_df["net_return"] / self.investment)

                cum_sum = cum_sum + (stock_df["net_return"].sum())
                event_count += (stock_df["event_flag"].sum())
                print(i, " : ", (stock_df["net_return"].sum()))

            print("\n")
            print("Stock Name: ", i)
            print("Trailing Window: ", w)
            print("STD Threshold: ", k)
            print("Total portfolio return: ", cum_sum)

            return cum_sum



        if self.strategy == 3:

            cum_sum = 0
            event_count = 0
            index_delta_dict = self.index_df.set_index('date').to_dict()['close']

            for i in self.micro_cap_list:

                stock_df = pd.read_csv(self.dir_path + "\\stock_csvs\\" + i + ".csv")
                stock_df.columns = map(str.lower, stock_df.columns)
                stock_df = stock_df.dropna()
                stock_df = stock_df.drop(columns=['low', 'high', 'adj close', 'volume'])
                stock_df['index_close'] = stock_df['date'].map(index_delta_dict)
                stock_df = stock_df.rename(index=str, columns={"close": "stock_close", "open": "stock_open"})
                stock_df["index_close_delta"] = ((stock_df["index_close"] - (stock_df["index_close"].shift)(1)) / (stock_df["index_close"].shift)(1))
                stock_df["stock_close_delta"] = (((stock_df["stock_close"]) - (stock_df["stock_close"].shift)(1)) / (stock_df["stock_close"].shift)(1))
                stock_df["net_close_delta"] = ((stock_df["stock_close_delta"]) - stock_df["index_close_delta"])
                stock_df["ncd_rolling_std"] = stock_df["net_close_delta"].rolling(w).std()
                stock_df["ncd_rolling_mean"] = stock_df["net_close_delta"].rolling(w).mean()
                stock_df["ncd_daily_k_stds"] = stock_df["net_close_delta"] / stock_df["ncd_rolling_std"]
                stock_df['mu_-_k_*_sd'] = (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))

                stock_df['event_flag'] = np.where(stock_df['net_close_delta'] < (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"])), 1, 0)
                stock_df["return"] = (self.investment / (stock_df["stock_close"].shift(-1)) * (stock_df["stock_open"].shift)(-2)) * stock_df['event_flag']
                stock_df["net_return"] = (stock_df["return"] - self.investment - self.transaction_cost) * stock_df['event_flag']
                stock_df["roi"] = (stock_df["net_return"] / self.investment)

                cum_sum = cum_sum + (stock_df["net_return"].sum())
                event_count += (stock_df["event_flag"].sum())
                print(i, " : ", (stock_df["net_return"].sum()))

            print("\n")
            print("Stock Name: ", i)
            print("Trailing Window: ", w)
            print("STD Threshold: ", k)
            print("Total portfolio return: ", cum_sum)

            return cum_sum

        if self.strategy == 4:

            cum_sum = 0
            event_count = 0
            index_delta_dict = self.index_df.set_index('date').to_dict()['close']

            for i in self.micro_cap_list:

                stock_df = pd.read_csv(self.dir_path + "\\stock_csvs\\" + i + ".csv")
                stock_df.columns = map(str.lower, stock_df.columns)
                stock_df = stock_df.dropna()
                stock_df = stock_df.drop(columns=['low', 'high', 'adj close', 'volume'])
                stock_df['index_close'] = stock_df['date'].map(index_delta_dict)
                stock_df = stock_df.rename(index=str, columns={"close": "stock_close", "open": "stock_open"})
                stock_df["index_close_delta"] = ((stock_df["index_close"] - (stock_df["index_close"].shift)(1)) / (stock_df["index_close"].shift)(1))
                stock_df["stock_close_delta"] = (((stock_df["stock_close"]) - (stock_df["stock_close"].shift)(1)) / (stock_df["stock_close"].shift)(1))
                stock_df["net_close_delta"] = ((stock_df["stock_close_delta"]) - stock_df["index_close_delta"])
                stock_df["ncd_rolling_std"] = stock_df["net_close_delta"].rolling(w).std()
                stock_df["ncd_rolling_mean"] = stock_df["net_close_delta"].rolling(w).mean()
                stock_df["ncd_daily_k_stds"] = stock_df["net_close_delta"] / stock_df["ncd_rolling_std"]
                stock_df['mu_-_k_*_sd'] = (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))

                stock_df['event_flag'] = np.where(stock_df['net_close_delta'] < (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"])), 1, 0)
                stock_df["return"] = ((self.investment / stock_df["stock_close"].shift(-1)) * stock_df["stock_close"].shift(-2)) * stock_df['event_flag']
                stock_df["net_return"] = (stock_df["return"] - self.investment - self.transaction_cost) * stock_df['event_flag']
                stock_df["roi"] = (stock_df["net_return"] / self.investment)

                cum_sum = cum_sum + (stock_df["net_return"].sum())
                event_count += (stock_df["event_flag"].sum())
                print(i, " : ", (stock_df["net_return"].sum()))

            print("\n")
            print("Stock Name: ", i)
            print("Trailing Window: ", w)
            print("STD Threshold: ", k)
            print("Total portfolio return: ", cum_sum)

            return cum_sum


        if self.strategy == 5:

            cum_sum = 0
            event_count = 0
            index_delta_dict = self.index_df.set_index('date').to_dict()['close']

            for i in self.micro_cap_list:

                stock_df = pd.read_csv( self.dir_path + "\\stock_csvs\\" + i + ".csv")
                stock_df.columns = map(str.lower, stock_df.columns)
                stock_df = stock_df.dropna()
                stock_df = stock_df.drop(columns=['low', 'high', 'adj close'])
                stock_df['index_close'] = stock_df['date'].map(index_delta_dict)
                stock_df = stock_df.rename(index=str, columns={"close": "stock_close", "open": "stock_open", "volume": "stock_volume"})
                stock_df["index_close_delta"] = ((stock_df["index_close"] - (stock_df["index_close"].shift)(1)) / (stock_df["index_close"].shift)(1))
                stock_df["stock_close_delta"] = (((stock_df["stock_close"]) - (stock_df["stock_close"].shift)(1)) / (stock_df["stock_close"].shift)(1))
                stock_df["net_close_delta"] = ((stock_df["stock_close_delta"]) - stock_df["index_close_delta"])
                stock_df["volume_delta"] = (((stock_df["stock_volume"]) - (stock_df["stock_volume"].shift)(1)) / (stock_df["stock_volume"].shift)(1))
                stock_df["volume_rolling_std"] = stock_df["volume_delta"].rolling(w).std()
                stock_df["volume_rolling_mean"] = stock_df["volume_delta"].rolling(w).mean()
                stock_df["volume_k_stds"] = stock_df["volume_delta"] / stock_df["volume_rolling_std"]
                stock_df["ncd_rolling_std"] = stock_df["net_close_delta"].rolling(w).std()  # add shift(1) before rolling to not include that rows day in the calculation
                stock_df["ncd_rolling_mean"] = stock_df["net_close_delta"].rolling(w).mean()
                stock_df["ncd_daily_k_stds"] = stock_df["net_close_delta"] / stock_df["ncd_rolling_std"]
                stock_df['mu_-_k_*_sd'] = (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))

                stock_df['event_flag'] = np.where((stock_df['net_close_delta'] < (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))) & \
                    (stock_df['volume_delta'] > (stock_df["volume_rolling_mean"] + (2 * stock_df["volume_rolling_std"]))), 1, 0)
                stock_df["return"] = (self.investment / (stock_df["stock_close"]) * (stock_df["stock_open"].shift)(-1)) * stock_df['event_flag']
                stock_df["net_return"] = (stock_df["return"] - self.investment - (2 * self.transaction_cost)) * stock_df['event_flag']
                stock_df["roi"] = (stock_df["net_return"] / self.investment)

                cum_sum = cum_sum + (stock_df["net_return"].sum())
                event_count += (stock_df["event_flag"].sum())

                print(i, " : ", (stock_df["net_return"].sum()))

            print("\n")
            print("Stock Name: ", i)
            print("Trailing Window: ", w)
            print("STD Threshold: ", k)
            print("Total portfolio return: ", cum_sum)
            return cum_sum


        if self.strategy == 6:

            cum_sum = 0
            event_count = 0
            index_delta_dict = self.index_df.set_index('date').to_dict()['close']

            for i in self.micro_cap_list:

                stock_df = pd.read_csv(self.dir_path + "\\stock_csvs\\" + i + ".csv")
                stock_df.columns = map(str.lower, stock_df.columns)
                stock_df = stock_df.dropna()
                stock_df = stock_df.drop(columns=['low', 'high', 'adj close'])
                stock_df['index_close'] = stock_df['date'].map(index_delta_dict)
                stock_df = stock_df.rename(index=str, columns={"close": "stock_close", "open": "stock_open", "volume": "stock_volume"})
                stock_df["index_close_delta"] = ((stock_df["index_close"] - (stock_df["index_close"].shift)(1)) / (stock_df["index_close"].shift)(1))
                stock_df["stock_close_delta"] = (((stock_df["stock_close"]) - (stock_df["stock_close"].shift)(1)) / (stock_df["stock_close"].shift)(1))
                stock_df["net_close_delta"] = ((stock_df["stock_close_delta"]) - stock_df["index_close_delta"])
                stock_df["volume_delta"] = (((stock_df["stock_volume"]) - (stock_df["stock_volume"].shift)(1)) / (stock_df["stock_volume"].shift)(1))
                stock_df["volume_rolling_std"] = stock_df["volume_delta"].rolling(w).std()
                stock_df["volume_rolling_mean"] = stock_df["volume_delta"].rolling(w).mean()
                stock_df["volume_k_stds"] = stock_df["volume_delta"] / stock_df["volume_rolling_std"]
                stock_df["ncd_rolling_std"] = stock_df["net_close_delta"].rolling(w).std()
                stock_df["ncd_rolling_mean"] = stock_df["net_close_delta"].rolling(w).mean()
                stock_df["ncd_daily_k_stds"] = stock_df["net_close_delta"] / stock_df["ncd_rolling_std"]
                stock_df['mu_-_k_*_sd'] = (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))

                stock_df['event_flag'] = np.where((stock_df['net_close_delta'] < (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))), 1, 0)
                stock_df["return"] = (self.investment + (self.investment - (self.investment / stock_df["stock_close"] * stock_df["stock_open"].shift(-1)))) * stock_df['event_flag']
                stock_df["net_return"] = (stock_df["return"] - self.investment - (2 * self.transaction_cost)) * stock_df['event_flag']
                stock_df["roi"] = (stock_df["net_return"] / self.investment)

                cum_sum = cum_sum + (stock_df["net_return"].sum())
                event_count += (stock_df["event_flag"].sum())

                print(i, " : ", (stock_df["net_return"].sum()))

            print("\n")
            print("Stock Name: ", i)
            print("Trailing Window: ", w)
            print("STD Threshold: ", k)
            print("Total portfolio return: ", cum_sum)

            return cum_sum


        if self.strategy == 7:

                cum_sum = 0
                event_count = 0
                index_delta_dict = self.index_df.set_index('date').to_dict()['close']

                for i in self.micro_cap_list:

                    stock_df = pd.read_csv(self.dir_path + "\\stock_csvs\\" + i + ".csv")
                    stock_df.columns = map(str.lower, stock_df.columns)
                    stock_df = stock_df.dropna()
                    stock_df = stock_df.drop(columns=['adj close', 'volume'])
                    stock_df['index_close'] = stock_df['date'].map(index_delta_dict)
                    stock_df = stock_df.rename(index=str, columns={"close": "stock_close", "open": "stock_open", "low": "stock_low", "high": "stock_high"})
                    stock_df["index_close_delta"] = ((stock_df["index_close"] - (stock_df["index_close"].shift)(1)) / (stock_df["index_close"].shift)(1))
                    stock_df["stock_close_delta"] = (((stock_df["stock_close"]) - (stock_df["stock_close"].shift)(1)) / (stock_df["stock_close"].shift)(1))
                    stock_df["net_close_delta"] = ((stock_df["stock_close_delta"]) - stock_df["index_close_delta"])
                    stock_df["ncd_rolling_std"] = stock_df["net_close_delta"].rolling(w).std()
                    stock_df["ncd_rolling_mean"] = stock_df["net_close_delta"].rolling(w).mean()
                    stock_df["ncd_daily_k_stds"] = stock_df["net_close_delta"] / stock_df["ncd_rolling_std"]
                    stock_df['mu_-_k_*_sd'] = (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))
                    stock_df["typical"] = ((stock_df["stock_high"] + stock_df["stock_low"] + stock_df["stock_open"] + stock_df["stock_close"]) / 4)

                    stock_df['event_flag'] = np.where(stock_df['net_close_delta'] < (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"])), 1, 0)
                    stock_df["return"] = ((self.investment / stock_df["typical"]) * stock_df["stock_open"].shift(-1)) * stock_df['event_flag']
                    stock_df["net_return"] = (stock_df["return"] - self.investment - (2 * self.transaction_cost)) * stock_df['event_flag']
                    stock_df["roi"] = (stock_df["net_return"] / self.investment)

                    cum_sum = cum_sum + (stock_df["net_return"].sum())
                    event_count += (stock_df["event_flag"].sum())

                    print(i, " : ", (stock_df["net_return"].sum()))

                print("\n")
                print("Stock Name: ", i)
                print("Trailing Window: ", w)
                print("STD Threshold: ", k)
                print("Total portfolio return: ", cum_sum)

                return cum_sum



        if self.strategy == 8:

                cum_sum = 0
                event_count = 0
                index_delta_dict = self.index_df.set_index('date').to_dict()['close']

                for i in self.micro_cap_list:

                    stock_df = pd.read_csv(self.dir_path + "\\stock_csvs\\" + i + ".csv")
                    stock_df.columns = map(str.lower, stock_df.columns)
                    stock_df = stock_df.dropna()
                    stock_df = stock_df.drop(columns=['adj close', 'volume'])
                    stock_df['index_close'] = stock_df['date'].map(index_delta_dict)
                    stock_df = stock_df.rename(index=str, columns={"close": "stock_close", "open": "stock_open", "low": "stock_low", "high": "stock_high"})
                    stock_df["index_close_delta"] = ((stock_df["index_close"] - (stock_df["index_close"].shift)(1)) / (stock_df["index_close"].shift)(1))
                    stock_df["stock_close_delta"] = (((stock_df["stock_close"]) - (stock_df["stock_close"].shift)(1)) / (stock_df["stock_close"].shift)(1))
                    stock_df["net_close_delta"] = ((stock_df["stock_close_delta"]) - stock_df["index_close_delta"])
                    stock_df["ncd_rolling_std"] = stock_df["net_close_delta"].rolling(w).std()
                    stock_df["ncd_rolling_mean"] = stock_df["net_close_delta"].rolling(w).mean()
                    stock_df["ncd_daily_k_stds"] = stock_df["net_close_delta"] / stock_df["ncd_rolling_std"]
                    stock_df['mu_-_k_*_sd'] = (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"]))
                    stock_df["typical"] = ((stock_df["stock_high"] + stock_df["stock_low"] + stock_df["stock_open"] + stock_df["stock_close"]) / 4)

                    stock_df['event_flag'] = np.where(stock_df['net_close_delta'] < (stock_df["ncd_rolling_mean"] - (k * stock_df["ncd_rolling_std"])), 1, 0)
                    stock_df["return"] = ((self.investment / stock_df["typical"]) * stock_df["stock_close"].shift(-1)) * stock_df['event_flag']
                    stock_df["net_return"] = (stock_df["return"] - self.investment - (2 * self.transaction_cost)) * stock_df['event_flag']
                    stock_df["roi"] = (stock_df["net_return"] / self.investment)

                    cum_sum = cum_sum + (stock_df["net_return"].sum())
                    event_count += (stock_df["event_flag"].sum())

                    print(i, " : ", (stock_df["net_return"].sum()))

                print("\n")
                print("Stock Name: ", i)
                print("Trailing Window: ", w)
                print("STD Threshold: ", k)
                print("Total portfolio return: ", cum_sum)

                return cum_sum


model_1 = backtest(strategy=8, index_name="XBI")
model_1.create_scatterplot()
