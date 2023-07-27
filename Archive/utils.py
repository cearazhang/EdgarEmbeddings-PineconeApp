# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 20:44:21 2023

@author: Marios
"""

import pandas as pd
import wikipedia as wp
import datetime
import yfinance as yf
import numpy as np
import scipy.sparse as sp
import cvxpy as cp
import matplotlib.pyplot as plt
import scipy.stats as spstats
import streamlit as st


###############################################################################################################
######################################### PAGE 6 ##############################################################
###############################################################################################################
 

def parametric_var(confidence,mu,sigma,investment):
    #calculate var based on a normal distribution of returns with mean and variance of daily returns 
    #return 1D to 15D, if user only wants 1D, they can just index the zeroth element
    s=spstats.norm.ppf(confidence,mu,sigma)
    var=[investment*(-s*np.sqrt(days)) for days in np.arange(1,16,1)]
    
    return var


def historical_var(confidence,returndata,weights,investment):
    #use historical returns to generate a vector of next day's returns
        
    s=returndata@weights  #returndata is a dataframe of returns for all dates and tickers. weights is the corresponding weight vector
    var=[investment* (-s.quantile(confidence))*np.sqrt(days) for days in np.arange(1,16,1)]
    expected_shortfall= investment*-s[s<=s.quantile(confidence)].mean()
    return var,expected_shortfall


###############################################################################################################
######################################### PAGE 5 ##############################################################
###############################################################################################################
    

def weight_bar_plotter(tickers,values,LongOnly=False,Leverage=False,LevAndRisk=False):
    
    if LongOnly:
        
        val=values[values>0.001]
        tick = np.array(tickers)[values>0.001]
        plt.figure(figsize=(10,6))
        plt.xlabel("Stocks",size=15)
        plt.ylabel("Weight",size=15)
        plt.title('Stocks with weight bigger than 0.1%')
        plt.ylim((0,1))
        
        
        p1=plt.bar(tick,val)
        for rect1 in p1:
            height=rect1.get_height()
            plt.annotate("{:.2f}%".format(height*100),(rect1.get_x() + rect1.get_width()/2, height),ha="center",va="bottom",fontsize=12)
            
            
    elif Leverage:
         val=values[np.where((values>0.001) | (values<-0.001))]
         tick=np.array(tickers)[np.where((values>0.001) | (values<-0.001))]
         plt.figure(figsize=(10,6))
         plt.xlabel("Stocks",size=15)
         plt.ylabel("Weight",size=15)
         plt.title('Stocks with absolute value of weight bigger than 0.1%')
         
         
         p2=plt.bar(tick,val)
         for rect1 in p2:
             height=rect1.get_height()
             if height>=0:
                 
                 plt.annotate("{:.2f}%".format(height*100),(rect1.get_x() + rect1.get_width()/2, height),ha="center",va="bottom",fontsize=12)
             else:
                 plt.annotate("{:.2f}%".format(height*100),(rect1.get_x() + rect1.get_width()/2, height-0.03),ha="center",va="bottom",fontsize=12)
                 
    elif LevAndRisk:
            val=values[np.where((values>0.001) | (values<-0.001))]
            tick=np.array(tickers)[np.where((values>0.001) | (values<-0.001))]
            plt.figure(figsize=(10,6))
            plt.xlabel("Stocks",size=15)
            plt.ylabel("Weight",size=15)
            plt.title('Stocks with absolute value of weight bigger than 0.1%')
            
            
            p2=plt.bar(tick,val)
            for rect1 in p2:
                height=rect1.get_height()
                if height>=0:
                    
                    plt.annotate("{:.2f}%".format(height*100),(rect1.get_x() + rect1.get_width()/2, height),ha="center",va="bottom",fontsize=12)
                else:
                    plt.annotate("{:.2f}%".format(height*100),(rect1.get_x() + rect1.get_width()/2, height-0.03),ha="center",va="bottom",fontsize=12)

         


def get_returns(tickers,start,end):
    
    data=yf.download(tickers,start,end)
    prices=data['Adj Close']
    returns=np.log(prices/prices.shift(1)).dropna()
    return returns 
     
    
    
def longonly(returns ,gamma_val=False):
    
    mu=returns.mean().to_numpy()
    sigma=returns.cov().to_numpy()
    w=cp.Variable(len(returns.columns))
    gamma=cp.Parameter(nonneg=True)
    ret=mu.T@w
    risk=cp.quad_form(w,sigma)
    prob=cp.Problem(cp.Maximize(ret - gamma * risk), [cp.sum(w) == 1, w >= 0])
    
    if not gamma_val:     #if no gamma value user input, solve for many gamma values to return efficient frontier analytics 
        risk_data=np.zeros(100)
        ret_data=np.zeros(100)
        gamma_vals=np.logspace(-2,3,100)
        for i in range(100):
            gamma.value=gamma_vals[i]
            prob.solve()
            risk_data[i]=cp.sqrt(risk).value
            ret_data[i]=ret.value
        return ret_data,risk_data,mu,sigma
            
    else:
        gamma.value=gamma_val        #if user inputs gamma value, solve for that gamma value and return analytics
        prob.solve()
        return w.value,ret.value, cp.sqrt(risk).value,mu,sigma
    

def with_leverage(returns,GammaUserInput=False,LmaxUserInput=False,SAMPLES=100,L_vals = [1, 2, 4]):
    
    mu=returns.mean().to_numpy()
    sigma=returns.cov().to_numpy()
    w=cp.Variable(len(returns.columns))
    gamma=cp.Parameter(nonneg=True)
    ret=mu.T@w
    risk=cp.quad_form(w,sigma)
    Lmax = cp.Parameter()
    prob2 = cp.Problem(cp.Maximize(ret - gamma * risk), [cp.sum(w) == 1, cp.norm(w, 1) <= Lmax])
    
    if GammaUserInput and LmaxUserInput:
        gamma.value=GammaUserInput
        Lmax.value=LmaxUserInput
        prob2.solve(solver=cp.SCS)
        
        return w.value, ret.value,cp.sqrt(risk).value,mu,sigma
    else:
        
        risk_data2 = np.zeros((len(L_vals), SAMPLES))
        ret_data2 = np.zeros((len(L_vals), SAMPLES))
        gamma_vals2 = np.logspace(-2, 3, num=SAMPLES)
        w_vals = []
        for k, L_val in enumerate(L_vals):
            for i in range(SAMPLES):
                Lmax.value = L_val
                gamma.value = gamma_vals2[i]
                prob2.solve(solver=cp.SCS)
                risk_data2[k, i] = cp.sqrt(risk).value
                ret_data2[k, i] = ret.value
        fig11=plt.figure("This is a figure,efficient frontiers for various leverage limits")        
        for idx, L_val in enumerate(L_vals):
            plt.plot(risk_data2[idx, :], ret_data2[idx, :], label=r"$L^{\max}$ = %d" % L_val)
         
        plt.xlabel("Standard deviation")
        plt.ylabel("Return")
        plt.legend(loc="lower right") 
        st.pyplot(plt)        
    

def efficient_frontier_plotter(risk_data,ret_data,sigma,mu,selected_stocks):
    
        markers_on = [20,40,60]
        fig1 = plt.figure("This is figure 1, efficient frontier")
        ax = fig1.add_subplot(111)
        plt.plot(risk_data,ret_data, "g-")
        
        zzzz=np.logspace(-2,3,100)  #just to be used to annotate points on efficient frontier on graph below
    
        for marker in markers_on:
            plt.plot(risk_data[marker], ret_data[marker], "bs")
            ax.annotate(
                r"$\gamma = %.2f$" % zzzz[marker],
                xy=(risk_data[marker]+0.0005  , ret_data[marker]-0.00001),
            )
            
        for i in range(len(selected_stocks)):
            plt.plot(cp.sqrt(sigma[i, i]).value, mu[i], "ro")
        plt.xlabel("Standard deviation")
        plt.ylabel("Return")
        plt.title("Efficient frontier")
        st.pyplot(plt)


def individual_dist_plotter(mu,std,stock_names,stock_weights,GammaUserInput,LongOnly=False,Leverage=False,LevAndRisk=False):
    
    
    
    if LongOnly:
        #this also works for lev and risk, since i dont plot for multiple leverages,same inputs
        fig2=plt.figure("figure 2",figsize=(8,5))
    
        
        x = np.linspace(-1.2, 2, 1000)
        plt.plot(
                x,
                spstats.norm.pdf(x, mu*252, std*np.sqrt(252)),
                label=r"$\gamma = %.2f$" % GammaUserInput,
            )
        plt.xticks(np.arange(-1.2,2,step=0.2))
        plt.xlabel("Return")
        plt.ylabel("Density")
        plt.legend(loc="upper right") 
        st.pyplot(plt)
        
        
        st.subheader("Stocks with corresponding weight over 0.1% for a long only portfolio")
        weight_bar_plotter(stock_names, stock_weights,LongOnly=True)
        st.pyplot(plt)
        
    elif Leverage:
        st.subheader("Distribution of returns for selected risk aversion level and leverage limit.")
        fig3=plt.figure("figure 3",figsize=(8,5))
    
        
        x = np.linspace(-1.2, 2, 1000)
        plt.plot(
                x,
                spstats.norm.pdf(x, mu*252, std*np.sqrt(252)),'y-',
                label=r"$\gamma = %.2f$" % GammaUserInput,
            )
        plt.xticks(np.arange(-1.2,2,step=0.2))
        plt.xlabel("Return")
        plt.ylabel("Density")
        plt.legend(loc="upper right") 
        st.pyplot(plt)
        
        
        st.subheader("Stocks weights in Leveraged portfolio")
        weight_bar_plotter(stock_names, stock_weights,Leverage=True)
        st.pyplot(plt)
        
    elif LevAndRisk:
        fig10=plt.figure("figure 10",figsize=(8,5))
    
        
        x = np.linspace(-1.2, 2, 1000)
        plt.plot(
                x,
                spstats.norm.pdf(x, mu*252, std*np.sqrt(252)),
                label=r"$\gamma = %.2f$" % GammaUserInput,
            )
        plt.xticks(np.arange(-1.2,2,step=0.2))
        plt.xlabel("Return")
        plt.ylabel("Density")
        plt.legend(loc="upper right") 
        st.pyplot(plt)
        
        
        st.subheader("Stocks with corresponding weight over 0.1% for a leveraged portfolio with risk limits")
        weight_bar_plotter(stock_names, stock_weights,LevAndRisk=True)
        st.pyplot(plt)
    
        
         
    

def with_leverage_and_risk_limit(returns,GammaUserInput,LmaxUserInput,RiskLimit):
    mu=returns.mean().to_numpy()
    sigma=returns.cov().to_numpy()
    w=cp.Variable(len(returns.columns))
    gamma=cp.Parameter(nonneg=True)
    ret=mu.T@w
    risk=cp.quad_form(w,sigma)
    Lmax = cp.Parameter()
    prob3 = cp.Problem(cp.Maximize(ret), [cp.sum(w) == 1, cp.norm(w, 1) <= Lmax, risk <= RiskLimit])
    Lmax.value=LmaxUserInput
    prob3.solve()
    return w.value, ret.value,cp.sqrt(risk).value,mu,sigma
    
    