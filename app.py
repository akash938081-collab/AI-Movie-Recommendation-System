import streamlit as st
import pickle
import pandas as pd
import ast

# ==============================
# Page Settings
# ==============================

st.set_page_config(
    page_title="AI Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# ==============================
# Load Files
# ==============================

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
poster_urls = pickle.load(open("poster_urls.pkl", "rb"))

movie_details = pd.read_csv("tmdb_5000_movies.csv")


# ==============================
# Get Genres
# ==============================

def get_genres(genres_data):

    try:
        genres = ast.literal_eval(genres_data)

        genre_names = []

        for genre in genres:
            genre_names.append(genre["name"])

        return ", ".join(genre_names)

    except:
        return "Not available"


# ==============================
# Get Movie Details
# ==============================

def get_movie_details(movie_id):

    details = movie_details[
        movie_details["id"] == movie_id
    ]

    if details.empty:
        return None

    movie = details.iloc[0]

    return {
        "overview": movie.get("overview", "Not available"),
        "release_date": movie.get("release_date", "Not available"),
        "rating": movie.get("vote_average", "Not available"),
        "vote_count": movie.get("vote_count", "Not available"),
        "genres": get_genres(movie.get("genres", "[]"))
    }


# ==============================
# Recommend Movies
# ==============================

def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []

    for i in movies_list:

        movie_row = movies.iloc[i[0]]

        movie_id = int(movie_row["movie_id"])
        movie_title = movie_row["title"]

        poster = poster_urls.get(movie_id)

        details = get_movie_details(movie_id)

        recommended_movies.append({
            "id": movie_id,
            "title": movie_title,
            "poster": poster,
            "details": details
        })

    return recommended_movies


# ==============================
# UI
# ==============================

st.title("🎬 AI Movie Recommendation System")

st.write(
    "Select a movie and get 5 similar movie recommendations."
)


# ==============================
# Select Movie
# ==============================

selected_movie = st.selectbox(
    "🎥 Select a Movie",
    movies["title"].values
)


# ==============================
# Selected Movie Details
# ==============================

selected_row = movies[
    movies["title"] == selected_movie
].iloc[0]

selected_movie_id = int(
    selected_row["movie_id"]
)

selected_poster = poster_urls.get(
    selected_movie_id
)

selected_details = get_movie_details(
    selected_movie_id
)


st.divider()

st.subheader(f"🎬 {selected_movie}")

col1, col2 = st.columns([1, 2])


# Poster
with col1:

    if selected_poster:

        st.image(
            selected_poster,
            use_container_width=True
        )

    else:

        st.info("Poster not available")


# Details
with col2:

    if selected_details:

        st.write(
            "🎭 **Genres:** "
            + selected_details["genres"]
        )

        st.write(
            "📅 **Release Date:** "
            + str(
                selected_details["release_date"]
            )
        )

        st.write(
            "⭐ **Rating:** "
            + str(
                selected_details["rating"]
            )
            + " / 10"
        )

        st.write(
            "👥 **Votes:** "
            + str(
                selected_details["vote_count"]
            )
        )

        st.write("### 📝 Overview")

        st.write(
            selected_details["overview"]
        )

    else:

        st.info(
            "Movie details not available."
        )


st.divider()


# ==============================
# Recommend Button
# ==============================

if st.button(
    "🎯 Recommend Movies",
    use_container_width=True
):

    recommendations = recommend(
        selected_movie
    )

    st.subheader(
        f"🎯 Recommended Movies for: {selected_movie}"
    )

    cols = st.columns(5)

    for i in range(5):

        movie = recommendations[i]

        with cols[i]:

            # Poster
            if movie["poster"]:

                st.image(
                    movie["poster"],
                    use_container_width=True
                )

            else:

                st.info(
                    "Poster not available"
                )


            # Title
            st.write(
                f"### {movie['title']}"
            )


            # Movie Details
            if movie["details"]:

                details = movie["details"]

                st.write(
                    "⭐ "
                    + str(details["rating"])
                    + " / 10"
                )

                with st.expander(
                    "📖 View Details"
                ):

                    st.write(
                        "🎭 **Genres:** "
                        + details["genres"]
                    )

                    st.write(
                        "📅 **Release Date:** "
                        + str(
                            details["release_date"]
                        )
                    )

                    st.write(
                        "### 📝 Overview"
                    )

                    st.write(
                        details["overview"]
                    )