import requests,os
import pandas as pd

base_url = "https://www.imhpa.gob.pa/es/datos-diarios"

def download_csv(year, month):
    url = f"{base_url}?estacion=12&mes={month}&ano={year}&csv=1"
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"las_tablas_data_{year}_{month:02d}.csv"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"Archivo guardado: {filename}")

        # Leer archivo csv completo
        df = pd.read_csv(filename)

        # Excluir las últimas 3 filas
        df = df[:-3]
        df['year'] = year
        df['month'] = month
        df.fillna(0, inplace=True)
        renombrar_cols = {
                    'Día': 'Dia',
                    'Temperaturas (°C) Máxima': 'TempMax',
                    'Temperaturas (°C) Mínima': 'TempMin',
                    'Temperaturas (°C) Promedio': 'TempProm',
                    'Lluvia Diaria mm (litros/m²) Mes Actual': 'LluviaMesActual',
                    'Lluvia Diaria mm (litros/m²) Acum. Actual': 'lluviaAcumActual',
                     'Lluvia Diaria mm (litros/m²) Promedio Histórico': 'LluviaAcumPromHistorico',
                     'Lluvia Diaria mm (litros/m²) Acum. Promedio Histórico': 'LluviaAcumPromHistorico'
                }

        df.rename(columns=renombrar_cols, inplace=True)
        print("numero de filas:", len(df))
        df.to_csv(f"./files/las_tablas/{filename}", index=False,encoding='utf-8')
        os.remove(filename)
        print(f"Archivo movido a ./files/las_tablas/{filename}")

    else:
        print(f"Error descargando archivo para las_tablas_{year}-{month:02d}")

for year in range(2016, 2026):
    for month in range(1, 13):
        download_csv(year, month)
