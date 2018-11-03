# Equity Backtesting Model:

- An exploratory analysis of the role that public disclosures plays in the share price of small and mid-cap biotech companies.  Analysis includes backtesting under a variety of independent inputs (sd-window, hold-period, etc.)

Please note that this repository is a "Directed Study" project at Boston University, and is a work in progress.  Once final trading strategies have been determined, individual trading strategies will be refactored into a single object-oriented module. 

- collect.py: Extracts a collection of micro-cap bio-tech company financial history and stores in a subdirectory as a set of .csv files. 
- transform.py: Creates Pandas dataframes from stored .csv files and runs backtesting simulations.
- strategy_x.py: Clone of transform.py with individual strategy implemented as dataframe manipulations.
