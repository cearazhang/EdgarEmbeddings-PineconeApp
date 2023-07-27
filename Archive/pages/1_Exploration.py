# -*- coding: utf-8 -*-
"""
Created on Tue May  9 17:15:47 2023

@author: Marios
"""

import streamlit as st

import datetime
import wikipedia as wp
import pandas as pd
import yfinance as yf
from utils import *
import plotly.express as px
import plotly.graph_objects as go




def run():
    
    st.title("Stock Data Exploration")
    
    st.markdown("From the sidebar on the left side of the page, select the following:")
    st.markdown("- Start Date")
    st.markdown("- End Date")
    st.markdown("- Ticker of the stock or index you want to display")
    
    st.subheader("Historical data for the chosen time frame")
    st.session_state.start_date=st.sidebar.date_input("Enter start date",value=datetime.date(2020,1,1))
    st.session_state.end_date=st.sidebar.date_input("Enter end date",value=datetime.date.today()-datetime.timedelta(days=1))
    
    html = wp.page("Dow_Jones_Industrial_Average").html().encode("UTF-8")
    st.session_state.dfwiki=pd.read_html(html)
    tickers=list(st.session_state.dfwiki[1]['Symbol'])+["^DJI"]
    full_names=list(st.session_state.dfwiki[1]['Company'])+["Dow Jones Industrial Average"]
    Index_Plus_Tickers=[i+" : "+j for i,j in zip(tickers,full_names)]
    full_name_option=st.sidebar.selectbox("View data for ticker:",Index_Plus_Tickers)
    option=full_name_option.split()[0]
    
    
    display_data=yf.download(option,st.session_state.start_date,st.session_state.end_date)
    st.dataframe(display_data,width=700,height=400)
    
    area_chart = px.area(display_data['Adj Close'], title = '{} Adj Close price from {} to {}'.format(option,st.session_state.start_date,st.session_state.end_date))     

    area_chart.update_xaxes(title_text = 'Date')
    area_chart.update_yaxes(title_text = '{} Adj Close Price'.format(option), tickprefix = '$')
    area_chart.update_layout(showlegend = False)
    
    st.plotly_chart(area_chart)

if st.session_state.check[0]:
    run()
    st.session_state.check[1]=True
else:
    st.markdown("""<style>.big-font {font-size:50px !important;}</style>""", unsafe_allow_html=True)

    st.markdown('<p class="big-font">Please execute the pages sequentially!</p>', unsafe_allow_html=True)      