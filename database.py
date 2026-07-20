import pandas as pd
import numpy as np
from models import REQUIRED_COLUMNS

def load_and_validate(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file, engine='openpyxl')
    
    # 1. 컬럼 이름 매핑 (있는 것만 매핑)
    mapping = {
        '광고 소재 이름': '광고 이름',
        '광고 그룹 이름': '광고 세트 이름',
        '총비용': '지출 금액 (KRW)',
        '노출수': '노출',
        '구매완료 수': '구매',
        '구매완료 전환매출액': '구매 전환값',
        '클릭률(%)': 'CTR(전체)',
        '평균 CPC': 'CPC(링크 클릭당 비용)',
        '구매완료 광고수익률(%)': '구매 ROAS(광고 지출 대비 수익률)'
    }
    df = df.rename(columns=mapping)
    
    # 2. 필수 데이터가 없으면 자동으로 계산
    # '링크 클릭당 구매율' 계산 (구매 / 클릭수) -> 클릭수 데이터 없으면 0 처리
    if '링크 클릭당 구매율' not in df.columns:
        df['링크 클릭당 구매율'] = np.where(df['구매'] > 0, (df['구매'] / df['구매'].sum()) * 100, 0) # 예시 로직
        
    # '구매당 비용' 계산 (지출 / 구매)
    if '구매당 비용' not in df.columns:
        df['구매당 비용'] = np.where(df['구매'] > 0, df['지출 금액 (KRW)'] / df['구매'], 0)
        
    # '구매 ROAS' 계산 (매출 / 지출)
    if '구매 ROAS(광고 지출 대비 수익률)' not in df.columns:
        df['구매 ROAS(광고 지출 대비 수익률)'] = np.where(df['지출 금액 (KRW)'] > 0, df['구매 전환값'] / df['지출 금액 (KRW)'], 0)

    return df