import pandas as pd

from deviations import get_national_offer_price, get_offer_prices, get_deviation_dispatch, operation_between_df, get_deviation_by_plant
from api_xm import ColumnsXM
from config import TEMP_PATH, PLANT_NAME

pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('future.no_silent_downcasting', True)


def main():
    date_init = "2024-06-01"
    date_end = "2024-10-01"
    plants = list(PLANT_NAME.keys())

    national_price = get_national_offer_price(date_init, date_end)
    offer_plants = get_offer_prices(plants, date_init, date_end)
    gen_real = get_deviation_dispatch("Gene", plants, date_init, date_end)
    dispatch = get_deviation_dispatch("GeneProgDesp", plants, date_init, date_end)
    redispatch = get_deviation_dispatch("GeneProgRedesp", plants, date_init, date_end)
    deviation_dispatch = get_deviation_dispatch("DesvGenVariableDesp", plants, date_init, date_end)
    deviation_redispatch = get_deviation_dispatch("DesvGenVariableRedesp", plants, date_init, date_end)

    # with pd.ExcelWriter("/desviaciones.xlsx") as writer:
    #     gen_real.to_excel(writer, sheet_name="Gene", index=False)
    #     dispatch.to_excel(writer, sheet_name="GeneProgDesp", index=False)
    #     redispatch.to_excel(writer, sheet_name="GeneProgRedesp", index=False)
    #     deviation_dispatch.to_excel(writer, sheet_name="DesvGenVariableDesp", index=False)
    #     deviation_redispatch.to_excel(writer, sheet_name="DesvGenVariableRedesp", index=False)

    gen_real.replace("", 0, inplace=True)
    dispatch.replace("", 0, inplace=True)
    redispatch.replace("", 0, inplace=True)
    deviation_dispatch.replace("", 0, inplace=True)
    deviation_redispatch.replace("", 0, inplace=True)

    results = {}
    for plant in plants:
        offer_plant = offer_plants[offer_plants[ColumnsXM.plant_code] == plant]
        difference_prices = operation_between_df(offer_plant, national_price, "sub")

        # Dinero realizando el calculo paso a paso

        deviation_dispatch_by_plant = get_deviation_by_plant(
            gen_real[gen_real[ColumnsXM.plant_code] == plant],
            dispatch[dispatch[ColumnsXM.plant_code] == plant],
            0.15
        )

        deviation_redispatch_by_plant = get_deviation_by_plant(
            gen_real[gen_real[ColumnsXM.plant_code] == plant],
            redispatch[redispatch[ColumnsXM.plant_code] == plant],
            0.08
        )

        deviation_dispatch_by_plant = deviation_dispatch[deviation_dispatch[ColumnsXM.plant_code] == plant]
        deviation_redispatch_by_plant = deviation_redispatch[deviation_redispatch[ColumnsXM.plant_code] == plant]

        # Dinero con las variables de xm
        money_dispatch = operation_between_df(deviation_dispatch_by_plant, difference_prices, "mul")
        monet_redispatch = operation_between_df(deviation_redispatch_by_plant, difference_prices, "mul")

        deviation_dispatch_by_plant["Energía_Despacho"] = deviation_dispatch_by_plant[ColumnsXM.hours].sum(axis=1)
        deviation_redispatch_by_plant["Energía_Redespacho"] = deviation_redispatch_by_plant[ColumnsXM.hours].sum(axis=1)
        money_dispatch["Dinero_Despacho"] = money_dispatch[ColumnsXM.hours].sum(axis=1)
        monet_redispatch["Dinero_Redespacho"] = monet_redispatch[ColumnsXM.hours].sum(axis=1)

        merge_energy = pd.merge(
            deviation_dispatch_by_plant[[ColumnsXM.date, "Energía_Despacho"]],
            deviation_redispatch_by_plant[[ColumnsXM.date, "Energía_Redespacho"]],
            on=ColumnsXM.date,
            how="outer"
        )
        merge_money = pd.merge(
            money_dispatch[[ColumnsXM.date, "Dinero_Despacho"]],
            monet_redispatch[[ColumnsXM.date, "Dinero_Redespacho"]],
            on=ColumnsXM.date,
            how="outer"
        )

        merge_energy_money = pd.merge(merge_energy, merge_money, on=ColumnsXM.date, how="outer")

        results[plant] = merge_energy_money

    # with pd.ExcelWriter(TEMP_PATH+f"/desviaciones.xlsx") as writer:
        # for plant in results:
        # results[plant].to_excel(writer, sheet_name=PLANT_NAME[plant], index=False)

    results_concat = pd.DataFrame()
    for plant in results:
        sub_results = results[plant]
        sub_results[ColumnsXM.plant_code] = PLANT_NAME[plant]
        results_concat = pd.concat([results_concat, sub_results])

    results_concat.to_excel(TEMP_PATH+f"/desviaciones.xlsx", index=False)


if __name__ == '__main__':
    main()
