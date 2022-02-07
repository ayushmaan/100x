from json.tool import main
from math import ceil, floor
from operator import index
from select import select
import streamlit as st
import json
import random
from functools import reduce

import talib
import pandas as pd
import scipy.signal as sp
st.set_page_config(layout="wide",page_title='100X.Space', page_icon=':money',initial_sidebar_state='expanded')

st.title("100X.Space")

def Intersection(lst1, lst2):
    return set(lst1).intersection(lst2)

index_stock = json.load(open("index_stock.json"))
unique_sym_lst = json.load(open("unique_sym_lst.json"))
daily_update = json.load(open("daily_udpate.json"))


index_lst_all = list(index_stock.keys())
option = "NIFTY 50"

with st.form(key='my-filter'):
    with st.sidebar:

        rs_flag= st.checkbox("RS Positive")

        sup_use_flag = st.checkbox("SuperTrend")
        sup_flag = st.radio(
        "SuperTrend",
            ('Above', 'Below'))

        sma_flag = st.checkbox("Above 200 SMA")
        ema_flag = st.checkbox("Above 200 EMA")


        dema_use_flag = st.checkbox("DEMA 200")
        dema_flag = st.radio(
        "DEMA 200",
            ('Above', 'Below'))


 
        rsi_use_flag = st.checkbox("RSI 50")
        rsi_flag = st.radio(
        "RSI 50",
            ('Above', 'Below'))

        st.form_submit_button("Filter")



option = st.selectbox(
    'Select Index:',
    (index_lst_all))



index_selected = index_stock[option]
filtered_stock = index_selected

main_list_stk = []
main_list_stk.append(filtered_stock)


if dema_flag=="Above" and dema_use_flag:
    main_list_stk.append(daily_update["dema_above_stk_lst"])
if dema_flag=="Below" and dema_use_flag:
    main_list_stk.append(daily_update["dema_below_stk_lst"])

if rsi_flag=="Above" and rsi_use_flag:
    main_list_stk.append(daily_update["rsi_above_stk_lst"])
if rsi_flag=="Below" and rsi_use_flag:
    main_list_stk.append(daily_update["rsi_below_stk_lst"])

if sup_flag=="Above" and sup_use_flag:
    main_list_stk.append(daily_update["sup_above_stk_lst"])
if sup_flag=="Below" and sup_use_flag:
    main_list_stk.append(daily_update["sup_below_stk_lst"])
# if rsi_flag:
#     filtered_stock  = list(Intersection(filtered_stock,rsi_list))

filtered_stock =  list(reduce(set.intersection, [set(item) for item in main_list_stk ]))



col = 5
nrow = ceil(len(filtered_stock)/col )
print(nrow)
cntn =0

for i in range(nrow):
        if (i+1)*col>len(filtered_stock):
            col = len(filtered_stock)%(col)
        # print("col",col)

        
        cols = st.columns(col)
        for j in range(col):
            symbx = filtered_stock[cntn]
            
            # cols[j].metric(filtered_stock[cntn], str(daily_update_all[filtered_stock[cntn]][0]["LTP"]), delta = str(daily_update_all[filtered_stock[cntn]][2]["PCT"])+"%")
            cols[j].metric(symbx, str(daily_update["stock_update"][symbx]["LTP"]), delta = str(daily_update["stock_update"][symbx]["PCT"])+"%")
            cntn+=1
