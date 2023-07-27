# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 23:34:26 2023

@author: Marios
"""
import streamlit as st
from utils import *
import tkinter
import matplotlib
matplotlib.use('agg')

st.title("Portfolio optimization using the CVX library.")
st.write("by [Marios](https://www.linkedin.com/in/mariosefstathiadis/)")
st.markdown("Throughout this example we will be optimizing a portfolio"
            "consisting of the companies that make up the DOW30 index.")
html = wp.page("Dow_Jones_Industrial_Average").html().encode("UTF-8")
dfwiki=pd.read_html(html)
tickers=list(dfwiki[1]['Symbol'])
tc=Portfolio(tickers)
tc.longonly(100)

st.header("Long Only Optimization.")
st.markdown("The first optimization is done under the restriction that all the weights of the individual stocks are positive"
            "(long only), and that the sum of the weights adds to 1")
#long only trade off curve plot
markers_on = [34, 50,70]
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(tc.LongOnly_risk_data, tc.LongOnly_ret_data, "g-")
for marker in markers_on:
    plt.plot(tc.LongOnly_risk_data[marker], tc.LongOnly_ret_data[marker], "bs")
    ax.annotate(
        r"$\gamma = %.2f$" % tc.gamma_vals[marker],
        xy=(tc.LongOnly_risk_data[marker]+0.0005  , tc.LongOnly_ret_data[marker]-0.00001),
    )
for i in range(30):
    plt.plot(cp.sqrt(tc.Sigma[i, i]).value, tc.mu[i], "ro")
plt.xlabel("Standard deviation")
plt.ylabel("Return")
st.pyplot(plt)


#start formatting sidebar
st.sidebar.title("Parameters")

#user inputs on sidebar
GammaUserInput = st.sidebar.slider('Risk aversion value', value=2.0, 
                      min_value=0.01, max_value=1000.0)
tc.gamma.value=GammaUserInput
z1,z2= tc.longonly()
z2.resize(1)
st.sidebar.write("Your annualized return for a long only portfolio with that risk aversion ", z1*252)
st.sidebar.write("Your annualized risk for a long only portfolio with that risk aversion ", z2[0]*np.sqrt(252))


st.subheader("Distrubition of returns for selected risk aversion level (long only portfolio).")


fig2=plt.figure("figure 2",figsize=(8,5))

#tc.LongOnly_prob.solve()
x = np.linspace(-1.2, 2, 1000)
plt.plot(
        x,
        spstats.norm.pdf(x, z1*252, z2[0]*np.sqrt(252)),
        label=r"$\gamma = %.2f$" % tc.gamma.value,
    )
plt.xticks(np.arange(-1.2,2,step=0.2))
plt.xlabel("Return")
plt.ylabel("Density")
plt.legend(loc="upper right") 
st.pyplot(plt)

st.subheader("Weights for each ticker after long only optimization for selected risk aversion level.")
df1=pd.DataFrame(data=tc.w.value.round(3),index=tickers)
st.dataframe(df1)

Confidence=st.sidebar.slider('VaR Confidence Level',value=0.05,min_value=0.01,max_value=0.4)
Investment=st.sidebar.slider('Investment amount',value=5e4,min_value=1e4,max_value=1e5)

z3=parametric_var(Confidence, z1, z2[0],Investment)

st.subheader('1D to 15D parametric VaR for selected confidence level.')

fig5=plt.figure("figure 4, parametric var value for 1 up to 15 days")
plt.plot(np.arange(1,16,1),z3,"g-")
plt.xticks(np.arange(1,16,1))
plt.xlabel("Parametric VaR horizon (# of days)")
plt.ylabel("Loss size")
st.pyplot(plt)

st.subheader("1D to 15D historical VaR for selected confidence level")

z4=historical_var(Confidence,tc.returns,tc.w.value,Investment)

fig6=plt.figure("figure 6, historical var value for 1 up to 15 days")
plt.plot(np.arange(1,16,1),z4,"g-")
plt.xticks(np.arange(1,16,1))
plt.xlabel("Historical VaR horizon (# of days)")
plt.ylabel("Loss size")
st.pyplot(plt)


st.header("Leveraged portfolio")
st.markdown("Here we introduce a leverage limit Lmax. Optimization happens under the constraints that the sum of the weights adds to 1,"
            "and the first norm is less than Lmax.Greater leverage allows for greater returns, accompanied with greater risk")

L_vals=[1,2,4]
tc.leverage(100,L_vals)

#Plot trade-off curves for each leverage limit.
fig3=plt.figure("figure 3")
for idx, L_val in enumerate(L_vals):
    plt.plot(tc.Leverage_risk_data[idx, :], tc.Leverage_ret_data[idx, :], label=r"$L^{\max}$ = %d" % L_val)
 
plt.xlabel("Standard deviation")
plt.ylabel("Return")
plt.legend(loc="lower right")
st.pyplot(plt)

st.header("Leveraged portfolio with an upper limit on risk")
st.markdown("We continue with the optimization of a leveraged portfolio, adding an extra constraint of maximum risk we are willing to take")
# Compute solution for different leverage limits.
w_vals=[]
risklimit=2
tc.levandrisk(100,L_vals,risklimit)
for k, L_val in enumerate(L_vals):
    tc.Lmax.value = L_val
    tc.LeverageAndRisk_prob.solve()
    w_vals.append(tc.w.value)
    
   
colors = ["b", "g", "r"]
indices = np.argsort(tc.mu.flatten())

fig4=plt.figure("figure 4")
for idx, L_val in enumerate(L_vals):
    plt.bar(
        np.arange(1, 31) + 0.25 * idx - 0.375,
        w_vals[idx][indices],
        color=colors[idx],
        label=r"$L^{\max}$ = %d" % L_val,
        width=0.25,
    )
plt.ylabel(r"$w_i$", fontsize=16)
plt.xlabel(r"$i$", fontsize=16)
plt.xlim([1 - 0.375, 30 + 0.375])
plt.xticks(np.arange(1, 31))
st.pyplot(plt)

  