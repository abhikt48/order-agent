import os, json, boto3

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_aws import ChatBedrockConverse
from langgraph.types import interrupt

## AWS Configuration
MODEL_ID = os.getenv("MODEL_ID")
REGION = os.getenv("AWS_REGION")
TABLE_NAME = os.getenv("ORDERS_TABLE")

## DynamoDB
dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

## Bedrock LLM connection
llm = ChatBedrockConverse( model=MODEL_ID, region_name=REGION, temperature=0)

# --------------------------------------------------
# 4. Business policy
# --------------------------------------------------

POLICY = """
Returns accepted within 30 days of delivery.
Refunds for damaged items are approved by a human agent.
Shipping takes 3-5 working days.
Orders in PROCESSING can be cancelled free of charge.
"""

## LangChain LCEL Chain
policyChain = (ChatPromptTemplate.from_messages([
    (
        "system",
        "Answer ONLY from this policy. If unsure, say so.\n\n{policy}"
    ),
    ("human", "{question}"),
   ])
    | llm
    | StrOutputParser()
)



@tool
def answer_policy_question(question: str) -> str :
    """ Answer questions about returns, refunds, shipping and cancellation policy. """

    return policyChain.invoke({
        "policy": POLICY,
        "question": question
    })

@tool
def get_order(order_id: str) -> str :
    """Look up an order by ID. Returns status, item, total."""
    item = table.get_item(Key={"order_id": order_id}).get("Item")

    return json.dumps(item, default=str) if item else "Order not found"

@tool
def issue_refund(order_id: str, reason: str) -> str :
    """Issue a refund for an order. Requires human approval."""
    decision = interrupt({
        "action": "refund",
        "order_id": order_id,
        "reason": reason
    })

    if decision != "approve":
        return "Refund was rejected by the human reviewer."

    table.update_item(
        Key={"order_id": order_id},
        UpdateExpression="SET #s = :r",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":r": "REFUNDED"},
    )
    return f"Refund issue for order {order_id} was accepted."

# --------------------------------------------------
# 9. Register all available tools
# --------------------------------------------------

TOOLS = [
    answer_policy_question,
    get_order,
    issue_refund
]