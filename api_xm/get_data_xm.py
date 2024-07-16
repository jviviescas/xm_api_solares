import datetime as dt
from typing import Literal
import os
import requests
import json

import pandas as pd

import config


class GetDataAPI():

    def __init__(
        self,
        metric: str,
        frecuency_time: Literal["hourly", "daily", "monthly", "annual", "lists"],
        entity_time: Literal["Agente", "Recurso", "Sistema"],
        filters: list | None,
        start_date: str,
        end_date: str
    ) -> None:

        self.metric = metric
        self.frecuency_time = frecuency_time
        self.filters = filters
        self.start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
        self.end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
        self.entity_time = entity_time
        self.data = pd.DataFrame()

    def post_request(self):
        values_frecuency = {
            'hourly': 'HourlyEntities',
            'daily': 'DailyEntities',
            'monthly': 'MonthlyEntities',
            'annual': 'AnnualEntities',
            'lists': 'ListEntities'
        }

        max_amount_days_category = {
            'hourly': 30,
            'daily': 30,
            'monthly': 731,
            'annual': 366,
            'lists': 366
        }

        value_type = values_frecuency[self.frecuency_time]
        max_days = max_amount_days_category[self.frecuency_time]

        url = f'http://servapibi.xm.com.co/{self.frecuency_time}'

        start = self.start_date
        end = self.end_date
        aux = True
        data = None
        condition = True

        while condition:
            if (start - self.end_date).days < max_days:
                end = start + dt.timedelta(max_days-1)
            if end > self.end_date:
                end = self.end_date

            request = {
                "MetricId": self.metric,
                "StartDate": "{}".format(str(start)),
                "EndDate": "{}".format(str(end)),
                'Entity': self.entity_time,
                "Filter": self.filters
            }

            connection = requests.post(url, json=request)
            data_json = json.loads(connection.content)
            temporal_data = pd.json_normalize(
                data_json['Items'], value_type, 'Date', sep='_'
            )

            # print(temporal_data)

            if data is None:
                data = temporal_data
                # print(data)
            else:
                data = pd.concat([data, temporal_data], axis=0)
                # print(data)

            start = start + dt.timedelta(max_days)
            if end == self.end_date:
                aux = False
            condition = (
                (end - start).days > max_days-1 |
                (end - self.end_date).days != 0
            ) | aux

        self.data = data

        columns = list(self.data.columns)
        columns_values = [x for x in columns if 'Values_H' in x or 'Value' == x]

        if columns_values:
            self.data[columns_values] = self.data[columns_values].map(
                convert_string_to_float
            ) if not self.data[columns_values].empty else None

        if 'Date' in columns:
            columns.remove('Date')
            columns.insert(0, 'Date')
            self.data = self.data[columns]

        return

    def export_excel(self, name):
        directory = os.path.join(config.TEMP_PATH, f'{name}.xlsx')
        self.data.to_excel(directory)

        return


def convert_string_to_float(value):
    try:
        return float(value)
    except:
        return value


if __name__ == '__main__':

    get_data = GetDataAPI(
        metric='ListadoRecursos',
        frecuency_time='lists',
        entity_time='Sistema',
        filters=None,
        start_date='2023-01-01',
        end_date='2023-01-01',
    )

    get_data.post_request()
    get_data.export_excel('ListadoRecursos1')
    exit()

    get_data = GetDataAPI(
        # metric='PrecBolsNaci',
        metric='PrecEscaAct',
        # frecuency_time='hourly',
        frecuency_time='daily',

        entity_time='Sistema',
        filters=[],
        start_date='2017-01-1',
        end_date='2017-12-31',
    )

    get_data.post_request()
    # get_data.export_excel('PreciosBolsaNacional')
    get_data.export_excel('PrecEscaAct')
