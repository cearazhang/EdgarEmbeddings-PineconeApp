# -*- coding: utf-8 -*-
"""
Created on Tue May  9 17:19:12 2023

@author: Marios
"""

import streamlit as st
import pandas as pd
import datetime
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
import scipy.stats as spstats

from utils import * 

#############################################################################################################
######################################  S C R I P T #########################################################
#############################################################################################################

def run():
    
    st.header("VaR Analytics")
    
    #start formatting sidebar
    st.sidebar.title("Parameters")
    
    Confidence=st.sidebar.slider('VaR Confidence Level',value=0.05,min_value=0.01,max_value=0.4)
    Investment=st.sidebar.slider('Investment amount',value=5e4,min_value=1e4,max_value=1e5)
    
    
    var1=parametric_var(Confidence, st.session_state.z2, st.session_state.z3 ,Investment)
    
    st.subheader('1D to 15D parametric VaR for selected confidence level.')
    
    fig5=plt.figure("figure 4, parametric var value for 1 up to 15 days")
    plt.plot(np.arange(1,16,1),var1,"g-")
    plt.xticks(np.arange(1,16,1))
    plt.xlabel("Parametric VaR horizon (# of days)")
    plt.ylabel("Loss size")
    st.pyplot(plt)
    
    
    st.subheader("1D to 15D historical VaR for selected confidence level")
    
    var_hist,expected_shortfall_hist=historical_var(Confidence,st.session_state.returns,st.session_state.z1,Investment)
    
    fig6=plt.figure("figure 6, historical var value for 1 up to 15 days")
    plt.plot(np.arange(1,16,1),var_hist,"g-")
    plt.xticks(np.arange(1,16,1))
    plt.xlabel("Historical VaR horizon (# of days)")
    plt.ylabel("Loss size")
    plt.axhline(y = expected_shortfall_hist, color = 'r', linestyle = 'dashed',label='Expected Shortfall')
    st.pyplot(plt)
    
    
    st.subheader("Expected Shortfall for Historical VaR")
    st.write("Your expected shortfall is ","{:.2f}".format(expected_shortfall_hist))

 
    

if all(st.session_state.check[:4]):
    run()
    st.session_state.check[4]=True   
else:
    st.markdown("""<style>.big-font {font-size:50px !important;}</style>""", unsafe_allow_html=True)

    st.markdown('<p class="big-font">Please execute the pages sequentially!</p>', unsafe_allow_html=True)    
        