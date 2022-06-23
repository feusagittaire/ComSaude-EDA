import numpy as np
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

#uploud csv data

with st.sidebar.header('Suba o arquivo CSV'):
    uplouded_file = st.sidebar.file_uploader("Escolha o arquivo CSV")
    
option = st.sidebar.selectbox('Selecione um formato', ('csv','excel'))
st.sidebar.write('Você selecionou:', option)
#pandas profiling report

if uplouded_file is not None:
    

    if option == 'csv':
        @st.cache
        def load_data(uplouded_file):
            data = pd.read_csv(uplouded_file)
            return data
    
    else:
        @st.cache
        def load_data(uplouded_file):
            data = pd.read_excel(uplouded_file)
            return data

    data_load_state = st.text('Carregando arquivo...')
    df = load_data(uplouded_file)
    data_load_state = st.text('Eitchan, carregamento conluido! (using st.cache)')
    pr = df.profile_report()
    st.header('**DataFrame**')
    st.write(df)
    st.write('-----')
    st.header('**Pandas Profile Report**')
    st_profile_report(pr)
    
else:
    st.info("Esperando que um arquivo CSV seja upado")
