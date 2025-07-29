import streamlit as st
import random
import pandas as pd
from matplotlib import rc
from streamlit.components.v1 import html
import ast

# ----------------------------
# 기본 설정
# ----------------------------
rc("font", family="Malgun Gothic")
st.set_page_config(layout="wide")


def search_hosun(hosun, name, direction, date, time):

    direction_map = {"상행": 0, "하행": 1}
    weekday_map = {"평일": ["MON", "TUE", "WED", "THU", "FRI"], "주말": ["SAT", "SUN"]}

    try:
        df = pd.read_csv(
            f"./model/data/api_데이터/날짜합친{hosun}.csv", encoding="euc-kr"
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            f"./model/data/api_데이터/날짜합친{hosun}.csv", encoding="utf-8"
        )

    filter_name_df = df[df["역명"] == name]
    filter_direction_df = filter_name_df[
        filter_name_df["상하행"] == direction_map[direction]
    ]
    filter_day_df = filter_direction_df[
        filter_direction_df["요일"].isin(weekday_map[date])
    ]
    hour, minute = map(int, time.split(":"))
    filter_time_df = filter_day_df[
        (filter_day_df["시간"] == hour) & (filter_day_df["분"] == minute)
    ]

    list_result_df = []
    for s in filter_time_df["congestionCar"]:
        try:
            v = eval(s)  # 또는 ast.literal_eval(s)
            list_result_df = v
        except:
            continue

    return list_result_df


# 배경화면
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
  position: relative;
  z-index: 0;
}

[data-testid="stAppViewContainer"]::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 110vw;
  height: 100vh;
  background-image: url("https://www.inat.fr/files/seoul-metro-subway-map.png");
  background-size: 80% auto;
  background-repeat: no-repeat;
  background-position: 70% -180px;
  opacity: 0.2;
  z-index: -1;
  pointer-events: none;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ----------------------------
