"""

"""

import pygsheets
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool


def getFile(key, secret):
    """
    Access GD file.

    Args:
        key (str):      identifier of file
        secret (str):   secret key

    Return:
        dataframe: loaded sheet
    """
    gc = pygsheets.authorize(outh_file=secret, outh_nonlocal=True, no_cache=True)
    sh = gc.open_by_key(key)
    wks = sh.sheet1
    df = wks.get_as_df()
    return df


def processData(df):
    """
    Process dataframe with data.

    Require certain column naming.

    Args:
        df (dataframe): dataframe with data
    """
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
    for index, row in df.iterrows():
        if not (type(row['Details']) is str and row['Details'].endswith('W')):
            df.drop(index, inplace=True)
    # Replace , after thousand and deal with W
    # http://pandas.pydata.org/pandas-docs/stable/basics.html#vectorized-string-methods
    df['Details'] = df['Details'].str.replace(',', '')
    df['Details'] = df['Details'].str[0:-1].astype(float)
    # Select only time and raw power
    data = df[['Timestamp', 'Details']]
    return data


def generatePlot(data, path):
    """
    Generate plot from data and save it.

    Args:
        data (dataframe):   dataframe with two columns - timestamp, power
        path (str):         path to html file with plot

    Return:
        bokeh.figure
    """
    hover = HoverTool(
        tooltips=[
            ('Timestamp',   '@Timestamp{%F %T}'),
            ('Details',  '@Details{%0.2f}'),  # use @{ } for field names with spaces
        ],
        formatters={
            'Timestamp': 'datetime',  # use 'datetime' formatter for 'date' field
            'Details': 'printf',   # use 'printf' formatter for 'adj close' field
            # use default 'numeral' formatter for other fields
        },
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    source = ColumnDataSource(data)
    output_file(path)
    # create a new plot with a title and axis labels
    p = figure(width=1600, height=500, title="simple line example", y_axis_label='W', x_axis_type="datetime",
               tools=[BoxZoomTool(), hover, ResetTool()])
    # add a line renderer with legend and line thickness
    p.line(x="Timestamp", y="Details", legend="Power", line_width=2, source=source)
    save(p)
    return p
