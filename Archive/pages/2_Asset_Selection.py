# -*- coding: utf-8 -*-
"""
Created on Tue May  9 17:16:49 2023

@author: Marios
"""

import streamlit as st

  


def run():
    st.title("Stock Selection")
    
    stock_tickers=list(st.session_state.dfwiki[1]['Symbol'])
    full_names=list(st.session_state.dfwiki[1]['Company'])
    tickers_plus_names=[i+" : "+j for i,j in zip(stock_tickers,full_names)]
    
    options=st.multiselect("Select the stocks you wish to include in your portfolio",tickers_plus_names)
    st.session_state.selected_stocks =[x.split()[0] for x in options]   
    
    st.subheader("Portfolio optimization methods")
    
    s=['Long Only','With Leverage','With Leverage and Risk Limit']
    
    st.session_state.selected_method=st.multiselect("Please select the constraints under which you wish to optimize",s)
    
    

if all(st.session_state.check[:2]):
    run()
    st.session_state.check[2]=True
else:
    st.markdown("""<style>.big-font {font-size:50px !important;}</style>""", unsafe_allow_html=True)

    st.markdown('<p class="big-font">Please execute the pages sequentially!</p>', unsafe_allow_html=True)   