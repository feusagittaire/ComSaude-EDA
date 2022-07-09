import numpy as np
import pandas as pd
import streamlit as st
import re
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


st.markdown('''
# **Vamos dar uma olhada mais aprofundada nos dados?**
Vejamos, selecione um arquivo para que possamos começar a análise.
''')


#uploud data
option = st.sidebar.selectbox('Selecione um formato', ('excel','csv'))
st.sidebar.write('Você selecionou:', option)
#pandas profiling report

with st.sidebar.header('Suba o arquivo'):
    uplouded_file = st.sidebar.file_uploader("Escolha o arquivo")
    


if uplouded_file is not None:
    
    
    if option == 'excel':

        @st.cache(allow_output_mutation=True)
        def load_data(uplouded_file):
            data = pd.read_excel(uplouded_file, engine = 'openpyxl')
            return data
        
    
    else:
        @st.cache(allow_output_mutation=True)
        def load_data(uplouded_file):
            data = pd.read_csv(uplouded_file)
            return data

    data_load_state = st.text('Carregando arquivo...')
    df = load_data(uplouded_file)
    data_load_state = st.text('Eitchan, carregamento conluido!')
    stop_words = stopwords.words('portuguese')

    #select the author to see their tweets
    taskchoice = st.selectbox('O que você quer fazer, analisar um relatório com os principais dados contidos no arquivo ou uma análise mais qualitativa?', ['relatório', 'qualitativa'])
    if taskchoice == 'relatório':
        st.subheader('**DataFrame**')
        st.write(df)
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
      
        st.subheader('**Descrição das tabelas contendo dados quantitativos (numéricos)**')
        st.write(df.describe().applymap("{0:.2f}".format))
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
        
        st.text('Será que existe alguma correlação (de Pearson) entre esses dados numéricos?')
        st.write(df.corr().round(1))
        st.write(df.corr().style.background_gradient(cmap='coolwarm'))
       
    #QUALITATIVE ANALYSIS   
    
    if taskchoice == 'qualitativa':
        st.write(df.head(1))
        
        #Assigning text column name and author column name variables
        #Streamlit forms
        
        with st.form('text and autor'):
            col1,col2 =  st.columns(2)
            textchoosen = col1.text_input('Qual coluna de texto deseja analisar?')
            author_column_name = col2.text_input('Copie e cole o nome da coluna que contém os nomes dos usuários')
            submitted = st.form_submit_button(label = 'Enviar')
        
        if submitted:
            if author_column_name:
                authorsname = df[author_column_name].tolist()
                st.subheader('**Usuários que mais publicaram**')
                authorpostnumber = df[author_column_name].value_counts()
                st.write(authorpostnumber)
            else: 
                st.warning('Copie e cole o nome da coluna na qual os nomes dos(as) usuários(as) fazem-se presente')


            st.subheader('**Quem mais foi mencionado**')
            if textchoosen:
                df['mentioned'] = df[textchoosen].apply(lambda x: re.findall(r'\@[\w\d]*(?=\s)',x))
                mentions = df.explode('mentioned')
                st.write(mentions.value_counts('mentioned'))
            else:
                st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

            st.subheader('**Principais hashtags**')
            if textchoosen:
                df['hashtags'] = df[textchoosen].apply(lambda x: re.findall(r'\#[\w\d]*(?=\s)',x))
                hashtags = df.explode('hashtags')
                st.write(hashtags.value_counts('hashtags'))
                if len(hashtags.value_counts('hashtags')) < 1:
                    st.write('Oh, parece que hashtags não foram usadas como ferramenta extra-textual na conversação que está a analisar')
            else:
                st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

            st.subheader('**Principais links**')
            if textchoosen:
                df['links'] = df[textchoosen].apply(lambda x: re.findall(r'http[\w\d:/]*(?=\s)',x))
                links = df.explode('links')
                st.write(links.value_counts('links'))
                if len(links.value_counts('links')) < 1:
                    st.write('Oh, parece que links não foram usados como ferramenta extra-textual na conversação que está a analisar')
            else:
                st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

            #TIMELINE ANALYSIS
            time_data_disponible = st.selectbox('Seu DataFrame contém coluna de data? É possível fazer análise temporal com os dados que possui?', ['Não', 'Sim'])
            if time_data_disponible == 'Sim':
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

                        timeday = st.text_input('Digite um dia (número sem zero. Ex: 1,2,3,4,...,12)')
                        timemonth = st.text_input('Agora o mês (número. Ex: 1,2,3,4,...,12)')
                        timeyear = st.text_input('Qual ano?')
                        textimecolumn = st.text_input('Que coluna deseja analisar?')

                        df['year'] = df[timecolumn].dt.year
                        df['month'] = df[timecolumn].dt.month
                        df['day'] = df[timecolumn].dt.day

                        if timeday == '':
                            st.text('Esperando você preencher os dados')
                        else:
                            nrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df)+1)
                            time_analysis_output = df.query(f"year == {timeyear}").query(f"month == {timemonth}")\
                                .query(f"day == {timeday}")[textimecolumn].drop_duplicates().dropna().head(nrows).tolist()


                            st.write(time_analysis_output)

                            #Visualize wordcloud if there's enough text input
                            if nrows > 20:
                                fig,ax = plt.subplots(figsize = (17,7))
                                word_cloud = WordCloud(stopwords = set(stop_words + ['t','co','https','sobre','vacina','covid'])).generate(' '.join(time_analysis_output))
                                ax.imshow(word_cloud, interpolation = 'bilinear')
                                plt.axis('off')
                                st.pyplot(fig)

            st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
            st.header('**Dataframe filtrado por usuário(a)/menção/hashtags/links**')

        

            st.subheader('***Usuário(a)***')

            authoroptions = st.selectbox('Qual deseja selecionar?', df[author_column_name].tolist())
            df_author = df[df[author_column_name].str.contains(authoroptions)]
            numberrows_user = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df_author)+1)
            df_author = df[df[author_column_name].str.contains(authoroptions)].head(numberrows_user)
            st.write(df_author)
            st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')

            if len(mentions.value_counts('mentioned')) > 1:
                mentions_names = mentions.explode('mentioned')['mentioned'].dropna().drop_duplicates().tolist()
                st.subheader('***Menção***')
                mentions_options = st.selectbox('Qual deseja selecionar?', mentions_names)
                df_mentions = mentions.dropna(subset = ['mentioned']).drop_duplicates('mentioned')[mentions['mentioned'].dropna().drop_duplicates().str.contains(mentions_options)]
                numberrows_mentions = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(mentions_names)+1)
                st.write(df_mentions.head(numberrows_mentions))
                st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')



        

        columns = df_author.columns
        columnpreference = st.checkbox('Seus dados estão classificados?')

        if columnpreference:
                columnchoosen = st.selectbox('Com base em que coluna você deseja que os textos sejam filtrados?', columns)
                textcontent = st.selectbox('Você tem interesse em ver os tweets do(a) usuário(a) selecionado(a) ou os tweets de todos(as) aqueles(as) que se enquadram na categoria/classe escolhida?', ['usuário','categoria'])

                if textcontent == 'usuário':
                    st.markdown('''
                                Tudo bem, você deseja entender qual a relação dos outros dados analíticos à sua disposição com os tweets que o(a) usuário(a) em questão publicou/compartilhou''')
                    columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse')

                    if textchoosen == '':
                        st.text('Esperando você escrever o nome da coluna de texto!')
                    else: 
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df_author[textchoosen].head(numberrows_user).tolist()
                        st.write(tweet)

                else:
                    columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse:')
                    numberrows_class = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df[df[columnchoosen].str.contains(columnvalue)])+1)

                    if textchoosen == '':
                        st.text('Esperando você escrever o nome da coluna de texto!')
                    else: 
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df_author[textchoosen].head(numberrows).tolist()
                        st.write(tweet)
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        tweet = df[df[columnchoosen].str.contains(columnvalue)][textchoosen].head(numberrows_class).tolist()
                        st.write(tweet)

        else:
            if textchoosen == '':
                st.text('Esperando você escrever o nome da coluna de texto!')
            else: 
                st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                analysis_choice = st.selectbox('Quer ver a relação de tweets com base em que?', ['usuário(a)', 'menção'])
                if analysis_choice == 'menção':
                    tweet = df_mentions[df_mentions['mentioned'].str.contains(mentions_options)][textchoosen].head(numberrows_mentions).tolist()
                    st.write(tweet)
                elif analysis_choice == 'usuário(a)':
                    tweet = df_author[textchoosen].head(numberrows_user).tolist()
                    st.write(tweet)



    else: 
                st.warning('Copie e cole o nome da coluna que contém os tweets e aquela onde se localizam os nomes dos usuários')


