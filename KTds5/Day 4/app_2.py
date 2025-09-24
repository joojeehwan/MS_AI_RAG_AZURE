import os
import time
import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# ====== 옵션: Azure OpenAI (있으면 챗탭 활성화) ======
load_dotenv()
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_KEY  = os.getenv("OPENAI_API_KEY")
AZURE_API_VER  = os.getenv("OPENAI_API_VERSION")
AZURE_DEPLOY   = os.getenv("DEPLOYMENT_NAME")
HAS_AZURE = all([AZURE_ENDPOINT, AZURE_API_KEY, AZURE_API_VER, AZURE_DEPLOY])

if HAS_AZURE:
    from openai import AzureOpenAI
    aoclient = AzureOpenAI(
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VER,
        azure_endpoint=AZURE_ENDPOINT,
    )

st.set_page_config(page_title="Streamlit 올인원 실습", page_icon="🧪", layout="wide")
st.title("🧪 Streamlit 올인원 실습 앱")
st.caption("실행/데이터 표시/차트·지도/위젯/사이드바·레이아웃/진행바/캐시/파일업로드 (+선택: Azure OpenAI)")

# ======================
# 사이드바(전역 컨트롤)
# ======================
with st.sidebar:
    st.header("⚙️ 전역 설정")
    demo_rows = st.slider("데이터 샘플 행 수", 5, 50, 20)
    auto_rerun = st.toggle("항상 다시 실행(개발 중 권장)", value=False)
    if auto_rerun:
        st.rerun  # 힌트용 (자동선택은 UI에서)
    st.divider()
    st.write("📌 실행 방법")
    st.code("streamlit run app.py\n# 또는\npython -m streamlit run app.py", language="bash")

# 공통 데모 데이터
rng = np.random.default_rng(42)
df_demo = pd.DataFrame(
    rng.normal(size=(demo_rows, 3)),
    columns=["a", "b", "c"]
)

# ======================
# 탭 구성
# ======================
tabs = st.tabs([
    "1) 기본/Magic", "2) 데이터 표시", "3) 차트·지도",
    "4) 위젯·세션상태", "5) 레이아웃", "6) 진행상태", "7) 캐시", "8) 파일 업로드"
] + (["9) Azure OpenAI (선택)"] if HAS_AZURE else []))

# ----------------------
# 1) 기본 / Magic
# ----------------------
with tabs[0]:
    st.subheader("1) 실행 & Magic")
    st.markdown("""
- **실행**: `streamlit run app.py` 또는 `python -m streamlit run app.py`
- **Magic**: 변수/리터럴을 한 줄에 두면 `st.write()` 없이도 렌더링됨.
    """)
    st.write("아래는 Magic 데모(그냥 DataFrame 이름만 적어도 테이블로 표시됨):")
    df_demo  # Magic (st.write 없이 출력)

    st.info("Tip) 스크립트 저장 시 자동 감지 → 우측 상단에서 'Always rerun' 켜면 자동 새로고침!")

# ----------------------
# 2) 데이터 표시
# ----------------------
with tabs[1]:
    st.subheader("2) 데이터 표시: st.write / st.dataframe / st.table")
    st.write("기본 write:")
    st.write(df_demo.head())

    st.write("대화형 테이블(st.dataframe): 열 너비/스크롤링 등 편함")
    st.dataframe(df_demo.style.highlight_max(axis=0))

    st.write("정적 테이블(st.table): 작은/고정 표에 적합")
    st.table(df_demo.head())

# ----------------------
# 3) 차트·지도
# ----------------------
with tabs[2]:
    st.subheader("3) 차트와 지도")
    st.write("라인 차트:")
    st.line_chart(df_demo)

    st.write("바 차트:")
    st.bar_chart(df_demo)

    st.write("맵(st.map): lat/lon 데이터 필요")
    map_df = pd.DataFrame(
        rng.normal(size=(300, 2)) / [50, 50] + [37.5665, 126.9780],  # 서울 근처
        columns=["lat", "lon"]
    )
    st.map(map_df)

# ----------------------
# 4) 위젯·세션상태
# ----------------------
with tabs[3]:
    st.subheader("4) 위젯 & 세션상태")
    name = st.text_input("이름을 입력하세요", key="name")
    x = st.slider("x 값", 0, 100, 10)
    st.write(f"✅ {x}의 제곱 = {x * x}")

    st.write("세션 상태 확인:")
    st.json(st.session_state)

    st.write("버튼/체크박스:")
    if st.button("누르면 증가"):
        st.session_state["clicks"] = st.session_state.get("clicks", 0) + 1
    st.write("클릭 수:", st.session_state.get("clicks", 0))

    show_df = st.checkbox("데이터프레임 보이기", value=True)
    if show_df:
        st.dataframe(df_demo)

