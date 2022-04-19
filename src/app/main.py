from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
import pickle
import os
import pandas as pd
from scipy.sparse import csr_matrix

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')
basic_auth = BasicAuth(app)

modelo = pickle.load(open('models/knn_model.sav','rb'))
movies = pd.read_pickle("data/processed/movies.pkl")
MovieDataset = pd.read_pickle("data/processed/FinalMoviesDataset.pkl")
csr_data = csr_matrix(MovieDataset.values)
#MovieDataset.reset_index(inplace=True)

@app.route('/')
def home(): 
    return """Type a movie that you like and you may also like the following list of movies
              type: /movie"""

@app.route('/<movie_name>' ,methods=['GET'])
@basic_auth.required         #OAUTH SCREEN
def get_movie_recommendation(movie_name,):
    n_movies_to_reccomend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = MovieDataset[MovieDataset['movieId'] == movie_idx].index[0]
        distances , indices = modelo.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = MovieDataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
        return jsonify(df.to_dict())
    else:
        return "No movies found. Please check your input"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')