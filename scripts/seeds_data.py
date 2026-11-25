import boto3, os

REGION = os.getenv("AWS_REGION", "eu-north-1")

# Connect to DynamoDB
ddb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

# Create Orders table
t = ddb.create_table(
    TableName="Orders",
    KeySchema=[
        {"AttributeName": "order_id", "KeyType": "HASH"}
    ],
    AttributeDefinitions=[
        {"AttributeName": "order_id", "AttributeType": "S"}
    ],
    BillingMode="PAY_PER_REQUEST"
)

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

