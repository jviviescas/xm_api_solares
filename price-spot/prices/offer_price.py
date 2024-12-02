from api_xm import GetDataAPI, ColumnsXM


def get_offer_prices(
    date_init: str,
    date_end: str
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
        metric='PrecOferDesp',
        frecuency_time='hourly',
        entity_time='Recurso',
        filters=None,
        start_date=date_init,
        end_date=date_end,
    )

    get_data.post_request()

    data = get_data.data
    data[ColumnsXM.plant_offer] = data[ColumnsXM.hours[0]]
    data.drop(columns=[ColumnsXM.id] + ColumnsXM.hours, inplace=True)
    data.sort_values(by=[ColumnsXM.date, ColumnsXM.plant_offer], inplace=True)
    data.reset_index(drop=True, inplace=True)

    # Convertir a la estructura de diccionarios anidados
    result_dict: dict = {}
    results2_dict: dict = {}

    for index, row in data.iterrows():
        date = row[ColumnsXM.date]
        code = row[ColumnsXM.plant_code]
        offer = row[ColumnsXM.plant_offer]
        if date not in result_dict:
            result_dict[date] = {}
            results2_dict[date] = {}

        result_dict[date][code] = {
            ColumnsXM.id: index,
            ColumnsXM.plant_offer: offer
        }
        results2_dict[date][index] = {
            ColumnsXM.plant_code: code,
            ColumnsXM.plant_offer: offer
        }

    return result_dict, results2_dict
