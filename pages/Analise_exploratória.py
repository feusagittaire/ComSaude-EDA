import numpy as np
import pandas as pd
import streamlit as st



st.markdown('''
# **Vamos dar uma olhada mais aprofundada nos dados?**

Vejamos, selecione um arquivo para que possamos começar a análise.
''')


#uploud data
option = st.sidebar.selectbox('Selecione um formato', ('csv','excel'))
st.sidebar.write('Você selecionou:', option)
#pandas profiling report

with st.sidebar.header('Suba o arquivo'):
    uplouded_file = st.sidebar.file_uploader("Escolha o arquivo")
    


if uplouded_file is not None:
    
    
    if option == 'excel':

        @st.cache
        def load_data(uplouded_file):
            data = pd.read_excel(uplouded_file, engine = 'openpyxl')
            return data
        
    
    else:
        @st.cache
        def load_data(uplouded_file):
            data = pd.read_csv(uplouded_file)
            return data

    data_load_state = st.text('Carregando arquivo...')
    df = load_data(uplouded_file)
    data_load_state = st.text('Eitchan, carregamento conluido! (using st.cache)')

    #select the author to see their tweets
    taskchoice = st.selectbox('O que você quer fazer, analisar um relatório com os principais dados contidos no arquivo ou uma análise mais qualitativa?', ['relatório', 'qualitativa'])
    if taskchoice == 'relatório':
        st.subheader('**DataFrame**')
        st.write(df)
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
      
        st.subheader('**Descrição das tabelas contendo dados quantitativos (numéricos)**')
        st.write(df.describe())
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
        
        st.text('Será que existe alguma correlação (de Pearson) entre esses dados numéricos?')
        st.write(df.corr().round(1))
        st.write(df.corr().style.background_gradient(cmap='coolwarm'))
       
        timepossibility = st.selectbox('Seu DataFrame contém coluna de data? É possível fazer análise temporal com os dados que possui?', ['Não', 'Sim'])
        if timepossibility == 'Sim':
            timecolumn = st.text_input('Qual o nome da coluna? (Você pode adquirir essa informação na sessão DataFrame. Olha na tabela qual o nome, copia, e cola aqui')
            timeformat = st.selectbox('Sua data está em qual formato?', ['dia/mes/ano', 'dia/mes/ano hora/min/segudos'])
            if timeformat == 'dia/mes/ano hora/min/segudos':
                df[timecolumn] = pd.to_datetime(df[timecolumn], utc = True)
                df['date'] = df[timecolumn].dt.date

                temporal = df.groupby('date').date.agg('count').to_frame('total').reset_index().sort_values('total', ascending = False)
                st.text('Aqui estão as datas em função do número de ocorrência em ordem decrescente')
                st.write(temporal)
                st.text('Vamos ver isso num gráfico de tendência?')
                st.line_chart(temporal.rename(columns ={'date':'index'}).set_index('index'))

            elif timeformat == 'dia/mes/ano':
                df[timecolumn] = pd.to_datetime(df[timecolumn])
                df['date'] = df[timecolumn].dt.date

                temporal = df.groupby('date').date.agg('count').to_frame('total').reset_index().sort_values('total', ascending = False)
                st.text('Aqui estão as datas em função do número de ocorrência em ordem decrescente')
                st.write(temporal)
                st.text('Vamos ver isso num gráfico de tendência?')
                st.line_chart(temporal.rename(columns ={'date':'index'}).set_index('index'))
                
            timeanalysischeck = st.checkbox('Quero analisar os tweets com base na data de publicação para melhor entender o gráfico')
            if timeanalysischeck:
                timeday = st.selectbox('Tudo bem, selecione o dia de interesse', [range(1,31)])
                timemonth = st.selectkbox('Agora o mês', [range(1,12)])
                timeyear = st.text_input('Qual ano?')
                textimecolumn = st.text_input('Que coluna deseja analisar?')
                    
                df['year'] = df['timecolumn'].dt.year
                df['month'] = df['timecolumn'].dt.month
                df['day'] = df['timecolumn'].dt.day
                    
                nrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df)+1)
                   
                st.write(df[df['year'].str.contains(timeyear)][df['month'] == timemonth][df['day'] == timeday][textimecolumn].head(nrows))
                    



    
    if taskchoice == 'qualitativa':
        authorsname = df['author'].tolist()
        
        st.subheader('**Usuários que mais publicaram**')
        authorpostnumber = df['author'].value_counts()
        st.write(authorpostnumber)
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
        
        st.text('**Agora que sabe quem é que mais foi ativo(a) na conversação, escolha aquele(a) que deseja selecionar para analisar suas publicações.**')
        st.subheader('**Dataframe filtrado por usuário(a)**')
        authoroptions = st.selectbox('Qual autor deseja selecionar?', authorsname)
        df_author = df[df['author'].str.contains(authoroptions)]
        numberrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df_author)+1)
        df_author = df[df['author'].str.contains(authoroptions)].head(numberrows)
        st.write(df_author)
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')

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


