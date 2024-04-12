# %%
import pandas as pd
import numpy as np
from datetime import date, datetime
import locale



# %%
df1 = pd.read_csv("../input/atus_anual_2020.csv", index_col = False)
df2 = pd.read_csv("../input/atus_anual_2021.csv", index_col = False)
df3 = pd.read_csv("../input/atus_anual_2022.csv", index_col = False)

# %% [markdown]
# 1. Cargue en un Dataframe los datos de los accidentes de los últimos 3 años

# %%
df_unido = [df1, df2, df3]
df_unido = pd.concat(df_unido)

# %% [markdown]
# 2. Agregue una columna tipo date que englobe las columnas correspondientes a Año, Mes, Dia, Hora y Minuto.

# %%
df_unido['FECHA'] = df_unido.apply(lambda row: f"{row['ANIO']}-{row['MES']}-{row['ID_DIA']} {row['ID_HORA']}:{row['ID_MINUTO']}", axis=1)

df_unido['FECHA'] = pd.to_datetime(df_unido['FECHA'], format='%Y-%m-%d %H:%M')

df_unido = df_unido.drop(['ANIO', 'MES', 'ID_DIA', 'ID_HORA', 'ID_MINUTO','DIASEMANA'], axis=1)
df_unido.head()

# %% [markdown]
# 3. Agregue una columna para Área cuyos valores serán Urbana o Suburbana dependiendo del área donde ocurrió el accidente.
# 4. Agregue una columna Zona cuyos valores serán la zona donde ocurrió el accidente
# 5. Elimine las columnas URBANA y SUBURBANA

# %%
df_unido['ZONA'] = df_unido.apply(lambda row: row['URBANA'] if row['URBANA'] != 'Sin accidente en esta zona' else (row['SUBURBANA'] if row['SUBURBANA'] != 'Sin accidente en esta zona' else None), axis=1)
df_unido['URBANA'] = (df_unido['URBANA']=='Sin accidente en esta zona').astype(int)
print(df_unido.groupby("URBANA"))
df_unido['URBANA'] = df_unido['URBANA'].apply(lambda x: 'Suburbana' if x == 1 else 'Urbana')
df_unido = df_unido.drop(['SUBURBANA'], axis=1)
df_unido = df_unido.rename(columns = {'URBANA' : 'AREA'})
df_unido.head()

# %% [markdown]
# 7. Resuma los accidentes del último año por tipo y que porcentaje representan

# %%
ultimo_año = df_unido['FECHA'].dt.year.max()

datos_ultimo_año = df_unido[df_unido['FECHA'].dt.year == ultimo_año]

tipo_accidente_counts = datos_ultimo_año['TIPACCID'].value_counts().reset_index()
tipo_accidente_counts.columns = ['Tipo de Accidente', 'Count']

total_accidentes_ultimo_año = tipo_accidente_counts['Count'].sum()
tipo_accidente_counts['Porcentaje sobre el Total'] = (tipo_accidente_counts['Count'] / total_accidentes_ultimo_año) * 100

print(tipo_accidente_counts)

# %% [markdown]
# 8. Obtenga la cantidad de muertos y lesionados de los últimos 3 años

# %%
Muertos_y_lesion = pd.DataFrame()

total_m_y_l = df_unido[['CONDMUERTO','PASAMUERTO','PEATMUERTO', 'CICLMUERTO', 'OTROMUERTO', 'NEMUERTO', 'CONDHERIDO','PASAHERIDO', 'PEATHERIDO', 'CICLHERIDO', 'OTROHERIDO', 'NEHERIDO']].sum()

Muertos_y_lesion['total'] = total_m_y_l

Muertos_y_lesion['categorias'] = df_unido[['CONDMUERTO','PASAMUERTO','PEATMUERTO', 'CICLMUERTO', 'OTROMUERTO', 'NEMUERTO', 'CONDHERIDO','PASAHERIDO', 'PEATHERIDO', 'CICLHERIDO', 'OTROHERIDO', 'NEHERIDO']].columns

Muertos_y_lesion['porcentaje sobre total'] = (Muertos_y_lesion['total'] / Muertos_y_lesion['total'].sum()) * 100


print(Muertos_y_lesion)

# %% [markdown]
# 9. ¿Cómo se compara el número de accidentes de cada año contra el anterior? ¿En qué porcentaje varió?

# %%
df_unido['FECHA'] = pd.to_datetime(df_unido['FECHA'])

df_unido['AÑO'] = df_unido['FECHA'].dt.year

total_accidentes_por_año = df_unido['AÑO'].value_counts().reset_index()
total_accidentes_por_año.columns = ['AÑO', 'Total_Accidentes']

total_accidentes_por_año['Porcentaje'] = (total_accidentes_por_año['Total_Accidentes'] / total_accidentes_por_año['Total_Accidentes'].sum()) * 100

datos = df_unido.drop('AÑO', axis = 1)
print(total_accidentes_por_año)


