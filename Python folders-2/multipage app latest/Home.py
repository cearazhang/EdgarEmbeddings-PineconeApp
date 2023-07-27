# -*- coding: utf-8 -*-
"""
Created on Tue May  9 16:41:04 2023

@author: Marios
"""

import streamlit as st
from utils import *
from PIL import Image


st.session_state.check=[True,False,False,False,False]


image=Image.open("QuantUniversityLogo.png")
st.image(image)

st.header("Quant University Portfolio Optimization")
st.write("by [Marios](https://www.linkedin.com/in/mariosefstathiadis/)")
st.markdown("In this application we will illustrate concepts of portfolio optimization using various optimization methods and techniques, as well as risk analytics.")
st.markdown("The universe we are operating in, is the set of stocks that constitute the DOW30 Index.")
st.markdown(" - In the Exploration page, you can choose to view information on any individual stock of the DOW30, or the index itself.")
st.markdown(" - In the Asset Selection page, you can choose a subset of stocks you wish to include in your portfolio, as well as constraints to optimize under.")
st.markdown(" - In the Portfolio Analytics page, you will be provided with various insights and analytics for your selected stock subset and optimization methods.")
st.markdown(" - In the Risk Analytics page, you will be provided with risk metrics for your portfolio.")
st.markdown("Please note that all pages have to be executed sequentially.")
 