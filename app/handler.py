import json, os
from langgraph.types import Command
from langgraph_checkpoint_aws import DynamoDBSaver
from .graph import build_graph

saver =DynamoDBSaver(table_name=os.environ.get("CHECKPOINT_TABLE"), region_name=os.environ.get("AWS_REGION"))

graph = build_graph()

def _text(msg):
    c = msg.content
    return c if isinstance(c, str) else "".join(b.get("text", "") for b in c if isinstance(b, dict))

def _resp(code, body):
    return {"statusCode": code, "headers": {"Content-Type": "application/json"}, "body": json.dumps(body)}

def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    cfg = {"configurable": {"thread_id": body["thread_id"]}}
    inp = Command(resume=body["resume"]) if "resume" in body else {"messages": [("user", body["message"])]}
    out = graph.invoke(inp, cfg)
    pending = out.get("__interrupt__")
    if pending:
        return _resp(200, {"status": "needs_approval", "pending": pending[0].value})
    return _resp(200, {"status": "done", "reply": _text(out["messages"][-1])})