import streamlit as st  # pip install streamlit
import pandas as pd

from ..utils import utils
from ..modules import feature_extraction
from ..modules import model
from ..modules import evaluation
from ..modules import txt_preprocessing
from ..utils.textCleaning import positiveOrNegativeDictionary
from ..utils.analiyst import analiystThisData

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Error Handling
import traceback

def file_predictor():
    try:

        # Menampilkan komponen file uploader
        uploaded_file = st.file_uploader("Unggah file CSV", type="csv")

        # Memeriksa apakah file sudah diunggah
        if uploaded_file is None:
            st.write("Upload file scraper data yang sudah anda miliki untuk memulai sentiment")
            return
        
        # Membaca file CSV sebagai DataFrame
        df = pd.read_csv(uploaded_file)
        selectedColumn = st.selectbox(
            'Pilih kolom apa yang ingin di analisis ?',
            (df.columns))
        if (st.button("Analisis")):
            analiystThisData(st, df, selectedColumn, page="file_predictor")
    except:
        print(traceback.format_exc())
        st.error(traceback.format_exc())

    uploaded_file.close()

