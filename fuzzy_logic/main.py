from fuzzy_logic.stock_market_fuzzy_logic import StockMarketFuzzyLogic
"""
FUZZY LOGIC
"""

beta = 1.28  # x1
ask = 131.78
bid = 131.75
mat_50 = 127.64
mat_200 = 107.17
rsi = 50.64  # x4

a = StockMarketFuzzyLogic(ma_s=mat_50, ma_l=mat_200, rsi=rsi, beta_stock=beta, bid_price=bid, ask_price=ask)
print(a.block3())