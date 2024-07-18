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

TITLE = "Gráfico"
TITLE_EJE_X = "Fecha"
TITLE_EJE_Y = "Valores"


def plot_excel(
    file_name: str,
    sheet_name: str = "Sheet1",
    export_path: str = TEMP_PATH,
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

    for index, column in enumerate(data.columns[1:]):
        trace = go.Scatter(
            x=data['date'],
            y=data[column],
            mode='lines+markers',
            name=column,
            line=dict(width=2, color=OPTION_COLORS[index]),
        )
        traces.append(trace)

    # Configurar el diseño del gráfico
    layout = go.Layout(
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
            type='date',
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

    export_path = export_path + file_name + ".svg"
    fig.write_image(export_path)
