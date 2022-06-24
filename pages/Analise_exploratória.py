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
            if timecolumn == '':
                st.text('Esperando você escrever o nome da coluna que contém as datas')
            else: 
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

                    timeday = st.text_input('Digite um dia (número)')
                    timemonth = st.text_input('Agora o mês')
                    timeyear = st.text_input('Qual ano?')
                    textimecolumn = st.text_input('Que coluna deseja analisar?')

                    df['year'] = df[timecolumn].dt.year
                    df['month'] = df[timecolumn].dt.month
                    df['day'] = df[timecolumn].dt.day
                    if timeday is not None:  
                        nrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df)+1)

                        st.write(df.query(f"year == {timeyear}").query(f"month == {timemonth}").query(f"day == {timeday}")[textimecolumn].head(nrows).tolist())
                    



    
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
            
            **Vamos nos aprofundar nesses dados!!**
            Veja como:
            
            Ex: Se estou analisando tweets em que usuários(as) citaram alguém, e eu tenho uma coluna que indica a menção.''')
            
            st.image('https://i.ibb.co/m4vy2Vg/demonstacaotabelastreamlit.png')
             
            st.markdown('''
            Até aqui, foi possível analisar tweets de uma maneira geral, **mas e se a usuária 1 (aquela que escolhi analisar anteriormente) fez menção à mais de uma pessoa?** Se eu quiser analisar 
            os tweets que ela fez menção à uma pessoa específica, em "Escreva qual o nome da classe/categoria" vou escrever a coluna "Menções", que é a que contem as categorias de interesse analítico.
            Em "qual coluna de texto", você vai colocar "Tweets". Nesse caso, só existe uma coluna contendo texto, mas poderiam haver outras.  
            
            No caso da análise da categoria, **você vai colocar o nome da classe/categoria que quer analisar**. Ou seja, A coluna é Menções, e quero analisar todos os tweets que fizeram menção à Atila.
            Logo, na área de especificação da categoria de interesse, vou colocar Atila, ou Atila Lamarino, ou Lamarino. 
            Em "qual coluna de texto", você vai colocar "Tweets". Nesse caso, só existe uma coluna contendo texto, mas poderiam haver outras. 
            
            
            ''')

            columns = df_author.columns
            columnpreference = st.checkbox('Seus dados estão classificados?')
            
            if columnpreference:
                columnchoosen = st.selectbox('Com base em que coluna você deseja que os textos sejam filtrados?', columns)
                textcontent = st.selectbox('Você tem interesse em ver os tweets do(a) usuário(a) selecionado(a) ou os tweets de todos(as) aqueles(as) que se enquadram na categoria/classe escolhida?', ['usuário','categoria'])
                
                if textcontent == 'usuário':
                    st.markdown('''
                    Tudo bem, você deseja entender qual a relação dos outros dados analíticos à sua disposição com os tweets que o(a) usuário(a) em questão publicou/compartilhou''')
                    columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse')
                    textchoosen = st.text_input('Qual coluna de texto quero analisar?')
                    if textchoosen == '':
                        st.text('Esperando você escrever o nome da coluna de texto!')
                    else: 
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df_author[textchoosen].head(numberrows).tolist()
                        st.write(tweet)
                    
                else:
                    columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse:')
                    numberrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df[df[columnchoosen].str.contains(columnvalue)])+1)
                    textchoosen = st.text_input('Qual coluna de texto quero analisar?')
                    if textchoosen == '':
                        st.text('Esperando você escrever o nome da coluna de texto!')
                    else: 
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df_author[textchoosen].head(numberrows).tolist()
                        st.write(tweet)
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df[df[columnchoosen].str.contains(columnvalue)][textchoosen].head(numberrows).tolist()
                        st.write(tweet)

            else:
                textchoosen = st.text_input('Qual coluna de texto quero analisar?')
                if textchoosen == '':
                    st.text('Esperando você escrever o nome da coluna de texto!')
                else: 
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
            if timecolumn == '':
                st.text('Esperando você escrever o nome da coluna que contém as datas')
            else: 
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

        analysetext = st.checkbox('Tudo bem, agora quero analisar os tweets!')
        
        if analysetext:
            st.markdown('''
            
            **Vamos nos aprofundar nesses dados!!**
            Veja como:
            
            Ex: Se estou analisando tweets em que usuários(as) citaram alguém, e eu tenho uma coluna que indica a menção.''')
            
            st.image('https://i.ibb.co/m4vy2Vg/demonstacaotabelastreamlit.png')
             
            st.markdown('''
            Até aqui, foi possível analisar tweets de uma maneira geral, **mas e se a usuária 1 (aquela que escolhi analisar anteriormente) fez menção à mais de uma pessoa?** Se eu quiser analisar 
            os tweets que ela fez menção à uma pessoa específica, em "Escreva qual o nome da classe/categoria" vou escrever a coluna "Menções", que é a que contem as categorias de interesse analítico.
            Em "qual coluna de texto", você vai colocar "Tweets". Nesse caso, só existe uma coluna contendo texto, mas poderiam haver outras.  
            
            No caso da análise da categoria, **você vai colocar o nome da classe/categoria que quer analisar**. Ou seja, A coluna é Menções, e quero analisar todos os tweets que fizeram menção à Atila.
            Logo, na área de especificação da categoria de interesse, vou colocar Atila, ou Atila Lamarino, ou Lamarino. 
            Em "qual coluna de texto", você vai colocar "Tweets". Nesse caso, só existe uma coluna contendo texto, mas poderiam haver outras. 
            
            
            ''')

            columns = df_author.columns
            columnpreference = st.checkbox('Seus dados estão classificados?')
            
            if columnpreference:
                columnchoosen = st.selectbox('Com base em que coluna você deseja que os textos sejam filtrados?', columns)
                textcontent = st.selectbox('Você tem interesse em ver os tweets do(a) usuário(a) selecionado(a) ou os tweets de todos(as) aqueles(as) que se enquadram na categoria/classe escolhida?', ['usuário','categoria'])
                
                if textcontent == 'usuário':
                    st.markdown('''
                    Tudo bem, você deseja entender qual a relação dos outros dados analíticos à sua disposição com os tweets que o(a) usuário(a) em questão publicou/compartilhou''')
                    columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse')
                    textchoosen = st.text_input('Qual coluna de texto quero analisar?')
                    if textchoosen == '':
                        st.text('Esperando você escrever o nome da coluna de texto!')
                    else: 
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df_author[textchoosen].head(numberrows).tolist()
                        st.write(tweet)
                    
                else:
                    columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse:')
                    numberrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df[df[columnchoosen].str.contains(columnvalue)])+1)
                    textchoosen = st.text_input('Qual coluna de texto quero analisar?')
                    if textchoosen == '':
                        st.text('Esperando você escrever o nome da coluna de texto!')
                    else: 
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df_author[textchoosen].head(numberrows).tolist()
                        st.write(tweet)
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df[df[columnchoosen].str.contains(columnvalue)][textchoosen].head(numberrows).tolist()
                        st.write(tweet)

            else:
                textchoosen = st.text_input('Qual coluna de texto quero analisar?')
                if textchoosen == '':
                    st.text('Esperando você escrever o nome da coluna de texto!')
                else: 
                    st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                    tweet = df_author[textchoosen].head(numberrows).tolist()
                    st.write(tweet)

    



