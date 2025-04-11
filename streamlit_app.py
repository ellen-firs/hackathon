import streamlit as st
import pandas as pd
import numpy as np

# Заголовок
st.title("📊 Анализ потребления тепловой энергии")

# Загрузка данных
uploaded_file = st.file_uploader("Загрузите файл с данными", type=["csv", "txt"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Данные")
    st.dataframe(df)

    # Фильтры
    year = st.selectbox("Год", sorted(df["Год"].dropna().unique()))
    month = st.selectbox("Месяц", sorted(df["Месяц"].dropna().unique()))
    district = st.selectbox("Район", sorted(df["Район"].dropna().unique()))

    filtered_df = df[
        (df["Год"] == year) &
        (df["Месяц"] == month) &
        (df["Район"] == district)
    ]

    st.subheader("Отфильтрованные данные")
    st.dataframe(filtered_df)

    # График потребления
    st.subheader("График потребления")
    st.line_chart(filtered_df[["Текущее потребление, Гкал"]])

    # Карта
    st.subheader("Карта объектов")
    st.map(filtered_df[["Широта", "Долгота"]].dropna())

    # Аномалии
    st.subheader("🚨 Аномалии (нулевые значения)")
    anomalies = filtered_df[filtered_df["Текущее потребление, Гкал"] == 0]
    st.dataframe(anomalies)
