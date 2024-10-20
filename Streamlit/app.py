import streamlit as st
import pandas as pd
import numpy as np     

## Ttitle of the application
st.title("Hello Streamlit")

## Display a Simple Text 

st.write("This is a simple text")

## Create a DF

df=pd.DataFrame({
    'First Column' : [1,2,3,4],
    'Second Column' : [10,20,30,40]
})

#Display DF
st.write("Here is the DF")
st.write(df)

## A line chart 
chart_data=pd.DataFrame(np.random.randn(20,3),columns=['a','b','c'])
st.line_chart(chart_data)