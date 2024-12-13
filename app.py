import pickle
import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.header('FILMS Recommender System')

# Load model và dữ liệu
model = pickle.load(open('model/model.pkl', 'rb'))
FILM_names = pickle.load(open('model/FILM_names.pkl', 'rb'))
final_rating = pickle.load(open('model/final_rating.pkl', 'rb'))
FILM_pivot = pickle.load(open('model/FILM_pivot.pkl', 'rb'))

# Function to fetch poster images
def fetch_poster(suggestion):
    FILM_name = []
    ids_index = []
    poster_url = []

    for FILM_id in suggestion:
        FILM_name.append(FILM_pivot.index[FILM_id])

    for name in FILM_name:
        if name not in final_rating['Movie'].values:
            st.error(f"Poster cho '{name}' không tồn tại.")
            continue
        ids = np.where(final_rating['Movie'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['Image_link']
        poster_url.append(url)

    return poster_url

# Function to recommend films
def recommend_FILM(FILM_name):
    FILM_name = FILM_name.strip().lower()
    FILM_name = FILM_name.replace("'", "")  # Remove special characters if needed

    FILM_pivot_lower = FILM_pivot.index.str.lower()
    if FILM_name not in FILM_pivot_lower:
        st.warning(f"Bộ phim '{FILM_name}' không có trong tập dữ liệu.")
        return [], []

    FILM_id = FILM_pivot_lower.get_loc(FILM_name)
    FILM_vector = FILM_pivot.iloc[FILM_id, :].values.reshape(1, -1)
    similarity_scores = cosine_similarity(FILM_pivot.values, FILM_vector).flatten()

    top_n = 5
    similar_indices = similarity_scores.argsort()[-top_n-1:-1][::-1]

    FILMs_list = []
    poster_url = fetch_poster(similar_indices)
    for idx in similar_indices:
        FILMs_list.append(FILM_pivot.index[idx])

    return FILMs_list, poster_url

# Load available films
available_FILMs = final_rating['Movie'].unique()

selected_FILMs = st.selectbox(
    "Chọn film bạn muốn xem ^^",
    available_FILMs
)



# Show recommendations when button is clicked
if st.button('Đề xuất'):
    recommended_FILMs, poster_url = recommend_FILM(selected_FILMs)
    if not recommended_FILMs or not poster_url:
        st.warning("Không có gợi ý nào được tìm thấy.")
    else:
        # Display the films with buttons for detail
        col1, col2, col3, col4, col5 = st.columns(5)

        for idx, col in enumerate([col1, col2, col3, col4, col5]):
            film_name = recommended_FILMs[idx]
            with col:
                st.text(film_name)
                st.image(poster_url[idx])
                # Use expander for details instead of buttons
                with st.expander(f"Xem chi tiết {film_name}"):
                    film_info = final_rating[final_rating['Movie'] == film_name].iloc[0]
                    st.write(f"**Tên phim**: {film_info['Movie']}")
                    st.write(f"**Năm sản xuất**: {film_info['Year']}")
                    st.write(f"**Thể loại**: {film_info['Genres']}")
                    st.write(f"**Đánh giá**: {film_info['Rating']}")
                    st.write(f"**Thời gian**: {film_info['Duration']}")
                    st.write(f"**MPAA Rating**: {film_info['MPAA']}")
                    st.write(f"**Đạo diễn**: {film_info['Director']}")
                    st.write(f"**Diễn viên**: {film_info['Stars']}")
                    st.write(f"**Tóm tắt cốt truyện**: {film_info['Plot_Summary']}")
                    st.image(film_info['Image_link'], caption="Poster", use_container_width=True)
# Display information about the selected film
if selected_FILMs:
    film_info = final_rating[final_rating['Movie'] == selected_FILMs].iloc[0]
    st.write(f"**Tên phim**: {film_info['Movie']}")
    st.write(f"**Năm sản xuất**: {film_info['Year']}")
    st.write(f"**Thể loại**: {film_info['Genres']}")
    st.write(f"**Đánh giá**: {film_info['Rating']}")
    st.write(f"**Thời gian**: {film_info['Duration']}")
    st.write(f"**MPAA Rating**: {film_info['MPAA']}")
    st.write(f"**Đạo diễn**: {film_info['Director']}")
    st.write(f"**Diễn viên**: {film_info['Stars']}")
    st.write(f"**Tóm tắt cốt truyện**: {film_info['Plot_Summary']}")
    st.image(film_info['Image_link'], caption="Poster", use_container_width=True)