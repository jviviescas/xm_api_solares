import pandas as pd

from api_xm import ColumnsXM


def get_deviation_by_plant(
    real_generation: pd.DataFrame,
    dispatch: pd.DataFrame,
    limit: float = 0.15,
) -> pd.DataFrame:

    real_generation["Total_RG"] = real_generation[ColumnsXM.hours].sum(axis=1)
    dispatch["Total_D"] = dispatch[ColumnsXM.hours].sum(axis=1)

    deviation = pd.merge(
        real_generation,
        dispatch,
        on=ColumnsXM.date,
        how="outer",
        suffixes=("_RG", "_D")
    )

    deviation["Desviación"] = deviation.apply(
        lambda x: abs(x["Total_RG"] - x["Total_D"]) / x["Total_D"] if x["Total_D"] != 0 else 1,
        axis=1
    )

    result = deviation.apply(
        lambda x: get_limits_exceeded(x, limit),
        axis=1
    )

    return result


def get_limits_exceeded(
    row: pd.Series,
    limit: float,
):
    for hour in ColumnsXM.hours:
        row[hour] = 0

    if not row["Desviación"] > limit:
        return row[[ColumnsXM.date] + ColumnsXM.hours]

    if row["Desviación"] > 0.20:
        tolerance = 0.05
    else:
        tolerance = 0.25 - row["Desviación"]

    if limit == 0.08:
        if row["Desviación"] > 0.15:
            tolerance = 0.05
        else:
            tolerance = 110/7 - 5/7 * row["Desviación"] * 100
            tolerance = tolerance / 100

    for hour in ColumnsXM.hours:
        hour_deviation = abs(row[hour + "_RG"] - row[hour + "_D"])
        percentage_hour_deviation = hour_deviation/row[hour + "_D"] if row[hour + "_D"] != 0 else 1

        if not percentage_hour_deviation >= tolerance:
            hour_deviation = 0

        row[hour] = hour_deviation

    return row[[ColumnsXM.date] + ColumnsXM.hours]
