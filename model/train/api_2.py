import requests
import pandas as pd
import os
import time
from itertools import product

# === 1. 설정부분 === #
API_KEY = "24AIKyAUZk4oWhfEx6tUX6Qsk15ccQJD5wmJe7gE"
HEADERS = {"appkey": API_KEY}
STATION_META_URL = "https://apis.openapi.sk.com/puzzle/subway/meta/stations"
CONGESTION_API_URL_FMT = "https://apis.openapi.sk.com/puzzle/subway/congestion/stat/car/stations/{}"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 예시: 2호선 거점역 리스트
target_stations_2 = [
    "시청역", "을지로입구역", "을지로3가역", "을지로4가역", "동대문역사문화공원역", "신당역", "상왕십리역",
    "왕십리역", "한양대역", "뚝섬역", "성수역", "건대입구역", "구의역", "강변역", "잠실나루역", "잠실역",
    "잠실새내역", "종합운동장역", "삼성역", "선릉역", "역삼역", "강남역", "교대역", "서초역", "방배역",
    "사당역", "낙성대역", "서울대입구역", "봉천역", "신림역", "신대방역", "구로디지털단지역", "대림역",
    "신도림역", "문래역", "영등포구청역", "당산역", "합정역", "홍대입구역", "신촌역", "이대역",
    "아현역", "충정로역"
    # 원한다면 도림천역~신정네거리역 등 비환승/지선 포함 추가
]

# 시간·요일 리스트
HOUR_LIST  = [f"{h:02d}" for h in range(6, 24)]   # "06"~"23"
DOW_LIST   = [("MON", "월요일"), ("SAT", "토요일")] # (영문, 한글)
TARGET_LINE = "2호선"  # 대상 호선


# === 2. 역 메타정보에서 "호선+역명→역코드" 사전 만들기 === #
def fetch_all_stations():
    """모든 역의 메타정보를 받아 (호선, 역명) → 역코드 매핑"""
    stations = []
    offset = 0
    limit = 100
    total_count = None
    while True:
        params = {"offset": offset, "limit": limit}
        r = requests.get(STATION_META_URL, headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()
        if total_count is None:
            total_count = int(data["status"]["totalCount"])
        stations.extend(data.get("contents", []))
        offset += limit
        if len(stations) >= total_count:
            break
        time.sleep(0.03)
    return stations

print("역 메타데이터 로딩중...")
all_stations = fetch_all_stations()
station_code_map = {}
for st in all_stations:
    key = (st["subwayLine"], st["stationName"])
    station_code_map[key] = st["stationCode"]
print(f"전체 역 수 : {len(all_stations)}")


# === 3. (호선, 역명) → "역코드" 조인된 타겟 목록 만들기 === #
joined_targets = [
    (station_code_map[(TARGET_LINE, name)], name)
    for name in target_stations_2
    if (TARGET_LINE, name) in station_code_map
]

print(f"{TARGET_LINE} 유효역 수 : {len(joined_targets)}")


# === 4. "전체 요청해야 할 (역코드, dow, hh)" 세트(all_targets) 생성 === #
dow_en_list = [d[0] for d in DOW_LIST]
all_targets = set(product([code for code, _ in joined_targets], dow_en_list, HOUR_LIST))
print(f"총 요청 대상 개수: {len(all_targets)}")   # ex. 42×2×18 = 1512


# === 5. 이미 저장된 CSV로부터 '완료된' (역코드, dow, hh) 세트 수집 === #
saved_targets = set()
for dow_en, dow_kr in DOW_LIST:
    fname = os.path.join(OUTPUT_DIR, f"{TARGET_LINE}_{dow_kr}_혼잡도_거점역.csv")
    if not os.path.isfile(fname):
        continue
    df = pd.read_csv(fname, encoding="utf-8-sig")
    # 컬럼명이 다를 경우, 맞게 조정하세요
    for tup in df[["역코드", "요일", "시간"]].itertuples(index=False, name=None):
        saved_targets.add(tup)
print(f"이미 저장된 (역코드, dow, hh) 조합 개수: {len(saved_targets)}")

# === 6. 누락된 요청 조합만 추출 === #
missing_targets = list(all_targets - saved_targets)
print(f"누락된 요청 개수: {len(missing_targets)}")
# (역코드, dow, hh) tuple 목록


# === 7. 누락된 부분만 API로 재수집 === #
def fetch_congestion_10min_block(station_code, dow, hh):
    url = CONGESTION_API_URL_FMT.format(station_code)
    params = {"dow": dow, "hh": hh}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    contents = r.json().get("contents", None)
    rows = []
    if not contents or "stat" not in contents: return rows
    # ... 이하 기존 코드 동일 (for stat_block ...)
    for stat_block in contents["stat"]:
        for d in stat_block["data"]:
            rows.append({
                "호선": contents["subwayLine"],
                "역명": contents["stationName"],
                "역코드": contents["stationCode"],
                "요일": dow,
                "시간": d["hh"],
                "분": d["mm"],
                "상하행": stat_block.get("updnLine", None),
                "직통여부": stat_block.get("directAt", None),
                "구간시작역코드": stat_block.get("startStationCode", ""),
                "구간시작역": stat_block.get("startStationName", ""),
                "구간종료역코드": stat_block.get("endStationCode", ""),
                "구간종료역": stat_block.get("endStationName", ""),
                "직전역코드": stat_block.get("prevStationCode", ""),
                "직전역": stat_block.get("prevStationName", ""),
                "congestionCar": d["congestionCar"],
            })
    return rows

# 10개 마다 저장 등의 안전장치 추가 가능
append_rows = []
for idx, (station_code, dow, hh) in enumerate(missing_targets):
    try:
        new_rows = fetch_congestion_10min_block(station_code, dow, hh)
        append_rows.extend(new_rows)
        print(f"[{idx+1}/{len(missing_targets)}] 수집 {station_code},{dow},{hh} ({len(new_rows)} rows)")
    except Exception as e:
        print(f"실패: {station_code},{dow},{hh}: {e}")
    time.sleep(0.1)  # 과도한 호출 방지, 필요시 조정

# === 8. 누락분만 기존 파일에 append === #
if append_rows:
    df_append = pd.DataFrame(append_rows)
    # 요일별로 저장
    for dow_en, dow_kr in DOW_LIST:
        # 이번 수집분 중 해당 요일만 선별
        df_sub = df_append[df_append["요일"] == dow_en]
        if not df_sub.empty:
            fname = os.path.join(OUTPUT_DIR, f"{TARGET_LINE}_{dow_kr}_혼잡도_거점역.csv")
            # 기존 파일 있으면 append(중복 안나게!), 아니면 새로 저장
            mode = "a" if os.path.isfile(fname) else "w"
            header = not os.path.isfile(fname)
            df_sub.to_csv(fname, mode=mode, header=header, index=False, encoding="utf-8-sig")
            print(f"[APPEND] {fname} ({len(df_sub)} rows)")
else:
    print("추가된 누락 데이터 없음.")

