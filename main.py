import os

import pandas as pd
from config import *
from data_plants import get_data_of_plants_by_daily_metrics, get_data_of_plants_by_hourly_metrics

SOLAR_PLANTS = [
    "3DDT",  # LATAM SOLAR LA LOMA, FPO: 2024-06-24
    "3HF5",  # FUNDACION, FPO: 2023-02-28
    "3IRX",  # PORTON DEL SOL, FPO: 2024-03-08
    "3IZ6",  # PARQUE SOLAR LA UNION, FPO: 2024-06-19
    "EPFV",  # EL PASO, FPO: 2024-03-23
    "MATA",  # LA MATA, FPO: 2024-06-27
    "TPUY",  # PARQUE SOLAR TEPUY, FPO: 2024-06-12
    # "TCBE", # TERMOCARIBE,
    # "3INX",  # CARACOLI I, FPO: 2023-07-31
    # "3IQA", #SUNNORTE, FPO: 2022-12-31
    # "GYPO", #GUAYEPO, FPO: 2022-09-30
]


def main():
    hour_variables = [
        "Gene",
        "DispoDeclarada",
        "DispoCome",
        "GeneProgDesp",
        "GeneProgRedesp",
        "PrecOferDesp",
        "DesvGenVariableDesp",
        "DesvGenVariableRedesp",
    ]

    daily_variables = [
        "IrrPanel",
        "IrrGlobal",
        "TempAmbSolar",
    ]

    hour_data = get_data_of_plants_by_hourly_metrics(
        hour_variables,
        SOLAR_PLANTS,
        "2023-01-01",
        "2024-07-01"
    )

    daily_data = get_data_of_plants_by_daily_metrics(
        daily_variables,
        SOLAR_PLANTS,
        "2023-01-01",
        "2024-07-01"
    )

    # Join data
    hour_data.update(daily_data)

    # Save daily data
    path_to_save = os.path.join(TEMP_PATH, "data.xlsx")
    with pd.ExcelWriter(path_to_save) as writer:
        for key, value in hour_data.items():
            value.to_excel(writer, sheet_name=key)


if __name__ == '__main__':
    main()
