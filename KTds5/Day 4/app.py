import os
from dotenv import load_dotenv
import streamlit as st
from openai import AzureOpenAI

# ====== 초기 설정 ======
load_dotenv()
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")              # ex) https://<resource>.openai.azure.com/
AZURE_API_KEY  = os.getenv("OPENAI_API_KEY")
API_VERSION    = os.getenv("OPENAI_API_VERSION")
DEPLOYMENT     = os.getenv("DEPLOYMENT_NAME")     # ⚠️ 모델명이 아니라 "배포 이름"

client = AzureOpenAI(api_key=AZURE_API_KEY,
                     api_version=API_VERSION,
                     azure_endpoint=AZURE_ENDPOINT)

st.set_page_config(page_title="Azure OpenAI Chat", page_icon="💬")
st.title("💬 Azure OpenAI Chat (Streamlit)")

# ====== 사이드바 ======
with st.sidebar:
    st.header("⚙️ 설정")
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful assistant.",
        height=120
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# ====== 세션 상태 ======
if "messages" not in st.session_state:
    st.session_state.messages = []

# ====== 과거 메시지 렌더 ======
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ====== 입력창 ======
user_input = st.chat_input("메시지를 입력하세요...")
if user_input:
    # 1) 사용자 메시지 화면 표시 & 저장
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2) 모델 요청(배포 이름을 model에!)
    messages_for_api = [{"role": "system", "content": system_prompt}] + st.session_state.messages
    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            resp = client.chat.completions.create(
                model=DEPLOYMENT,                 # ⚠️ 배포 이름
                temperature=temperature,
                messages=messages_for_api,
            )
            reply = resp.choices[0].message.content
        except Exception as e:
            reply = f"오류가 발생했습니다: {e}"
        placeholder.markdown(reply)

    # 3) 어시스턴트 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": reply})
