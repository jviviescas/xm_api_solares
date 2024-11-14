import json
import os

import pandas as pd

from main import SOLAR_PLANTS
from config import TEMP_PATH


VARIABLES: dict[str, str] = {
    "ALLSKY_SFC_SW_DWN": "Radiación",
    "CLRSKY_SFC_SW_DWN": "Radiación abierta",
    "QV2M": "Humedad relativa",
    "RH2M": "Humedad especifica",
}


def get_data(name_file):
    with open(f'data_nasa/data/{name_file}.json') as f:
        data = json.load(f)
    return data


def divide_date_to_hours_columns(df):
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date
    df['hour'] = df['date'].dt.strftime('hour_%H')
    pivot_df = df.pivot(index='day', columns='hour', values='value').reset_index()
    pivot_df = pivot_df[['day'] + [f'hour_{str(i).zfill(2)}' for i in range(24)]]

    return pivot_df


def save_dict_to_excel(name_file: str, data: dict[str, pd.DataFrame]):
    path_to_save = os.path.join(TEMP_PATH, f"{name_file}.xlsx")
    with pd.ExcelWriter(path_to_save) as writer:
        for key, value in data.items():
            value.to_excel(writer, sheet_name=key)


def process_data(file_name: str):

    results_by_variables = {
        value: pd.DataFrame()
        for value in VARIABLES.values()
    }

    for plant in SOLAR_PLANTS:

        data = get_data(plant)
        data_by_variables = data["properties"]["parameter"]

        for variable in data_by_variables.keys():

            data_by_time = data_by_variables[variable]

            data_by_time_df = pd.DataFrame(
                list(data_by_time.items()),
                columns=['date', 'value']
            )

            # Convert date_str to datetime
            data_by_time_df['date'] = pd.to_datetime(
                data_by_time_df['date'],
                format='%Y%m%d%H'
            )

            data_by_time_df = divide_date_to_hours_columns(data_by_time_df)
            data_by_time_df["plant"] = plant
            data_by_time_df = data_by_time_df[["plant"] + list(data_by_time_df.columns[:-1])]

            variable_name = VARIABLES.get(variable)

            results_by_variables[variable_name] = pd.concat(
                [results_by_variables[variable_name], data_by_time_df]
            )

    # Save data
    save_dict_to_excel(file_name, results_by_variables)


if __name__ == '__main__':
    process_data("data_metereologica")
