import streamlit as st
import pandas as pd

st.set_page_config(page_title="Анализ теплопотребления", layout="wide")

st.title("📊 Анализ потребления тепловой энергии")

# Загрузка CSV
uploaded_file = st.file_uploader("Загрузите CSV или TXT файл с данными", type=["csv", "txt"])

if uploaded_file is not None:
    try:
        # Попытка чтения с кодировкой cp1251
        df = pd.read_csv(uploaded_file, encoding="cp1251", sep=",")
        st.success("✅ Файл успешно загружен!")

        # Проверка и отображение таблицы
        st.subheader("📋 Исходные данные")
        st.dataframe(df.head(50), use_container_width=True)

        # -------------------
        # ФИЛЬТРЫ
        # -------------------
        st.sidebar.header("🔎 Фильтры")

        year_options = sorted(df["Год"].dropna().unique())
        year = st.sidebar.selectbox("Год", year_options)

        month_options = sorted(df[df["Год"] == year]["Месяц"].dropna().unique())
        month = st.sidebar.selectbox("Месяц", month_options)

        district_options = df["Район"].dropna().unique()
        district = st.sidebar.multiselect("Район", district_options, default=district_options)

        type_options = df["Тип объекта"].dropna().unique()
        building_type = st.sidebar.multiselect("Тип объекта", type_options, default=type_options)

        filtered_df = df[
            (df["Год"] == year) &
            (df["Месяц"] == month) &
            (df["Район"].isin(district)) &
            (df["Тип объекта"].isin(building_type))
        ]

        st.subheader(f"📂 Отфильтрованные данные ({len(filtered_df)} записей)")
        st.dataframe(filtered_df, use_container_width=True)

        # -------------------
        # ГРАФИК потребления
        # -------------------
        st.subheader("📈 График потребления тепловой энергии")

        if "Текущее потребление, Гкал" in filtered_df.columns:
            chart_data = filtered_df[["Упрощенный адрес", "Текущее потребление, Гкал"]].dropna()
            chart_data = chart_data.sort_values("Текущее потребление, Гкал", ascending=False).head(20)
            st.bar_chart(chart_data.set_index("Упрощенный адрес"))
        else:
            st.warning("Колонка 'Текущее потребление, Гкал' отсутствует в данных.")

        # -------------------
        # КАРТА объектов
        # -------------------
        st.subheader("🗺️ Карта объектов с координатами")

        if "Широта" in filtered_df.columns and "Долгота" in filtered_df.columns:
            map_df = filtered_df[["Широта", "Долгота"]].dropna().copy()
            map_df = map_df.rename(columns={"Широта": "latitude", "Долгота": "longitude"})
            st.map(map_df)
        else:
            st.warning("В данных отсутствуют координаты (Широта/Долгота).")


        # -------------------
        # АНОМАЛИИ
        # -------------------
        st.subheader("🚨 Аномалии в потреблении")

        # Нулевые потребления
        zero_df = filtered_df[filtered_df["Текущее потребление, Гкал"] == 0]
        if not zero_df.empty:
            st.error(f"🔻 Найдено {len(zero_df)} объектов с **нулевым потреблением**:")
            st.dataframe(zero_df, use_container_width=True)
        else:
            st.success("✅ Нулевых значений не найдено.")

    except Exception as e:
        st.error(f"❌ Ошибка при загрузке файла: {e}")
else:
    st.info("⬆️ Загрузите CSV или TXT файл для начала анализа.")
