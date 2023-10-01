import json

from streamlit_elements import nivo, mui
from .dashboard import Dashboard

from reporting.transformers import scatter_data


class Scatter(Dashboard.Item):
    DEFAULT_DATA = [{'id': 'Deloitte', 'data': [{'x': 105000, 'y': 4.0}]},
                    {'id': 'EY', 'data': [{'x': 75, 'y': 3.9}]},
                    {'id': 'Capgemini', 'data': [{'x': 7300, 'y': 5.0}]},
                    {'id': 'DXC Technology', 'data': [{'x': 250, 'y': 3.6}]},
                    {'id': 'Santander', 'data': [{'x': 18000, 'y': 3.8}]}]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#252526",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def __call__(self):
        data = scatter_data

        with mui.Paper(key=self._key,
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                       elevation=1):
            with self.title_bar():
                mui.icon.ScatterPlot()
                mui.Typography("Companies Glassdoor Rating", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.ScatterPlot(
                    data=data,
                    xScale={'type': 'symlog', 'min': 0, 'max': 100000},
                    yScale={'type': 'linear', 'min': 1, 'max': 5},
                    axisBottom={
                        'enable': True,
                        'tickSize': 5,
                        'tickPadding': 4,
                        'tickRotation': -90,
                        'legend': 'number of reviews',
                        'legendPosition': 'middle',
                        'legendOffset': 60},
                    axisLeft={
                        'enable': True,
                        'tickSize': 5,
                        'tickPadding': 4,
                        'tickRotation': 0,
                        'tickValues': [1, 2, 3, 4, 5],
                        'legend': 'rating',
                        'legendPosition': 'middle',
                        'legendOffset': -60},
                    enableGridX=True,
                    enableGridY=True,
                    margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
                    theme=self._theme["dark" if self._dark_mode else "light"],
                )
