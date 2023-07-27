# -*- coding: utf-8 -*-
"""
Created on Tue May  9 17:18:34 2023

@author: Marios
"""

import streamlit as st
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



def run():

    st.title("Optimization Analytics")
    
    st.write("For the optimization procedure the [CVX Library](https://www.cvxpy.org/) is used.")
    
    st.session_state.returns=get_returns(st.session_state.selected_stocks,start=st.session_state.start_date,end=st.session_state.end_date)
    
    #start formatting sidebar
    st.sidebar.title("Portfolio Constraint Parameters")
    
    GammaUserInput = st.sidebar.slider('Risk aversion value', value=2.0, 
                          min_value=0.01, max_value=10.0)
    LmaxUserInput=st.sidebar.slider("Leverage limit value",value=2.0,min_value=1.0,max_value=5.0)
    RiskLimitUserInput=st.sidebar.slider("Risk limit value",value=2.0,min_value=0.5,max_value=10.0)
    
    st.sidebar.subheader("Monte Carlo Parameters")
    NumberStepsUserInput=st.sidebar.slider("Number of Steps",value=150,min_value=1,max_value=1000)
    NumberSimsUserInput=st.sidebar.slider("Number of Trajectories",value=1000,min_value=100,max_value=10000)
    Investment=st.sidebar.slider('Investment amount',value=5e4,min_value=1e4,max_value=1e5)
    
    st.session_state.inv=Investment
    
    if 'Long Only' in st.session_state.selected_method:  #CHECK THIS CONDITION, HOW DO I CONNECT IT TO CHOICE, WHAT DOES IT RETURN
               
        ret_data,risk_data,mu,sigma=longonly(st.session_state.returns)
        st.header("Long Only Optimization")
        st.markdown("The first optimization is done under the restriction that all the weights of the individual stocks are positive"
                    "(long only), and that the sum of the weights adds to 1.")
        
       
        efficient_frontier_plotter(risk_data,ret_data,sigma,mu,st.session_state.selected_stocks)
        
        st.session_state.lo_weights,st.session_state.lo_returns,st.session_state.lo_risk,lo_mu,lo_sigma=longonly(st.session_state.returns,gamma_val=GammaUserInput)  #see what the function returns above, can't use convinient names for everything
        st.subheader("Distribution of returns for selected risk aversion level (long only portfolio).")
        individual_dist_plotter(st.session_state.lo_returns,st.session_state.lo_risk,st.session_state.selected_stocks,st.session_state.lo_weights,GammaUserInput,LongOnly=True)
        
        st.write(" - Your annualized return for a long only portfolio with risk aversion {} is: ".format(GammaUserInput), '{:.2%}'.format(st.session_state.lo_returns*252))
        st.write(" - Your annualized risk for a long only portfolio with risk aversion {} is: ".format(GammaUserInput), '{:.2%}'.format(st.session_state.lo_risk *np.sqrt(252)))


        st.subheader("Monte Carlo Simulation for the selected long only portfolio")
        
        st.session_state.lo_St=mc_sim(Investment,NumberStepsUserInput,NumberSimsUserInput,st.session_state.lo_returns,st.session_state.lo_risk)
        fig15=plt.figure()
        ax1=fig15.add_subplot(111)
        
        for i in np.random.choice(np.array(range(1,NumberSimsUserInput+1)),size=100):
            ax1.plot(st.session_state.lo_St[i],'b',lw=0.5)
        
        plt.ylabel("Porftolio Value")
        plt.xlabel("Time Steps (in days)")
        plt.title("Displaying 100 out of {} trajectories.".format(NumberSimsUserInput))
            
        st.pyplot(plt)   
        
    if 'With Leverage' in st.session_state.selected_method:
        
        st.header("Optimization with leverage")
        st.markdown("This optimization is done under the restriction that the weights of the individual stocks add to 1, but we allow for negative weights.")
        
        st.subheader("Efficient frontier for various leverage limits")
        with_leverage(st.session_state.returns)
        
        st.session_state.lev_w_value,st.session_state.lev_ret_value,st.session_state.lev_risk_value,lev_mu,lev_sigma=with_leverage(st.session_state.returns,GammaUserInput,LmaxUserInput)
                
        individual_dist_plotter(st.session_state.lev_ret_value,st.session_state.lev_risk_value,st.session_state.selected_stocks,st.session_state.lev_w_value,GammaUserInput,Leverage=True)
        
        st.write(" - Your annualized return for a leveraged portfolio with risk aversion {} and Lmax {} is: ".format(GammaUserInput,LmaxUserInput), '{:.2%}'.format(st.session_state.lev_ret_value*252))
        st.write(" - Your annualized risk for a leveraged portfolio with risk aversion {} and Lmax {} is: ".format(GammaUserInput,LmaxUserInput), '{:.2%}'.format(st.session_state.lev_risk_value*np.sqrt(252)))

        st.subheader("Monte Carlo Simulation for the selected leveraged portfolio")
        st.session_state.lev_St=mc_sim(Investment,NumberStepsUserInput,NumberSimsUserInput,st.session_state.lev_ret_value,st.session_state.lev_risk_value)
        fig16=plt.figure()
        ax2=fig16.add_subplot(111)
        
        for i in np.random.choice(np.array(range(1,NumberSimsUserInput+1)),size=100):
            ax2.plot(st.session_state.lev_St[i],'r',lw=0.5)
        
        plt.ylabel("Porftolio Value")
        plt.xlabel("Time Steps (in days)")
        plt.title("Displaying 100 out of {} trajectories.".format(NumberSimsUserInput))
            
        st.pyplot(plt) 
              
    if 'With Leverage and Risk Limit' in st.session_state.selected_method:
        
        st.header("Optimization with Leverage and Risk Limit")
        st.markdown("This optimization is done under the restriction that the weights of the individual stocks add to 1, allowing for negative weights, and placing an upper limit on portfolio risk")
        st.session_state.wlar_weights,st.session_state.wlar_return,st.session_state.wlar_risk,wlar_mu,wlar_sigma=with_leverage_and_risk_limit(st.session_state.returns,GammaUserInput,LmaxUserInput,RiskLimitUserInput)
        individual_dist_plotter(st.session_state.wlar_return,st.session_state.wlar_risk,st.session_state.selected_stocks,st.session_state.wlar_weights,GammaUserInput,LevAndRisk=True)
        
        st.subheader("Monte Carlo Simulation for the selected leveraged portfolio under risk constraints")
        st.session_state.wlar_St=mc_sim(Investment,NumberStepsUserInput,NumberSimsUserInput,st.session_state.lev_ret_value,st.session_state.lev_risk_value)
        fig17=plt.figure()
        ax3=fig17.add_subplot(111)
        
        for i in np.random.choice(np.array(range(1,NumberSimsUserInput+1)),size=100):
            ax3.plot(st.session_state.wlar_St[i],'y',lw=0.5)
        
        plt.ylabel("Porftolio Value")
        plt.xlabel("Time Steps (in days)")
        plt.title("Displaying 100 out of {} trajectories.".format(NumberSimsUserInput))
            
        st.pyplot(plt)
        
        
        
if all(st.session_state.check[:3]):
    
    if len(st.session_state.selected_stocks)<=1 or len(st.session_state.selected_method)<1:
        
        st.subheader("Invalid Input Error")
        st.markdown("Please ensure that:")
        st.markdown(" - You have selected at least two assets.")
        st.markdown(" - You have selected a method of optimization.")

        
    else:
        st.session_state.check[3]=True
        run()
        

    
else:
    st.markdown("""<style>.big-font {font-size:50px !important;}</style>""", unsafe_allow_html=True)

    st.markdown('<p class="big-font">Please execute the pages sequentially!</p>', unsafe_allow_html=True)
   