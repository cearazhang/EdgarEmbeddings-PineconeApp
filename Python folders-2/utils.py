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


def parametric_var(confidence,mu,sigma,investment):
    #calculate var based on a normal distribution of returns with mean and variance of daily returns 
    #return 1D to 15D, if user only wants 1D, they can just index the zeroth element
        
    return [investment*(-spstats.norm.ppf(confidence,mu,sigma)*np.sqrt(days)) for days in np.arange(1,16,1)]


def historical_var(confidence,returndata,weights,investment):
    #use historical returns to generate a vector of next day's returns
    
    
    s=returndata@weights  #returndata is a dataframe of returns for all dates and tickers. weights is the corresponding weight vector
    return [investment* (-s.quantile(confidence))*np.sqrt(days) for days in np.arange(1,16,1)]
    



class Portfolio:
    def __init__(self,tickers,start=datetime.date(2020,1,1),end=datetime.date.today()-datetime.timedelta(days=1)):
        #set cvx params
        
        self.tickers=tickers
        self.start=start
        self.end=end
        self.data = yf.download(tickers, start,end)
        self.prices=self.data['Adj Close']
        self.returns=np.log(self.prices/self.prices.shift(1))
        self.mu=self.returns.mean().to_numpy()
        self.Sigma=self.returns.cov().to_numpy()
        self.w = cp.Variable(len(self.tickers))
        self.gamma = cp.Parameter(nonneg=True)
        self.ret = self.mu.T @ self.w
        self.risk = cp.quad_form(self.w, self.Sigma)
        self.Lmax = cp.Parameter()
        
        
    def longonly(self,samples=False):
        #solve for long only portfolio
        
        self.LongOnly_prob = cp.Problem(cp.Maximize(self.ret - self.gamma * self.risk), [cp.sum(self.w) == 1, self.w >= 0]) #keep prob without self so that it can be reused at every problem
        
        
        if samples:
            self.LongOnly_risk_data = np.zeros(samples)
            self.LongOnly_ret_data = np.zeros(samples) 
            self.gamma_vals = np.logspace(-2, 3, num=samples)
            for i in range(samples):
                self.gamma.value = self.gamma_vals[i]
                self.LongOnly_prob.solve()
                self.LongOnly_risk_data[i] = cp.sqrt(self.risk).value
                self.LongOnly_ret_data[i] = self.ret.value
                
        else:
            
            self.LongOnly_prob.solve()
            return self.ret.value, cp.sqrt(self.risk).value
    
    def leverage(self,samples,L_vals):
        # Portfolio optimization with leverage limit.
        
        self.Leverage_prob = cp.Problem(cp.Maximize(self.ret - self.gamma * self.risk), [cp.sum(self.w) == 1, cp.norm(self.w, 1) <= self.Lmax])
        self.Leverage_risk_data = np.zeros((len(L_vals), samples))
        self.Leverage_ret_data = np.zeros((len(L_vals), samples))
        self.gamma_vals2 = np.logspace(-2, 3, num=samples)
        for k, L_val in enumerate(L_vals):
            for i in range(samples):
                self.Lmax.value = L_val
                self.gamma.value = self.gamma_vals2[i]
                self.Leverage_prob.solve(solver=cp.SCS)
                self.Leverage_risk_data[k, i] = cp.sqrt(self.risk).value
                self.Leverage_ret_data[k, i] = self.ret.value
                
    def levandrisk(self,samples,L_vals,risklimit):
        # Portfolio optimization with a leverage limit and a bound on risk.
        
        self.LeverageAndRisk_prob=cp.Problem(cp.Maximize(self.ret), [cp.sum(self.w) == 1, cp.norm(self.w, 1) <= self.Lmax, self.risk <= risklimit])
        
        
