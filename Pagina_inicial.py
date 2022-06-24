import numpy as np
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


#Putting an image to make the web app more appealing
st.image('https://www.cei.int/sites/default/files/2020-11/TOL%20Education.PNG')
#Presentation
st.markdown('''
# **Análise exploratória de dados para pesquisas na área da comunicação em saúde**

Essa é uma aplicação web criada através da biblioteca Streamlit (https://docs.streamlit.io/l), em linguagem Python, por Arthur Lopes (UFBA); durante vigência da bolsa FAPESB/Fiocruz.
O intuito da aplicação é tornar mais fácil e acessível a análise exploratória de dados para pesquisadores(as) leigas em programação.

Boa pesquisa!
''')
#Image reference
st.caption('Image source: Central European Initiative (CEI). Url: <https://www.cei.int/events/countering-the-infodemic-best-practices-in-debunking-disinformation>')


st.sidebar.image("https://i.ibb.co/Y2f21V2/python-logo-1.png")
st.sidebar.image("http://www.fapesb.ba.gov.br/wp-content/uploads/2019/08/FAPESB-SITE-01-300x99.png")



