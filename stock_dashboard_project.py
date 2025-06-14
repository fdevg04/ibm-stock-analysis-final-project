# ======================================================
# Peer Graded Assignment
# Fernando Gonzalez Ramon
# ======================================================

# ======================================================
# S1 – Import Libraries
# ======================================================

import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

pio.renderers.default = "browser"

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# ======================================================
# S2 – make_graph Function
# ======================================================

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    
    stock_data_specific = stock_data[stock_data["Date"] <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data["Date"] <= '2021-04-30']
    
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific["Date"], infer_datetime_format=True),
                             y=stock_data_specific["Close"].astype("float"), name="Share Price"), row=1, col=1)

    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific["Date"], infer_datetime_format=True),
                             y=revenue_data_specific["Revenue"].astype("float"), name="Revenue"), row=2, col=1)
    
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    
    fig.show()
    #from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))


# ======================================================
# S3 – Question 1
# ======================================================

import yfinance as yf
import json

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)  #importante
tesla_data.to_json("tesla_data.json")
tesla_data = pd.read_json("tesla_data.json")
tesla_data.reset_index(inplace=True)

#print("DataFrame Tesla Test:")
#print(tesla_data.head())

# ======================================================
# S4 – Question 2
# ======================================================

with open("html_data.html", "r", encoding="utf-8") as file:
    html_data = file.read()

soup = BeautifulSoup(html_data, "html.parser")
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
rows = soup.find_all("tbody")[1].find_all("tr")

for row in rows:
    cols = row.find_all("td")
    if len(cols) == 2:
        date = cols[0].text.strip()
        revenue = cols[1].text.strip()
        tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)

tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(",", "")
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace("$", "")

tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]

#print("DataFrame Tesla Test Revenue:")
#print(tesla_revenue.tail())


# ======================================================
# S5 – Question 3
# ======================================================

import yfinance as yf
import json

gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)  #importante
gme_data.to_json("gme_data.json")
gme_data = pd.read_json("gme_data.json")
gme_data.reset_index(inplace=True)

#print("DataFrame GameStop Test:")
#print(gme_data.head())

# ======================================================
# S6 – Question 4
# ======================================================

with open("html_data_2.html", "r", encoding="utf-8") as file:
    html_data_2 = file.read()

soup = BeautifulSoup(html_data_2, "html.parser")
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
rows = soup.find_all("tbody")[1].find_all("tr")

for row in rows:
    cols = row.find_all("td")
    if len(cols) == 2:
        date = cols[0].text.strip()
        revenue = cols[1].text.strip()
        gme_revenue = pd.concat([gme_revenue, pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)

gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(",", "")
gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace("$", "")

gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue["Revenue"] != ""]

#print("DataFrame GameStop Test Revenue:")
#print(gme_revenue.tail())


# ======================================================
# S7 – Question 5
# ======================================================

#make_graph(tesla_data, tesla_revenue, "Tesla")

# ======================================================
# S8 – Question 6
# ======================================================

#make_graph(gme_data, gme_revenue, "GameStop")
