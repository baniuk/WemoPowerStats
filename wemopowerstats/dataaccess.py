"""

"""
import logging
import pygsheets
import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool
import os
log = logging.getLogger(__name__)


class GeneratePlot:
    """
    Generate plots from sheets.

    Configuration through constructor, then execution by self-call.
    """

    def __init__(self, secret, path, plotall=True):
        """
        Configure object.

        Args:
            secret (str):   path to secret file
            path (str):     folder where plot are saved. Name of plot is same as name of datafile.
            plotall (bool): If True, filename given when calling object is interpreted as prefix.
                            Otherwise it is exact name of file and only this plot is generated.
        """
        self.gc = pygsheets.authorize(outh_file=secret, outh_nonlocal=True, no_cache=True)
        self.path = os.path.dirname(path)
        self.plotall = plotall

    def __call__(self, fileName):
        """
        Create plots from given filename.

        If plotall was set to True, filename is considered as prefix and all matching files
        are converted to plots. Otherwise exact filename is loaded.
        """
        filelist = self.listFiles(fileName, wildcards=self.plotall)
        for f in filelist:
            df = self.getFile(f)
            data = self.processData(df)
            self.generatePlot(data, os.path.join(self.path, f + ".html"))

    def listFiles(self, coreName, wildcards=True):
        """
        Return list of files that start with coreName.

        Args:
            secret (str):   secret key
            coreName (str): string that file must begin with to be returned

        Return:
            list: list of names that match criteria
        """
        if wildcards:
            names = self.gc.list_ssheets()
            matched = [element['name'] for element in names if element['name'].startswith(coreName)]
        else:
            self.gc.open(coreName)  # try to open
            matched = [coreName]
        return matched

    def getFile(self, file):
        """
        Access GD file.

        Args:
            file (str):     file name to open
            secret (str):   secret key

        Return:
            dataframe: loaded sheet
        """
        sh = self.gc.open(file)
        wks = sh.sheet1
        df = wks.get_as_df()
        log.debug("{0} file opened".format(file))
        return df

    def processData(self, df):
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

    def generatePlot(self, data, path):
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
        p = figure(width=1600, height=500, title="Power usage", y_axis_label='W', x_axis_type="datetime",
                   tools=[BoxZoomTool(), hover, ResetTool()])
        # add a line renderer with legend and line thickness
        p.line(x="Timestamp", y="Details", legend="Power", line_width=2, source=source)
        save(p)
        log.debug("Saved graph at: " + path)
        return p
