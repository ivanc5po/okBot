import json

import okx.Account_api as Account
import okx.Funding_api as Funding
import okx.Market_api as Market
import okx.Public_api as Public
import okx.Trade_api as Trade
import okx.status_api as Status
import okx.subAccount_api as SubAccount
import okx.TradingData_api as TradingData
import okx.Broker_api as Broker
import okx.Convert_api as Convert
import time
import os

start_time = time.time()

os.system("clear")

flag = '0'
api_key = "XXXX"
secret_key = "XXXX"
passphrase = "XXXX"

tradingDataAPI = TradingData.TradingDataAPI(api_key, secret_key, passphrase, False, flag)
accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
convertAPI = Convert.ConvertAPI(api_key, secret_key, passphrase, False, flag)
marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, True, flag)
publicAPI = Public.PublicAPI(api_key, secret_key, passphrase, False, flag)
tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)

m = 10

import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
wd = webdriver.Chrome(options=chrome_options)
wd.get('https://tw.tradingview.com/chart/xEDy2dON/')

is_buy_sell = "buy"

time.sleep(5)
wd.find_element(by=By.XPATH, value='//*[@id="footer-chart-panel"]/div[1]/div[1]/div[2]/div').click()
time.sleep(1)
wd.find_element(by=By.XPATH, value='//*[@id="bottom-area"]/div[4]/div/div[1]/div[3]/div/div/div/div/div/button[3]').click()
total = float(str(fundingAPI.get_asset_valuation(ccy = 'USDT')).split(", ")[4].split("'")[3])-218263.75*int(flag)
time.sleep(1)

text = ""

st = 0

while True:
    try:
        coin = str(wd.title).split()[0].replace("USDT", "")+"-USDT-SWAP"
        price = float(str(wd.title).split()[1])

        if is_buy_sell == "buy" and wd.find_element(by=By.XPATH, value='//*[@id="bottom-area"]/div[4]/div/div[2]/div/div/div/div/table/tbody[1]/tr[2]/td[2]').text == "SELL":
            ### 賣出
            if st != 0:
                r1 = tradeAPI.close_positions(coin, 'cross', posSide="long")
                accountAPI.set_leverage(instId=coin, lever=str(m), mgnMode='cross')
                result = tradeAPI.place_order(instId=coin, tdMode='cross', side='sell', ordType='market', sz=str(int(total+0.5)*2), posSide="short")
                if "'code': '0'" in str(result):
                    text += "\n做空 "+str(price)
                    total = float(str(fundingAPI.get_asset_valuation(ccy = 'USDT')).split(", ")[4].split("'")[3])-218263.75*int(flag)
                    time.sleep(1)
                is_buy_sell = "sell"
            else:
                is_buy_sell = "sell"
                st = 1

        elif is_buy_sell == "sell" and wd.find_element(by=By.XPATH, value='//*[@id="bottom-area"]/div[4]/div/div[2]/div/div/div/div/table/tbody[1]/tr[2]/td[2]').text == "BUY":
            ### 買入
            if st != 0:
                r1 = tradeAPI.close_positions(coin, 'cross', posSide="short")
                accountAPI.set_leverage(instId=coin, lever=str(m), mgnMode='cross')
                result = tradeAPI.place_order(instId=coin, tdMode='cross', side='buy', ordType='market', sz=str(int(total+0.5)*2), posSide="long")
                if "'code': '0'" in str(result):
                    text += "\n做多 "+str(price)
                    total = float(str(fundingAPI.get_asset_valuation(ccy = 'USDT')).split(", ")[4].split("'")[3])-218263.75*int(flag)
                    time.sleep(1)

                is_buy_sell = "buy"
            else:
                is_buy_sell = "buy"
                st = 1
        elif wd.find_element(by=By.XPATH, value='//*[@id="bottom-area"]/div[4]/div/div[2]/div/div/div/div/table/tbody[1]/tr[1]/td[3]').text == "CLOSE":
            tradeAPI.close_positions(coin, 'cross', posSide="long")
            tradeAPI.close_positions(coin, 'cross', posSide="short")
            time.sleep(1)

        os.system("clear")
        print(coin+"\n")
        print("price :", price)
        print("total :", total, "\n")
        print("-------------------------")
        print(text)
        print("-------------------------")

    except:
        time.sleep(0.5)

    time.sleep(0.5)


