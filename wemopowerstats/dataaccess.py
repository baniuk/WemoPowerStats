"""

"""

import pygsheets
import os
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.plotting import figure, output_file, show
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool

print(os.getcwd())
# gc = pygsheets.authorize(service_file='My Project-b8132c60e17e.json', no_cache=True)
gc = pygsheets.authorize(outh_file='client_secrets.json', outh_nonlocal=True, no_cache=True)

sh = gc.open_by_key("1xzu4byUB7kGqwvgLNDVTfSQxf0P2qVC_NTPer6iT7S8")
wks = sh.sheet1
df = wks.get_as_df()
df.to_hdf('data.hd5', 'table')
# type(df['Details'].values[227])
# raw = df['Details'].values

# %% Read data and select only rows that contain power (W)
df = pd.read_hdf('data.hd5', 'table')
df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
for index, row in df.iterrows():
    if not (type(row['Details']) is str and row['Details'].endswith('W')):
        df.drop(index, inplace=True)

# df
# %% Replace , after thousand and deal with W
# http://pandas.pydata.org/pandas-docs/stable/basics.html#vectorized-string-methods
df['Details'] = df['Details'].str.replace(',', '')
df['Details'] = df['Details'].str[0:-1].astype(float)
# df
#
# %% Select only time and raw power
data = df[['Timestamp', 'Details']]
data.shape
data

# %% Remove duplicated times but leave one entry (non-zero power if exist)
# # does not work as expected
data = data.groupby(['Timestamp']).max()
data
# %% try with median
data = data.copy()
data1 = data['Details'].rolling(window=3, center=True).median()
data['Details'] = data1
# %%
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
output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(width=1600, height=500, title="simple line example", y_axis_label='W', x_axis_type="datetime",
           tools=[BoxZoomTool(), hover, ResetTool()])

# add a line renderer with legend and line thickness
p.line(x="Timestamp", y="Details", legend="Power", line_width=2, source=source)

# show the results
show(p)
