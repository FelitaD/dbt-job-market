import json

from streamlit_elements import nivo, mui
from reporting.dashboard.board import Dashboard


class Treemap(Dashboard.Item):
    # TODO: modify default data
    DEFAULT_DATA = [
        {"id": "java", "label": "java", "value": 465, "color": "hsl(128, 70%, 50%)"},
        {"id": "rust", "label": "rust", "value": 140, "color": "hsl(178, 70%, 50%)"},
        {"id": "scala", "label": "scala", "value": 40, "color": "hsl(322, 70%, 50%)"},
        {"id": "ruby", "label": "ruby", "value": 439, "color": "hsl(117, 70%, 50%)"},
        {"id": "elixir", "label": "elixir", "value": 366, "color": "hsl(286, 70%, 50%)"}
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#252526",
                "textColor": "#000000",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "#000000",
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
                    },
                    "node": {f'node.pathComponents: node.formattedValue'}
                }
            }
        }

    def __call__(self):
        try:
            # TODO: Add transform_treemap module
            with open('reporting/data/test_data.json', 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = self.DEFAULT_DATA

        with mui.Paper(key=self._key,
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                       elevation=1):
            with self.title_bar():
                mui.icon.TreeMap()
                mui.Typography("Technologies Frequency", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.TreeMap(
                    data=data,
                    identity='name',
                    value="loc",
                    label='id',
                    title='binary',
                    labelSkipSize=50,
                    orientLabel=True,
                    labelTextColor={'theme': 'background'},
                    enableParentLabel=False,
                    parentLabelPosition="top",
                    parentLabelTextColor={'theme': 'background'},
                    margin={"top": 40, "right": 40, "bottom": 40, "left": 40},
                    theme=self._theme["dark" if self._dark_mode else "light"],
                )
