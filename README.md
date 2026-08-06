# 台灣權證 API 資料來源整理

> 整理台灣認購／認售權證（Warrant）可用的 API 與資料來源，方便程式交易、篩選與自動化使用。

**最後更新**：2026-08-06

---

## 目錄

- [1. 臺灣證券交易所官方 OpenAPI（免費）](#1-台灣證券交易所官方-openapi免費)
- [2. FinMind（開源台股資料平台）](#2-finmind開源台股資料平台)
- [3. 永豐金 Shioaji（交易 + 行情）](#3-永豐金-shioaji交易--行情)
- [4. 其他券商 API](#4-其他券商-api)
- [5. 即時報價補充](#5-即時報價補充)
- [使用建議](#使用建議)
- [範例程式](#範例程式)
- [注意事項](#注意事項)

---

## 1. 臺灣證券交易所官方 OpenAPI（免費）

**最推薦的免費起點。**

- **Base URL**：`https://openapi.twse.com.tw/v1/`
- **Swagger 文件**：https://openapi.twse.com.tw/v1/swagger.json
- **特色**：免註冊、免金鑰、回傳 JSON 或 CSV

### 權證相關端點

| 端點 | 說明 | 主要欄位 |
|------|------|----------|
| `/opendata/t187ap37_L` | 上市權證基本資料彙總表 | 權證代號、簡稱、類型、標的、履約價、行使比例、上下限價、到期日等 |
| `/opendata/t187ap36_L` | 上市認購(售)權證年度發行量概況統計表 | 發行人、發行量統計 |
| `/opendata/t187ap42_L` | 上市認購(售)權證每日成交資料檔 | 成交金額、成交張數 |
| `/opendata/t187ap43_L` | 上市認購(售)權證交易人數檔 | 交易人數 |

**直接呼叫範例**：
```bash
curl "https://openapi.twse.com.tw/v1/opendata/t187ap37_L"
```

政府資料開放平臺也有對應的 CSV 下載連結。

---

## 2. FinMind（開源台股資料平台）

- **Base URL**：`https://api.finmindtrade.com/api/v4`
- **文件**：https://finmind.github.io/
- **Python SDK**：`pip install FinMind`

### 權證相關資料集

| Dataset | 說明 | 層級 |
|---------|------|------|
| `TaiwanStockInfoWithWarrant` | 台股總覽（含權證） | Free |
| `TaiwanStockInfoWithWarrantSummary` | 權證標的對照表（母股 ↔ 權證） | Sponsor |
| `TaiwanStockWarrantTradingDailyReport` | 權證當日券商分點表 | Sponsor |

**使用方式**：
1. 到 https://finmindtrade.com 註冊取得 token
2. 請求時帶 `Authorization: Bearer {token}`

免費額度約 300–600 次／小時（有 token 較高）。

---

## 3. 永豐金 Shioaji（交易 + 行情）

完整支援權證合約查詢、即時行情訂閱與下單。

- **官方文件**：https://sinotrade.github.io/
- **Python 套件**：`pip install shioaji`

### 權證查詢範例

```python
import shioaji as sj

api = sj.Shioaji()
api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

# 取得某標的發行的所有權證
c = api.Contracts.Stocks["2330"]  # 台積電
warrants = api.Contracts.warrants(c)

# 可進一步篩選認購/認售、履約價區間、到期日等
```

需開立永豐金證券帳戶並申請 API Key + 憑證。

---

## 4. 其他券商 API

| 券商 | 說明 | 備註 |
|------|------|------|
| 凱基證券 | 證券數位贏家 API（QuoteCom + TradeCom） | 支援 C# / Python，需申請 |
| 群益、元大、中信等 | 多有自家下單／報價 API | 需開戶申請，權證支援程度不一 |

---

## 5. 即時報價補充

- 證交所 MIS 即時報價：`https://mis.twse.com.tw/stock/api/getStockInfo.jsp`
  - 支援多檔同時查詢（用 `|` 分隔）
  - 約 5 秒更新一次
  - 範例：`ex_ch=tse_2330.tw|tse_030001.tw`

權證專用即時報價仍以券商 API 較完整。

---

## 使用建議

1. **免費起步**：先用 TWSE OpenAPI 抓基本資料 + 日成交。
2. **進階篩選**：搭配 FinMind 做標的對照與歷史資料。
3. **即時 + 下單**：開戶後使用 Shioaji 或凱基 API。
4. **核爆條件**（價外程度、槓桿、IV、成交量等）：官方 API 多只提供基本欄位，進階指標需自行計算或從券商權證網頁取得後再串接。

權證檔數極多（數千～上萬檔），查詢時務必用標的、到期日、認購／認售等條件過濾。

---

## 範例程式

請見 [`examples/`](./examples/) 資料夾：

- `fetch_warrant_basic.py`：抓取上市權證基本資料
- `filter_example.py`：簡單篩選範例（可自行擴充核爆條件）

---

## 注意事項

- 資料僅供參考，不構成任何投資建議。
- 請遵守各 API 的使用條款與流量限制。
- 下單相關 API 需簽署風險預告書，並符合主管機關規範。
- 本整理持續更新中，歡迎 PR 補充。

---

## 相關連結

- [TWSE OpenAPI Swagger](https://openapi.twse.com.tw/v1/swagger.json)
- [FinMind 文件](https://finmind.github.io/)
- [Shioaji 文件](https://sinotrade.github.io/)
- [政府資料開放平臺 - 權證](https://data.gov.tw/dataset/32444)

---

**維護者**：炫龍開運命理館  
**授權**：MIT（僅供學習與研究使用）
