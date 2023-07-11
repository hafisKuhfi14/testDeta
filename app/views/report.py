import streamlit as st
import datetime
import pandas as pd
from ..utils.textCleaning import textCleaning, countTotalSentimentFrequency
import io

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def to_excel(df):
    excel_io = io.BytesIO()
    # Menulis DataFrame ke Excel
    with pd.ExcelWriter(excel_io, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    excel_io.seek(0)

    return excel_io

def report():
    st.markdown("## Laporan") 
    start_date_col, end_date_col = st.columns(2)   
    df = pd.read_csv("app/data/indihome3_scrape.csv")

    with start_date_col:
        start_date = st.date_input(
            "Masukan Tanggal Awal",
            pd.to_datetime(df['postDate']).min(),
            min_value=pd.to_datetime(df['postDate']).min(),
            max_value=pd.to_datetime(df['postDate']).max().date() - pd.DateOffset(days=1)
        )
        st.write('Tanggal Awal:', start_date)
    with end_date_col:
        end_date = st.date_input(
            "Masukan Tanggal Akhir",
            pd.to_datetime(df['postDate']).min().date() + pd.DateOffset(days=1),
            min_value=pd.to_datetime(df['postDate']).min().date() + pd.DateOffset(days=1),
            max_value=pd.to_datetime(df['postDate']).max().date() - pd.DateOffset(days=1)
        )
        st.write('Tanggal Akhir is:', end_date)
    
    # Mengubah kolom timestamp menjadi tipe data datetime
    df['postDate'] = pd.to_datetime(df['postDate'])
    
    # Mengonversi input tanggal menjadi tipe data datetime
    start_date = pd.to_datetime(start_date).tz_localize('UTC')
    end_date = pd.to_datetime(end_date).tz_localize('UTC')
    filtered_df = df.loc[(df['postDate'] >= start_date) & (df['postDate'] <= end_date)]

    df, result = textCleaning(filtered_df)
    df = df.drop(['retweets', 'likes', 'Text_Clean_split', 'username'], axis=1)
    st.dataframe(df, use_container_width=True)
    if (len(df[df.polarity == "positive"]) > len(df[df.polarity == "negative"])):
        st.success(f"Data lebih dominan bernada positive, {len(df[df.polarity == 'positive'])} polarity positive")
    else:
        st.error(f"Data lebih dominan bernada negative, {len(df[df.polarity == 'negative'])} polarity negative")

    # ------ Download dataframe
    csv = convert_df(df)
    df['postDate'] = df['postDate'].dt.tz_convert(None)
    df_xlsx = to_excel(df)
    
    st.download_button("Download CSV", csv, f"Data Sentimen {start_date} - {end_date}.csv")
    st.download_button("Download Excel", df_xlsx, f"Data Sentimen {start_date} - {end_date}.xlsx")