# Instructions

## Step 0: AMI and install Python

If using AWS Timestram, ensure your EC2 has full AMI access to AWS timestream

```plain
git clone repo
```

Install Python and PIP if you have not already done so already.

Add a database and table to AWS Timestream if you have not done so

## Step 1: Setup Python

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install python-decouple==3.7 web3==5.31.3 xgboost==1.7.4 scikit-learn==1.1.3 pandas==1.5.1
pip3 install matplotlib==3.7.0
pip3 install boto3==1.26.81 graphviz==0.20.1
```

## Step 2: Setup Environment Vars

```plain
touch .env
sudo nano .env
```

```plain
# For AWS Timestream
DATABASE_NAME=<ONLY_IF_USING_AWS_TIMESTREAM>
DATABASE_TABLE=<ONLY_IF_USING_AWS_TIMESTREAM>

# BSC Contract Connection
PROVIDER=https://bsc-dataseed1.binance.org:443
CONTRACT_ADDRESS=0x18B2A687610328590Bc8F2e5fEdDe3b582A49cdA

# Wallet
ACCOUNT=0x<YOUR ACCOUNT>
PRIVATE_KEY=0x<YOUR PRIVATE KEY - MAKE SURE TO BEGIN WITH "0x">

# Enter the amount of BNB to wager on each trade
WAGER_BNB=0.015
```

### Special Note: ABI JSON file

Note, you might need to save the abi.json file in the root folder or specify its absolte path in your code.

Developer note: When running on local machine, the absolute path was not required. When running on an AWS EC2 instance, it was. This problem can also
be easily solved by saving the abi.json in the root of your EC2 instance.

## Step 3: Setup Cron for Tracking Data

This step will enable you to have a bot that tracks PancakeSwap data live.

Run every 5 minutes (the script will wait until it needs to capture data).

```plain
crontab -e
*/5 * * * * /bin/timeout -s 2 299 python3 myproject/PancakeTracker/learn/main.py  2>&1
crontab -l
```

You should track at least 7 days of data before moving on to the next step or alternatively rely upon the Excel data provided with this repo.

## Step 4: Setup Cron: Learner

Run the learner once per day. This will ensure that the slow change in market conditions is factored into new machine learning models.

```plain
0 1 * * * /bin/timeout -s 2 300 python3 pancake-learner/src/main.py over  2>&1
15 1 * * * /bin/timeout -s 2 300 python3 pancake-learner/src/main.py under  2>&1
```

Trading Cron: Run on every 4th minute of every 5 minute interval. This will execute the program to code for you.

```plain
4-59/5 * * * * /bin/timeout -s 2 300 python3 pancake-learner/trade/trade.py  2>&1
```
