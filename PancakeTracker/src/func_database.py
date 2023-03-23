import boto3
import time
from decouple import config


# Send data to AWS timestream
def timestream_write(data_obj):

  # Create client
  # Must have region for this to work on EC2
  client = boto3.client("timestream-write", region_name='us-east-1')

  # Specify database and table
  database_name = config("DATABASE_NAME")
  table_name = config("DATABASE_TABLE")

  # # Create dimensions
  keys = list(data_obj.keys())
  keys.remove("epoch")
  dimensions = []
  for k in keys:
    dimension = {
      'Name': k,
      'Value': str(data_obj[k])
    }
    dimensions.append(dimension)

  # Structure record
  epoch = {
    'Dimensions': dimensions,
    'MeasureName': 'epoch',
    'MeasureValue': str(data_obj["epoch"]),
    'MeasureValueType': 'BIGINT',
    'Time': str(int(time.time() * 1000))
  }

  # Add record
  records = [epoch]

  # Submit to database
  try:
    print("Saving records")
    print(records)
    result = client.write_records(DatabaseName=database_name, TableName=table_name, Records=records, CommonAttributes={})
    print("WriteRecords Status: [%s]" % result['ResponseMetadata']['HTTPStatusCode'])
  except Exception as err:
    print("Error:", err)
