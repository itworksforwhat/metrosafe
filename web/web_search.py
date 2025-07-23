import pandas as pd

def search_hosun(hosun,name,direction,date,time):

    #파일 이름 바뀌면 여기도 (절대경로에요 여기를 바꿔주세요)
    df = pd.read_csv('C:/Users/user/Desktop/project/metrosafe/model/test/'+hosun+'_혼잡도_전체예측결과.csv', encoding='utf-8-sig')
    
    #데이터 서치
    filter_name_df = df[df['역명']==name]
    filter_direction_df = filter_name_df[filter_name_df['방향']==direction]
    filter_date_df = filter_direction_df[filter_direction_df['평일/주말']==date]
    filter_time_df = filter_date_df[filter_date_df['시간대']==time]
    
    list_result_df = filter_time_df['혼잡레벨']
search_hosun('8호선',"암사","상행","평일","07:00")
    
    
    