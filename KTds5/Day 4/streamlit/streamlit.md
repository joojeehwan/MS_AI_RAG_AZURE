# Streamlit의 기본 개념
Streamlit으로 작업하는 것은 간단합니다. 먼저 몇 가지 Streamlit 명령을 뿌립니다 일반 Python 스크립트에 넣은 다음 다음과 같이 실행합니다.streamlit run

streamlit run your_script.py [-- script args]
위와 같이 스크립트를 실행하자마자 로컬 Streamlit 서버가 스핀업을 하면 앱이 기본 웹 브라우저의 새 탭에서 열립니다. 앱 은 차트, 텍스트, 위젯, 표 등을 그릴 수 있는 캔버스입니다.

앱에서 무엇을 그릴지는 당신에게 달려 있습니다. 예를 들어 st.text는 앱에 원시 텍스트를 쓰고, st.line_chart 는 짐작할 수 있듯이 꺾은선형 차트. 다음과 같은 모든 명령을 보려면 API 설명서를 참조하십시오. 사용할 수 있습니다.
 
**메모**
> 스크립트에 일부 사용자 지정 인수를 전달할 때 두 개의 대시 뒤에 전달해야 합니다. 그렇지 않으면 arguments는 Streamlit 자체에 대한 인수로 해석됩니다.

Streamlit을 실행하는 또 다른 방법은 Python 모듈로 실행하는 것입니다. 이것은 될 수 있습니다 Streamlit과 함께 작동하도록 PyCharm과 같은 IDE를 구성할 때 유용합니다.

### Running
```
python -m streamlit run your_script.py
```

### is equivalent to:
streamlit run your_script.py

URL을 ! 이것은 다음과 결합될 때 훌륭합니다. GitHub Gists. 예를 들어:streamlit run

```
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py
```


# 개발 흐름
앱을 업데이트할 때마다 소스 파일을 저장하세요. 당신이 할 때 Streamlit은 변경 사항이 있는지 감지하고 변경 사항이 있는지 묻습니다 앱을 다시 실행합니다. 화면 오른쪽 위에 있는 "항상 다시 실행"을 선택하여 다음을 수행합니다. 소스 코드를 변경할 때마다 앱을 자동으로 업데이트합니다.

이를 통해 빠른 대화형 루프에서 작업할 수 있습니다: 코드를 입력하고 저장합니다. 라이브로 사용해 본 다음 코드를 더 입력하고, 저장하고, 사용해 보는 등의 작업을 수행합니다 결과에 만족할 때까지. 코딩과 시청 사이의 긴밀한 고리 결과 라이브는 Streamlit이 삶을 더 쉽게 만드는 방법 중 하나입니다.


팁
> Streamlit 앱을 개발하는 동안 편집기를 배치하고 브라우저 창이 나란히 있으므로 코드와 앱을 동시에 볼 수 있습니다. 시간. 한 번 시도해 보세요!

Streamlit 버전 1.10.0 이상부터는 Linux 배포판의 루트 디렉터리에서 Streamlit 앱을 실행할 수 없습니다. 루트 디렉터리에서 Streamlit 앱을 실행하려고 하면 Streamlit에서 오류가 발생합니다. 자세한 내용은 GitHub 문제 #5239를 참조하세요.FileNotFoundError: [Errno 2] No such file or directory

Streamlit 버전 1.10.0 이상을 사용하는 경우 기본 스크립트는 루트 디렉터리가 아닌 다른 디렉터리에 있어야 합니다. Docker를 사용할 때 명령을 사용하여 기본 스크립트가 있는 디렉토리를 지정할 수 있습니다. 이 작업을 수행하는 방법의 예는 Dockerfile 만들기를 참조하세요.WORKDIR

# 데이터 흐름
Streamlit의 아키텍처를 사용하면 일반 작성과 동일한 방식으로 앱을 작성할 수 있습니다 Python 스크립트. 이를 잠금 해제하기 위해 Streamlit 앱에는 고유한 데이터 흐름이 있습니다. 화면에서 무언가를 업데이트해야 할 때 Streamlit은 전체를 다시 실행합니다. Python 스크립트를 위에서 아래로 이동합니다.

이 문제는 두 가지 상황에서 발생할 수 있습니다.

앱의 소스 코드를 수정할 때마다.

사용자가 앱에서 위젯과 상호 작용할 때마다. 예를 들어 드래그할 때 슬라이더, 입력 상자에 텍스트를 입력하거나 단추를 클릭합니다.

