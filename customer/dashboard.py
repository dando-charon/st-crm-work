import streamlit as st
import pandas as pd
import numpy as np
from vega_datasets import data

st.title("dashboard")

source = data.barley()

st.bar_chart(source, x="variety", y="yield", color="site", horizontal=True)

source = data.barley()

st.bar_chart(source, x="year", y="yield", color="site", stack=False)
