'''
import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
import os

# Load environment variables from .env file
load_dotenv()

print("Azure OpenAI API Key:", os.getenv('OPENAI_API_KEY'))
print("Azure OpenAI Endpoint:", os.getenv('AZURE_ENDPOINT'))
print("Azure OpenAI API Type:", os.getenv('OPENAI_API_TYPE'))
print("Azure OpenAI API Version:", os.getenv('OPENAI_API_VERSION'))

model = AzureChatOpenAI(deployment_name=os.getenv("DEPLOYMENT_NAME")
                       ,api_version=os.getenv("OPENAI_API_VERSION"))

response = model.invoke("삼성전자의 파운드리 사업에 대해서 알려줘")
print(response.content)
'''
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
api_key  = os.getenv("OPENAI_API_KEY")
api_ver  = os.getenv("OPENAI_API_VERSION")
deploy   = os.getenv("DEPLOYMENT_NAME")   # ← 반드시 '배포 이름'

# 진단용 출력
print("endpoint:", endpoint)
print("api_key  :", api_key)
print("api_ver :", api_ver)
print("deploy  :", deploy)

# 필수값 확인
missing = [k for k,v in {
    "AZURE_ENDPOINT": endpoint,
    "OPENAI_API_KEY": api_key,
    "OPENAI_API_VERSION": api_ver,
    "DEPLOYMENT_NAME": deploy,
}.items() if not v]
if missing:
    raise RuntimeError(f"환경변수 누락: {missing}")

prompt = ChatPromptTemplate.from_template(
    "주제: {topic}\n"
    "요구사항:\n"
    "- 해당 주제를 한국어로 정확히 10문장으로 요약\n"
    "- 불릿/번호 없이 문장만 출력\n"
    "- 각 문장은 줄바꿈(\\n)으로 구분\n"
)


model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_ver,
    deployment_name=deploy
)

parser = StrOutputParser()

chain  = prompt | model | parser

topic = "천안, 원주 헬스장 추천 오짐이나, 로로짐 같이 프리미엄 헬스장으로"
#answer = chain.invoke({"topic" : topic})

# invoke() 대신 stream() 사용
for chunk in chain.stream({"topic" : topic}):
    print(chunk, end="", flush=True)
#print(answer)
#resp = model.invoke("삼성전자의 파운드리 사업에 대해서 알려줘")
#print(resp.content)