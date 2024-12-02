class ColumnsXM:
    id = "Id"
    plant_code = "Values_code"
    plant_offer = "Offer"
    date = "Date"
    hours = [f"Values_Hour{x:02}" for x in range(1, 25)]
