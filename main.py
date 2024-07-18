from scripts import export_data_by_concept, get_deviation, plot_excel
from config import TEMP_PATH, IMAGE_PATH

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

HOUR_VARS = [
    "Gene",
    "DispoDeclarada",
    "DispoCome",
    "GeneProgDesp",
    "GeneProgRedesp",
    "PrecOferDesp",
    "DesvGenVariableDesp",
    "DesvGenVariableRedesp",
]

DAILY_VARS = [
    "IrrPanel",
    "IrrGlobal",
    "TempAmbSolar",
]

OPERATION_DATE = {
    "TPUY": "2024-06-12",
    "3IRX": "2024-03-08",
    "3HF5": "2024-06-24",
    "MATA": "2024-06-27",
    "3IZ6": "2024-06-19",
    "3DDT": "2024-06-24",
    "EPFV": "2024-03-23"
}


def main():
    init_date = "2024-01-01"
    end_date = "2024-07-18"
    data_file_name = "data_by_concept"
    deviation_file_name = "desviaciones"

    # export_data_by_concept(
    #     SOLAR_PLANTS,
    #     HOUR_VARS,
    #     DAILY_VARS,
    #     init_date,
    #     end_date,
    #     data_file_name
    # )

    # get_deviation(
    #     data_file_name,
    #     deviation_file_name,
    #     HOUR_VARS[0],
    #     HOUR_VARS[3],
    #     HOUR_VARS[4],
    #     OPERATION_DATE
    # )

    # plot_excel(
    #     deviation_file_name,
    #     "desvGeneProgDesp_by_plant",
    #     export_path=IMAGE_PATH,
    #     title="Desviación de la generación programada despacho",
    #     title_eje_y="Desviación"
    # )

    plot_excel(
        "error_magnitude_consolidated",
        export_path=IMAGE_PATH,
        title="Error en la desviación",
        title_eje_y="Desviación"
    )


if __name__ == '__main__':
    main()
