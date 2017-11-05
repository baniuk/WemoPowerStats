import wemopowerstats.dataaccess as wps
import pandas as pd
from bokeh.plotting import show, save
df = pd.read_hdf('data.hd5', 'table')

datap = wps.processData(df)
p = wps.generatePlot(datap, "plot.html")

# %% Remove duplicated times but leave one entry (non-zero power if exist)
# does not work as expected
# data = data.groupby(['Timestamp']).max()
# data
# %% try with median
# data = data.copy()
# data1 = data['Details'].rolling(window=3, center=True).median()
# data['Details'] = data1
# %%
