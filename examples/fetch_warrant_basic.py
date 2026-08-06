"""
抓取台灣證券交易所上市權證基本資料
使用官方 OpenAPI（免金鑰）
"""

import requests
import pandas as pd
from datetime import datetime


def fetch_warrant_basic():
    """抓取上市權證基本資料彙總表"""
    url = "https://openapi.twse.com.tw/v1/opendata/t187ap37_L"
    
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if not data:
            print("沒有取得資料")
            return None
        
        df = pd.DataFrame(data)
        print(f"成功取得 {len(df)} 筆權證資料")
        print(f"更新時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n欄位：")
        print(df.columns.tolist())
        print("\n前 5 筆預覽：")
        print(df.head())
        
        return df
    
    except Exception as e:
        print(f"錯誤：{e}")
        return None


def fetch_daily_trading():
    """抓取權證每日成交資料"""
    url = "https://openapi.twse.com.tw/v1/opendata/t187ap42_L"
    
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        df = pd.DataFrame(data)
        print(f"\n每日成交資料共 {len(df)} 筆")
        return df
    
    except Exception as e:
        print(f"錯誤：{e}")
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("台灣權證基本資料抓取範例")
    print("=" * 50)
    
    df_basic = fetch_warrant_basic()
    
    if df_basic is not None:
        # 儲存成 CSV
        output_file = f"warrant_basic_{datetime.now().strftime('%Y%m%d')}.csv"
        df_basic.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"\n已儲存至：{output_file}")
    
    # 可選：抓取每日成交
    # df_trading = fetch_daily_trading()
