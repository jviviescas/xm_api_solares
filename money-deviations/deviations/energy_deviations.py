from api_xm import GetDataAPI, ColumnsXM


def get_deviation_dispatch(
    metric: str,
    filters: list,
    date_init: str,
    date_end: str,
):
    """
    Get the offer prices from the API and export them in a df.

    Parameters
    ----------
    date_init : str
        Initial date to get the data.
    date_end : str
        End date to get the data.
    """

    get_data = GetDataAPI(
        metric=metric,
        frecuency_time='hourly',
        entity_time='Recurso',
        filters=filters,
        start_date=date_init,
        end_date=date_end,
    )

    get_data.post_request()
    data = get_data.data
    return data
