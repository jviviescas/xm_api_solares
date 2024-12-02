from api_xm import GetDataAPI, ColumnsXM


def get_marginal_prices(date_init: str, date_end: str):
    """
    Get the marginal prices from the API and export them to an Excel file.

    Parameters
    ----------
    date_init : str
        Initial date to get the data.
    date_end : str
        End date to get the data.
    """

    get_data = GetDataAPI(
        metric='IndRecMargina',
        frecuency_time='hourly',
        entity_time='Recurso',
        filters=None,
        start_date=date_init,
        end_date=date_end,
    )
    get_data.post_request()

    data = get_data.data
    for column in ColumnsXM.hours:
        data[column] = data.apply(
            lambda row: row[ColumnsXM.plant_code] if row[column] == 1 else None,
            axis=1
        )

    data.drop(columns=[ColumnsXM.plant_code, ColumnsXM.id], inplace=True)

    # Concatenate the values of each day in order to get only a one day and plant
    data_group = data.groupby(ColumnsXM.date).sum()
    data_group = data_group.reset_index()

    return data_group