# 역 데이터 및 열차칸 수 설정
# ----------------------------
station_name = {
    "1호선": [
        "서울역",
        "시청역",
        "종각역",
        "종로3가역",
        "종로5가역",
        "동대문역",
        "신설동역",
        "제기동역",
        "청량리역",
        "동묘앞역",
    ],
    "2호선": [
        "시청역",
        "을지로입구역",
        "을지로3가역",
        "을지로4가역",
        "동대문역사문화공원역",
        "신당역",
        "상왕십리역",
        "왕십리역",
        "한양대역",
        "뚝섬역",
        "건대입구역",
        "구의역",
        "강변역",
        "잠실나루역",
        "잠실역",
        "잠실새내역",
        "종합운동장역",
        "삼성역",
        "선릉역",
        "역삼역",
        "강남역",
        "교대역",
        "서초역",
        "방배역",
        "사당역",
        "낙성대역",
        "서울대입구역",
        "봉천역",
        "신림역",
        "신대방역",
        "구로디지털단지역",
        "대림역",
        "신도림역",
        "문래역",
        "영등포구청역",
        "당산역",
        "합정역",
        "홍대입구역",
        "신촌역",
        "이대역",
        "아현역",
        "충정로역",
    ],
    "3호선": [
        "지축역",
        "구파발역",
        "연신내역",
        "불광역",
        "녹번역",
        "홍제역",
        "무악재역",
        "독립문역",
        "경복궁역",
        "안국역",
        "종로3가역",
        "을지로3가역",
        "충무로역",
        "동대입구역",
        "약수역",
        "금호역",
        "옥수역",
        "압구정역",
        "신사역",
        "잠원역",
        "고속터미널역",
        "교대역",
        "남부터미널역",
        "양재역",
        "매봉역",
        "도곡역",
        "대치역",
        "학여울역",
        "대청역",
        "일원역",
        "수서역",
        "가락시장역",
        "경찰병원역",
        "오금역",
    ],
    "4호선": [
        "상계역",
        "노원역",
        "창동역",
        "쌍문역",
        "수유역",
        "미아역",
        "미아삼거리역",
        "길음역",
        "성신여대입구역",
        "한성대입구역",
        "혜화역",
        "동대문역",
        "동대문역사문화공원역",
        "충무로역",
        "명동역",
        "회현역",
        "서울역",
        "숙대입구역",
        "삼각지역",
        "신용산역",
        "이촌역",
        "동작역",
        "사당역",
        "남태령역",
    ],
    "5호선": [
        "개화산역",
        "김포공항역",
        "송정역",
        "마곡역",
        "발산역",
        "우장산역",
        "화곡역",
        "까치산역",
        "신정역",
        "목동역",
        "오목교역",
        "양평역",
        "영등포구청역",
        "영등포시장역",
        "신길역",
        "여의도역",
        "여의나루역",
        "마포역",
        "공덕역",
        "애오개역",
        "충정로역",
        "서대문역",
        "광화문역",
        "종로3가역",
        "을지로4가역",
        "동대문역사문화공원역",
        "청구역",
        "신금호역",
        "행당역",
        "왕십리역",
        "마장역",
        "답십리역",
        "장한평역",
        "군자역",
        "아차산역",
        "광나루역",
        "천호역",
        "강동역",
        "길동역",
        "굽은다리역",
        "명일역",
        "고덕역",
        "상일동역",
        "둔촌동역",
        "올림픽공원역(한국체대)",
        "방이역",
        "오금역",
        "개롱역",
        "거여역",
        "마천역",
        "강일역",
        "미사역",
        "하남풍산역",
        "하남시청역",
        "하남검단산역",
    ],
    "6호선": [
        "응암역",
        "새절역",
        "증산역",
        "디지털미디어시티역",
        "월드컵경기장역",
        "마포구청역",
        "망원역",
        "합정역",
        "상수역",
        "광흥창역",
        "대흥역",
        "공덕역",
        "효창공원앞역",
        "삼각지역",
        "녹사평역",
        "이태원역",
        "한강진역",
        "버티고개역",
        "약수역",
        "청구역",
        "신당역",
        "동묘앞역",
        "창신역",
        "보문역",
        "안암역",
        "고려대역",
        "월곡역",
        "상월곡역",
        "돌곶이역",
        "석계역",
        "태릉입구역",
        "화랑대역",
        "봉화산역",
        "신내역",
    ],
    "7호선": [
        "도봉산역",
        "수락산역",
        "마들역",
        "노원역",
        "중계역",
        "하계역",
        "공릉역",
        "태릉입구역",
        "먹골역",
        "중화역",
        "상봉역",
        "면목역",
        "사가정역",
        "용마산역",
        "중곡역",
        "군자역",
        "어린이대공원역",
        "건대입구역",
        "자양역(뚝섬한강공원)",
        "청담역",
        "강남구청역",
        "학동역",
        "논현역",
        "반포역",
        "고속터미널역",
        "내방역",
        "총신대입구역",
        "남성역",
        "숭실대입구역",
        "상도역",
        "장승배기역",
        "신대방삼거리역",
        "보라매역",
        "신풍역",
        "대림역",
        "남구로역",
        "가산디지털단지역",
        "철산역",
        "광명사거리역",
        "천왕역",
        "온수역",
    ],
    "8호선": [
        "천호역",
        "강동구청역",
        "몽촌토성역",
        "잠실역",
        "석촌역",
        "송파역",
        "가락시장역",
        "문정역",
        "장지역",
        "복정역",
        "산성역",
        "남한산성입구역",
        "단대오거리역",
        "신흥역",
        "수진역",
        "모란역",
    ],
}

hosun_car_count = {
    "1호선": 10,
    "2호선": 10,
    "3호선": 10,
    "4호선": 10,
    "5호선": 8,
    "6호선": 8,
    "7호선": 8,
    "8호선": 6,
}
station_time = [f"{i:02d}:00" for i in list(range(6, 24)) + [0]]

st.sidebar.title("선택 구간")
select_hosun = st.sidebar.selectbox("호선", list(station_name.keys()))
select_name = st.sidebar.selectbox("역명", station_name[select_hosun])
select_time = st.sidebar.selectbox("시간", station_time)
select_direction = st.sidebar.selectbox("상/하행", ["상행", "하행"])
select_weekend = st.sidebar.selectbox("평일/주말", ["평일", "주말"])

hosun_colors = {
    "1호선": "#0052A4",
    "2호선": "#009D3E",
    "3호선": "#EF7C1C",
    "4호선": "#00A5DE",
    "5호선": "#996CAC",
    "6호선": "#CD7C2F",
    "7호선": "#747F00",
    "8호선": "#E6186C",
}