콜백이 (또는 ) 매개변수를 통해 위젯에 전달될 때마다 콜백은 항상 스크립트의 나머지 부분보다 먼저 실행됩니다. 콜백 API에 대한 자세한 내용은 Session State API Reference Guide를 참조하세요.on_changeon_click

그리고 이 모든 것을 빠르고 원활하게 하기 위해 Streamlit은 몇 가지 힘든 일을 합니다 무대 뒤에서 당신을 위해. 이 이야기에서 큰 역할을 하는 것은 @st.cache_data 데코레이터로, 개발자가 특정 항목을 건너뛸 수 있습니다. 앱을 다시 실행할 때 비용이 많이 드는 계산. 이 글의 뒷부분에서 캐싱에 대해 다루겠습니다 페이지.

# 데이터 표시 및 스타일 지정
Streamlit에서 데이터(테이블, 배열, 데이터 프레임)를 표시하는 몇 가지 방법이 있습니다 아래에서는 magic과 st.write()를 소개할 것입니다. 텍스트에서 표에 이르기까지 모든 것. 그런 다음 설계된 방법을 살펴보겠습니다 특히 데이터 시각화를 위한 것입니다.

### 마법을 사용하세요
Streamlit 메서드를 호출하지 않고 앱에 쓸 수도 있습니다. Streamlit은 "매직 커맨드"를 지원하는데, 이는 st.write()를 전혀 사용할 필요가 없다는 것을 의미합니다! 이 작업을 보려면 다음 스니펫을 사용해 보세요.

```
"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df
```
Streamlit이 변수 또는 리터럴을 볼 때마다 value를 한 줄에 넣으면 st.write()를 사용하여 앱에 자동으로 씁니다. 자세한 내용은 를 참조하십시오. 매직 명령에 대한 설명서.

# 데이터 프레임 쓰기
마법 명령어와 함께 st.write()는 Streamlit의 "스위스 군용 칼"입니다. 너 거의 모든 것을 st.write()에 전달할 수 있습니다. 텍스트, 데이터, Matplotlib 그림, Altair 차트 등. 걱정하지 마세요, Streamlit 그것을 알아 내고 올바른 방법으로 사물을 렌더링 할 것입니다.

```
import streamlit as st
import pandas as pd

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
```

st.dataframe() 및 st.table() 과 같은 다른 데이터 특정 함수를 표시하는 데 사용할 수도 있습니다 데이터. 이러한 기능을 언제 사용해야 하는지, 데이터 프레임에 색상과 스타일을 추가하는 방법을 이해해 보겠습니다.

당신은 스스로에게 "왜 나는 항상 사용하지 않을까요?" 있습니다 몇 가지 이유는 다음과 같습니다.st.write()

1. Magic 및 st.write() 는 의 유형을 검사합니다. 전달한 데이터를 만든 다음 에서 가장 잘 렌더링하는 방법을 결정합니다. 앱. 때로는 다른 방식으로 그리고 싶을 때가 있습니다. 예를 들어 대신 DataFrame을 대화형 테이블로 그리는 경우 다음과 같이 그릴 수 있습니다. 를 사용하여 정적 테이블 .st.table(df)
2. 두 번째 이유는 다른 메소드가 사용할 수있는 객체를 반환하기 때문입니다 데이터를 추가하거나 교체하여 수정했습니다.
3. 마지막으로, 보다 구체적인 Streamlit 메서드를 사용하는 경우 추가 동작을 사용자 지정하는 인수입니다.

예를 들어 데이터 프레임을 만들고 Pandas 개체로 서식을 변경해 보겠습니다. 이 예제에서는 Numpy를 사용하여 무작위 샘플을 생성합니다. 그리고 st.dataframe() 메소드를 사용하여 대화형 테이블.Styler

**메모**
>이 예제에서는 Numpy를 사용하여 무작위 샘플을 생성하지만 Pandas를 사용할 수 있습니다 DataFrames, Numpy 배열 또는 일반 Python 배열.

```
import streamlit as st
import numpy as np

dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)
```

Pandas 객체를 사용하여 강조 표시한 첫 번째 예제를 확장해 보겠습니다 대화형 테이블의 일부 요소.Styler

```
import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
```

Streamlit에는 정적 테이블 생성 방법인 st.table()도 있습니다.

```
import streamlit as st
import numpy as np
import pandas as pd

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)
```

# 차트 및 지도 그리기
Streamlit은 Matplotlib와 같은 여러 인기 있는 데이터 차트 라이브러리를 지원합니다. 알테어, deck.gl 등 이 섹션에서는 다음을 수행합니다 가로 막대형 차트, 꺾은선형 차트 및 지도를 앱에 추가합니다.

