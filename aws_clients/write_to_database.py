import boto3
import os
import time
from dotenv import load_dotenv

load_dotenv()

AWS_DYNAMODB_TABLE_NAME = os.getenv('AWS_DYNAMODB_TABLE_NAME')
AWS_REGION = os.getenv('AWS_REGION')


def add_item_to_table(metadata: dict, summary: str) -> dict:
    """
    Add an item to the specified DynamoDB table.

    Args:
    - table_name (str): The name of the DynamoDB table.
    - item (dict): The item to be added to the table.
    - dynamodb_client (boto3.client): The DynamoDB client.

    Returns:
    - dict: The response from the put_item operation.
    """
    try:

        dynamodb_client = boto3.resource('dynamodb',
                                         region_name=AWS_REGION)
        print(AWS_DYNAMODB_TABLE_NAME)
        table = dynamodb_client.Table(AWS_DYNAMODB_TABLE_NAME)
        print(table)
        print(type(table))
        item = metadata
        item['summary'] = summary
        item['created_at'] = str(time.time())
        response = table.put_item(Item=item)
        return response
    except Exception as e:
        print(f"Error adding item to table: {e}")
        return None
