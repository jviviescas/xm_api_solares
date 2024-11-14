import os
import pandas as pd

from data_plants import *
from config import TEMP_PATH


def export_data_by_concept(
    plants: list[str],
    hour_variables: list[str],
    daily_variables: list[str],
    start_date: str,
    end_date: str,
    file_name: str,
    hour_system_variables: list[str] = [],
):

    hour_data = get_data_of_plants_by_hourly_metrics(
        hour_variables,
        plants,
        start_date,
        end_date
    )

    daily_data = get_data_of_plants_by_daily_metrics(
        daily_variables,
        plants,
        start_date,
        end_date
    )

    hour_system_data = get_data_of_system_by_hourly_metrics(
        hour_system_variables,
        start_date,
        end_date
    )

    # Join data
    hour_data.update(daily_data)
    hour_data.update(hour_system_data)

    # Save daily data
    path_to_save = os.path.join(TEMP_PATH, f"{file_name}.xlsx")
    with pd.ExcelWriter(path_to_save) as writer:
        for key, value in hour_data.items():
            value.to_excel(writer, sheet_name=key)
