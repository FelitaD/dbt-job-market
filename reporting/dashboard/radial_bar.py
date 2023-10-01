import json

from streamlit_elements import nivo, mui
from .dashboard import Dashboard

from reporting.transformers import radial_data


class RadialBar(Dashboard.Item):
    DEFAULT_DATA = [{'id': 'remote',
                     'data': [{'x': 'partial', 'y': 1}, {'x': 'total', 'y': 1}]},
                    {'id': 'rating_score',
                     'data': [{'x': '3.0', 'y': 1}, {'x': '1.0', 'y': 1}, {'x': '-1.0', 'y': 1}]},
                    {'id': 'seniority_score',
                     'data': [{'x': '3.0', 'y': 1}, {'x': '4.0', 'y': 1}, {'x': '-1.0', 'y': 1}]}]

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
        try:
            data = radial_data
        except Exception as e:
            print(e)
            data = self.DEFAULT_DATA

        with mui.Paper(key=self._key,
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                       elevation=1):
            with self.title_bar():
                mui.icon.RadialBar()
                mui.Typography("Data Engineer Jobs Specs", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.RadialBar(
                    data=data,
                    margin={"top": 40, "right": 40, "bottom": 40, "left": 40},
                    theme=self._theme["dark" if self._dark_mode else "light"],
                )
