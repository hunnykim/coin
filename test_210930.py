# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 14:07:04 2021
@author: mechpark
"""
print('Running..')
import time
time.sleep(30) # 컴퓨터 재부팅 시 인터넷 연결 대기
#%%
import os
os.chdir('/home/pi/PARKBIT/')
from parkendecrypt import simEnDecrypt

# Setting
try :
    f = open("parkbit.txt", 'r')
    lines = f.readlines()
    key = lines[0].strip()
    EnDecrypt = simEnDecrypt(key = key)
    
    access = EnDecrypt.decrypt(lines[1]).strip()
    secret = EnDecrypt.decrypt(lines[2]).strip()
    f.close()
except :
    print('Failed')
    check = input('Wanna Recreate?(Y/N)')
    if check == 'Y' :
        f = open("parkbit.txt", 'w')
        data = []
        data.append(str(simEnDecrypt().key)) # 새로운 암호키 생성
        data.append(input("엑세스 : "))
        data.append(input("시크릿 : "))
        EnDecrypt = simEnDecrypt(key = data[0])
        for i in range(3) :
            if i==0:
                f.write(data[i]+'\n')
            else :
                f.write(EnDecrypt.encrypt(data[i])+'\n')
        f.close()
     else :
        assert check !='Y'

#%%
import pyupbit
import datetime
import numpy as np
upbit = pyupbit.Upbit(access, secret)
# 보유 현금 조회
balance = upbit.get_balance(ticker="KRW")
print(balance)

# # 종목 조회
# print(pyupbit.get_tickers())
# # 최근 체결 가격 조회
# BTC_price = pyupbit.get_current_price("KRW-BTC")
# print(BTC_price)

# # 최근 정보 데이터프레임 
# search_days = 10
# df = pyupbit.get_ohlcv("KRW-BTC", count = search_days)
# print(df.tail())

# 목표가 기능 추가
def cal_target(ticker) :
    search_days = 10
    df = pyupbit.get_ohlcv("KRW-BTC", count = search_days)
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    target = today['open'] + yesterday_range * 0.5
    return target
target = cal_target("KRW-BTC")
print("목표가 :", target)

# #%% 수익률 계산(수수료 포함)
# def get_ror(k=0.5) :
#     df = pyupbit.get_ohlcv("KRW-BTC", count = 200)
#     df['range'] = (df['high'] - df['low']) * k
#     df['target'] = df['open'] + df['range'].shift(1)
#     fee = 0.05 * 0.01
#     df['ror'] = np.where(df['high'] > df['target'], # rate of returns
#                          df['close'] / df['target'] - fee,
#                          1)
#     ror = df['ror'].cumprod()[-2]
#     return ror
# # k값 최적 확인
# for k in np.arange(0.1,1.0, 0.1):
#     ror = get_ror(k)
#     print("%.1f %f" % (k, ror))
# 
# #%% MDD(낙폭) 계산
# df = pyupbit.get_ohlcv("KRW-BTC", count = 200)
# df['range'] = (df['high'] - df['low']) * k
# df['target'] = df['open'] + df['range'].shift(1)
# fee = 0.05 * 0.01
# df['ror'] = np.where(df['high'] > df['target'], # rate of returns
#                      df['close'] / df['target'] - fee,
#                      1)
# df['hpr'] = df['ror'].cumprod() # 기간 수익률
# df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
# print("MDD(%): ", df['dd'].max())
# # df.to_excel('dd.xlsx')
# 
# #%% 변동성 돌파 + 상승장 전략 백테스팅
# df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
# df['range'] = (df['high'] - df['low']) * 0.5
# df['target'] = df['open'] + df['range'].shift(1)
# df['bull'] = df['open'] > df['ma5']
# fee = 0.05 * 0.01
# df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
#                    df['close'] / df['target'] - fee,
#                    1)
# 
# df['hpr'] = df['ror'].cumprod()
# df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
# print("MDD: ", df['dd'].max())
# print("HPR: ", df['hpr'][-2])
# # df.to_excel("larry_ma.xlsx")

# #%% 기간수익률 높은 코인 찾기
# def get_hpr(ticker):
#     try:
#         df = pyupbit.get_ohlcv(ticker)
#         df = df['2018']
# 
#         df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
#         df['range'] = (df['high'] - df['low']) * 0.5
#         df['target'] = df['open'] + df['range'].shift(1)
#         df['bull'] = df['open'] > df['ma5']
# 
#         fee = 0.0032
#         df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
#                               df['close'] / df['target'] - fee,
#                               1)
# 
#         df['hpr'] = df['ror'].cumprod()
#         df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
#         return df['hpr'][-2]
#     except:
#         return 1
#  
#  
# tickers = pyupbit.get_tickers()
# 
# hprs = []
# for ticker in tickers:
#     hpr = get_hpr(ticker)
#     hprs.append((ticker, hpr))
# 
# sorted_hprs = sorted(hprs, key=lambda x:x[1], reverse=True)
# print(sorted_hprs[:5])

# #%% 이동평균
# def get_yesterday_ma5(ticker):
#     df = pyupbit.get_ohlcv(ticker)
#     close = df['close']
#     ma = close.rolling(5).mean()
#     return ma[-2]
# 
# now = datetime.datetime.now()
# mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
# ma5 = get_yesterday_ma5("KRW-BTC")
# target_price = cal_target("KRW-BTC")

# #%% 호가 확인
# orderbook = pyupbit.get_orderbook("KRW-BTC")
# 
# market = orderbook[0]['market']
# timestamp = orderbook[0]['timestamp']
# total_ask_size = orderbook[0]['total_ask_size']
# total_bid_size = orderbook[0]['total_bid_size']
# bids_asks = orderbook[0]['orderbook_units'] # orderbook에서 bids_asks를 추출
# 
# print(market, timestamp, total_ask_size, total_bid_size)
# 
# print("          sell      /         buy")
# for bid_ask in bids_asks:
#     print(bid_ask)
from logging.config import dictConfig
import logging

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})

logging.debug("Program Started, balance : " + str(balance))
# 재부팅 후 코인 매수 여부 확인
if upbit.get_balance("KRW-BTC") > 0 :
    hold = True
    op_mode = True
else :
    op_mode = False
    hold = False
    
# Display Current Price
while True :
    now = datetime.datetime.now()
    # 매도 시도
    if now.hour == 8 and now.minute == 49 and 50 <= now.second <= 59:
        if op_mode is True and hold is True :
            eth_balance = upbit.get_balance("KRW-BTC")
            upbit.sell_market_order("KRW-BTC", eth_balance)
            logging.debug("매도 : "+ str(eth_balance))
            hold = False
        op_mode = False
        time.sleep(10)
        
    # 09시 목표가 갱신
    if now.hour == 8 and now.minute == 50 and (20<=now.second <= 30) :
        target = cal_target("KRW-BTC")
        print("목표가 :", target)
        op_mode = True 
    # 현재가 확인
    cur_price = pyupbit.get_current_price("KRW-BTC")
    
    # 매초마다 조건을 확인한 후 매수 시도
    print(now,cur_price)
    if op_mode is True and cur_price >= target and hold is False :
        buy_price = 1000000
        # 매수
        balance = upbit.get_balance(ticker="KRW")
        upbit.buy_market_order('KRW-BTC', buy_price)
        logging.debug("매수 : "+ str(buy_price))
        hold = True 
        
    print(f"현재 시간: {now} 목표가: {target} 현재가: {cur_price} 보유상태: {hold} 동작상태: {op_mode}")
    time.sleep(1)

# #%%
# # [BTC order]
# # # print(upbit.buy_limit_order("KRW-BTC", 41840000, 1)) #입력 금액에 BTC 1개 매수
# # # print(upbit.sell_limit_order("KRW-BTC", 50000000, 1)) #입력 금액에 BTC 1개 매도
# print(upbit.buy_market_order("KRW-BTC", 0)) #BTC 10,000원어치 시장가 매수
# # # print(upbit.sell_market_order("KRW-BTC", 1))  #BTC 1개 시장가매도
# 
# # [XRP order]
# # # print(upbit.buy_limit_order("KRW-XRP", 500, 20)) #500원에 리플20개 매수
# # # print(upbit.sell_limit_order("KRW-XRP", 500, 20)) #500원에 리플20개 매도
# # print(upbit.buy_market_order("KRW-XRP", 10000)) #리플 10000원어치 시장가 매수
# # # print(upbit.sell_market_order("KRW-XRP", 30))  #리플 30개 시장가매도
# 
# #시장가 매수 매도는 매수할때는 원화, 매도할때는 매도수량 값을 넘깁니다.
# # ret = upbit.buy_limit_order("KRW-XRP", 100, 20)    # Buy
# # ret = upbit.sell_limit_order("KRW-XRP", 1000, 10)  # Sell
# # print(ret)
# 
# # [order cnacle]
# # uuid = ret['uuid'] # 주문번호 얻기
# # print(uuid)
# # ret = upbit.cancel_order(uuid) # 주문 취소
# # print(ret)
