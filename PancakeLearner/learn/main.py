from func_download import download_data
from func_xgboost import run_xgboost


# Constants
DATABASE = "aws"
PROBA_THRESH = 0.52


# Main function execution
if __name__ == "__main__":

  # Download data
  # Select between supabase and aws
  df_download = download_data(DATABASE, is_open=True)

  # Define columns
  X_data_columns = ['bull_ratio_1', 'bull_ratio_0', 'bull_ratio_2', 'bull_amount_0',
       'bull_amt_change_2', 'bull_amount_2', 'bull_amt_change_1',
       'lock_price_change_1', 'bull_amount_1', 'bull_amt_change_0',
       'lock_price_change_2', 'bull_ratio_change_0', 'total_amount_2',
       'bull_ratio_change_2', 'total_amount_0', 'bull_ratio_change_1',
       'total_amount_1']

  # Keep relevant columns
  df = df_download[X_data_columns]

  # Add percentages
  df["bull_perc_1"] = 1 / df["bull_ratio_1"]

  # Add Target - Bet on Shorts
  df.loc[df["bull_perc_1"].shift(-1) > 0.5, "TARGET"] = 0
  df.loc[df["bull_perc_1"].shift(-1) <= 0.5, "TARGET"] = 1

  # Drop NA
  df.dropna(inplace=True)

  # Define X_Data
  X_data = df.iloc[:, :-1]
  y_data = df.iloc[:, -1]

  # Run XGBOOST
  run_xgboost(df.columns[:-1], X_data, y_data, PROBA_THRESH)