# 꺾은선형 차트 그리기
st.line_chart()를 사용하여 앱에 꺾은선형 차트를 쉽게 추가할 수 있습니다. 우리는 무작위를 생성할 것입니다 Numpy를 사용하여 샘플링 한 다음 차트로 작성하십시오.

```
import streamlit as st
import numpy as np
import pandas as pd

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)
```

# 지도 플로팅
st.map()을 사용하면 지도에 데이터 포인트를 표시할 수 있습니다. Numpy를 사용하여 몇 가지 샘플 데이터를 생성하고 맵에 플로팅해 보겠습니다. 샌프란시스코.

```
import streamlit as st
import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)
```

# 위젯
데이터 또는 모델을 탐색하려는 상태로 가져오면 다음을 수행할 수 있습니다 st.slider(), st.button() 또는 st.selectbox()와 같은 위젯을 추가할 수 있습니다. 정말 간단합니다 — 위젯을 변수로 취급:

```
import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)
```

처음 실행할 때 위의 앱은 "0 squared is 0"이라는 텍스트를 출력해야 합니다. 그러면 사용자가 위젯과 상호 작용할 때마다 Streamlit은 스크립트를 다시 실행합니다 위에서 아래로, 위젯의 현재 상태를 변수에 할당합니다 그 과정에서.

예를 들어 사용자가 슬라이더를 위치로 이동하면 Streamlit은 위의 코드를 다시 실행하고 그에 따라 설정합니다. 이제 당신은 볼 수 있습니다 "10의 제곱은 100"이라는 텍스트.10x10

위젯은 위젯의 고유 키로 사용할 문자열을 지정하도록 선택한 경우 키로 액세스할 수도 있습니다.

```
import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name
```

키가 있는 모든 위젯은 세션 상태에 자동으로 추가됩니다. 세션 상태, 위젯 상태와의 연관성 및 제한 사항에 대한 자세한 내용은 Session State API Reference Guide를 참조하세요.

# 확인란을 사용하여 데이터 표시/숨기기
확인란의 한 가지 사용 사례는 특정 차트 또는 섹션을 숨기거나 표시하는 것입니다. st.checkbox()는 단일 인자를 취합니다. 위젯 레이블입니다. 이 샘플에서는 확인란을 사용하여 조건문.

```
import streamlit as st
import numpy as np
import pandas as pd

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data
```

# 옵션에 선택 상자 사용
st.selectbox를 사용하여 시리즈에서 선택하십시오. 너 원하는 옵션을 작성하거나 배열 또는 데이터 프레임을 전달할 수 있습니다. 열.

앞서 만든 데이터 프레임을 사용해봅시다.df

```
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option
```

# 레이아웃
Streamlit을 사용하면 st.sidebar를 사용하여 왼쪽 패널 사이드바에서 위젯을 쉽게 구성할 수 있습니다. st.sidebar 에 전달 된 각 요소는 왼쪽에 고정되어 있습니다. 사용자가 UI에 계속 액세스할 수 있는 동안 앱의 콘텐츠에 집중할 수 있습니다. 컨트롤.

예를 들어 선택 상자와 슬라이더를 사이드바에 추가하려는 경우 and 대신 and 사용 :st.sidebar.sliderst.sidebar.selectboxst.sliderst.selectbox

```
import streamlit as st

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
```

사이드바 외에도 Streamlit은 레이아웃을 제어하는 몇 가지 다른 방법을 제공합니다 st.columns를 사용하면 위젯을 나란히 배치할 수 있고 st.expander를 사용하면 큰 콘텐츠를 숨겨 공간을 절약할 수 있습니다.

```
import streamlit as st

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")
```

**메모**
> st.echo 현재 사이드바 내에서 지원되지 않습니다. 또는 레이아웃 옵션. 하지만 현재 해당 항목에 대한 지원을 추가하기 위해 노력하고 있으니 안심하셔도 됩니다!st.spinner

# 진행 상황 표시
앱에 장기 실행 계산을 추가할 때 st.progress()를 사용하여 실시간으로 상태를 표시할 수 있습니다.

먼저 시간을 가져오겠습니다. 우리는 그 방법을 사용하여 다음을 수행할 것입니다. 장기 실행 계산을 시뮬레이션합니다.time.sleep()

```
import time
```

이제 진행률 표시줄을 만들어 보겠습니다.

```
import streamlit as st
import time

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'
```