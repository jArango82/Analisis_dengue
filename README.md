# Análisis de Datos sobre Dengue: Pipeline Técnico

Este repositorio alberga el pipeline de procesamiento y visualización de datos clínicos y hematológicos relacionados con casos de dengue. La interfaz técnica está documentada en el `index.html`, y la visualización interactiva se despliega mediante Streamlit.

A continuación se detalla la arquitectura técnica del procesamiento de los datos.

---

## Arquitectura del Pipeline de Datos (ETL)

El procesamiento de la información se estructura en tres fases fundamentales (Ingesta, Transformación y Carga) para asegurar la integridad y fiabilidad de los datos en de nuestro dashboard interactivo interactivo.

### 1. Ingesta de Datos (Extract)
**¿De dónde vienen los datos?**
* **Fuentes Originales:** Los datos derivan de registros con historiales clínicos y hemogramas enfocados en la detección de enfermedades infecciosas y transmitidas por mosquitos (Dengue).
* **Almacenamiento:** El dataset central se aloja estáticamente bajo el nombre `Dengue_diseases_dataset_modified (1).csv` dentro del directorio estructurado `data/`.
* **Proceso de Adquisición:** Dentro de `app.py`, el proceso de ingesta invoca la captura del documento consolidado mediante la API de `pandas`, leyendo nativamente la tabla CSV y montándola en un *DataFrame* en memoria.

### 2. Transformación (Transform)
**Limpieza, manejo de nulos y normalización:**
* **Limpieza y Manejo de Nulos:** La integridad médica requiere precisión; por ello, la estrategia implementada descarta cualquier registro con campos faltantes mediante la función de omisión (`df.dropna()`). Esto garantiza que los estadísticos y algoritmos predictivos no estén distorsionados por datos interpolados (como posibles niveles falsos en el conteo crítico de plaquetas).
* **Conversión Semántica (Mapeo):** Se incluye un preprocesamiento categórico para mejorar la interpretabilidad en la vista visual. El campo analítico binario original (`dengue_label`: 1 o 0) es transformado estructuralmente a una nueva variable categórica estandarizada (`dengue_status`: 'Positivo' o 'Negativo').
* **Normalizaciones Base:** La ingesta nativa respeta los tipos de datos biométricos como rangos dinámicos en sus métricas estándar (ej. gramos por decilitro para Hemoglobina `hemoglobin_g_dl`).

### 3. Carga (Load)
**Estructura final para la visualización:**
* **Persistencia en Memoria (Caché):** Para sostener una alta interactividad y bajo retraso en dashboard, el *DataFrame* transformado no se exporta a disco, sino que se carga usando memorización en el motor del servidor (`@st.cache_data`).
* **Estructura Multidimensional:** El objeto consolidado que entra al motor de visualización (Plotly) cuenta con los ejes necesarios pre-procesados:
  * **Ejes Descriptivos:** Género (`gender`) y la clasificación natural del paciente (`dengue_status`).
  * **Variables Cuantitativas:** Rangos de edad (`age`), conteos exactos (`platelet_count`), y espectros de hemoglobina.
* **Carga Filtrada Bajo Demanda:** Sobre esta estructura matriz, el sistema efectúa *queries* en tiempo real segmentando las filas según eventos en el menú lateral (rango de edad y subgrupos demográficos), entregando una instancia cargada y depurada *(_filtered_df_)* para ser consumida inmediatamente por las representaciones gráficas (Boxplots, Scatter Plots o Histograms).

---

### Enlaces de Interés
* **Aplicación desplegada:** [Streamlit Cloud App](https://dengueingdatos.streamlit.app/)
* **Documentación Adicional:** Visite el archivo estático `index.html`.
