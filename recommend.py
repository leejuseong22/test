import pandas as pd
import warnings; warnings.filterwarnings('ignore')
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity




def weighted_vote_average(record):
    v = record['vote_count']
    R = record['vote_average']
    
    return ( (v/(v+m)) * R ) + ( (m/(m+v)) * C )   




def find_sim_movie(df, sorted_ind, title_name, top_n=10):
    title_movie = df[df['title'] == title_name]
    title_index = title_movie.index.values
    
    # top_n의 2배에 해당하는 쟝르 유사성이 높은 index 추출 
    similar_indexes = sorted_ind[title_index, :(top_n*2)]
    similar_indexes = similar_indexes.reshape(-1)
# 기준 영화 index는 제외
    similar_indexes = similar_indexes[similar_indexes != title_index]
    
    # top_n의 2배에 해당하는 후보군에서 weighted_vote 높은 순으로 top_n 만큼 추출 
    tmp = df.iloc[similar_indexes].sort_values('weighted_vote', ascending=False)[:top_n]
   
    return tmp




  # for i in range(5):

  #   b = input("영화를 선택하세요 : ")

  #   a.append(b)  


def run(a):
  movies =pd.read_csv('movies.csv')
      
  movies_df = movies[['id','title', 'genres', 'vote_average', 'vote_count',
                  'popularity', 'keywords', 'overview']]

  pd.set_option('max_colwidth', 100)
  movies_df[['genres','keywords']][:1]
      
  movies_df['genres'] = movies_df['genres'].apply(literal_eval)
  movies_df['keywords'] = movies_df['keywords'].apply(literal_eval)

  movies_df['genres'] = movies_df['genres'].apply(lambda x : [ y['name'] for y in x])
  movies_df['keywords'] = movies_df['keywords'].apply(lambda x : [ y['name'] for y in x])
  movies_df[['genres', 'keywords']][:1]
      
  movies_df['genres_literal'] = movies_df['genres'].apply(lambda x : (' ').join(x))
  count_vect = CountVectorizer(min_df=0, ngram_range=(1,2))
  genre_mat = count_vect.fit_transform(movies_df['genres_literal'])
      
  genre_sim = cosine_similarity(genre_mat, genre_mat)
  genre_sim_sorted_ind = genre_sim.argsort()[:, ::-1]

  # 전역변수 선언
  global result
  global m
  global C

  C = movies_df['vote_average'].mean()
  m = movies_df['vote_count'].quantile(0.6)

  percentile = 0.6
  m = movies_df['vote_count'].quantile(percentile)
  C = movies_df['vote_average'].mean()

  movies_df['weighted_vote'] = movies_df.apply(weighted_vote_average, axis=1)

  movies_df[['title','vote_average','weighted_vote','vote_count']].sort_values('weighted_vote',
                                                                            ascending=False)[:10]
  
  result = pd.DataFrame({'title':[], 'vote_average':[], 'weighted_vote':[]})

  for j in range(len(a)):
    similar_movies = find_sim_movie(movies_df, genre_sim_sorted_ind, a[j],10)
    result=result.append(similar_movies[['title', 'vote_average', 'weighted_vote']])

  dresult = result.drop_duplicates()

  d_result = dresult.sort_values('weighted_vote', ascending = False).head(20)

  movie_result = {}

  mov = d_result['title'].values.tolist()

  # for i in range(len(mov)):
  #   movie_result[i] = mov[i]

  return mov


# 실행문
# print(run(['Avatar']))