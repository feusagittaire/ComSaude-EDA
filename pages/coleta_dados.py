import numpy as np
import pandas as pd
import streamlit as st
import time
import snscrape.modules.twitter as sntwitter
import itertools
import unicodedata
import re
from wordcloud import WordCloud
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from profileclassifier import nlpclassifier_profilener
import io
import networkx as nx
import streamlit.components.v1 as components
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation


stop = stopwords.words('portuguese')
novos = ['vc','pra','vai','usa','faz','pq','ainda','sobre','ta','porque','assim',
         'agora','pois','nao','so','pl','news','fake','contra','fakenews','ai','que','de', 'das','dos','da',
         'do','por','isso','em','para','no','na','se','uma','um','com','esta','essa',
         'esse','ser','tem','nem','ele','ela','como','mas','mais','os','as','ao','sao','eu','ja','ou']
for word in novos:
    stop.append(word)

def strip_accents(text):
  text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
  return str(text)

def preprocess(text, lower = False):
  text = text.replace('http ','https//')
  text = re.sub('https.\S*', '', str(text)) #remove urls
  text = text.replace('\n','')
  text = re.sub('\@\S*', '', text) #remove menções
  text = re.sub('\#\S*', '', text) #remove hashtags
  text = re.sub('[0-9]','',text) #remove numbers
  text = re.sub('_+','',text)
  text = re.sub('[^\w\s]','',text) #remove everything except strings and scape - just to make sure
  text = text.strip(' ')
  
 
  if lower:
    text = text.lower() 
  return text

def removeStopWords(text, stop = []):
  words = [word for word in text.split() if word not in stop]
  sentence = ' '.join(words)
  return sentence

def wordcloud(text, stop = []):
  wordcloud = WordCloud(
      stopwords = stop,
      width = 4000,
      height = 3000,
      max_words =1000,
      background_color= 'white',
      colormap = cm.magma).generate(str(text))
  fig = plt.figure(
      figsize = (17, 7))
  plt.imshow(wordcloud, interpolation = 'bilinear')
  plt.axis('off')
  plt.tight_layout(pad=0)
  plt.show()


def basic_text(text, stop):
  text = preprocess(text, lower = True)
  text = strip_accents(text)
  stop = [strip_accents(word) for word in stop]
  #text = re.sub('[^\w\s]','', text)
  words = text.split()
  result = [word for word in words if word not in stop]
  return ' '.join(result)

def get_ngrams(serie,ngram_from:int = 1, ngram_to:int = 1, n:int = 20):
    doc = serie.apply(lambda x: basic_text(str(x), stop = stop))
    cv = CountVectorizer(stop_words=stop, ngram_range=(ngram_from,ngram_to)).fit(doc)
    bow = cv.transform(doc)
    sum_words = bow.sum(axis=0)
    words_freq = [(word,sum_words[0,i]) for word,i in cv.vocabulary_.items()]
    words_freq = sorted(words_freq, key= lambda x: x[1], reverse= True)
    
    return words_freq[:n]

# Inspect topics
def describe_topics(lda, feature_names, top_n_words=5, show_weight=False):
    """Print top n words for each topic from lda model."""
    feature_names = feature_names
    normalised_weights = lda.components_ / lda.components_.sum(axis=1)[:, np.newaxis]
    for i, weights in enumerate(normalised_weights):
      st.write(f"********** Topic {i} **********")
      if show_weight:
          feature_weights = [*zip(np.round(weights, 4), feature_names)]
          feature_weights.sort(reverse=True)
          st.write(feature_weights[:top_n_words], '\n')
      else:
          top_words = [feature_names[i] for i in weights.argsort()[:-top_n_words-1:-1]]
          st.write(top_words, '\n')



@st.cache          
def scraper(n:int=80000):
   df = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
        query).get_items(),n))
   return df
###################################################################################3

dataset = st.selectbox('Você já tem um dataset?', ('Escolha','sim','não'))
if dataset == 'sim':
#uploud data
    option = st.sidebar.selectbox('Selecione um formato', ('Escolha','csv','excel'))
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
data_load_state = st.text('Carregamento conluido! (using st.cache)')

    

