from scripts import export_data_by_concept, get_deviation, plot_excel
from config import TEMP_PATH, IMAGE_PATH

SOLAR_PLANTS = [
    # "3DDT",  # LATAM SOLAR LA LOMA, FPO: 2024-06-24
    # "3HF5",  # FUNDACION, FPO: 2023-02-28
    "3IRX",  # PORTON DEL SOL, FPO: 2024-03-08
    # "3IZ6",  # PARQUE SOLAR LA UNION, FPO: 2024-06-19
    # "EPFV",  # EL PASO, FPO: 2024-03-23
    # "MATA",  # LA MATA, FPO: 2024-06-27
    # "TPUY",  # PARQUE SOLAR TEPUY, FPO: 2024-06-12
    # "TCBE", # TERMOCARIBE,
    # "3INX",  # CARACOLI I, FPO: 2023-07-31
    # "3IQA", #SUNNORTE, FPO: 2022-12-31
    # "GYPO", #GUAYEPO, FPO: 2022-09-30
]

EOLICS_PLANTS: list = [
    # "3DDT",  # LATAM SOLAR LA LOMA, FPO: 2024-06-24
    # "APHA",  # FUTURA - PARQUE ALPHA
    # "APLU",  # FUTURA - APOTOLORRU
    # "BETA",  # FUTURA - PARQUE BETA
    # "CELE",  # FUTURA - CASA ELECTRICA
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
    "DesvMoneda",
]

HOUR_SYSTEM_VARS = [
    "PrecBolsNaci"
]


DAILY_VARS: list = [
    # "IrrPanel",
    # "IrrGlobal",
    # "TempAmbSolar",
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
    init_date = "2023-01-01"
    end_date = "2024-12-01"
    data_file_name = "data_by_concept"
    deviation_file_name = "desviaciones"

    export_data_by_concept(
        SOLAR_PLANTS,
        HOUR_VARS,
        DAILY_VARS,
        init_date,
        end_date,
        data_file_name,
        hour_system_variables=HOUR_SYSTEM_VARS,
    )

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

    # plot_excel(
    #     "data_by_concept",
    #     sheet_name="2024-03-28",
    #     export_path=IMAGE_PATH,
    #     export_file_name="energia_el_paso_2024-03-28",
    #     title="El Paso 2024-03-28",
    #     title_eje_x="Hora",
    #     title_eje_y="Energía [kWh]"
    # )


if __name__ == '__main__':
    main()
