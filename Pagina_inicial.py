import numpy as np
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


col1, col2, col3= st.columns([1,4,1])
with col2:
    st.image('https://api.observatorio.analisepoliticaemsaude.org/media/thematic_axes/bbbee2c4f109e102018d901cead397f2/imgs/bbbee2c4f109e102018d901cead397f2.png')
st.markdown('''
# **Observatório de Análise Política de Saúde - eixo Mídia e Saúde**

Essa é uma aplicação web criada através da biblioteca Streamlit (https://docs.streamlit.io/l), em linguagem Python, por Arthur Lopes (UFBA).
O intuito da aplicação é ser uma ferramenta de Infovigilância para pesquisadoras(es) do grupo de pesquisa a fim de viabilizar a criação de relatórios através de dados de conversações públicas e cobertura jornalistica sobre temas de interesse da saúde pública.

Boa pesquisa!
''')