else:

    st.sidebar.title('Vamos começar!')
    scraping = st.sidebar.selectbox('De qual mídia deseja extrair dados?',['Twitter (snscrape)','Midia jornalística'])


    if scraping == 'Twitter (snscrape)':
        extracted_tweets = []

        extracted_tweets = []
        term = st.sidebar.text_input('Qual o descritor?')
        lang = st.sidebar.text_input('Qual a língua (e.g pt, en, etc)?')
        choice = st.sidebar.selectbox('Você quer fazer análise temporal?', ['Escolha','Sim','Não'])
        if choice == 'Sim':
            st.sidebar.text('Formato = ano-mês-dia')
            data_inicio = st.sidebar.text_input('Data inicial')
            data_fim = st.sidebar.text_input('Data final')
            query = f'{term} lang:{lang} until:{data_fim} since:{data_inicio}'
            st.sidebar.text(query)

        else:
            query = f"{term} lang:{lang}"

        stop_query = query.split(' ')
        for word in stop_query:
            stop.append(word)

        if lang:
            if query is not None:
                try:
                    df = scraper()
                except:
                    time.sleep(0.5)
                    df = scraper()
                        #df = df[df['content'].str.contains(f'{term}')]
                        #st.dataframe(df)
        else:
            pass

        
st.title('Resultados')
st.markdown(f"**:red[\nTweet mais retuitado:]** {df.sort_values('retweetCount', ascending = False).head(1)['rawContent'].tolist()}")
st.markdown(f"**:red[\nTweet mais visto:]** {df.sort_values('viewCount', ascending = False).head(1)['rawContent'].tolist()}")
st.dataframe(df)

download = st.selectbox('Deseja baixar o dataframe em formato excel?', ['Escolha', 'Sim','Não'])
if download == 'Sim':
         df['date'] = pd.to_datetime(df['date'])
         df['date'] = df['date'].dt.date
         buffer = io.BytesIO()
         with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                  df.to_excel(writer, sheet_name='Sheet1', index=False)
                         # Close the Pandas Excel writer and output the Excel file to the buffer
                  writer.save()
         
                  download2 = st.download_button(
                                                 label="Download dados como Excel",
                                                 data=buffer,
                                                 file_name='resultados oaps.xlsx',
                                                 mime='application/vnd.ms-excel'
                )
        
st.subheader('Análise temporal')
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].dt.date
temporal = df.groupby('date').date.agg('count').to_frame('total').reset_index()
st.line_chart(data = temporal, x = 'date', y = 'total')

st.subheader('Frequência de palavras')
st.markdown(get_ngrams(df['rawContent'], ngram_from = 1, ngram_to = 1,n= 20))

ngram = get_ngrams(df['rawContent'], ngram_from = 1, ngram_to = 1,n= 20)
df_ngram = {'word':[],'freq':[]}
for x in ngram:
    df_ngram['word'].append(x[0])
    df_ngram['freq'].append(x[1])

df_ngram = pd.DataFrame.from_dict(df_ngram, orient= 'index')
df_ngram = df_ngram.transpose()

st.bar_chart(df_ngram, x = 'word',y = 'freq')
#df['user'] = df['user'].apply(lambda x: str(x).replace(r"\,\'id.*", '')).apply(lambda x: x.replace(r"\{\'username\'\:",'')).apply(lambda x: x.replace(r"\'",''))
textchoosen = st.text_input('Qual coluna de texto deseja analisar?')
authorsname = df['user'].tolist()

st.subheader('**Usuários que mais publicaram**')
authorpostnumber = df['user'].value_counts()
st.write(authorpostnumber)

df_copy = df.copy()
st.subheader('**Quem mais foi mencionado**')
if textchoosen:
    df_copy['mentioned'] = df_copy[textchoosen].apply(lambda x: re.findall(r'\@[\w\d]*(?=\s)',x))
    mentions = df_copy.explode('mentioned')
    st.write(mentions.value_counts('mentioned'))
