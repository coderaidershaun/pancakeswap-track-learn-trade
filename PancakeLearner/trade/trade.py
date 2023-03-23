from func_contract import get_contract_info, get_unix_timestamp
from func_xgb import xgb_predict_ratio
from func_write import send_tx
from constants import CONTRACT
from datetime import datetime
import time


# Constants
PROBA_THRESH = 0.52


# Execute placing a trade
if __name__ == "__main__":

  """
    1 - Check we are at the right point in time and sleep if not
    2 - The latest metrics data is fed into the ML model.
        The same features are used that were used for training
  """

  # Get current epoch
  epoch_0 = CONTRACT.functions.currentEpoch().call()

  # Get time until next round
  rounds_list_curr = CONTRACT.functions.rounds(epoch_0).call()
  lock_timestamp = rounds_list_curr[2]
  date_log = datetime.fromtimestamp(lock_timestamp)
  datenow = get_unix_timestamp()
  seconds_diff = lock_timestamp - int(datenow)

  # Sleep for 30 seconds until just before lock time
  if seconds_diff > 30:
    sleep_time = seconds_diff - 30
  else:
    sleep_time = 0

  # Sleep until ready
  print("Sleeping for: ", sleep_time)
  time.sleep(sleep_time)

  # Get contract round price information
  print("Retrieving live data...")
  df_download = get_contract_info()

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
  df["bull_perc_1"] = 1 / df_download["bull_ratio_1"]

  # Make predictions
  X_data = df.iloc[:]

  # Get probability that bear perc is over 0.5
  print("Predicting next outcome...")
  pred_over_1 = xgb_predict_ratio(X_data)

  # Determine trade
  if pred_over_1 > PROBA_THRESH:
    print("Placing trade...")
    # send_tx("bear")
