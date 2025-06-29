"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """
    import os
    import pandas as pd

    # Definir rutas de archivos
    ruta_entrada = 'files/input/solicitudes_de_credito.csv'
    directorio_salida = 'files/output'
    ruta_salida = os.path.join(directorio_salida, 'solicitudes_de_credito.csv')
    
    # Cargar el dataset
    df = pd.read_csv(ruta_entrada, sep=';')
    
    # === LIMPIEZA INICIAL ===
    # Eliminar columna de índice innecesaria
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    
    # Remover registros con valores faltantes
    df.dropna(inplace=True)
    
    # Eliminar registros duplicados (primera pasada)
    df.drop_duplicates(inplace=True)

    # === NORMALIZACIÓN DE FECHAS ===
    # Dividir la fecha en componentes para manejar diferentes formatos
    df[['día', 'mes', 'año']] = df['fecha_de_beneficio'].str.split('/', expand=True)
    
    # Corregir casos donde el formato es año/mes/día (año tiene menos de 4 dígitos significa que está mal ubicado)
    mascara_formato_invertido = df['año'].str.len() < 4
    df.loc[mascara_formato_invertido, ['día', 'año']] = df.loc[mascara_formato_invertido, ['año', 'día']].values
    
    # Reconstruir fecha en formato estándar YYYY-MM-DD
    df['fecha_de_beneficio'] = df['año'] + '-' + df['mes'] + '-' + df['día']
    
    # Limpiar columnas temporales
    df.drop(['día', 'mes', 'año'], axis=1, inplace=True)

    # === ESTANDARIZACIÓN DE CAMPOS CATEGÓRICOS ===
    # Normalizar columnas de texto categóricas a minúsculas y limpiar caracteres especiales
    columnas_categoricas = ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito']
    df[columnas_categoricas] = df[columnas_categoricas].apply(
        lambda col: col.str.lower().replace(['-', '_'], ' ', regex=True).str.strip()
    )
    
    # Normalizar barrio por separado (puede tener tratamiento diferente)
    df['barrio'] = df['barrio'].str.lower().replace(['-', '_'], ' ', regex=True)

    # === LIMPIEZA DE MONTOS MONETARIOS ===
    # Remover símbolos monetarios y espacios del campo de monto
    df['monto_del_credito'] = df['monto_del_credito'].str.replace("[$, ]", "", regex=True).str.strip()
    
    # Convertir a formato numérico manejando errores
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'], errors='coerce')
    
    # Rellenar valores faltantes con 0 y convertir a entero
    df['monto_del_credito'] = df['monto_del_credito'].fillna(0).astype(int)
    
    # Convertir de vuelta a string limpio (sin decimales)
    df['monto_del_credito'] = df['monto_del_credito'].astype(str).str.replace('.00', '')

    # === LIMPIEZA FINAL ===
    # Segunda pasada para eliminar duplicados que puedan haber surgido después de la normalización
    df.drop_duplicates(inplace=True)
   
    # === EXPORTACIÓN ===
    # Crear directorio de salida si no existe
    os.makedirs(directorio_salida, exist_ok=True)
    
    # Guardar dataset limpio
    df.to_csv(ruta_salida, sep=';', index=False)


if __name__ == "__main__":
    pregunta_01()