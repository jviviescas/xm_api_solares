from api_xm import GetDataAPI


def main():
    get_data = GetDataAPI(
        metric='PrecPromContRegu',
        frecuency_time='hourly',
        entity_time='Sistema',
        filters=[],
        start_date='2024-01-1',
        end_date='2024-12-31',
    )
    get_data.post_request()

    get_data.export_excel("Precio_Medio_Contratos", "./")


if __name__ == '__main__':
    main()
