import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import ast
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
import surprise
import MySQLdb

# Data Source: https://www.kaggle.com/rounakbanik/the-movies-dataset/data
# Reference: https://www.datacamp.com/community/tutorials/recommender-systems-python
def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words

# display function credit: Mohtadi Ben Fraj
def display_posters(df):
    poster_html = ''
    for ref in df.poster_path:
            if ref != '':
                link = 'http://image.tmdb.org/t/p/w185/' + ref
                poster_html += "<img style='width: 120px; margin: 0px; \
                  float: left; border: 1px solid black;' src='%s' />" \
              % link

    return poster_html

# database
def connection():
    conn = MySQLdb.connect(
        host='localhost', #127.0.0.1
        user='root',
        passwd='',
        db='movies'
    )

    return conn

def top_by_genre(genre,min_count,top):
    '''
    :param:
    genre option: Action,Animation,Adventure,Comedy,Crime,Drama,Fantasy,Family,Horror,History,Romance,Science Fiction,Thriller,
    :return:
    '''
    sql = '''
    select id, title,vote_average,vote_count from moviemeta
    where genres like '%{}%' and vote_count > {}
    order by vote_average desc
    limit {};
    '''.format(genre, int(min_count), int(top))

    cursor = connection().cursor()
    cursor.execute(sql)
    result = pd.DataFrame(list(cursor.fetchall()), columns=['id', 'title', 'rate_average', 'rate_count'])
    return result

DATA_DIR = '../data'
raw = pd.read_csv(os.path.join(DATA_DIR, 'movies_metadata.csv'))
raw['year'] = pd.to_datetime(raw['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
#raw.head(n=2)
#raw.isnull().sum()
#raw.info()
raw['id'] = raw['id'].apply(convert_int)
# check id is null rows to decide drop
raw[raw.id.isnull()]
raw_drop = raw.drop([19730, 29503, 35587])
raw_drop['id'] = raw_drop['id'].astype('int')
df = raw_drop
links_small = pd.read_csv(os.path.join(DATA_DIR, 'links_small.csv'))
links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
df_s = df[df['id'].isin(links_small)]
df_s = df_s.reset_index(drop=True)
df_s = df_s.reset_index(drop=False)


############### Content based Recommender  #################
# similarity between movies based on movie's overview

tf = sklearn.feature_extraction.text.TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df_s.overview.fillna(''))
#tfidf_matrix.shape

cosine_sim = sklearn.metrics.pairwise.linear_kernel(tfidf_matrix, tfidf_matrix)
# now we have pairwise cosine similarity matrix
#cosine_sim.shape

###### based on movie overview, recommend top n similar #########
def recommendation_base_overview(movie,n):
    # get movie's index value, !!!not id
    idx = df_s[df_s.title == movie].index[0] # attention: the idx is Int64Index (basically a list)
    # cosine_sim[idx]: get corresponse cosine similarity
    # sort base on value, also keep index
    sort = sorted(enumerate(cosine_sim[idx]),reverse=True,key = lambda x: x[1])
    idx_top = [i[0] for i in sort[1:n+1]]
    similarity = [i[1] for i in sort[1:n+1]]
    rank = df_s.iloc[idx_top][['index','title','poster_path']]
    rank['similarity'] = similarity
    # return index, movie title and cosine_sim rate
    return rank.reset_index(drop=True)

#recommendation_base_overview('The Godfather',3)

###### based on crew and cast ##########
credits = pd.read_csv(os.path.join(DATA_DIR, 'credits.csv'))
keywords = pd.read_csv(os.path.join(DATA_DIR, 'keywords.csv'))
credits.id = credits.id.astype('int')
keywords.id = keywords.id.astype('int')
df = raw_drop.merge(credits, how='left',on='id')
df = df.merge(keywords, how='left', on='id')
df_s = df[df.id.isin(links_small)]
df_s = df_s.reset_index(drop=True)
df_s = df_s.reset_index(drop=False)

#df_s.shape
df_s.crew = df_s.crew.apply(ast.literal_eval)
df_s['director'] = df_s.crew.apply(get_director)
df_s['cast_edit'] = df_s['cast'].apply(ast.literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
# top 3 cast
df_s['cast_top3'] = df_s.cast_edit.apply(lambda x: x[:3] if len(x)>=3 else x)
df_s['keywords_edit'] = df_s['keywords'].apply(ast.literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
df_s.cast_top3 = df_s.cast_top3.apply(lambda x: [str.lower(i.replace(' ','')) for i in x])
df_s.director = df_s.director.astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
df_s['director_weighted'] = df_s.director.apply(lambda x: [x,x])
s = df_s.apply(lambda x: pd.Series(x['keywords_edit']),axis=1).stack().reset_index(level=1, drop=True)
s = s.value_counts() #keywords_count
keyword_list = s[s>1] #keywords_list

stem = nltk.stem.snowball.SnowballStemmer('english')
df_s['keyword_final'] = df_s.keywords_edit.apply(filter_keywords).apply(lambda x: [stem.stem(i) for i in x]).apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
df_s['genres_final'] = df_s['genres'].fillna('[]').apply(ast.literal_eval).apply(lambda x: [i['name'].lower() for i in x] if isinstance(x, list) else [])
df_s['soup'] = df_s.keyword_final + df_s.cast_top3 + df_s.director_weighted + df_s.genres_final
df_s.soup = df_s.soup.apply(lambda x: ' '.join(x))

count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
count_matrix_crew = count.fit_transform(df_s['soup'])
cosine_sim_crew = sklearn.metrics.pairwise.cosine_similarity(count_matrix_crew, count_matrix_crew)

def recommendation_base_crew(movie,n):
    # get movie's index value
    idx = df_s[df_s.title == movie].index[0] # attention: the idx is Int64Index (basically a list)
    # cosine_sim_crew[idx]: get corresponse cosine similarity
    # sort base on value, also keep index
    sort = sorted(enumerate(cosine_sim_crew[idx]),reverse=True,key = lambda x: x[1])
    idx_top = [i[0] for i in sort[1:n+1]]
    similarity = [i[1] for i in sort[1:n+1]]
    rank = df_s.iloc[idx_top][['index','title']]
    rank['similarity'] = similarity
    return rank.reset_index(drop=True)

############### Collaborative Filtering(user-user)  #################
'''
ratings = pd.read_csv('movies-master/ratings_small.csv')
data = surprise.Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader=surprise.Reader())
svd = surprise.SVD()
data.split(n_folds=5)
surprise.evaluate(algo=svd, data=data, measures=['rmse','mae'])
trainset = data.build_full_trainset()
svd.train(trainset=trainset)
svd.predict(uid=1, iid=302)
'''