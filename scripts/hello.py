from langchain_aws import ChatBedrockConverse

#AWS Configuration
AI_MODEL_ID= "amazon.nova-lite-v1:0"
AWS_REGION= "eu-north-1"

## Initialize Amazon Bedrock Converse API
llm = ChatBedrockConverse(
            model= AI_MODEL_ID,
            region_name= AWS_REGION,
            temperature= 0)

## Send message to AI MODEL
response = llm.invoke("Say hello in one line")

print("Print AI MODEL Response : ")
print(response.content)