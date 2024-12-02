import pandas as pd

from prices import get_marginal_prices, get_offer_prices, get_spot_offer
from api_xm import ColumnsXM
from config import TEMP_PATH


def main():
    date_init = "2024-06-01"
    date_end = "2024-11-01"

    spot_offer = get_spot_offer(date_init, date_end)
    marginal_plants = get_marginal_prices(date_init, date_end)

    price_offers_format_1, price_offers_format_2 = get_offer_prices(date_init, date_end)

    # Convertir el diccionario de mapeo en un DataFrame auxiliar
    mapping_current_offers = []
    mapping_before_offers = []
    mapping_after_offers = []

    for __, row in marginal_plants.iterrows():
        date = row[ColumnsXM.date]

        current_offer_dict = {ColumnsXM.date: date}
        before_offer_dict = {ColumnsXM.date: date}
        after_offer_dict = {ColumnsXM.date: date}

        for hour in ColumnsXM.hours:
            plant = row[hour]
            date_dict = price_offers_format_1[date]
            if plant not in date_dict:
                continue

            plant_dict = date_dict[plant]
            plant_id = plant_dict[ColumnsXM.id]

            current_offer_dict[hour] = plant_dict[ColumnsXM.plant_offer]
            before_offer_dict[hour] = price_offers_format_2[date][plant_id-1][ColumnsXM.plant_offer]
            after_offer_dict[hour] = price_offers_format_2[date][plant_id+1][ColumnsXM.plant_offer]

        mapping_current_offers.append(current_offer_dict)
        mapping_before_offers.append(before_offer_dict)
        mapping_after_offers.append(after_offer_dict)

    df_current_offers = pd.DataFrame(mapping_current_offers)
    df_before_offers = pd.DataFrame(mapping_before_offers)
    df_after_offers = pd.DataFrame(mapping_after_offers)

    # save in a excel with multiple sheets
    with pd.ExcelWriter(TEMP_PATH+"/ofertas.xlsx") as writer:
        spot_offer.to_excel(writer, sheet_name='precio_bolsa', index=False)
        df_current_offers.to_excel(writer, sheet_name='oferta_marginal', index=False)
        df_before_offers.to_excel(writer, sheet_name='oferta_marginal_anterior', index=False)
        df_after_offers.to_excel(writer, sheet_name='oferta_marginal_posterior', index=False)


if __name__ == '__main__':
    main()
