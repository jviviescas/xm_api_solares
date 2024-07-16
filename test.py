from datetime import datetime as dt

hora = '2018-12-140'


hora = dt.strptime(hora, '%Y-%m-%d%H')


print(hora)
