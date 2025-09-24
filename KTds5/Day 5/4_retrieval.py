import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import FAISS 
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

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

texts = [
    "원주 프리미엄 헬스장 리스트에는 오짐과 로로짐이 포함된다.",
    "천안의 프리미엄 헬스장은 시설이 넓고 PT 프로그램을 제공한다.",
    "아이폰 17 실판(실판매) 일정은 루머 단계이다.",
]

vector_store = FAISS.from_texts(texts, embeddings)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})


llm = AzureChatOpenAI(
    azure_endpoint="",
    api_key="",
    api_version=api_ver,
    model="gpt-4o-mini",   # ← 배포 "이름"
    temperature=0.2,
)

prompt = ChatPromptTemplate.from_template(
    """다음 컨텍스트를 참고하여 한국어로 간결히 답하라.
가능하면 근거가 된 문장을 함께 요약해라.
컨텍스트:
{context}
질문: {input}
답변:"""
)

# 4) 문서 결합 체인 + RAG 체인
doc_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, doc_chain)

# 5) 실행
question = "원주에서 프리미엄 헬스장 추천해줘."
result = rag_chain.invoke({"input": question})
print("\n[답변]\n", result["answer"])
print("\n[참고 문서 수]", len(result.get("context", [])))
