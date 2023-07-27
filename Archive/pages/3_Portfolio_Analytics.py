# -*- coding: utf-8 -*-
"""
Created on Tue May  9 17:18:34 2023

@author: Marios
"""

import streamlit as st

# can't import from utils since it's from another directory. Cant put it in this directory because streamlit regards it as a page
#All the utils will have to be in here, every page needs to be self sustainable. So utils + execution code will be in this page


import pandas as pd
import wikipedia as wp
import datetime
import yfinance as yf
import numpy as np
import scipy.sparse as sp
import cvxpy as cp
import matplotlib.pyplot as plt
import scipy.stats as spstats
from utils import *   

#############################################################################################################
######################################  S C R I P T #########################################################
#############################################################################################################

def run():

    st.title("Optimization Analytics")
    
    st.write("For the optimization procedure the [CVX Library](https://www.cvxpy.org/) is used.")
    
    st.session_state.returns=get_returns(st.session_state.selected_stocks,start=st.session_state.start_date,end=st.session_state.end_date)
    
    #start formatting sidebar
    st.sidebar.title("Parameters")
    
    GammaUserInput = st.sidebar.slider('Risk aversion value', value=2.0, 
                          min_value=0.01, max_value=10.0)
    LmaxUserInput=st.sidebar.slider("Leverage limit value",value=2.0,min_value=1.0,max_value=5.0)
    RiskLimitUserInput=st.sidebar.slider("Risk limit value",value=2.0,min_value=0.5,max_value=10.0)
    
    if 'Long Only' in st.session_state.selected_method:  #CHECK THIS CONDITION, HOW DO I CONNECT IT TO CHOICE, WHAT DOES IT RETURN
               
        ret_data,risk_data,mu,sigma=longonly(st.session_state.returns)
        st.header("Long Only Optimzation")
        st.markdown("The first optimization is done under the restriction that all the weights of the individual stocks are positive"
                    "(long only), and that the sum of the weights adds to 1.")
        
       
        efficient_frontier_plotter(risk_data,ret_data,sigma,mu,st.session_state.selected_stocks)
        
        st.session_state.z1,st.session_state.z2,st.session_state.z3,z4,z5=longonly(st.session_state.returns,gamma_val=GammaUserInput)  #see what the function returns above, can't use convinient names for everything
        st.subheader("Distribution of returns for selected risk aversion level (long only portfolio).")
        individual_dist_plotter(st.session_state.z2,st.session_state.z3,st.session_state.selected_stocks,st.session_state.z1,GammaUserInput,LongOnly=True)
        
        st.write(" - Your annualized return for a long only portfolio with risk aversion {} is: ".format(GammaUserInput), '{:.2%}'.format(st.session_state.z2*252))
        st.write(" - Your annualized risk for a long only portfolio with risk aversion {} is: ".format(GammaUserInput), '{:.2%}'.format(st.session_state.z3*np.sqrt(252)))

        
    if 'With Leverage' in st.session_state.selected_method:
        
        st.header("Optimization with leverage")
        st.markdown("This optimization is done under the restriction that the weights of the individual stocks add to 1, but we allow for negative weights.")
        
        st.subheader("Efficient frontier for various leverage limits")
        with_leverage(st.session_state.returns)
        
        lev_w_value,lev_ret_value,lev_risk_value,lev_mu,lev_sigma=with_leverage(st.session_state.returns,GammaUserInput,LmaxUserInput)
                
        individual_dist_plotter(lev_ret_value,lev_risk_value,st.session_state.selected_stocks,lev_w_value,GammaUserInput,Leverage=True)
        
        st.write(" - Your annualized return for a leveraged portfolio with risk aversion {} and Lmax {} is: ".format(GammaUserInput,LmaxUserInput), '{:.2%}'.format(lev_ret_value*252))
        st.write(" - Your annualized risk for a leveraged portfolio with risk aversion {} and Lmax {} is: ".format(GammaUserInput,LmaxUserInput), '{:.2%}'.format(lev_risk_value*np.sqrt(252)))

              
    if 'With Leverage and Risk Limit' in st.session_state.selected_method:
        
        st.header("Optimization with Leverage and Risk Limit")
        st.markdown("This optimization is done under the restriction that the weights of the individual stocks add to 1, allowing for negative weights, and placing an upper limit on portfolio risk")
        wlar_weights,wlar_return,wlar_risk,wlar_mu,wlar_sigma=with_leverage_and_risk_limit(st.session_state.returns,GammaUserInput,LmaxUserInput,RiskLimitUserInput)
        individual_dist_plotter(wlar_return,wlar_risk,st.session_state.selected_stocks,wlar_weights,GammaUserInput,LevAndRisk=True)
        
        
        
        
if all(st.session_state.check[:3]):
    run()
    st.session_state.check[3]=True

    
else:
    st.markdown("""<style>.big-font {font-size:50px !important;}</style>""", unsafe_allow_html=True)

    st.markdown('<p class="big-font">Please execute the pages sequentially!</p>', unsafe_allow_html=True)
   