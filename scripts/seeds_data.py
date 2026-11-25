import boto3, os
from botocore.exceptions import ClientError

REGION = os.getenv("AWS_REGION")
TABLE_NAME = os.getenv("ORDERS_TABLE")

# Connect to DynamoDB
ddb = boto3.resource(
    "dynamodb",
    region_name=REGION
)
def get_or_create_table():
    try:
        ddb.meta.client.describe_table(TableName=TABLE_NAME)
        print(f"{TABLE_NAME} already exists, skipping create")
        return ddb.Table(TABLE_NAME)
    except ClientError as e:
        if e.response["Error"]["Code"] != "ResourceNotFoundException":
            raise

    t = ddb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "order_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "order_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    t.wait_until_exists()
    print(f"Created {TABLE_NAME}")
    return t


t = get_or_create_table()

# Wait until table is available
t.wait_until_exists()

# Sample order data
items = [
    {
        "order_id": "1001",
        "status": "SHIPPED",
        "item": "Running shoes",
        "total": "79.99",
        "eta": "2026-11-08"
    },
    {
        "order_id": "1002",
        "status": "DELIVERED",
        "item": "Headphones",
        "total": "129.00"
    },
    {
        "order_id": "1003",
        "status": "PROCESSING",
        "item": "Backpack",
        "total": "45.50"
    }
]

#insert orders

for i in items:
    t.put_item(Item=i)

print("Orders seeded successfully!")

