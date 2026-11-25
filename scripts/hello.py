from langchain_aws import ChatBedrockConverse
import os

## Initialize Amazon Bedrock Converse API
llm = ChatBedrockConverse(
            model= os.environ.get("MODEL_ID"),
            region_name= os.environ.get("AWS_REGION"),
            temperature= 0)

## Send message to AI MODEL
response = llm.invoke("Say hello in one line")

print("Print AI MODEL Response : ")
print(response.content)

def hello_world(): {
    print("Hello World")
}
hello_world()