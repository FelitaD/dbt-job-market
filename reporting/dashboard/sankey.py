import json
import pandas as pd

from streamlit_elements import nivo, mui
from .dashboard import Dashboard

from .transformers import sankey_df


class Sankey(Dashboard.Item):
    # TODO: Create transform_sankey module
    DATA = {
        "nodes": [
            {"id": "raw data", "nodeColor": "hsl(126, 32%, 67%)"},
            {"id": "tech jobs", "nodeColor": "hsl(126, 32%, 67%)"},
            {"id": "no technologies", "nodeColor": "hsl(204, 8%, 76%)"},
            {"id": "data engineer jobs", "nodeColor": "hsl(126, 32%, 67%)"},
            {"id": "not relevant", "nodeColor": "hsl(204, 8%, 76%)"},
            {"id": "unspecified", "nodeColor": "hsl(126, 32%, 67%)"},
            {"id": "senior", "nodeColor": "hsl(126, 32%, 67%)"},
            {"id": "graduate", "nodeColor": "hsl(126, 32%, 67%)"},
            {"id": "junior", "nodeColor": "hsl(126, 32%, 67%)"}
        ],
        "links": [
            {"source": "raw data", "target": "tech jobs", "value": sankey_df.jobs},
            {"source": "raw data", "target": "no technologies", "value": sankey_df.raw - sankey_df.jobs},
            {"source": "tech jobs", "target": "data engineer jobs", "value": sankey_df.relevant},
            {"source": "tech jobs", "target": "not relevant", "value": sankey_df.jobs - sankey_df.relevant},
            {"source": "data engineer jobs", "target": "unspecified", "value": sankey_df.unspecified},
            {"source": "data engineer jobs", "target": "senior", "value": sankey_df.senior},
            {"source": "data engineer jobs", "target": "junior", "value": sankey_df.junior},
            {"source": "data engineer jobs", "target": "graduate", "value": sankey_df.graduate}
        ]
    }

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
                    }
                }
            }
        }

    def __call__(self):
        data = self.DATA

        with mui.Paper(key=self._key,
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"},
                       elevation=1):
            with self.title_bar():
                mui.icon.Sankey()
                mui.Typography("Data Retention after Raw Layer", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Sankey(
                    data=data,
                    margin={"top": 40, "right": 40, "bottom": 40, "left": 40},
                    theme=self._theme["dark" if self._dark_mode else "light"],
                )
