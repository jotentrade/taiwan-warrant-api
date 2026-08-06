"""
權證簡單篩選範例
可自行擴充成核爆條件（價外程度、槓桿、成交量、IV 等）
"""

import requests
import pandas as pd


def get_warrant_data():
    """取得權證基本資料"""
    url = "https://openapi.twse.com.tw/v1/opendata/t187ap37_L"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


def simple_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    簡單篩選範例（請依實際需求修改）
    
    常見可用欄位（依實際回傳為準）：
    - 權證代號
    - 權證簡稱
    - 標的
    - 權證類型（認購 / 認售）
    - 最新履約價格
    - 行使比例
    - 到期日
    """
    
    # 範例：只看認購權證
    if "權證類型" in df.columns:
        df = df[df["權證類型"].str.contains("認購", na=False)]
    
    # 範例：標的為台積電（2330）
    if "標的證券代號" in df.columns or "標的代號" in df.columns:
        col = "標的證券代號" if "標的證券代號" in df.columns else "標的代號"
        df = df[df[col] == "2330"]
    
    # 可自行加入更多條件：
    # - 剩餘天數
    # - 價內外程度
    # - 成交量門檻
    # - 價格區間
    
    return df.reset_index(drop=True)


if __name__ == "__main__":
    print("正在抓取權證資料...")
    df = get_warrant_data()
    print(f"原始資料：{len(df)} 筆")
    
    filtered = simple_filter(df)
    print(f"篩選後：{len(filtered)} 筆")
    
    if len(filtered) > 0:
        print("\n篩選結果預覽：")
        print(filtered.head(10))
        
        # 儲存
        filtered.to_csv("filtered_warrants.csv", index=False, encoding="utf-8-sig")
        print("\n已儲存至 filtered_warrants.csv")
    else:
        print("沒有符合條件的資料，請檢查欄位名稱或篩選條件。")