else:
    st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

st.subheader('**Principais hashtags**')
if textchoosen:
    df_copy['hashtags'] = df_copy[textchoosen].apply(lambda x: re.findall(r'\#[\w\d]*(?=\s)',x))
    hashtags = df_copy.explode('hashtags')
    st.write(hashtags.value_counts('hashtags'))
if len(hashtags.value_counts('hashtags')) < 1:
    st.write('Oh, parece que hashtags não foram usadas como ferramenta extra-textual na conversação que está a analisar')
else:
    st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

st.subheader('**Principais links**')
if textchoosen:
    df_copy['links'] = df_copy[textchoosen].apply(lambda x: re.findall(r'http[\w\d:/]*(?=\s)',x))
    links = df_copy.explode('links')
    st.write(links.value_counts('links'))
if len(links.value_counts('links')) < 1:
    st.write('Oh, parece que links não foram usados como ferramenta extra-textual na conversação que está a analisar')
else:
    st.warning('Copie e cole o nome da coluna de texto na qual menções fazem-se presente')

st.text('━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━━◦○◦━◦○◦━')

st.subheader('Entidades Mencionadas')

@st.cache
def ner():
    nlpc = nlpclassifier_profilener.NLPClassifier('ner')
    nlp = nlpc.nlp()
    df['processed'] = df['rawContent'].apply(lambda x: preprocess(str(x), lower = True)).apply(lambda x: strip_accents(str(x)))
    df['tokens'] = df['processed'].apply(lambda x: nlp(str(x)))
    df['ner'] = df['tokens'].apply(lambda x: nlpc.ner_en(x))
    ner = nlpc.get_ner_en(df)
    return ner

load_ner = st.checkbox('Carregar dados')
if load_ner:
    ner = ner()
    col1, col2 = st.columns(2)
    col1.bar_chart(ner['ner'].value_counts().to_frame('total'), y ='total')

    entidade = st.text_input('Qual entidade gostaria de ve no gráfico de frequencias das entidades?')
if entidade:
    col2.bar_chart(ner[ner['ner'] == f'{entidade}']['tokens'].value_counts().to_frame('total'), y ='total')

st.subheader('Explorar o conteúdo')
filtro = st.text_input('Qual termo quer buscar? (filtro de tweets que o contenham)')
df['processed'] = df['rawContent'].apply(lambda x: preprocess(str(x)))
st.write(df[df['rawContent'].str.contains(f'{filtro}')].drop_duplicates('processed')['rawContent'].tolist())

st.subheader('Modelagem de Tópicos (LDA)')
load_lda = st.checkbox('Carregar tópicos')
#Inicializar a sessão
if load_lda:
    @st.cache
    def topic_modeling(df):
        doc = df['rawContent'].apply(lambda x: preprocess(str(x), lower = True)).apply(lambda x: strip_accents(x)).apply(lambda x: removeStopWords(x,novos))
        #stop_en = set(stopwords.words('english'))
        #stop_pt = stopwords.words('portuguese')
        #stop_esp = set(stopwords.words('spanish'))
        #stop = stop_en.union(stop_esp).union(novos)
        tfidf = TfidfVectorizer(stop_words= novos, min_df = 2)
        document_term_matrix = tfidf.fit_transform(doc) #bag-of-words

        # Init the Model
        lda = LatentDirichletAllocation(n_components = 5, max_iter= 200, verbose=1, random_state=1)


        # Do the Grid Search
        lda.fit(document_term_matrix)

        # Create Document - Topic Matrix
        lda_output = lda.transform(document_term_matrix)

        feature_names = tfidf.get_feature_names_out()
        #print(describe_topics(lda, feature_names, show_weight=False))
        lda_output = lda.transform(document_term_matrix)

        # column names
        topicnames = ["Topic" + str(i) for i in range(lda.n_components)]

        # index names
        docnames = [i for i in range(len(df))]

        # Make the pandas dataframe
        df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)

        # Get dominant topic for each document
        dominant_topic = np.argmax(df_document_topic.values, axis=1)
        df_document_topic['dominant_topic'] = dominant_topic
        #st.dataframe(df_document_topic)
        df_topic_distribution = df_document_topic['dominant_topic'].value_counts().reset_index(name="Num Documents")
        df_topic_distribution.columns = ['Topic Num', 'Num Documents']
        #df_document_topic = df_topic_distribution.reset_index()
        df_document_topic['index'] = df_document_topic.index


        df = df.reset_index()
        df['index'] = df.index

        df_ = df.merge(df_document_topic, on = 'index', how = 'right' )
        df_topic_distribution = df_topic_distribution.rename(columns = {'Topic Num': 'dominant_topic'})
        df_ = df_.merge(df_topic_distribution, on= 'dominant_topic', how = 'right')
        return lda, feature_names, df_document_topic, df_ 

