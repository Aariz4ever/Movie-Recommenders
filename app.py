import streamlit as st
import pickle
import pandas as pd
import difflib
import requests



def fetch_poster(movie_id):
    # api_key = '5cf515145ae20bf3973820c4798428d5'
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5cf515145ae20bf3973820c4798428d5&language=en-US'.format(movie_id))
    data = response.json()
    # st.text(data)
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


def recommend(movie):
    try:
        movie_lower_stripped = movie.lower().strip()
        
        matches = difflib.get_close_matches(movie_lower_stripped, movies['title'].apply(lambda x: x.lower().strip()))
        
        if matches:
            movie_index = movies[movies['title'].apply(lambda x: x.lower().strip()) == matches[0]].index[0]
            distances = similarity[movie_index]
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:6]
            recommended_movies = []
            recommended_movies_poster = []
            for i in movies_list:
                movie_id = movies.iloc[i[0]]['movie_id'] # fetch poster using id
                recommended_movies.append(movies.iloc[i[0]]['title'])
                recommended_movies_poster.append(fetch_poster(movie_id))
            return recommended_movies, recommended_movies_poster
        else:
            st.write("No similar movie found.")
    except IndexError:
        st.write("Movie not found in the dataset.")


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'A place to find youself....',
    movies['title'].values
)

if st.button('Recommend'):
    titles, posters = recommend(selected_movie_name)
    # Create three columns
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Add content to each column
    with col1:
        st.image(posters[0])
        st.text(titles[0])
    with col2:
        st.image(posters[1])
        st.text(titles[1])
    with col3:
        st.image(posters[2])
        st.text(titles[2])        
    with col4:
        st.image(posters[3])
        st.text(titles[3])
    with col5:
        st.image(posters[4])
        st.text(titles[4])
    with col6:
        st.image(posters[5])
        st.text(titles[5])