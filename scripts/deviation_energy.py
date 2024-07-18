import warnings
import pandas as pd
import numpy as np


from config import TEMP_PATH


TOTAL_GENERATION = "Total_Generation"
TOTAL_PROGRAM = "Total_Program"
TOTAL_DEVIATION = "Total_Deviation"
PERCENTAGE_DEVIATION = "Percentage_Deviation"
DATE_COL = "Date"
PLANT_COL = "Values_code"


def trim_nan_edges(data_list):
    start = 0
    end = len(data_list)

    # Encuentra el primer índice que no es NaN
    while start < end and (np.isnan(data_list[start]) or data_list[start] == 0):
        start += 1

    # Encuentra el último índice que no es NaN
    while end > start and (np.isnan(data_list[end - 1]) or data_list[end - 1] == 0):
        end -= 1

    return data_list[start:end]


def calculate_deviation(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    hour_columns: list[str],
    limit_dates: dict[str, str],
):
    # Ignorar el SettingWithCopyWarning
    warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)
    warnings.simplefilter(action='ignore', category=FutureWarning)

    # total generation
    df1[TOTAL_GENERATION] = df1[hour_columns].abs().sum(axis=1)
    df2[TOTAL_PROGRAM] = df2[hour_columns].abs().sum(axis=1)

    # merge dataframes gen_data and gen_prog_desp_data
    data_deviation = pd.DataFrame(columns=df1.columns)
    for __, row in df1.iterrows():
        date = row[DATE_COL]
        values_code = row[PLANT_COL]

        row2 = df2[
            (df2[DATE_COL] == date) & (df2[PLANT_COL] == values_code)
        ]
        if row2.empty:
            continue
        data2_list_hours = row2[hour_columns].values.tolist()[0]
        data2_list_hours = trim_nan_edges(data2_list_hours)
        data_2_continuous = [
            False if data2_list_hours[i-1] > 0 and (data2_list_hours[i] <= 0 or data2_list_hours[i] != data2_list_hours[i])
            else True
            for i in range(len(data2_list_hours)-1)
        ]
        is_data_2_continuous = all(data_2_continuous)
        if not is_data_2_continuous:
            continue

        for hour in hour_columns:
            value1 = row[hour]
            value2 = row2[hour].values[0]

            if value2 == 0 or value2 != value2:
                row[hour] = 0
            else:
                row[hour] = value1 - value2

        row[TOTAL_PROGRAM] = row2[TOTAL_PROGRAM].values[0]
        data_deviation = data_deviation._append(row, ignore_index=True)

    # delete rows who has a date minor than the limit date
    # Convert Date columns to datetime
    data_deviation[DATE_COL] = pd.to_datetime(data_deviation[DATE_COL])
    operation_date = {k: pd.to_datetime(v) for k, v in limit_dates.items()}

    # Filter the DataFrame
    filtered_df = data_deviation[data_deviation.apply(
        lambda row:
        row[DATE_COL] >= operation_date.get(row[PLANT_COL], pd.Timestamp('1970-01-01')), axis=1
    )]

    # Get percentage of deviation
    filtered_df[TOTAL_DEVIATION] = filtered_df[hour_columns].abs().sum(axis=1)
    filtered_df.loc[:, PERCENTAGE_DEVIATION] = (filtered_df[TOTAL_DEVIATION] / filtered_df[TOTAL_GENERATION])

    # leave the format of theDATE_COLas a string
    filtered_df[DATE_COL] = filtered_df[DATE_COL].dt.strftime('%Y-%m-%d')

    # move columns hours to the end of the dataframe
    filtered_df = filtered_df[
        [col for col in filtered_df.columns if col not in hour_columns] +
        hour_columns
    ]

    return filtered_df


def get_deviation(
    file_name: str,
    file_export_name: str,
    gen_sheet_name: str,
    gen_prog_desp_sheet_name: str,
    gen_prog_redesp_sheet_name: str,
    limit_dates: dict[str, str],
):
    file_path = TEMP_PATH + file_name + ".xlsx"
    file_export_path = TEMP_PATH + file_export_name + ".xlsx"

    # import dataframe for each sheet
    gen_data = pd.read_excel(file_path, sheet_name=gen_sheet_name, index_col=0)
    gen_prog_desp_data = pd.read_excel(file_path, sheet_name=gen_prog_desp_sheet_name, index_col=0)
    gen_prog_redesp_data = pd.read_excel(file_path, sheet_name=gen_prog_redesp_sheet_name, index_col=0)

    hour_columns = [col for col in gen_data.columns if 'Hour' in col]

    # Calculate deviation
    deviation_gen_prog_desp = calculate_deviation(
        gen_data,
        gen_prog_desp_data,
        hour_columns,
        limit_dates,
    )

    deviation_gen_prog_desp_by_plant = deviation_gen_prog_desp.pivot(
        index=DATE_COL,
        columns=PLANT_COL,
        values=PERCENTAGE_DEVIATION,
    )
    deviation_gen_prog_desp_by_plant.reset_index(inplace=True)

    deviation_gen_prog_redesp = calculate_deviation(
        gen_data,
        gen_prog_redesp_data,
        hour_columns,
        limit_dates,
    )

    deviation_gen_prog_redesp_by_plant = deviation_gen_prog_redesp.pivot(
        index=DATE_COL,
        columns=PLANT_COL,
        values=PERCENTAGE_DEVIATION,
    )
    deviation_gen_prog_redesp_by_plant.reset_index(inplace=True)

    # Create a new excel and export the data in two sheets
    with pd.ExcelWriter(file_export_path) as writer:
        deviation_gen_prog_desp.to_excel(
            writer,
            sheet_name="desv" + gen_prog_desp_sheet_name
        )

        deviation_gen_prog_desp_by_plant.to_excel(
            writer,
            sheet_name="desv" + gen_prog_desp_sheet_name + "_by_plant"
        )

        deviation_gen_prog_redesp.to_excel(
            writer,
            sheet_name="desv" + gen_prog_redesp_sheet_name
        )

        deviation_gen_prog_redesp_by_plant.to_excel(
            writer,
            sheet_name="desv" + gen_prog_redesp_sheet_name + "_by_plant"
        )
