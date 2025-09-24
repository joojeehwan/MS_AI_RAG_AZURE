import streamlit as st

st.title("3/6/9 게임 웹버전")
st.write("1부터 입력한 숫자까지 3, 6, 9가 들어가는 숫자에 '짝'을 출력합니다.")

max_num = st.number_input("숫자를 입력하세요", min_value=1, max_value=1000, value=50)

if st.button("게임 시작!"):
    result = []
    for i in range(1, max_num + 1):
        s = str(i)
        clap = s.count('3') + s.count('6') + s.count('9')
        if clap > 0:
            result.append("짝" * clap)
        else:
            result.append(str(i))
    st.write(result)