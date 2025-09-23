
import pickle
import os
import streamlit as st
import requests

# Load movie dataset
file_path = os.path.join(os.path.dirname(__file__), "movie_list.pkl")
with open(file_path, "rb") as f:
    movies = pickle.load(f)  # movies should be a DataFrame

# Load similarity data
similarity_path = os.path.join(os.path.dirname(__file__), "similarity.pkl")
with open(similarity_path, "rb") as f:
    similarity = pickle.load(f)

# OMDb API poster fetch function
def fetch_poster(movie_title):
    api_key = "515cef2f"  
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data.get("Poster", None)

# Recommendation function
def recommending(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters

# Streamlit UI
st.title("🎬 MOVIE RECOMMENDATION SYSTEM")
option = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Show Recommendations"):
    recommended_movie_names, recommended_movie_posters = recommending(option)
    cols = st.columns(5)  # instead of beta_columns
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            if recommended_movie_posters[idx]:
                st.image(recommended_movie_posters[idx])
            else:
                st.write("Poster not available")


# Movie-themed background
movie_bg = """
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1524985069026-dd778a71c7b4");  /* movie wallpaper URL */
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    color: white;
}
h1, h2, h3, h4 {
    color: #FFD700;  /* golden text for movie vibe */
    text-align: center;
    font-family: 'Trebuchet MS', sans-serif;
}
</style>
"""

st.markdown(movie_bg, unsafe_allow_html=True)
card_style = """
<style>
div[data-testid="stVerticalBlock"] {
    background: rgba(0, 0, 0, 0.6);  /* transparent black */
    padding: 15px;
    border-radius: 15px;
}
</style>
"""
st.markdown(card_style, unsafe_allow_html=True)
from difflib import get_close_matches
closest_match = get_close_matches(option, movies['title'].values, n=1)
if closest_match:
    option = closest_match[0]

