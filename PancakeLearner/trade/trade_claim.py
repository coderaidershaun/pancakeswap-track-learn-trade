from constants import CONTRACT
from func_write import claim_winnings
import time

# Execute placing a trade
if __name__ == "__main__":

  try:
    # Check is claimable
    current_epoch = CONTRACT.functions.currentEpoch().call()
    epoch_T1 = current_epoch - 1
    epoch_T2 = epoch_T1 - 1
    epoch_T3 = epoch_T2 - 1

    # Claim Winnings
    claim_winnings(epoch_T1)
    time.sleep(0.5)
    claim_winnings(epoch_T2)
    time.sleep(0.5)
    claim_winnings(epoch_T3)
  except Exception as e:
    print(e)
    pass