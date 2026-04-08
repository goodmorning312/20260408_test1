# 20260408_test1

!pip install yfinance requests -q

import requests

BOT_TOKEN = "8708571879:AAFZtBa1yJXCbXbzyqTq7y3uyxZIRe8TIfE"
CHAT_ID   = "7835854615"

# 傳送測試訊息
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
res = requests.post(url, json={
    "chat_id":    CHAT_ID,
    "text":       "✅ 連線測試成功！\n🤖 @TakeALookAtTheStocks_bot 準備就緒，即將開始定時傳送股價！",
    "parse_mode": "HTML"
})
print(res.json())
# 看到 "ok": true 代表設定正確 ✅


import yfinance as yf
import requests
import time
import random
from datetime import datetime

BOT_TOKEN = "8708571879:AAFZtBa1yJXCbXbzyqTq7y3uyxZIRe8TIfE"
BOT_NAME  = "@TakeALookAtTheStocks_bot"
CHAT_ID   = "7835854615"
INTERVAL  = 5 * 60

STOCK_POOL = [
    "2330.TW", # 台積電
    "0050.TW", # 元大台灣50
]

def get_stock_price(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        info  = stock.fast_info
        current_price  = info.get("lastPrice") or info.get("previousClose", 0)
        day_high       = info.get("dayHigh", 0)
        day_low        = info.get("dayLow", 0)
        previous_close = info.get("previousClose", 0)
        change_pct = (
            (current_price - previous_close) / previous_close * 100
            if previous_close else 0.0
        )
        try:
            company_name = stock.info.get("longName", ticker_symbol)
        except Exception:
            company_name = ticker_symbol
        return {
            "symbol": ticker_symbol, "name": company_name,
            "price": current_price, "change_pct": change_pct,
            "day_high": day_high, "day_low": day_low,
            "previous_close": previous_close, "success": True
        }
    except Exception as e:
        return {"symbol": ticker_symbol, "success": False, "error": str(e)}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        res = requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=10)
        result = res.json()
        if result.get("ok"):
            print(f"✅ 傳送成功 [{datetime.now().strftime('%H:%M:%S')}]")
        else:
            print(f"❌ 傳送失敗：{result.get('description')}")
    except Exception as e:
        print(f"❌ 網路錯誤：{str(e)}")

def run_stock_report():
    ticker = random.choice(STOCK_POOL)
    now    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n⏰ [{now}] 正在查詢：{ticker} ...")
    data = get_stock_price(ticker)
    if data["success"]:
        emoji = "📈" if data["change_pct"] >= 0 else "📉"
        message = (
            f"🤖 <b>{BOT_NAME} 股價定時回報</b>\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"📌 股票代碼：<b>{data['symbol']}</b>\n"
            f"🏢 公司名稱：{data['name']}\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"💰 現　　價：<b>{data['price']:.2f}</b>\n"
            f"{emoji} 漲　　跌：{data['change_pct']:+.2f}%\n"
            f"⬆️ 今日最高：{data['day_high']:.2f}\n"
            f"⬇️ 今日最低：{data['day_low']:.2f}\n"
            f"📊 昨日收盤：{data['previous_close']:.2f}\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"🕐 查詢時間：{now}"
        )
    else:
        message = (
            f"⚠️ <b>股價查詢失敗</b>\n"
            f"股票代碼：{data['symbol']}\n"
            f"錯誤訊息：{data['error']}\n"
            f"查詢時間：{now}"
        )
    send_telegram_message(message)

print("=" * 50)
print(f"🚀 {BOT_NAME} 啟動！")
print(f"👤 Chat ID：{CHAT_ID}")
print(f"⏱️  每 {INTERVAL // 60} 分鐘自動傳送一次")
print(f"🎯 監聽股票：{STOCK_POOL}")
print("⛔ 停止請按 Colab ■ 按鈕")
print("=" * 50)

run_stock_report()

while True:
    time.sleep(INTERVAL)
    run_stock_report()
