import os
import datetime
import pandas as pd
from constante import Constante
from metadata_structure import MetadataStruture



dict_data_frame = {}
constante = Constante()
structure = MetadataStruture()
raw = constante.DIRETORIO_DATA_RAW
formato = '.parquet'


def get_date(line):
    year = line.year
    month = str(months.index(line.month) + 1).zfill(2)
    day = '01'
    _date_str = f'{year}-{month}-{day}'
    _date = datetime.date.fromisoformat(_date_str)
    return _date


for file in os.listdir(raw):
    if file.endswith(formato):
        file_path = os.path.join(raw, file)
        data_frame = pd.read_parquet(file_path)
        dict_data_frame[file.replace(formato, '')] = data_frame

for column, df in dict_data_frame.items():
    months = list(df.columns)
    df = df.reset_index().rename(columns={'index': 'year'})

    df = df.melt(id_vars='year', value_vars=months)
    df.value = df.value.astype('float32')
    df.rename(columns={'variable': 'month', 'value': column}, inplace=True)
    dict_data_frame[column] = df

df_merge = pd.DataFrame()
for _, df in dict_data_frame.items():
    if df_merge.empty:
        df_merge = df
    else:
        df_merge = pd.merge(left=df_merge, right=df, how='inner', on=['year', 'month'])

df_merge['date'] = df_merge.apply(get_date,axis=1)
df_merge['year'] = df_merge.year.astype(int)
df_merge['date'] = pd.to_datetime(df_merge.date)
df_merge['month'] = df_merge.date.dt.month
df_merge.dropna(inplace=True)
structure.save_parquet(data_frame=df_merge,
                        stage='processed',
                        data_name='processed')



