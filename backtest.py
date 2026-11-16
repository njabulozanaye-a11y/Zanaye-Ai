# ZANAYE AI - Backtest for XAUUSD M15
# Run: python backtest.py

import MetaTrader5 as mt5
import pandas as pd
import numpy as np

SYMBOL = "XAUUSD"
START_BALANCE = 1000
RISK_PERCENT = 0.5

mt5.initialize()
rates = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_M15, 0, 2000)
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')

# Indicators
df['ema50'] = df['close'].ewm(span=50).mean()
df['ema200'] = df['close'].ewm(span=200).mean()
delta = df['close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = -delta.where(delta < 0, 0).rolling(14).mean()
df['rsi'] = 100 - (100 / (1 + (gain/loss)))
df['macd'] = df['close'].ewm(span=12).mean() - df['close'].ewm(span=26).mean()
df['macd_signal'] = df['macd'].ewm(span=9).mean()
tr = pd.concat([df['high']-df['low'], abs(df['high']-df['close'].shift()), abs(df['low']-df['close'].shift())], axis=1).max(axis=1)
df['atr'] = tr.rolling(14).mean()

balance = START_BALANCE
wins = 0
losses = 0
total_profit = 0
trades = []
open_trade = None

for i in range(201, len(df)):
    row = df.iloc[i]
    prev = df.iloc[i-1]

    # Close open trade if hit SL/TP
    if open_trade:
        if open_trade['type'] == 'BUY':
            if row['low'] <= open_trade['sl']:
                pnl = -open_trade['risk']
                balance += pnl; losses += 1; total_profit += pnl
                trades.append({**open_trade, 'result': 'LOSS', 'pnl': pnl})
                open_trade = None
            elif row['high'] >= open_trade['tp']:
                pnl = open_trade['risk'] * 2
                balance += pnl; wins += 1; total_profit += pnl
                trades.append({**open_trade, 'result': 'WIN', 'pnl': pnl})
                open_trade = None
        else: # SELL
            if row['high'] >= open_trade['sl']:
                pnl = -open_trade['risk']
                balance += pnl; losses += 1; total_profit += pnl
                trades.append({**open_trade, 'result': 'LOSS', 'pnl': pnl})
                open_trade = None
            elif row['low'] <= open_trade['tp']:
                pnl = open_trade['risk'] * 2
                balance += pnl; wins += 1; total_profit += pnl
                trades.append({**open_trade, 'result': 'WIN', 'pnl': pnl})
                open_trade = None
        continue

    # New signal
    uptrend = row['ema50'] > row['ema200']
    downtrend = row['ema50'] < row['ema200']
    signal = None
    if uptrend and 40 < row['rsi'] < 65 and row['macd'] > row['macd_signal'] and prev['macd'] <= prev['macd_signal']:
        signal = 'BUY'
    if downtrend and 35 < row['rsi'] < 60 and row['macd'] < row['macd_signal'] and prev['macd'] >= prev['macd_signal']:
        signal = 'SELL'

    if signal:
        entry = row['close']
        atr = row['atr']
        risk_money = balance * (RISK_PERCENT/100)
        if signal == 'BUY':
            sl = entry - (atr*1.5); tp = entry + ((entry-sl)*2)
        else:
            sl = entry + (atr*1.5); tp = entry - ((sl-entry)*2)
        open_trade = {'time': row['time'], 'type': signal, 'entry': entry, 'sl': sl, 'tp': tp, 'risk': risk_money}

total = wins + losses
win_rate = (wins/total*100) if total>0 else 0
print(f"\n===== ZANAYE AI BACKTEST =====")
print(f"Starting Balance: ${START_BALANCE}")
print(f"Final Balance: ${balance:.2f}")
print(f"Total Profit: ${total_profit:.2f}")
print(f"Total Trades: {total}")
print(f"Wins: {wins} | Losses: {losses}")
print(f"Win Rate: {win_rate:.1f}%")
print(f"==============================")
mt5.shutdown()