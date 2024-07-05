import streamlit as st
import numpy as np

col1, col2, col3 = st.columns(3, gap="large")

with col1:
   st.header("MEOW")
   st.bar_chart(np.random.randn(50, 3))

with col2:
   st.header("MEOW")
   st.bar_chart(np.random.randn(50, 3))

with col3:
   st.header("MEOW")
   st.bar_chart(np.random.randn(50, 3))