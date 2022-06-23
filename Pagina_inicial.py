import numpy as np
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import xlrd


#Web App Title
st.markdown('''
# **Análise exploratória de dados do CoronaJor**

Essa é uma aplicação web criada através da biblioteca Streamlit (https://docs.streamlit.io/l) em linguagem Python por Arthur Lopes.
O intuito da aplicação é tornar mais fácil e acessível a análise exploratória de dados para pesquisadores(as) leigas em programação.

Boa pesquisa!
''')




