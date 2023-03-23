import time
from datetime import datetime
from web3 import Web3


# Structure info
def structure_info(round_info, epoch_num):
  lock_timestamp = round_info[2]
  lock_price = round_info[4]
  close_price = round_info[5]
  lock_timestamp = round_info[2]
  total_amount = round_info[8]
  bull_amount = round_info[9]
  bear_amount = round_info[10]

  # Sleep
  time.sleep(0.2)

  # Convert datetime
  date_log = datetime.fromtimestamp(lock_timestamp)

  # Calculate Ratio
  total_amount_normal = round(float(Web3.fromWei(total_amount, "ether")), 5)
  bull_amount_normal = round(float(Web3.fromWei(bull_amount, "ether")), 5)
  bear_amount_normal = round(float(Web3.fromWei(bear_amount, "ether")), 5)

  # Normalise prices
  lock_price_normal = round(float(Web3.fromWei(lock_price, "gwei")), 5) * 10
  close_price_normal = round(float(Web3.fromWei(close_price, "gwei")), 5) * 10

  # Format prices
  lock_price_normal = float(f'{lock_price_normal:.{5}g}')
  close_price_normal = float(f'{close_price_normal:.{5}g}')

  # Ratios
  if bull_amount_normal != 0 and bear_amount_normal != 0:
    bull_ratio = round(bull_amount_normal / bear_amount_normal, 2) + 1
    bear_ratio = round(bear_amount_normal / bull_amount_normal, 2) + 1

    # Format numbers
    bull_ratio = float(f'{bull_ratio:.{3}g}')
    bear_ratio = float(f'{bear_ratio:.{3}g}')
  else:
    bull_ratio = 0
    bear_ratio = 0

  # Construct item
  item_dict = {
    "epoch": epoch_num,
    "datetime": date_log.strftime('%Y-%m-%d %H:%M:%S'),
    "hour": date_log.hour,
    "minute": date_log.minute,
    "second": date_log.second,
    "lock_price": lock_price_normal,
    "close_price": close_price_normal,
    "total_amount": total_amount_normal,
    "bull_amount": bull_amount_normal,
    "bear_amount": bear_amount_normal,
    "bull_ratio": bull_ratio,
    "bear_ratio": bear_ratio,
  }

  # Return dict
  return item_dict
   