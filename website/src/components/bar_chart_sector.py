import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchemaSector, sectors_dict
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART_SECTOR, "children"),
        [
            Input(ids.SECTORS_DROPDOWN, "value"),
            Input(ids.CHART_DROPDOWN_SECTOR, "value")
        ],
    )
    def update_bar_chart(
        sectors: list[str], chart: str,
    ) -> html.Div:
        filtered_data = data.query(
            "sector in @sectors"
        )
        if chart == 'Bar':

            if filtered_data.shape[0] == 0:
                return html.Div("No data selected.", id=ids.BAR_CHART_SECTOR)

            filtered_data['sector'] = filtered_data["sector"].replace(sectors_dict)

            def create_pivot_table() -> pd.DataFrame:
                pt = filtered_data.pivot_table(
                    values=DataSchemaSector.CORRELATION,
                    index=[DataSchemaSector.SECTOR],
                    aggfunc="sum",
                    fill_value=0,
                    dropna=False,
                )
                return pt.reset_index().sort_values(DataSchemaSector.CORRELATION, ascending=False)

            fig = px.bar(
                create_pivot_table(),
                x=DataSchemaSector.SECTOR,
                y=DataSchemaSector.CORRELATION,
                color=DataSchemaSector.SECTOR,
                labels={DataSchemaSector.SECTOR: 'Sector', DataSchemaSector.CORRELATION: 'Correlation Value'},
            )

            fig.update_yaxes(range=[0.6, 1.0])

            return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART_SECTOR)
        else:
            return html.Div(id=ids.BAR_CHART_SECTOR)

    return html.Div(id=ids.BAR_CHART_SECTOR)
