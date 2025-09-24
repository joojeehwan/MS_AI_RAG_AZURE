import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS 

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

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_ver,
    model=deploy
)

documents = [
    "우리 할먼는 생일엔 미역국 끓여주던 ....",
    "대학교 다닐 떄 유럽 여행 간적이 있다",
    "우리 사무실 화이트 보드에는 예전에 그린 공룡 낙서가 있다."
]

vector_store = FAISS.from_texts(documents, embeddings)

query = "생일 때 누가 미역국 끊였냐?!"

results = vector_store.similarity_search(query, k=5)

print("검색결과")
for r in results:
    print("-", r.page_content)