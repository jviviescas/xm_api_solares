import pandas as pd
from api_xm import ColumnsXM


def operation_between_df(df1, df2, operation):

    df = pd.merge(df1, df2, on=ColumnsXM.date, suffixes=('_plant', '_national'))
    df.replace("", 0, inplace=True)

    for hour in ColumnsXM.hours:
        if operation == "sum":
            df[hour] = df[hour + "_plant"] + df[hour + "_national"]
        elif operation == "sub":
            df[hour] = abs(df[hour + "_plant"] - df[hour + "_national"])
        elif operation == "mul":
            df[hour] = df[hour + "_plant"] * df[hour + "_national"]
        elif operation == "div":
            df[hour] = df[hour + "_plant"] / df[hour + "_national"]
        else:
            raise ValueError("operation not found")

    return df[[ColumnsXM.date] + ColumnsXM.hours]
