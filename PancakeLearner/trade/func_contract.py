from constants import CONTRACT
from func_structure import structure_info
import pandas as pd
import requests
import time


# Get contract information
def get_contract_info():

  # Get current epoch
  epoch_0 = CONTRACT.functions.currentEpoch().call()
  epoch_1 = epoch_0 - 1
  epoch_2 = epoch_1 - 1
  epoch_3 = epoch_2 - 1

  # Get next epoch for referencing later
  next_epoch = epoch_0 + 1

  # Store record for each epoch
  try:
    rounds_list_0 = CONTRACT.functions.rounds(epoch_0).call()
    time.sleep(0.1)
    rounds_list_1 = CONTRACT.functions.rounds(epoch_1).call()
    time.sleep(0.1)
    rounds_list_2 = CONTRACT.functions.rounds(epoch_2).call()
    time.sleep(0.1)
    rounds_list_3 = CONTRACT.functions.rounds(epoch_3).call()
  except Exception as e:
    print(e)
    exit(1)
  
  # Get stats for current and last two periods
  result_dict_0 = structure_info(rounds_list_0, epoch_0)
  result_dict_1 = structure_info(rounds_list_1, epoch_1)
  result_dict_2 = structure_info(rounds_list_2, epoch_2)
  result_dict_3 = structure_info(rounds_list_3, epoch_3)

  # Get changes - Current Epoch
  bull_amt_change_0 = round(result_dict_0["bull_amount"] / result_dict_1["bull_amount"], 2)
  bear_amt_change_0 = round(result_dict_0["bear_amount"] / result_dict_1["bear_amount"], 2)
  bull_ratio_change_0 = round(result_dict_0["bull_ratio"] / result_dict_1["bull_ratio"], 2)

  # Get changes - Epoch - 1
  bull_amt_change_1 = round(result_dict_1["bull_amount"] / result_dict_2["bull_amount"], 2)
  bear_amt_change_1 = round(result_dict_1["bear_amount"] / result_dict_2["bear_amount"], 2)
  bull_ratio_change_1 = round(result_dict_1["bull_ratio"] / result_dict_2["bull_ratio"], 2)

  # Get changes - Epoch - 2
  bull_amt_change_2 = round(result_dict_2["bull_amount"] / result_dict_3["bull_amount"], 2)
  bear_amt_change_2 = round(result_dict_2["bear_amount"] / result_dict_3["bear_amount"], 2)
  bull_ratio_change_2 = round(result_dict_2["bull_ratio"] / result_dict_3["bull_ratio"], 2)

  # Last known lock or close price change
  try:
    lock_price_change_1 = round(result_dict_1["lock_price"] / result_dict_2["lock_price"], 5)
    lock_price_change_2 = round(result_dict_2["lock_price"] / result_dict_3["lock_price"], 5)
  except:
    lock_price_change_1 = 0
    lock_price_change_2 = 0


  """
    Timestem 0: Represents current round you can place a bet on (up or down) - payouts still being entered
    Timestem 1: Represents the prior wagered round playing out in live play - payouts are known
    Timestem 2: Represents the last known full game which has ended - round fully complete
  """


  # Store results
  store_dict = {
    "epoch": epoch_0,

    "total_amount_0": result_dict_0["total_amount"],
    "bull_amount_0": result_dict_0["bull_amount"],
    "bull_ratio_0": result_dict_0["bull_ratio"],

    "bull_amt_change_0": bull_amt_change_0,
    "bull_ratio_change_0": bull_ratio_change_0,

    "total_amount_1": result_dict_1["total_amount"],
    "bull_amount_1": result_dict_1["bull_amount"],
    "bull_ratio_1": result_dict_1["bull_ratio"],
    
    "bull_amt_change_1": bull_amt_change_1,
    "bull_ratio_change_1": bull_ratio_change_1,
    "lock_price_change_1": lock_price_change_1,

    "total_amount_2": result_dict_2["total_amount"],
    "bull_amount_2": result_dict_2["bull_amount"],
    "bull_ratio_2": result_dict_2["bull_ratio"],

    "bull_amt_change_2": bull_amt_change_2,
    "bull_ratio_change_2": bull_ratio_change_2,
    "lock_price_change_2": lock_price_change_2,
  }

  # Construct dataframe
  df = pd.DataFrame([store_dict])

  # Return dict
  return df


# Get Unix Timestamp
def get_unix_timestamp():
  endpoint = "http://worldtimeapi.org/api/timezone/Etc/UTC"
  response = requests.get(endpoint)

  if response.status_code == 200:
    dt = response.json()["unixtime"]
    return dt
  else:
    print("No datetime available via API")
    exit(1)