#EXEMPLE WHEN NO FILE IS UPLOADED
else: 
    data = {'autor':['diego','maria','maria', 'carla'],'publicacao':['2020-12-12T09:19:37+00:00','2021-01-24T09:19:37+00:00','2021-05-05T09:19:37+00:00','2021-05-05T09:19:37+00:00'],
            'tweet':['@minsaude cadê as vacinas?','@prefeitura como vai funcionar a vacinação de idosos essa semana?','vovó se vacinou ontem, obrigada, @SUS!', '@jairbolsonaro cansada de tanta desinformação! As vacinas não têm qualquer relação com o HIV!'], 'menção': ['minsaude', 'prefeitura', 'SUS', 'jairbolsonaro'], 'likes':[100000,25000,895000, 5584266],'retweets':[68500,25050,5876321, 54215452]}
    df = pd.DataFrame.from_dict(data)


    #select the author to see their tweets
    taskchoice = st.selectbox('O que você quer fazer, analisar um relatório com os principais dados contidos no arquivo ou uma análise mais qualitativa?', ['relatório', 'qualitativa'])
    if taskchoice == 'relatório':
        st.subheader('**DataFrame**')
        st.write(df)
        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
        
        st.subheader('**Descrição das tabelas contendo dados quantitativos (numéricos)**')
        st.write(df.describe().applymap("{0:.2f}".format))
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
                    
                    
                timeanalysischeck = st.checkbox('Quero analisar os tweets com base na data de publicação para melhor entender o gráfico')
                if timeanalysischeck:

                    timeday = st.text_input('Digite um dia (número)')
                    timemonth = st.text_input('Agora o mês (número. Ex: 1,2,3,4,...,12')
                    timeyear = st.text_input('Qual ano?')
                    textimecolumn = st.text_input('Que coluna deseja analisar?')

                    df['year'] = df[timecolumn].dt.year
                    df['month'] = df[timecolumn].dt.month
                    df['day'] = df[timecolumn].dt.day
                    if timeday == '':
                        st.text('Esperando você preencher os dados')
                    else:
                        nrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df)+1)

                        st.write(df.query(f"year == {timeyear}").query(f"month == {timemonth}").query(f"day == {timeday}")[textimecolumn].head(nrows).tolist())    
               


    
    if taskchoice == 'qualitativa':
        textchoosen = st.text_input('Qual coluna de texto deseja analisar?')
        authorsname = df['autor'].tolist()
        
        st.subheader('**Usuários que mais publicaram**')
        authorpostnumber = df['autor'].value_counts()
        st.write(authorpostnumber)

        
        st.subheader('**Quem mais foi mencionado**')
        if textchoosen:
            df['mentioned'] = df[textchoosen].apply(lambda x: re.findall(r'\@[\w\d]*(?=\s)',x))
            mentions = df.explode('mentioned')
            st.write(mentions.value_counts('mentioned'))
        else:
            st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

        st.subheader('**Principais hashtags**')
        if textchoosen:
            df['hashtags'] = df[textchoosen].apply(lambda x: re.findall(r'\#[\w\d]*(?=\s)',x))
            hashtags = df.explode('hashtags')
            st.write(hashtags.value_counts('hashtags'))
            if len(hashtags.value_counts('hashtags')) < 1:
                st.write('Oh, parece que hashtags não foram usadas como ferramenta extra-textual na conversação que está a analisar')
        else:
            st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

        st.subheader('**Principais links**')
        if textchoosen:
            df['links'] = df[textchoosen].apply(lambda x: re.findall(r'http[\w\d:/]*(?=\s)',x))
            links = df.explode('links')
            st.write(links.value_counts('links'))
            if len(links.value_counts('links')) < 1:
                st.write('Oh, parece que links não foram usados como ferramenta extra-textual na conversação que está a analisar')
        else:
            st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

        st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')
        st.header('**Dataframe filtrado por usuário(a)/menção/hashtags/links**')

        

        if textchoosen:

            st.subheader('***Usuário(a)***')

            authoroptions = st.selectbox('Qual deseja selecionar?', authorsname)
            df_author = df[df['autor'].str.contains(authoroptions)]
            numberrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df_author)+1)
            df_author = df[df['autor'].str.contains(authoroptions)].head(numberrows)
            st.write(df_author)
            st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')

            if len(mentions.value_counts('mentioned')) > 1:
                mentions_names = mentions.explode('mentioned')['mentioned'].dropna().drop_duplicates().tolist()
                st.subheader('***Menção***')
                mentions_options = st.selectbox('Qual deseja selecionar?', mentions_names)
                df_mentions = mentions.dropna().drop_duplicates()[mentions['mentioned'].dropna().drop_duplicates().str.contains(mentions_options)]
                numberrows_mentions = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(mentions_names)+1)
                st.write(df_mentions.head(numberrows_mentions))
                st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')

           

            
                

            columns = df_author.columns
            columnpreference = st.checkbox('Seus dados estão classificados?')
                
            if columnpreference:
                columnchoosen = st.selectbox('Com base em que coluna você deseja que os textos sejam filtrados?', columns)
                textcontent = st.selectbox('Você tem interesse em ver os tweets do(a) usuário(a) selecionado(a) ou os tweets de todos(as) aqueles(as) que se enquadram na categoria/classe escolhida?', ['usuário','categoria'])

                if textcontent == 'usuário':
                    st.markdown('''
                        Tudo bem, você deseja entender qual a relação dos outros dados analíticos à sua disposição com os tweets que o(a) usuário(a) em questão publicou/compartilhou''')
                    columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse')
                
                    if textchoosen == '':
                            st.text('Esperando você escrever o nome da coluna de texto!')
                    else: 
                            st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                            tweet = df_author[textchoosen].head(numberrows).tolist()
                            st.write(tweet)
                        
                else:
                        columnvalue = st.text_input('Escreva qual o nome da classe/categoria de interesse:')
                        numberrows = st.slider('Selecione a quantidade de dados que deseja ver:', min_value = 1, max_value=len(df[df[columnchoosen].str.contains(columnvalue)])+1)
                        
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
                    
                if textchoosen == '':
                        st.text('Esperando você escrever o nome da coluna de texto!')
                else: 
                        st.markdown('**INFO** Os tweets serão apresentados em formato de lista, de texto corrido, cada linha respresentará o tweet diferente!')
                        analysis_choice = st.selectbox('Quer ver a relação de tweets com base em que?', ['usuário(a)', 'menção'])
                        if analysis_choice == 'menção':
                            tweet = df_mentions[df_mentions['mentioned'].str.contains(mentions_options)][textchoosen].head(numberrows_mentions).tolist()
                            st.write(tweet)
                        elif analysis_choice == 'usuário(a)':
                            tweet = df_author[textchoosen].head(numberrows).tolist()
                            st.write(tweet)
            
            

        else: 
            st.warning('Copie e cole o nome da coluna de texto')
    