line_color = hosun_colors.get(select_hosun, "#555")

# 상단 UI
html_content = f"""
<div style="position: relative; width: 100%; display: flex; justify-content: center; margin-top: 10px; margin-bottom: 50px;">
    <div style="position: absolute; top: 50%; left: 0; width: 100%; height: 50px; background-color: {line_color}; transform: translateY(-50%); z-index: 0; border-radius: 40px;"></div>
    <div style="display: flex; align-items: center; background-color: white; padding: 20px 70px 20px 100px; border-radius: 50px; border: 10px solid {line_color}; z-index: 1; position: relative; min-width: 400px; max-width: 700px; box-shadow: 3px 3px 10px rgba(0,0,0,0.15); outline: 4px solid white; outline-offset: 0px;">
        <div style="background-color: {line_color}; color: white; font-weight: bold; font-size: 25px; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; position: absolute; left: 20px; top: 50%; transform: translateY(-50%); border: 4px solid white; box-shadow: 1px 1px 5px rgba(0,0,0,0.1);">
            {select_hosun}
        </div>
        <div style="flex: 1; text-align: center; font-size: 45px; font-weight: bold; color: black; padding-left: 20px;">
            {select_name}
        </div>
    </div>
</div>
"""
html(html_content, height=150, scrolling=False)


# 추천 칸 판단 함수
def get_color(p):
    if p <= 40:
        return "#70ad47"
    elif p <= 70:
        return "#ffc000"
    elif p <= 110:
        return "#ff7e00"
    else:
        return "#ff0000"


def get_label(p):
    if p <= 40:
        return "여유"
    elif p <= 70:
        return "보통"
    elif p <= 110:
        return "혼잡"
    else:
        return "매우혼잡"


car_count = hosun_car_count.get(select_hosun, 8)

congestion_data = search_hosun(
    select_hosun, select_name, select_direction, select_weekend, select_time
)
# congestion_data = ast.literal_eval(congestion_data)
cars_with_data = [(i, congestion_data[i]) for i in range(car_count)]
# ----------------------- 여기만 변경(추천칸 선택 부분!!) -----------------------
cars_with_data = [(i, congestion_data[i]) for i in range(car_count)]
cars_with_data.sort(key=lambda x: x[1])
recommended_car_indices = [idx for idx, _ in cars_with_data[:2]]
# --------------------------------------------------------------------------

# 상단 정보 및 추천 텍스트 출력
info_bar = f"""
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 25px; color: #666; margin-top: 10px; margin-bottom: 20px; font-weight: bold; padding-left: 20px; padding-right: 20px;">
    <div>🚇 {select_direction} | {select_weekend} | {select_time} 기준</div>
    {f'<div style="font-size: 22px; font-weight: bold; color: #008000; display: flex; align-items: center;"><span style="font-size:25px; margin-right:5px;">✅</span> 탑승추천</div>' if recommended_car_indices else ''}
</div>
"""
st.markdown(info_bar, unsafe_allow_html=True)

# 공백 추가 (추천 아래)
st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

# 열차 시각화
train_html = f"""
<div style='display: flex; justify-content: center; gap: 3px; flex-wrap: wrap;'>
"""
for i in range(car_count):
    color = get_color(congestion_data[i])
    label = get_label(congestion_data[i])
    print(congestion_data)
    recommend_tag = ""
    if i in recommended_car_indices:
        recommend_tag = """
        <div style="text-align: center; margin-top: 5px; font-size: 15px; font-weight: bold; color: #008000;">
            ✅ 추천
        </div>
        """
    car_html = f"""
    <div style="display: flex; flex-direction: column; align-items: center;">
        <div style="background-color:{color}; border: 2px solid white; border-radius:12px; padding:10px; width: 80px; height: 110px; font-family:'Malgun Gothic', sans-serif; color:white; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <div style='font-weight:bold; font-size:25px;'>{i+1}</div>
            <div style='font-weight:bold; font-size:15px; color:#f0f0f0;'>{label}</div>
        </div>
        {recommend_tag}
    </div>
    """
    train_html += car_html

train_html += "</div>"
html(train_html, height=200, scrolling=False)
