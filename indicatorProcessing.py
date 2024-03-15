import json

import pandas as pd
import warnings
import os

warnings.filterwarnings(action='ignore')

# 입력 및 출력 디렉토리
excel_files_directory = 'data/'
output_directory = 'result/'

# 입력 디렉토리에서 Excel 파일 목록 가져오기
excel_files = [file for file in os.listdir(excel_files_directory) if file.endswith('.xlsx')]

# 모든 데이터를 저장할 빈 리스트 생성
all_data = []

# 각 Excel 파일의 데이터를 JSON 배열에 추가
for excel_file in excel_files:
    # Excel 파일 읽기
    df = pd.read_excel(os.path.join(excel_files_directory, excel_file))

    # 날짜 형식 변경 및 , 제거
    df['일자'] = pd.to_datetime(df['일자'], format='%Y/%m/%d')
    df['일자'] = df['일자'].dt.strftime('%Y-%m-%d')

    # 열 이름 변경
    df.rename(columns={
        '일자': 'date',
        '종가': 'close',
        '대비': 'compare',
        '등락률': 'fluctuation',
        '시가': 'open',
        '고가': 'high',
        '저가': 'low',
        '거래량': 'volume',
        '거래대금': 'tradingValue',
        '시가총액': 'marketCapitalization',
        '상장주식수': 'outstandingShares'
    }, inplace=True)

    # 데이터를 JSON 형식으로 변환
    all_data.extend(df.to_dict(orient='records'))

    # JSON 파일로 저장
    output_filename = 'mock-indicator-' + os.path.splitext(excel_file)[0] + '.json'
    output_path = os.path.join(output_directory, output_filename)
    with open(output_path, 'w') as f:
        json.dump(all_data, f, indent=4)

    all_data = []

print("모든 Excel 파일의 데이터가 JSON으로 변환되어 저장되었습니다.")