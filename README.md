# 🤖 ZANAYE AI
### Gold Trading Assistant for XAUUSD

**Market:** XAUUSD (Gold)  
**Timeframe:** M15  
**Risk:** 0.5% per trade  
**Platform:** MetaTrader 5 + Python

---

## ✨ What It Does
- Analyses Gold market on M15
- Gives BUY and SELL signals
- Calculates Entry, Stop Loss, Take Profit
- Auto calculates lot size from 0.5% risk
- Trades automatically on MT5

## 🧠 Strategy
- **Trend:** EMA 50 vs EMA 200
- **Momentum:** RSI 14 + MACD Cross
- **Stop Loss:** ATR x 1.5
- **Take Profit:** 1:2 Risk Reward
- **Max Trades:** 3 per day, 1 trade at a time

## 📁 Files
- `zanaye_mt5_bot.py` - Main auto trading bot
- `requirements.txt` - Python libraries
- `strategy/backtest.py` - Backtest (coming soon)

## 🚀 How To Run
```bash
pip install -r requirements.txt
python zanaye_mt5_bot.py