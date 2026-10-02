import plotly.express as px


def create_chart(
    df,
    chart_type,
    x_column,
    y_column=None,
):

    if chart_type == "bar":

        return px.bar(
            df,
            x=x_column,
            y=y_column,
        )

    if chart_type == "line":

        return px.line(
            df,
            x=x_column,
            y=y_column,
        )

    if chart_type == "scatter":

        return px.scatter(
            df,
            x=x_column,
            y=y_column,
        )

    if chart_type == "histogram":

        return px.histogram(
            df,
            x=x_column,
        )

    raise ValueError(
        f"Unsupported chart type: {chart_type}"
    )
    