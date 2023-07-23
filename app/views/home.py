import streamlit as st  # pip install streamlit
import pandas as pd
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from ..utils.analiyst import analiystThisData
# Error Handling
import traceback

async def home():
    try:

        st.markdown("### Ulasan Pelanggan Berdasarkan Platform Media Sosial")
        st.write("pilih media sosial mana yang ingin kamu analisis")
        # --- NAVIGATION MENU ---
        selected = option_menu(
            menu_title=None,
            options=["Twitter", "Facebook"],
            icons=["twitter", "facebook"],  # https://icons.getbootstrap.com/
            orientation="horizontal",
        )
        
        # --- INPUT & SAVE PERIODS ---
        if (selected == "Twitter"):
            df = pd.read_csv("app/data/indihome3_twitterscrape.csv")
            
        if (selected == "Facebook"):
            df = pd.read_csv("app/data/indihome3_facebookscrape.csv")

        if (st.session_state['username'] == "admin"):
            analiystThisData(st, df, page="home")
        else:
            st.dataframe(df.head(10))
    except:
        print(traceback.format_exc())

        # df, result = sentimentAnalysis(df, False)
        # df, df_positive, df_negative, total_freq_by_month = countTotalSentimentFrequency(df, result)

        # st.write(total_freq_by_month)
        # data = df
        # # ====================
        # st.markdown("### <center> Total Sentiment Berdasarkan Topik</center>", unsafe_allow_html=True)
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.dataframe(df_positive, use_container_width=True)
        # with col2:
        #     st.dataframe(df_negative, use_container_width=True)
        
        # tweets=st.sidebar.radio('Sentiment Type',('nothing','positive','negative'))
        # dataPolarity = data
        # if (tweets == "nothing"):
        #     dataPolarity = data
        # else:
        #     dataPolarity = data.query('polarity==@tweets')
        # st.markdown("**Review Ulasan**")
        # st.markdown(f"{dataPolarity[['Text_Clean']].sample(1).iat[0,0]}\n**[{dataPolarity[['polarity']].sample(1).iat[0,0]}]**")
        
        # sentiment=dataPolarity['polarity'].value_counts()
        # sentiment=pd.DataFrame({'Sentiment':sentiment.index,'Tweets':sentiment.values})
        # st.markdown("###  Sentiment count")
        # fig = px.pie(sentiment, values='Tweets', names='Sentiment')
        # st.plotly_chart(fig)

        # # ----- SVM
        # X_train, X_test, y_train, y_test, data_latih, data_test, all_data = model.train_test_splitTFIDF(X=X, y=y, testSize = 0.1, randState = 0)

        # st.table(pd.DataFrame({
        #     "Total Keseluruhan data": [all_data],
        #     "Total Data Latih": [data_latih],
        #     "Total Data Test": [data_test]
        # }).reset_index(drop=True))
        
        # score_svmlk, svmLinear, y_pred = algorithm.predictSVM(X_train, y_train, X_test, y_test)
        # st.markdown(f"<center>Akurasi dengan menggunakan Support Vector Machine Linear Kernel: <b color='white'>{score_svmlk:.0%}</b></center>", unsafe_allow_html=True)
        # accuracy = algorithm.plot_confusion_matrix_box(svmLinear=svmLinear, X_test=X_test, y_test=y_test, y_pred=y_pred)
        # st.pyplot()
        # ====== end svm

