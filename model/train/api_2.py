import pandas as pd

# 파일 경로
f_mon = "output/7호선_월요일_혼잡도_거점역.csv"
f_sat = "output/7호선_토요일_혼잡도_거점역.csv"
f_merged = "output/날짜합친7호선.csv"

# 파일 읽기 (encoding='utf-8-sig'로 저장되었을 확률 높음)
df_mon = pd.read_csv(f_mon, encoding='utf-8-sig')
df_sat = pd.read_csv(f_sat, encoding='utf-8-sig')

# 병합 (위아래로 행을 붙임)
df_merged = pd.concat([df_mon, df_sat], ignore_index=True)

# 저장
df_merged.to_csv(f_merged, index=False, encoding='utf-8-sig')
print(f"병합 결과 저장: {f_merged} (총 {len(df_merged)} rows)")