# ----------------------
# 5) 레이아웃 (사이드바/컬럼/익스팬더)
# ----------------------
with tabs[4]:
    st.subheader("5) 레이아웃")
    st.write("- 사이드바: `st.sidebar.xxx`\n- 컬럼: `st.columns`\n- 확장영역: `st.expander`")

    left, right = st.columns(2)
    with left:
        st.write("왼쪽 컬럼")
        st.selectbox("연락 방법", ["Email", "Home phone", "Mobile phone"])
    with right:
        st.write("오른쪽 컬럼")
        chosen = st.radio("정렬모자", ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
        st.success(f"당신은 **{chosen}**!")

    with st.expander("🔽 길어지는 내용/코드를 접어두기"):
        st.code(
            "left, right = st.columns(2)\nwith left: ...\nwith right: ...",
            language="python"
        )

# ----------------------
# 6) 진행상태 (progress/spinner)
# ----------------------
with tabs[5]:
    st.subheader("6) 진행상태 표시")
    st.write("장시간 작업 시 진행률/상태를 보여줄 수 있어요.")
    if st.button("긴 작업 시작"):
        with st.spinner("계산 중..."):
            latest = st.empty()
            bar = st.progress(0)
            for i in range(100):
                latest.text(f"Iteration {i+1}")
                bar.progress(i + 1)
                time.sleep(0.02)
        st.success("완료!")

# ----------------------
# 7) 캐시(@st.cache_data)
# ----------------------
with tabs[6]:
    st.subheader("7) 캐시로 느린 연산/IO 가속")
    st.code(
        "@st.cache_data\ndef slow_sum(n):\n    time.sleep(2); return sum(range(n))",
        language="python"
    )

    @st.cache_data
    def slow_sum(n: int):
        time.sleep(2)  # 느린 계산 시뮬레이션
        return sum(range(n))

    n = st.number_input("합계 n", min_value=10, max_value=2_000_000, value=100_000, step=10_000)
    if st.button("계산"):
        s = slow_sum(int(n))
        st.success(f"결과: {s}  (첫 실행만 느리고, 이후 캐시됨)")

# ----------------------
# 8) 파일 업로드 (PDF/TXT/CSV) & 미리보기
# ----------------------
with tabs[7]:
    st.subheader("8) 파일 업로드")
    files = st.file_uploader("파일 선택 (txt/pdf/csv)", accept_multiple_files=True, type=["txt", "pdf", "csv"])
    if files:
        for f in files:
            st.write(f"**{f.name}**")
            if f.name.lower().endswith(".txt"):
                st.code(f.read().decode("utf-8", errors="ignore")[:1000])
            elif f.name.lower().endswith(".csv"):
                df = pd.read_csv(f)
                st.dataframe(df.head())
            elif f.name.lower().endswith(".pdf"):
                try:
                    from pypdf import PdfReader
                    reader = PdfReader(f)
                    text = []
                    for p in reader.pages[:3]:  # 미리보기 3쪽
                        text.append(p.extract_text() or "")
                    st.code("\n\n".join(text)[:1500])
                except Exception as e:
                    st.error(f"PDF 미리보기에 pypdf 필요: pip install pypdf\n{e}")

# ----------------------
# 9) Azure OpenAI (선택)
# ----------------------
if HAS_AZURE:
    with tabs[8]:
        st.subheader("9) Azure OpenAI (옵션)")
        st.caption("`.env`에 AZURE_* 값이 있으면 활성화됩니다. model=에는 반드시 **배포이름**을 사용하세요.")
        sys_prompt = st.text_area("System Prompt", "You are a helpful assistant.", height=100)
        q = st.text_input("질문")
        temp = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
        if st.button("질의하기"):
            try:
                resp = aoclient.chat.completions.create(
                    model=AZURE_DEPLOY,  # ⚠️ 모델명이 아니라 배포 이름
                    temperature=temp,
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": q or "테스트 한 줄만 답해줘."}
                    ],
                )
                st.success(resp.choices[0].message.content)
            except Exception as e:
                st.error(f"호출 에러: {e}")
else:
    st.info("🔐 Azure OpenAI 탭을 쓰려면 .env에 AZURE_ENDPOINT, OPENAI_API_KEY, OPENAI_API_VERSION, DEPLOYMENT_NAME 를 설정하세요.")
