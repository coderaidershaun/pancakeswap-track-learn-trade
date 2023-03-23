import boto3
from decouple import config


# Send data to AWS timestream
def timestream_query():

  # Specify database and table
  database_name = config("DATABASE_NAME")
  table_name = config("DATABASE_TABLE")

  # Structure query
  query_string = f'SELECT * FROM "{database_name}"."{table_name}" WHERE time between ago(10.5d) AND now() ORDER BY time ASC'

  # Create client
  # Must have region for this to work on EC2
  client = boto3.client("timestream-query", region_name='us-east-1')

  # Execute the query
  try:
    response = client.query(QueryString=query_string)
    return response
  except Exception as e:
    print(e)
    return []
