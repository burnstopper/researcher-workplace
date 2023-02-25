from pathlib import Path

import pandas as pd
import numpy as np

from loader.errors import LazarusKeysLoadingError

__loaded_df = None

def load_coping_calc_table() -> pd.DataFrame:
    """Loads dataframe for calculating coping strategies.
    Schema:
    | sex | age | score | indicator | t_score |
    | --- | --- | ----- | --------- | ------- |
    | str | str |  int  |    str    |   int   |

    The dataframe is loaded only at first call.
    Result is cached and every new call returns the copy of previously loaded dataframe.

    Exceptions:
     - LazarusKeysLoadingError is raised when dataframe loading failed.
    """
    global __loaded_df

    if __loaded_df is None:
        folder = Path(__file__).resolve().parent
        calc_table_file = folder / 'calc_table.xlsx'
        try:
            __loaded_df = pd.read_excel(
                calc_table_file, 
                sheet_name='Main',
                dtype={
                    'sex': str,
                    'age': str,
                    'score': np.int32,
                    'indicator': str,
                    't_score': np.int32
                })
            __loaded_df.reset_index(drop=True, inplace=True)
        except Exception as e:
            raise LazarusKeysLoadingError(f"Cannot load lazarus keys from file {calc_table_file}", e)
    
    return __loaded_df.copy()
