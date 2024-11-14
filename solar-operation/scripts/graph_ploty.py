import plotly.graph_objects as go
import pandas as pd

from config import TEMP_PATH

OPTION_COLORS = [
    "#19647e",
    "#FA8072",
    "#28afb0",
    "#ee964b",
    "#f4d35e",
    "#A52A2A",
    "#006400",
    "#CD5C5C",
    "#FF4500",
    "#EEE8AA",
    "#FF0000",
    "#F5F5DC",
]

OPTION_MARKERS = [
    "circle",
    "diamond",
    "triangle-up",
    "cross",
    "square",
    "x",
    "pentagon",
    "hexagon",
    "octagon",
    "star",
    "hexagram",
    "star-triangle-up",
]

OPTION_WIDTH = [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
]

TITLE = "Gráfico"
TITLE_EJE_X = "Fecha"
TITLE_EJE_Y = "Valores"


def plot_excel(
    file_name: str,
    sheet_name: str = "Sheet1",
    export_path: str = TEMP_PATH,
    export_file_name: str = "plot",
    title: str = TITLE,
    title_eje_x: str = TITLE_EJE_X,
    title_eje_y: str = TITLE_EJE_Y,
):
    # import dataframe for each sheet
    file_path = TEMP_PATH + file_name + ".xlsx"
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    data.columns = data.columns.str.lower()
    # if has a column unnamed, drop it
    columns_to_drop = [column for column in data.columns if "unnamed" in column]
    data = data.drop(columns=columns_to_drop)

    traces = []
    total_energy = []
    for index, column in enumerate(data.columns[1:]):
        energy = data[column].to_list()
        total_energy.append(sum(energy)/1000)
        trace = go.Scatter(
            x=data['date'],
            y=data[column],
            mode='lines+markers',
            marker=dict(symbol=OPTION_MARKERS[index], size=8),
            name=column,
            line=dict(width=2, color=OPTION_COLORS[index]),
        )
        traces.append(trace)

    annotations = [
        dict(
            x=0.97,
            y=1,
            xref='paper',
            yref='paper',
            text=f'Energía {total_energy[0]:.1f} MWh-dia <br>Despacho {total_energy[1]:.1f} MWh-dia <br> Redespacho {total_energy[2]:.1f} MWh-dia ',
            showarrow=False,
            font=dict(
                size=12,
                color='black'
            ),
            align='right',
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(211, 211, 211, 0.5)',  # Fondo gris tenue con opacidad
            bordercolor='black',
            borderwidth=1
        )
    ]

    # Configurar el diseño del gráfico
    layout = go.Layout(
        annotations=annotations,
        font=dict(
            color='black',
            family='system-ui',
        ),
        title=dict(
            text=title,
            x=0.5,
            y=0.9,
            xanchor='center',
            font=dict(
                size=20,
                weight='bold'
            )
        ),
        xaxis=dict(
            title=title_eje_x,
            # type='date',
            type='category',  # Configuración para el tipo de datos categóricos
            # tickformat='%I',  # Formato de la etiqueta para mostrar horas y minutos
            tickvals=data['date'],
            ticktext=[f'{time:02}' for time in data['date']],  # Convertir a formato AM/PM
            autorange=True,
            # linecolor='black',
            # linewidth=0.5,
            # gridcolor='#e5e5e5',
            mirror=True
        ),
        yaxis=dict(
            title=title_eje_y,
            autorange=True,
            linecolor='black',
            linewidth=1,
            gridcolor='#e5e5e5',
            mirror=True
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        width=1000,
        height=500,
    )

    fig = go.Figure(data=traces, layout=layout)
    # fig.show()

    export_path = export_path + export_file_name + ".svg"
    fig.write_image(export_path)
