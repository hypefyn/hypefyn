import yfinance as yf
import pandas as pd


tsla_data1 = yf.download("TSLA", start="2020-03-24", end="2020-03-31", interval = "1m")
tsla_data2 = yf.download("TSLA", start="2020-03-31", end="2020-04-07", interval = "1m")
tsla_data3 = yf.download("TSLA", start="2020-04-07", end="2020-04-14", interval = "1m")
tsla_data4 = yf.download("TSLA", start="2020-04-14", end="2020-04-21", interval = "1m")

tsla_data1 = tsla_data1.append(tsla_data2)
tsla_data1 = tsla_data1.append(tsla_data3)
tsla_data1 = tsla_data1.append(tsla_data4)
tsla_data1 = tsla_data1.iloc[:,[0]]
tsla_data1 = tsla_data1.rename(columns = {"Open": "TSLA_price"})

ZM_data1 = yf.download("ZM", start="2020-03-24", end="2020-03-31", interval = "1m")
ZM_data2 = yf.download("ZM", start="2020-03-31", end="2020-04-07", interval = "1m")
ZM_data3 = yf.download("ZM", start="2020-04-07", end="2020-04-14", interval = "1m")
ZM_data4 = yf.download("ZM", start="2020-04-14", end="2020-04-21", interval = "1m")

ZM_data1 = ZM_data1.append(ZM_data2)
ZM_data1 = ZM_data1.append(ZM_data3)
ZM_data1 = ZM_data1.append(ZM_data4)
ZM_data1 = ZM_data1.iloc[:,[0]]
ZM_data1 = ZM_data1.rename(columns = {"Open": "ZM_price"})

AMZN_data1 = yf.download("AMZN", start="2020-03-24", end="2020-03-31", interval = "1m")
AMZN_data2 = yf.download("AMZN", start="2020-03-31", end="2020-04-07", interval = "1m")
AMZN_data3 = yf.download("AMZN", start="2020-04-07", end="2020-04-14", interval = "1m")
AMZN_data4 = yf.download("AMZN", start="2020-04-14", end="2020-04-21", interval = "1m")

AMZN_data1 = AMZN_data1.append(AMZN_data2)
AMZN_data1 = AMZN_data1.append(AMZN_data3)
AMZN_data1 = AMZN_data1.append(AMZN_data4)
AMZN_data1 = AMZN_data1.iloc[:,[0]]
AMZN_data1 = AMZN_data1.rename(columns = {"Open": "AMZN_price"})

DAL_data1 = yf.download("DAL", start="2020-03-24", end="2020-03-31", interval = "1m")
DAL_data2 = yf.download("DAL", start="2020-03-31", end="2020-04-07", interval = "1m")
DAL_data3 = yf.download("DAL", start="2020-04-07", end="2020-04-14", interval = "1m")
DAL_data4 = yf.download("DAL", start="2020-04-14", end="2020-04-21", interval = "1m")

DAL_data1 = DAL_data1.append(DAL_data2)
DAL_data1 = DAL_data1.append(DAL_data3)
DAL_data1 = DAL_data1.append(DAL_data4)
DAL_data1 = DAL_data1.iloc[:,[0]]
DAL_data1 = DAL_data1.rename(columns = {"Open": "DAL_price"})

GOOGL_data1 = yf.download("GOOGL", start="2020-03-24", end="2020-03-31", interval = "1m")
GOOGL_data2 = yf.download("GOOGL", start="2020-03-31", end="2020-04-07", interval = "1m")
GOOGL_data3 = yf.download("GOOGL", start="2020-04-07", end="2020-04-14", interval = "1m")
GOOGL_data4 = yf.download("GOOGL", start="2020-04-14", end="2020-04-21", interval = "1m")

GOOGL_data1 = GOOGL_data1.append(GOOGL_data2)
GOOGL_data1 = GOOGL_data1.append(GOOGL_data3)
GOOGL_data1 = GOOGL_data1.append(GOOGL_data4)
GOOGL_data1 = GOOGL_data1.iloc[:,[0]]
GOOGL_data1 = GOOGL_data1.rename(columns = {"Open": "GOOGL_price"})

NFLX_data1 = yf.download("NFLX", start="2020-03-24", end="2020-03-31", interval = "1m")
NFLX_data2 = yf.download("NFLX", start="2020-03-31", end="2020-04-07", interval = "1m")
NFLX_data3 = yf.download("NFLX", start="2020-04-07", end="2020-04-14", interval = "1m")
NFLX_data4 = yf.download("NFLX", start="2020-04-14", end="2020-04-21", interval = "1m")

NFLX_data1 = NFLX_data1.append(NFLX_data2)
NFLX_data1 = NFLX_data1.append(NFLX_data3)
NFLX_data1 = NFLX_data1.append(NFLX_data4)
NFLX_data1 = NFLX_data1.iloc[:,[0]]
NFLX_data1 = NFLX_data1.rename(columns = {"Open": "NFLX_price"})

NVS_data1 = yf.download("NVS", start="2020-03-24", end="2020-03-31", interval = "1m")
NVS_data2 = yf.download("NVS", start="2020-03-31", end="2020-04-07", interval = "1m")
NVS_data3 = yf.download("NVS", start="2020-04-07", end="2020-04-14", interval = "1m")
NVS_data4 = yf.download("NVS", start="2020-04-14", end="2020-04-21", interval = "1m")

NVS_data1 = NVS_data1.append(NVS_data2)
NVS_data1 = NVS_data1.append(NVS_data3)
NVS_data1 = NVS_data1.append(NVS_data4)
NVS_data1 = NVS_data1.iloc[:,[0]]
NVS_data1 = NVS_data1.rename(columns = {"Open": "NVS_price"})

PFE_data1 = yf.download("PFE", start="2020-03-24", end="2020-03-31", interval = "1m")
PFE_data2 = yf.download("PFE", start="2020-03-31", end="2020-04-07", interval = "1m")
PFE_data3 = yf.download("PFE", start="2020-04-07", end="2020-04-14", interval = "1m")
PFE_data4 = yf.download("PFE", start="2020-04-14", end="2020-04-21", interval = "1m")

PFE_data1 = PFE_data1.append(PFE_data2)
PFE_data1 = PFE_data1.append(PFE_data3)
PFE_data1 = PFE_data1.append(PFE_data4)
PFE_data1 = PFE_data1.iloc[:,[0]]
PFE_data1 = PFE_data1.rename(columns = {"Open": "PFE_price"})

TRIP_data1 = yf.download("TRIP", start="2020-03-24", end="2020-03-31", interval = "1m")
TRIP_data2 = yf.download("TRIP", start="2020-03-31", end="2020-04-07", interval = "1m")
TRIP_data3 = yf.download("TRIP", start="2020-04-07", end="2020-04-14", interval = "1m")
TRIP_data4 = yf.download("TRIP", start="2020-04-14", end="2020-04-21", interval = "1m")

TRIP_data1 = TRIP_data1.append(TRIP_data2)
TRIP_data1 = TRIP_data1.append(TRIP_data3)
TRIP_data1 = TRIP_data1.append(TRIP_data4)
TRIP_data1 = TRIP_data1.iloc[:,[0]]
TRIP_data1 = TRIP_data1.rename(columns = {"Open": "TRIP_price"})

data = pd.concat([tsla_data1, ZM_data1, AMZN_data1, DAL_data1, GOOGL_data1, NFLX_data1, NVS_data1, PFE_data1, TRIP_data1], axis = 1, join = "inner")
data.to_csv("data/finance_data.csv", index = True)
