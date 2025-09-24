import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import Tool
from langchain.agents import initialize_agent

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
api_key  = os.getenv("OPENAI_API_KEY")
api_ver  = os.getenv("OPENAI_API_VERSION")
deploy   = os.getenv("DEPLOYMENT_NAME")

# 진단용 출력
print("endpoint :", endpoint)
print("api_key  :", api_key)
print("api_ver  :", api_ver)
print("deploy   :", deploy)

# 필수값 확인
missing = [k for k,v in {
    "AZURE_ENDPOINT": endpoint,
    "OPENAI_API_KEY": api_key,
    "OPENAI_API_VERSION": api_ver,
    "DEPLOYMENT_NAME": deploy,
}.items() if not v]
if missing:
    raise RuntimeError(f"환경변수 누락: {missing}")

# prompt = ChatPromptTemplate.from_template(
#     "주제: {topic}\n"
#     "요구사항:\n"
#     "- 해당 주제를 한국어로 정확히 10문장으로 요약\n"
#     "- 불릿/번호 없이 문장만 출력\n"
#     "- 각 문장은 줄바꿈(\\n)으로 구분\n"
# )

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_ver,
    deployment_name=deploy
)

def get_weather(city) :
    """주어진 도시에 대해 맞는 날찌 정보를 가져옵니다."""

    return f"{city}의 날씨는 맑고 기온은 23도 입니다."

def recommend_outfit(temp:int):
    """주어진 기온에 맞는 적절한 옷차림을 추천합니다."""
    if isinstance(temp, str) : 
       temp = int(temp)
    if temp > 25:
        return "웃통까기"
    else:
        return "아무거나 입어라.."
    

weather_tool = Tool(
name = "get_weather",
func = get_weather,
description = "주어진 도시에 대해 맞는 날씨 정보를 가져온다."
)

outfit_tool = Tool(
name = "recommend_outfit",
func = recommend_outfit,
description = "적절한 옷 차림 ㅊ천."
)


tools = [weather_tool, outfit_tool]
agent = initialize_agent(tools, model, agent="zero-shot-react-description")
response = agent.run("서울의 날씨를 알려줘. 옷차림은 어떻게 할까?")
print(response)

# parser = StrOutputParser()

# chain  = prompt | model | parser

# topic = "천안, 원주 헬스장 추천 오짐이나, 로로짐 같이 프리미엄 헬스장으로"
# #answer = chain.invoke({"topic" : topic})

# # invoke() 대신 stream() 사용
# for chunk in chain.stream({"topic" : topic}):
#     print(chunk, end="", flush=True)
#print(answer)
#resp = model.invoke("삼성전자의 파운드리 사업에 대해서 알려줘")
#print(resp.content)