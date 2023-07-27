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
    
    
    if 'Long Only' in st.session_state.selected_method:
        var1=parametric_var(Confidence, st.session_state.lo_returns, st.session_state.lo_risk ,st.session_state.inv)
        
               
        st.subheader('Long Only Optimization.')
        
        fig5=plt.figure("figure 4, parametric var value for 1 up to 15 days")
        plt.plot(np.arange(1,16,1),var1,"g-")
        plt.xticks(np.arange(1,16,1))
        plt.xlabel("Parametric VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.title('1D to 15D parametric VaR for selected confidence level.')
        st.pyplot(plt)
        
        
        
        
        var_hist,expected_shortfall_hist=historical_var(Confidence,st.session_state.returns,st.session_state.lo_weights,st.session_state.inv)
        
        fig6=plt.figure("figure 6, historical var value for 1 up to 15 days")
        plt.plot(np.arange(1,16,1),var_hist,"g-")
        plt.xticks(np.arange(1,16,1))
        plt.xlabel("Historical VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.axhline(y = expected_shortfall_hist, color = 'r', linestyle = 'dashed',label='Expected Shortfall')
        plt.title('1D to 15D Historical VaR for selected confidence level')
        st.pyplot(plt)
        
        
        st.write("Your Expected Shortfall for Historical VaR is ","{:.2f}".format(expected_shortfall_hist))
        
        fig13=plt.figure("figure 13,monte carlo var for 1 up to 15 days")
        lo_val=np.array([st.session_state.inv-st.session_state.lo_St.iloc[i].quantile(0.05) for i in range(1,16)])
        plt.plot(np.arange(1,16,1),lo_val,'b-')
        plt.xlabel("Monte Carlo VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.title('1D to 15D Monte Carlo VaR for selected confidence level')
        st.pyplot(plt)
        


    if 'With Leverage' in st.session_state.selected_method:
        var1=parametric_var(Confidence, st.session_state.lev_ret_value, st.session_state.lev_risk_value ,st.session_state.inv)
        
                
        st.subheader('Optimization with Leverage.')
        
        fig7=plt.figure("figure 7, parametric var value for 1 up to 15 days")
        plt.plot(np.arange(1,16,1),var1,"g-")
        plt.xticks(np.arange(1,16,1))
        plt.xlabel("Parametric VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.title('1D to 15D parametric VaR for selected confidence level.')
        st.pyplot(plt)
        
        
        
        
        var_hist,expected_shortfall_hist=historical_var(Confidence,st.session_state.returns,st.session_state.lev_w_value,st.session_state.inv)
        
        fig8=plt.figure("figure 8, historical var value for 1 up to 15 days")
        plt.plot(np.arange(1,16,1),var_hist,"g-")
        plt.xticks(np.arange(1,16,1))
        plt.xlabel("Historical VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.axhline(y = expected_shortfall_hist, color = 'r', linestyle = 'dashed',label='Expected Shortfall')
        plt.title('1D to 15D Historical VaR for selected confidence level')
        st.pyplot(plt)
        
        
       
        st.write("Your Expected Shortfall for Historical VaR is ","{:.2f}".format(expected_shortfall_hist))
        
        fig12=plt.figure("figure 12,monte carlo var for 1 up to 15 days")
        lev_val=np.array([st.session_state.inv-st.session_state.lev_St.iloc[i].quantile(0.05) for i in range(1,16)])
        plt.plot(np.arange(1,16,1),lev_val,'y-')
        plt.xlabel("Monte Carlo VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.title('1D to 15D Monte Carlo VaR for selected confidence level')
        st.pyplot(plt)
        
        
        
    if 'With Leverage and Risk Limit' in st.session_state.selected_method:
        
         
        var1=parametric_var(Confidence, st.session_state.wlar_return, st.session_state.wlar_risk ,st.session_state.inv)
        
                
        st.subheader('Optimization with Leverage under risk constraints.')
        
        fig9=plt.figure("figure 9, parametric var value for 1 up to 15 days")
        plt.plot(np.arange(1,16,1),var1,"g-")
        plt.xticks(np.arange(1,16,1))
        plt.xlabel("Parametric VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.title('1D to 15D parametric VaR for selected confidence level.')
        st.pyplot(plt)
        
        
        
        
        var_hist,expected_shortfall_hist=historical_var(Confidence,st.session_state.returns,st.session_state.wlar_weights,st.session_state.inv)
        
        fig10=plt.figure("figure 10, historical var value for 1 up to 15 days")
        plt.plot(np.arange(1,16,1),var_hist,"g-")
        plt.xticks(np.arange(1,16,1))
        plt.xlabel("Historical VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.axhline(y = expected_shortfall_hist, color = 'r', linestyle = 'dashed',label='Expected Shortfall')
        plt.title('1D to 15D Historical VaR for selected confidence level')
        st.pyplot(plt)
        
        
        st.write("Your Expected Shortfall for Historical VaR is ","{:.2f}".format(expected_shortfall_hist))
        
        fig14=plt.figure("figure 14,monte carlo var for 1 up to 15 days")
        wlar_val=np.array([st.session_state.inv-st.session_state.wlar_St.iloc[i].quantile(0.05) for i in range(1,16)])
        plt.plot(np.arange(1,16,1),wlar_val,'r-')
        plt.xlabel("Monte Carlo VaR horizon (# of days)")
        plt.ylabel("Loss size")
        plt.title('1D to 15D Monte Carlo VaR for selected confidence level')
        st.pyplot(plt)
        
        


if all(st.session_state.check[:4]):
    run()
    st.session_state.check[4]=True
    
else:
    st.markdown("""<style>.big-font {font-size:50px !important;}</style>""", unsafe_allow_html=True)

    st.markdown('<p class="big-font">Please execute the pages sequentially!</p>', unsafe_allow_html=True)    
        