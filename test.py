import akshare as ak

stock_financial_us_analysis_indicator_em_df = ak.stock_financial_us_analysis_indicator_em(symbol="AAPL", indicator="年报")
print(stock_financial_us_analysis_indicator_em_df['PARENT_HOLDER_NETPROFIT'])