#EXEMPLE WHEN NO FILE IS UPLOADED
else: 
    data = {'autor':['diego','clara','maria'],'publicacao':['2020-12-12T09:19:37+00:00','2021-01-24T09:19:37+00:00','2021-05-05T09:19:37+00:00'],
            'tweet':['amo vacinas!','vou me vacinar amanhã!','vovó se vacinou ontem, obrigada, SUS!'], 'likes':[100000,25000,895000],'retweets':[68500,25050,5876321]}
    df = pd.DataFrame.from_dict(data)


    #select the author to see their tweets
    taskchoice = st.selectbox('O que você quer fazer, analisar um relatório com os principais dados contidos no arquivo ou uma análise mais qualitativa?', ['relatório', 'qualitativa'])
    if taskchoice == 'relatório':
        st.subheader('**DataFrame**')
        st.write(df)
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
        
        st.subheader('**Descrição das tabelas contendo dados quantitativos (numéricos)**')
        st.write(df.describe())
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
        
        st.text('Será que existe alguma correlação (de Pearson) entre esses dados numéricos?')
        st.write(df.corr().round(1))
        st.write(df.corr().style.background_gradient(cmap='coolwarm'))
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
       
        timepossibility = st.selectbox('Seu DataFrame contém coluna de data? É possível fazer análise temporal com os dados que possui?', ['Não', 'Sim'])
        if timepossibility == 'Sim':
            timecolumn = st.text_input('Qual o nome da coluna? (Você pode adquirir essa informação na sessão DataFrame. Olha na tabela qual o nome, copia, e cola aqui')
            timeformat = st.selectbox('Sua data está em qual formato?', ['dia/mes/ano', 'dia/mes/ano hora/min/segudos'])
            if timeformat == 'dia/mes/ano hora/min/segudos':
                df[timecolumn] = pd.to_datetime(df[timecolumn], utc = True)
                df['date'] = df[timecolumn].dt.date

                temporal = df.groupby('date').date.agg('count').to_frame('total').reset_index().sort_values('total', ascending = False)
                st.text('Aqui estão as datas em função do número de ocorrência em ordem decrescente')
                st.write(temporal)
                st.text('Vamos ver isso num gráfico de tendência?')
                st.line_chart(temporal.rename(columns ={'date':'index'}).set_index('index'))

            elif timeformat == 'dia/mes/ano':
                df[timecolumn] = pd.to_datetime(df[timecolumn])
                df['date'] = df[timecolumn].dt.date

                temporal = df.groupby('date').date.agg('count').to_frame('total').reset_index().sort_values('total', ascending = False)
                st.text('Aqui estão as datas em função do número de ocorrência em ordem decrescente')
                st.write(temporal)
                st.text('Vamos ver isso num gráfico de tendência?')
                st.line_chart(temporal.rename(columns ={'date':'index'}).set_index('index'))



    
    if taskchoice == 'qualitativa':
        authorsname = df['autor'].tolist()
        
        st.subheader('**Usuários que mais publicaram**')
        authorpostnumber = df['autor'].value_counts()
        st.write(authorpostnumber)
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
       
        st.text('Agora que sabe quem é que mais foi ativo(a) na conversação, escolha ao lado aquele(a) que deseja selecionar para analisar suas publicações.')
        st.subheader('**Dataframe filtrado por usuário(a)**')
        authoroptions = st.selectbox('Qual autor deseja selecionar?', authorsname)
        df_author = df[df['autor'].str.contains(authoroptions)]
        numberrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df_author)+1)
        df_author = df[df['autor'].str.contains(authoroptions)].head(numberrows)
        st.write(df_author)
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')

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
                 
    



