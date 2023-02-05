import os
import json

import pandas as pd
from constante import Constante


class MetadataStruture:
    def __init__(self):
        constante = Constante()
        self.__directory = constante.DIRETORIO_DATA

    def save_parquet(self,  data_frame: pd.DataFrame, stage, data_name, subtitle: str = None, title: str = None):
        local = os.path.join(self.__directory, stage)
        local = os.path.join(local, data_name)
        data_frame.to_parquet(f'{local}.parquet')
        if stage == 'raw':
            self.__write_metadata(local, data_name, subtitle, title)

    def __write_metadata(self, local: str, data_name: pd.DataFrame, subtitle: str, title: str):
        dict_metadata = {
            data_name:
            {
                'subtitle': subtitle,
                'title': title
            }
        }
        content = json.dumps(dict_metadata, indent=4)
        with open(f'{local}.json', 'w') as file:
            file.write(content)


