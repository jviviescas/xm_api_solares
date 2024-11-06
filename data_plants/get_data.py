import pandas as pd

from api_xm import GetDataAPI


def get_data_of_plants_by_hourly_metrics(
    metrics: list[str],
    plants: list[str],
    start_date: str,
    end_date: str,

) -> dict[str, pd.DataFrame]:

    data = {}
    for metric in metrics:
        get_data = GetDataAPI(
            metric=metric,
            frecuency_time='hourly',
            entity_time='Recurso',
            filters=plants,
            start_date=start_date,
            end_date=end_date,
        )
        get_data.post_request()
        data[metric] = get_data.data

    return data


def get_data_of_plants_by_daily_metrics(
    metrics: list[str],
    plants: list[str],
    start_date: str,
    end_date: str,

) -> dict[str, pd.DataFrame]:

    data = {}
    for metric in metrics:
        get_data = GetDataAPI(
            metric=metric,
            frecuency_time='daily',
            entity_time='Recurso',
            filters=plants,
            start_date=start_date,
            end_date=end_date,
        )
        get_data.post_request()
        data[metric] = get_data.data

    return data


def get_data_of_system_by_hourly_metrics(
    metrics: list[str],
    start_date: str,
    end_date: str,

) -> dict[str, pd.DataFrame]:

    data = {}
    for metric in metrics:
        get_data = GetDataAPI(
            metric=metric,
            frecuency_time='hourly',
            entity_time='Sistema',
            filters=[],
            start_date=start_date,
            end_date=end_date,
        )
        get_data.post_request()
        data[metric] = get_data.data

    return data
