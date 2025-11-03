import pandas as pd
import numpy as np

# --- CONFIGURACIÓN ---
# Archivos de entrada (los que tienes ahora)
FILE_A_IN = 'documentos_generados/PCOS_data_transformado.csv'
FILE_B_IN = 'notebooks/PCOS_data_FINAL_sin_multicolinealidad.csv'

# Archivos de salida (los nuevos que se van a crear)
FILE_A_OUT = 'PCOS_data_transformado_LIMPIO.csv'
FILE_B_OUT = 'PCOS_data_FINAL_sin_multicolinealidad_LIMPIO.csv'

TARGET_COL = 'SOP (S/N)'
# ---------------------

def limpiar_columna_robusta(col_series):
    """
    Toma una serie de pandas, la fuerza a string,
    limpia los corchetes y la convierte a numérico.
    Esta es la función que soluciona el error '[5E-1]'.
    """
    # 1. Forzar la columna a tipo string (para encontrar texto escondido)
    col_str = col_series.astype(str)
    
    # 2. Limpiar corchetes y espacios
    col_limpia = col_str.str.replace('[', '', regex=False) \
                         .str.replace(']', '', regex=False) \
                         .str.strip()
    
    # 3. Convertir a numérico. Todo lo que no sea un número se volverá NaN.
    #    'coerce' es la clave.
    col_numerica = pd.to_numeric(col_limpia, errors='coerce')
    
    return col_numerica

def procesar_dataset(archivo_in, archivo_out):
    """
    Proceso completo: Cargar, Limpiar, Imputar y Guardar.
    """
    print(f"Procesando: {archivo_in}...")
    
    try:
        df = pd.read_csv(archivo_in)
    except FileNotFoundError:
        print(f"--- ERROR ---")
        print(f"No se encontró el archivo '{archivo_in}'.")
        print("Asegúrate de que este script esté en la misma carpeta que tus CSVs.")
        print("--------------------------------------------------")
        return

    # 1. Identificar columnas de features (todas menos el target)
    if TARGET_COL not in df.columns:
        print(f"--- ERROR ---")
        print(f"El dataset no contiene la columna objetivo: '{TARGET_COL}'")
        print("--------------------------------------------------")
        return
        
    features_cols = [col for col in df.columns if col != TARGET_COL]
    
    # 2. Aplicar la limpieza robusta a CADA feature
    print("  Limpiando valores no numéricos (ej. '[5E-1]')...")
    for col in features_cols:
        df[col] = limpiar_columna_robusta(df[col])

    # 3. Imputar (rellenar) NaNs creados por la limpieza
    #    (Usamos la mediana, que es robusto a outliers)
    print("  Rellenando valores nulos/faltantes con la mediana...")
    nans_totales = 0
    for col in features_cols:
        if df[col].isnull().any():
            nans_col = df[col].isnull().sum()
            nans_totales += nans_col
            mediana = df[col].median()
            df[col] = df[col].fillna(mediana)
            
    if nans_totales > 0:
        print(f"  Se corrigieron {nans_totales} valores nulos/problemáticos.")
    else:
        print("  El dataset ya estaba limpio.")

    # 4. Guardar el nuevo archivo LIMPIO
    df.to_csv(archivo_out, index=False)
    print(f"✓ ¡Éxito! Guardado como: {archivo_out}")
    print("--------------------------------------------------")

# --- EJECUTAR EL PROCESO ---
if __name__ == "__main__":
    print("Iniciando script de limpieza de datasets...")
    print("==================================================")
    procesar_dataset(FILE_A_IN, FILE_A_OUT)
    procesar_dataset(FILE_B_IN, FILE_B_OUT)
    print("==================================================")
    print("Limpieza completada. Ya puedes usar los archivos '_LIMPIO.csv' en tu notebook.")