from api_xm import GetDataAPI, ColumnsXM


def get_spot_offer(
    date_init: str,
    date_end: str
):
    """
    Get the spot offer national price from the API and export them in a df.

    Parameters
    ----------
    date_init : str
        Initial date to get the data.
    date_end : str
        End date to get the data.
    """

    get_data = GetDataAPI(
        metric='PrecBolsNaci',
        frecuency_time='hourly',
        entity_time='Sistema',
        filters=None,
        start_date=date_init,
        end_date=date_end,
    )

    get_data.post_request()

    data = get_data.data
    data.drop([ColumnsXM.id, ColumnsXM.plant_code], axis=1, inplace=True)

    return data
