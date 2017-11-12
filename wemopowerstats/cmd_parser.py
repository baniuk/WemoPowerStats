"""CMD parser."""

from ._version import __version__
import argparse

_def_refresh = 60
parser = argparse.ArgumentParser(description="WeMo statistics displayer")
parser.add_argument("-r", "--refresh", action="store", metavar="SEC", default=_def_refresh, type=int,
                    help="Refresh time in sec. Default {0} seconds".format(_def_refresh))
parser.add_argument("secret", action="store", default="", help="Path to secret.json file")
parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
parser.add_argument("--deamon", action="store_true", default=False, help="Run as deamon.")
parser.add_argument("-d", "--debug", action="store_true", default=False, help="Enable debug logging")
parser.add_argument("-w", "--wildcard", action="store_true", default=False,
                    help="Log file name is wildcard. Use it to match all files that begin with it")
parser.add_argument("output_file_path", help="Path to output plot. Should end with /")
parser.add_argument("log_file", help="Name of file to open")
