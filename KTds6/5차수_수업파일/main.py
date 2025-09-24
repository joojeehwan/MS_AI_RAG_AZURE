from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

from langchain_openai import ChatOpenAI
from typing import TypedDict

from dotenv import load_dotenv
load_dotenv()

# LLM 인스턴스 생성
llm = ChatOpenAI(model="gpt-4.1-mini")

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from langchain_openai import ChatOpenAI

# 상태 정의
class State(TypedDict):
    original_text: str   # 원본 텍스트
    summary: str         # 요약본
    final_summary: str   # 최종 요약본

# LLM 인스턴스 생성
summary_llm = ChatOpenAI(model="gpt-4.1-mini")
eval_llm = ChatOpenAI(model="gpt-4.1")

# 요약 생성 노드
def generate_summary(state: State) -> Command[Literal["improve_summary", "finalize_summary"]]:
    """원본 텍스트를 요약하고 품질을 평가하는 노드"""
    # 요약 생성
    summary_prompt = f"""다음 텍스트를 핵심 내용 중심으로 간단히 요약해주세요:

    [텍스트]
    {state['original_text']}

    [요약]
    """
    summary = summary_llm.invoke(summary_prompt).content

#     summary = """인공지능은 컴퓨터 과학의 한 분야이며 인간의 능력을 구현한 것인데 \
# 요즘에는 정말 다양한 분야에서 활용되고 있고 특히 기계학습이랑 딥러닝이 발전하면서 \
# 더욱 활용도가 높아지고 있다고 합니다"""  # 테스트용

    # 품질 평가
    eval_prompt = f"""다음 요약의 품질을 평가해주세요. 
    요약이 명확하고 핵심을 잘 전달하면 'good'을, 
    개선이 필요하면 'needs_improvement'를 응답해주세요.
    
    요약본: {summary}
    """
    quality = eval_llm.invoke(eval_prompt).content.lower().strip()
    
    # 상태 업데이트와 함께 다음 노드로 라우팅
    return Command(
        goto="finalize_summary" if "good" in quality else "improve_summary",
        update={"summary": summary}
    )

# 요약 개선 노드
def improve_summary(state: State) -> Command[Literal[END]]:
    """요약을 개선하고 다듬는 노드"""
    prompt = f"""다음 요약을 더 명확하고 간결하게 개선해주세요:
    
    [기존 요약]
    {state['summary']}

    [개선 요약]
    """
    improved_summary = llm.invoke(prompt).content
    
    # 상태 업데이트와 함께 다음 노드로 라우팅
    return Command(
        goto=END,
        update={"final_summary": improved_summary}
    )

# 최종 요약 설정 노드
def finalize_summary(state: State) -> Command[Literal[END]]:
    """현재 요약을 최종 요약으로 설정하는 노드"""

    # 상태 업데이트와 함께 다음 노드로 라우팅
    return Command(
        goto=END,
        update={"final_summary": state["summary"]}
    )

# 워크플로우 구성
workflow = StateGraph(State)

# 노드 추가
workflow.add_node("generate_summary", generate_summary)
workflow.add_node("improve_summary", improve_summary)
workflow.add_node("finalize_summary", finalize_summary)

# 기본 엣지 추가
workflow.add_edge(START, "generate_summary")

# 그래프 컴파일
graph = workflow.compile()