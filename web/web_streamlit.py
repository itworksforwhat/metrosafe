import streamlit as st
import random
from matplotlib import rc
from streamlit.components.v1 import html

# ----------------------------
# 기본 설정
# ----------------------------
rc('font', family="Malgun Gothic")
st.set_page_config(layout="wide")

# 배경화면
page_bg_img = '''
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
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# ----------------------------
# 역 데이터 및 열차칸 수 설정
# ----------------------------
station_name = {
    "1호선": ['서울역','시청','종각','종로3가','종로5가','동대문','신설동','제기동','청량리','동묘앞'],
    "2호선": ['시청','을지로입구','을지로3가','을지로4가','동대문역사문화공원','신당','상왕십리','왕십리','한양대','뚝섬','성수','건대입구','구의','강변','잠실나루','잠실','잠실새내','종합운동장','삼성','선릉','역삼','강남','교대','서초','방배','사당','낙성대','서울대입구','봉천','신림','신대방','구로디지털단지','대림','신도림','문래','영등포구청','당산','합정','홍대입구','신촌(지하)','이대','아현','충정로','용답','신답','신설동','도림천','양천구청','신정네거리','용두'],
    "3호선": ['지축','구파발','연신내','불광','녹번','홍제','무악재','독립문','경복궁','안국','종로3가','을지로3가','충무로','동대입구','약수','금호','옥수','압구정','신사','잠원','고속터미널','교대','남부터미널','양재','매봉','도곡','대치','학여울','대청','일원','수서','가락시장','경찰병원','오금'],
    "4호선": ['상계','노원','창동','쌍문','수유','미아','미아삼거리','길음','성신여대입구','한성대입구','혜화','동대문','동대문역사문화공원','충무로','명동','회현','서울역','숙대입구','삼각지','신용산','이촌','동작','총신대입구','사당','남태령'],
    "5호선": ['개화산','김포공항','송정','마곡','발산','우장산','화곡','까치산','신정','목동','오목교','양평','영등포구청','영등포시장','신길','여의도','여의나루','마포','공덕','애오개','충정로','서대문','광화문','종로3가','을지로4가','동대문역사문화공원','청구','신금호','행당','왕십리','마장','답십리','장한평','군자','아차산','광나루','천호','강동','길동','굽은다리','명일','고덕','상일동','둔촌동','올림픽공원(한국체대)','방이','오금','개롱','거여','마천','강일','미사','하남풍산','하남시청','하남검단산'],
    "6호선": ['응암','새절','증산','디지털미디어시티','월드컵경기장','마포구청','망원','합정','상수','광흥창','대흥','공덕','효창공원앞','삼각지','녹사평','이태원','한강진','버티고개','약수','청구','신당','동묘앞','창신','보문','안암','고려대','월곡','상월곡','돌곶이','석계','태릉입구','화랑대','봉화산','신내'],
    "7호선": ['도봉산','수락산','마들','노원','중계','하계','공릉','태릉입구','먹골','중화','상봉','면목','사가정','용마산','중곡','군자','어린이대공원','건대입구','자양(뚝섬한강공원)','청담','강남구청','학동','논현','반포','고속터미널','내방','총신대입구','남성','숭실대입구','상도','장승배기','신대방삼거리','보라매','신풍','대림','남구로','가산디지털단지','철산','광명사거리','천왕','온수'],
    "8호선": ['천호','강동구청','몽촌토성','잠실','석촌','송파','가락시장','문정','장지','복정','산성','남한산성입구','단대오거리','신흥','수진','모란']
}

hosun_car_count = { '1호선': 10, '2호선': 10, '3호선': 10, '4호선': 10, '5호선': 8, '6호선': 8, '7호선': 8, '8호선': 8 }
station_time = [f"{i}:00" for i in range(5, 24)] + ["0:00"]

st.sidebar.title("선택 구간")
select_hosun = st.sidebar.selectbox("호선", list(station_name.keys()))
select_name = st.sidebar.selectbox("역명", station_name[select_hosun])
select_time = st.sidebar.selectbox("시간", station_time)
select_direction = st.sidebar.selectbox("상/하행", ['상행', '하행'])
select_weekend = st.sidebar.selectbox("평일/주말", ['평일', '주말'])

hosun_colors = {
    '1호선': '#0052A4',
    '2호선': '#009D3E',
    '3호선': '#EF7C1C',
    '4호선': '#00A5DE',
    '5호선': '#996CAC',
    '6호선': '#CD7C2F',
    '7호선': '#747F00',
    '8호선': '#E6186C'
}

line_color = hosun_colors.get(select_hosun, '#555')

# 상단 UI
html_content = f'''
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
'''
html(html_content, height=150, scrolling=False)

# 추천 칸 판단 함수
def get_color(p):
    if p < 30: return "#70ad47"
    elif p < 50: return "#ffc000"
    elif p < 80: return "#ff7e00"
    else: return "#ff0000"

def get_label(p):
    if p < 30: return "여유"
    elif p < 50: return "보통"
    elif p < 80: return "혼잡"
    else: return "매우혼잡"

car_count = hosun_car_count.get(select_hosun, 8)
congestion_data = [random.randint(10, 100) for _ in range(car_count)]
cars_with_data = [(i, congestion_data[i]) for i in range(car_count)]
relaxed_cars = [(idx, p) for idx, p in cars_with_data if get_label(p) == "여유"]
relaxed_cars.sort(key=lambda x: x[1])
recommended_car_indices = [idx for idx, _ in relaxed_cars[:2]]

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
