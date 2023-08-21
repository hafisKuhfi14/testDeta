import streamlit as st  # pip install streamlit

def text_preprocessing(df):
    st.markdown(kotak_berwarna("#dadada4d", f"Casefolding: {df['Text_Clean'][0]}"), unsafe_allow_html=True)
    st.markdown(kotak_berwarna("#c2c2c27a", f"Cleansing: {df['Cleansing'][0]}"), unsafe_allow_html=True)
    st.markdown(kotak_berwarna("#dadada4d", f"Stemming: {df['Stemming'][0]}"), unsafe_allow_html=True)
    st.markdown(kotak_berwarna("#c2c2c27a", f"Slangword: {df['Slangword'][0]}"), unsafe_allow_html=True)
    st.markdown(kotak_berwarna("#dadada4d", f"Stopword: {df['Stopword'][0]}"), unsafe_allow_html=True)
    st.markdown(kotak_berwarna("#c2c2c27a", f"Shortword: {df['Shortword'][0]}"), unsafe_allow_html=True)
    df_labeling = {
            "split_word": df['Text_Clean_split'],
            "polarity": df['polarity'],
            "bobot": df['polarity_score']
    }
    st.dataframe(df_labeling, use_container_width=True)
    # st.dataframe(df['Text_Clean'].head(20), use_container_width=True)

# Fungsi untuk mengatur CSS styling untuk kotak berwarna
def kotak_berwarna(color, text):
    return f"""
        <div style="
            background-color: {color};
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            color: black;
            font-weight: 600;
        ">{text}</div>
    """