from func_aws import timestream_query
import pandas as pd


# Download data from supabase or aws
def download_data(database, is_open=True):
  
  # Handle if aws
  if database == "aws" and not is_open:
    pass

    """
      Was using this code previosly to pull live information from AWS timestream.
      No longer required as now have data in training_data.csv
      Timestream database and table have thus since been removed as no longder required.
    """

    # data = timestream_query()

    # # Get columns
    # cols = []
    # for col in data["ColumnInfo"]:
    #   cols.append(col["Name"])
    # cols = [word.replace("measure_value::bigint", "epoch") for word in cols]

    # # Get rows
    # rows=[]
    # for data in data["Rows"]:
    #   item = data["Data"]
    #   row = []
    #   for i in item:
    #     try:
    #       val = float(i["ScalarValue"])
    #     except:
    #       val = i["ScalarValue"]
    #     row.append(val)
    #   rows.append(row)

    # # Structure dataframe
    # df = pd.DataFrame(rows, columns=cols)
    # df.set_index("time", inplace=True)
    # df.drop(columns=["measure_name", "epoch"], inplace=True)
    # df.to_csv("training_data.csv")
    # return df
  
  # Handle neither case
  else:
    df = pd.read_csv("training_data.csv")
    return df
