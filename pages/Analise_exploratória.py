import numpy as np
import pandas as pd
import streamlit as st
import xlrd
import openpyxl


st.markdown('''
# **Vamos dar uma olhada mais aprofundada na participação de usuários(as) na conversação?**

Vejamos, selecione um arquivo para que possamos começar a análise.
''')


#uploud data
option = st.sidebar.selectbox('Selecione um formato', ('csv','excel'))
st.sidebar.write('Você selecionou:', option)
#pandas profiling report

with st.sidebar.header('Suba o arquivo'):
    uplouded_file = st.sidebar.file_uploader("Escolha o arquivo")
    


if uplouded_file is not None:
    

    if option == 'csv':
        @st.cache
        def load_data(uplouded_file):
            data = pd.read_csv(uplouded_file)
            return data
    
    else:
        @st.cache
        def load_data(uplouded_file):
            data = pd.read_excel(uplouded_file, engine='openpyxl')
            return data

    data_load_state = st.text('Carregando arquivo...')
    df = load_data(uplouded_file)
    data_load_state = st.text('Eitchan, carregamento conluido! (using st.cache)')

    #select the author to see their tweets


    authorsname = df['author'].tolist()
    authoroptions = st.sidebar.selectbox('Qual autor deseja selecionar?', authorsname)
    st.subheader('**Usuários que mais publicaram**')
    authorpostnumber = df['author'].value_counts()
    st.write(authorpostnumber)
    st.text('Agora que sabe quem é que mais foi ativo(a) na conversação, escolha ao lado aquele(a) que deseja selecionar para analisar suas publicações.')
    st.subheader('**Dataframe filtrado por usuário(a)**')
    df_author = df[df['author'].str.contains(authoroptions)]
    numberrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df_author)+1)
    df_author = df[df['author'].str.contains(authoroptions)].head(numberrows)
    st.write(df_author)

    analysetext = st.checkbox('Tudo bem, agora quero analisar os tweets desse(a) usuário(a)')
    
    if analysetext:
        st.markdown('''
        
        **Vamos lá!** 
        
        Vamos explorar esses dados mais à fundo! À partir de agora, você precisa fazer algumas escolhas.


        Veja bem, na caixa de seleção **qual coluna?** você vai selecionar a coluna de interesse. 

            Ex:  No caso da pesquisa sobre os(as) heróis(inas) da desinformação, a coluna "herois" corresponde àquela de interesse, pois seu valor corresponde à qual heroi foi mencionado no tweet correspondente.

        Uma vez selecionada a coluna, você tem interesse em fazer uma análise à nivel de usuário(a) ou de categoria?
            Ex: 

            Usuário: quero entender de que maneira o(a) usuário(a) em questão acionou cada heroi, ou um heroi específico. Caso seja específico, escreva o nome do(a) herói(ina) no espaço reservado.
            Categoria: quero entender de que maneira um(a) dado(a) herói(ina) se fez ser mencionada no geral. Escreva no espaço reservado o nome do(a) herói(ina) que deseja analisar.
        ''')

        columns = df_author.columns
        columnpreference = st.checkbox('Tenho algum filtro? Ex: Desejo selecionar apenas textos pertencentes à uma dada classificação.')
        if columnpreference:
            columnchoosen = st.selectbox('Qual coluna?', columns)
            textcontent = st.selectbox('Você tem interesse em ver os tweets do(a) usuário(a) selecionado(a) ou os tweets de todos(as) aqueles(as) que se enquadram na categoria/classe escolhida?', ['usuário','categoria'])
            if textcontent == 'usuário':
                columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse relacionada às publicações do(a) usuário(a) selecionado(a):')
                textchoosen = st.selectbox('Qual coluna quero analisar, title ou description?',['title','description'])
                st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                tweet = df_author[df_author[columnchoosen].str.contains(columnvalue)][textchoosen].head(numberrows).tolist()
                st.write(tweet)
            else:
                columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse:')
                numberrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df[df[columnchoosen].str.contains(columnvalue)])+1)
                textchoosen = st.selectbox('Qual coluna quero analisar, title ou description?',['title','description'])
                st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                tweet = df[df[columnchoosen].str.contains(columnvalue)][textchoosen].head(numberrows).tolist()
                st.write(tweet)
                
        else:
            textchoosen = st.selectbox('Qual coluna quero analisar, title ou description?',['title','description'])
            st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
            tweet = df_author[textchoosen].head(numberrows).tolist()
            st.write(tweet)
    
                 
    




    #select a specific column to filter the dataframe frame based on that