lda, feature_names, df_document_topic, df = topic_modeling(df)

print(describe_topics(lda, feature_names, show_weight=False))

#plot bar chart topics frequency
if lda:
    topic_frequency= df.groupby('dominant_topic').dominant_topic.agg('count').to_frame('total').reset_index()
    st.bar_chart(data= topic_frequency.sort_values('total', ascending = True),x= 'dominant_topic',y = 'total')


    load_explorar = st.checkbox('Quer investigar de que maneira algum dos termos dos tópicos foram acionados nos tweets?')
    st.dataframe(df)
if load_explorar:
    topico = st.text_input('Qual tópico deseja filtrar?')
    df['dominant_topic'] = df['dominant_topic'].astype(str)
    res = df[df['dominant_topic'] == topico]['rawContent'].tolist()
    text = ''
for tweet in res:
    tweet = basic_text(tweet, stop)
    text += ' '+tweet

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(fig = wordcloud(text, stop = stop))

st.write(res) 
#st.write(explore_topics(i))


st.subheader('Análise de Redes')
choice = st.selectbox('Deseja realizar análise de rede?', ['Escolha','Sim','Não'])
if choice == 'Sim':

    df['author'] = df['user'].apply(lambda x: re.sub('\,.*','',str(x))).apply(lambda x: re.sub('.*: ','',str(x))).apply(lambda x: x.strip())
    df['target'] = df['inReplyToUser'].apply(lambda x: re.sub('\,.*','',str(x))).apply(lambda x: re.sub('.*: ','',str(x))).apply(lambda x: x.strip())
    edgeslist = []
    source= df['author'].apply(lambda x: re.sub("\'",'',str(x))).tolist()
    target = df['target'].apply(lambda x: re.sub("\'",'',str(x))).tolist()
    df = df.dropna(subset = ['author'])
    for i in range(len(df)):
        edgeslist.append((source[i], target[i]))

    edgeslist_df = pd.DataFrame(edgeslist, columns = ['Source','Target'])
    labels = edgeslist_df['Target'].value_counts().head(10).to_frame('total').reset_index()
    labels = labels['index'][1:].tolist()



    g = nx.DiGraph()

    g.add_edges_from(edgeslist)

    labels_ = {}
    for node in g.nodes():
             if node in labels:
                      #set the node name as the key and the label as its value 
                      labels_[node.replace('"','')] = node
                      labels_

    d = nx.degree(g)
    val = [val for (node, val) in g.degree()]

    fig, ax = plt.subplots()
    #pos = nx.kamada_kawai_layout(g4)
    nx.draw_spring(g,with_labels=True, labels = labels_,nodelist= [node for (node, val) in g.degree()], node_size=[v * 50 for v in val])
    st.pyplot(fig)

    download_nx = st.selectbox('Deseja baixar a rede em formato excel?', ['Escolha', 'Sim','Não'])
    if download_nx == 'Sim':

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            edgeslist_df.to_excel(writer, sheet_name='Sheet1', index=False)
            # Close the Pandas Excel writer and output the Excel file to the buffer
            writer.save()

            download_nx = st.download_button(
            label="Download redes como Excel",
            data=buffer,
            file_name='redes oaps.xlsx',
            mime='application/vnd.ms-excel')
