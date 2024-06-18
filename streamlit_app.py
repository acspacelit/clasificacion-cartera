import streamlit as st
import pandas as pd
import os

def calculate_percentile_score(column):
    percentiles = column.rank(pct=True)
    scores = percentiles.apply(lambda x: 1 if x <= 0.25 else (2 if x <= 0.5 else (3 if x <= 0.75 else 4)))
    return scores

def reassign_segment(row):
    if row['Puntuacion_Avance_Temporal'] in [3, 4] and row['Puntuacion_NoDesembolsos'] in [3, 4] and row['Puntuacion_Porcentaje_Desembolsado'] in [3, 4]:
        return 'Finalizando en Buen estado'
    elif row['Puntuacion_Avance_Temporal'] in [3, 4] and row['Puntuacion_NoDesembolsos'] in [3, 4] and row['Puntuacion_Porcentaje_Desembolsado'] in [1, 2]:
        return 'Necesitara Extensión o Desembolso Abrupto'
    elif row['Puntuacion_Avance_Temporal'] in [3, 4] and row['Puntuacion_NoDesembolsos'] in [1, 2] and row['Puntuacion_Porcentaje_Desembolsado'] in [3, 4]:
        return 'Finalizando en Buen estado'
    elif row['Puntuacion_Avance_Temporal'] in [3, 4] and row['Puntuacion_NoDesembolsos'] in [1, 2] and row['Puntuacion_Porcentaje_Desembolsado'] in [1, 2]:
        return 'Necesitara Extensión o Desembolso Abrupto'
    elif row['Puntuacion_Avance_Temporal'] in [1, 2] and row['Puntuacion_NoDesembolsos'] in [3, 4] and row['Puntuacion_Porcentaje_Desembolsado'] in [3, 4]:
        return 'Desembolso Anticipado'
    elif row['Puntuacion_Avance_Temporal'] in [1, 2] and row['Puntuacion_NoDesembolsos'] in [3, 4] and row['Puntuacion_Porcentaje_Desembolsado'] in [1, 2]:
        return 'Potencialmente bueno'
    elif row['Puntuacion_Avance_Temporal'] in [1, 2] and row['Puntuacion_NoDesembolsos'] in [1, 2] and row['Puntuacion_Porcentaje_Desembolsado'] in [3, 4]:
        return 'Desembolso Anticipado'
    elif row['Puntuacion_Avance_Temporal'] in [1, 2] and row['Puntuacion_NoDesembolsos'] in [1, 2] and row['Puntuacion_Porcentaje_Desembolsado'] in [1, 2]:
        return 'Proyecto Joven'
    else:
        return 'Otros'

st.title('Análisis de Desembolsos')

# Define the path to the Excel file
file_path = os.path.join('data', 'anp.xlsx')

# Check if the file exists
if os.path.exists(file_path):
    data = pd.read_excel(file_path)
    
    st.write("Datos cargados del archivo de análisis:")
    st.write(data.head())
    
    # Calculate scores for each of the specified columns
    data['Puntuacion_Avance_Temporal'] = calculate_percentile_score(data['Avance Temporal'])
    data['Puntuacion_NoDesembolsos'] = calculate_percentile_score(data['NoDesembolsos'])
    data['Puntuacion_Porcentaje_Desembolsado'] = calculate_percentile_score(data['Porcentaje Desembolsado'])
    
    # Concatenate the scores
    data['Puntuacion_Concatenada'] = (
        data['Puntuacion_Avance_Temporal'].astype(str) +
        data['Puntuacion_NoDesembolsos'].astype(str) +
        data['Puntuacion_Porcentaje_Desembolsado'].astype(str)
    )
    
    # Assign segments based on the concatenated scores
    data['Segmento'] = data.apply(reassign_segment, axis=1)
    
    st.write("Datos con puntuaciones y segmentos:")
    st.write(data.head())
    
    # Option to download the updated data
    output_file = 'analysis_anp_updated.xlsx'
    data.to_excel(output_file, index=False)
    
    with open(output_file, "rb") as file:
        btn = st.download_button(
            label="Descargar archivo con análisis",
            data=file,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.write("Asegúrate de que el archivo analysis_anp.xlsx esté en la carpeta 'data'.")

    data = data['Estado Gop'] = "VIGENTE"
    st.write("Datos Vigentes con segmentos:")
    st.write(data.head())
