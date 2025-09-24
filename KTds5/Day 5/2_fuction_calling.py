import os, json, math, ast, operator, urllib.parse, requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool

load_dotenv()
endpoint = os.getenv("AZURE_ENDPOINT")
api_key  = os.getenv("OPENAI_API_KEY")
api_ver  = os.getenv("OPENAI_API_VERSION")
deploy   = os.getenv("DEPLOYMENT_NAME")
for k, v in {"AZURE_ENDPOINT":endpoint,"OPENAI_API_KEY":api_key,"OPENAI_API_VERSION":api_ver,"DEPLOYMENT_NAME":deploy}.items():
    if not v: raise RuntimeError(f"env missing: {k}")

# ── Tools ──────────────────────────────────────────────────────────────
class WeatherArgs(BaseModel):
    city: str
    unit: str = Field(default="metric", pattern="^(metric|imperial)$")

def _wdesc(code: int) -> str:
    m={0:"맑음",1:"대체로 맑음",2:"부분적으로 구름",3:"흐림",45:"안개",48:"착빙 안개",
       51:"이슬비(약)",53:"이슬비(중)",55:"이슬비(강)",61:"비(약)",63:"비(중)",65:"비(강)",
       71:"눈(약)",73:"눈(중)",75:"눈(강)",80:"소나기(약)",81:"소나기(중)",82:"소나기(강)"}
    return m.get(code, f"코드 {code}")

@tool("get_weather", args_schema=WeatherArgs)
def get_weather(city: str, unit: str="metric") -> str:
    geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                       params={"name":city,"count":1,"language":"ko","format":"json"}, timeout=10).json()
    if not geo.get("results"): return json.dumps({"ok":False,"error":f"도시 없음: {city}"}, ensure_ascii=False)
    g0=geo["results"][0]; lat,lon,name,country=g0["latitude"],g0["longitude"],g0["name"],g0.get("country","")
    params={"latitude":lat,"longitude":lon,"current":"temperature_2m,apparent_temperature,weather_code,wind_speed_10m",
            "timezone":"Asia/Seoul"}
    if unit=="imperial": params.update(temperature_unit="fahrenheit", wind_speed_unit="mph")
    else: params.update(temperature_unit="celsius", wind_speed_unit="kmh")
    wx = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10).json()
    cur = wx.get("current", {})
    out={"ok":True,"city":f"{name}, {country}","temp":cur.get("temperature_2m"),
         "apparent":cur.get("apparent_temperature"),"wind":cur.get("wind_speed_10m"),
         "desc":_wdesc(cur.get("weather_code")) if cur.get("weather_code") is not None else None,
         "unit":unit,"time":cur.get("time")}
    return json.dumps(out, ensure_ascii=False)

class CalcArgs(BaseModel):
    expr: str

_ALLOWED_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos,
}

def _safe_eval(node):
    if isinstance(node, ast.Num): return node.n
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS: return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS: return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    raise ValueError("unsupported")

@tool("calc", args_schema=CalcArgs)
def calc(expr: str) -> str:
    val = _safe_eval(ast.parse(expr, mode="eval").body)
    return json.dumps({"ok":True,"expr":expr,"result":val}, ensure_ascii=False)

class WikiArgs(BaseModel):
    query: str
    sentences: int = 2

@tool("wiki_summary", args_schema=WikiArgs)
def wiki_summary(query: str, sentences: int=2) -> str:
    s = requests.get("https://ko.wikipedia.org/w/rest.php/v1/search/title",
                     params={"q":query,"limit":1}, timeout=10).json()
    if not s.get("pages"): return json.dumps({"ok":False,"error":"검색 결과 없음"}, ensure_ascii=False)
    title = s["pages"][0]["title"]
    summ = requests.get(f"https://ko.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}", timeout=10).json()
    text = (summ.get("extract") or "").splitlines()
    joined = " ".join(" ".join(text).split()[:500])
    return json.dumps({"ok":True,"title":title,"url":summ.get("content_urls",{}).get("desktop",{}).get("page"),
                       "summary":" ".join(joined.split(". ")[:sentences])}, ensure_ascii=False)

class NowArgs(BaseModel):
    city: str

@tool("now_in", args_schema=NowArgs)
def now_in(city: str) -> str:
    geo = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                       params={"name":city,"count":1,"language":"en","format":"json"}, timeout=10).json()
    if not geo.get("results"): return json.dumps({"ok":False,"error":f"도시 없음: {city}"}, ensure_ascii=False)
    g0=geo["results"][0]; lat,lon=g0["latitude"],g0["longitude"]
    wx = requests.get("https://api.open-meteo.com/v1/forecast",
                      params={"latitude":lat,"longitude":lon,"current":"temperature_2m","timezone":"auto"},
                      timeout=10).json()
    return json.dumps({"ok":True,"timezone":wx.get("timezone"),"local_time":wx.get("current",{}).get("time")}, ensure_ascii=False)

tools = [get_weather, calc, wiki_summary, now_in]

# ── LLM (Function-Calling) ─────────────────────────────────────────────
llm_fc = AzureChatOpenAI(
    azure_endpoint=endpoint, api_key=api_key, api_version=api_ver, deployment_name=deploy, temperature=0.2
).bind_tools(tools)

def chat_with_tools(user_text: str, max_calls: int = 4) -> str:
    messages = [{"role":"system","content":"한국어로 답하라. 필요 시 제공된 도구만 사용하라."},
                {"role":"user","content":user_text}]
    ai = llm_fc.invoke(messages); messages.append(ai)
    calls = getattr(ai, "tool_calls", None) or []
    n = 0
    while calls and n < max_calls:
        for tc in calls:
            name, args = tc["name"], tc["args"]
            if name == "get_weather": out = get_weather.invoke(args)
            elif name == "calc": out = calc.invoke(args)
            elif name == "wiki_summary": out = wiki_summary.invoke(args)
            elif name == "now_in": out = now_in.invoke(args)
            else: out = json.dumps({"ok":False,"error":"unknown tool"}, ensure_ascii=False)
            messages.append({"role":"tool","tool_call_id":tc["id"],"content":out})
        ai = llm_fc.invoke(messages); messages.append(ai)
        calls = getattr(ai, "tool_calls", None) or []
        n += 1
    return ai.content

if __name__ == "__main__":
    print("─①", chat_with_tools("서울과 원주의 현재 날씨를 비교하고, 25+17의 계산 결과도 알려줘."))
    print("─②", chat_with_tools("위키백과에서 아이폰 17을 찾아 1문장 요약해줘."))
    print("─③", chat_with_tools("런던의 현재 시각과 시간대만 알려줘."))
    print("─④", chat_with_tools("천안 날씨는 화씨로 알려주고 옷차림 한 줄로 추천해줘."))