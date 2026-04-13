import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuración de la página
st.set_page_config(page_title="Dashboard: Dengue Data", page_icon="🦟", layout="wide")

# Título y Descripción
st.title("🦟 Análisis de Datos Clínicos de Dengue")
st.markdown("Esta aplicación interactiva permite explorar los datos clínicos y hematológicos de pacientes evaluados para Dengue. Utiliza los filtros en el menú lateral para personalizar la vista.")

# Función para cargar los datos usando caché
@st.cache_data
def load_data():
    file_path = os.path.join("data", "Dengue_diseases_dataset_modified (1).csv")
    df = pd.read_csv(file_path)
    # Limpieza básica
    df = df.dropna()
    # Mapear las etiquetas para mejor legibilidad
    df['dengue_status'] = df['dengue_label'].map({1: 'Positivo', 0: 'Negativo'})
    return df

# Cargar los datos
try:
    df = load_data()
except Exception as e:
    st.error(f"Error al cargar los datos. Verifica la ruta del archivo. Detalle: {e}")
    st.stop()

# --- Sidebar ---
st.sidebar.header("Filtros Interactivos")

# Filtro por Género
selected_gender = st.sidebar.multiselect(
    "Selecciona el Género / Grupo Poblacional",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

# Filtro por Edad
min_age = int(df['age'].min())
max_age = int(df['age'].max())
age_range = st.sidebar.slider(
    "Selecciona el Rango de Edad",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Aplicar filtros
filtered_df = df[
    (df['gender'].isin(selected_gender)) &
    (df['age'] >= age_range[0]) & 
    (df['age'] <= age_range[1])
]

# --- Métricas Generales ---
st.write("### 📊 Métricas Generales")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Pacientes", len(filtered_df))
positivos = len(filtered_df[filtered_df['dengue_label'] == 1])
negativos = len(filtered_df[filtered_df['dengue_label'] == 0])
col2.metric("Positivos para Dengue", positivos)
col3.metric("Negativos para Dengue", negativos)
col4.metric("Promedio de Edad", f"{filtered_df['age'].mean():.1f}" if len(filtered_df) > 0 else "0")

st.markdown("---")

# --- Gráficos interactivos ---
st.write("### 📈 Visualizaciones Dinámicas")

colA, colB = st.columns(2)

with colA:
    # 1. Distribución de casos (Pie Chart)
    st.subheader("Distribución de Casos de Dengue")
    fig1 = px.pie(
        filtered_df, 
        names='dengue_status', 
        hole=0.4,
        color='dengue_status',
        color_discrete_map={'Positivo': '#ef553b', 'Negativo': '#00cc96'}
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # 3. Boxplot: Plaquetas por género
    st.subheader("Niveles de Plaquetas por Grupo/Género")
    fig3 = px.box(
        filtered_df, 
        x="gender", 
        y="platelet_count", 
        color="dengue_status",
        color_discrete_map={'Positivo': '#ef553b', 'Negativo': '#00cc96'}
    )
    st.plotly_chart(fig3, use_container_width=True)

with colB:
    # 2. Histograma del conteo de plaquetas
    st.subheader("Distribución del Conteo de Plaquetas")
    fig2 = px.histogram(
        filtered_df, 
        x='platelet_count', 
        color='dengue_status',
        barmode='overlay',
        color_discrete_map={'Positivo': '#ef553b', 'Negativo': '#00cc96'},
        nbins=40
    )
    fig2.update_layout(xaxis_title="Conteo de Plaquetas", yaxis_title="Frecuencia")
    st.plotly_chart(fig2, use_container_width=True)

    # 4. Scatter Plot: Hemoglobina vs Plaquetas
    st.subheader("Hemoglobina vs Conteo de Plaquetas")
    fig4 = px.scatter(
        filtered_df, 
        x='platelet_count', 
        y='hemoglobin_g_dl', 
        color='dengue_status',
        color_discrete_map={'Positivo': '#ef553b', 'Negativo': '#00cc96'},
        hover_data=['age', 'wbc_count']
    )
    fig4.update_layout(xaxis_title="Conteo de Plaquetas", yaxis_title="Hemoglobina (g/dL)")
    st.plotly_chart(fig4, use_container_width=True)

# Vista previa de datos
if st.checkbox("Mostrar Dataframe"):
    st.write(filtered_df)
