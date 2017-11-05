"""CMD parser."""

# from .__init__ import __version__
import argparse

_def_refresh = 60
parser = argparse.ArgumentParser(description="WeMo statistics displayer")
parser.add_argument("-r", "--refresh", action="store", metavar="SEC", default=_def_refresh, type=int,
                    help="Refresh time in sec. Default {0} seconds".format(_def_refresh))
parser.add_argument("-s", "--secret", action="store", metavar="PATH", default="", help="Path to secret.json file")
parser.add_argument('--version', action='version', version="%(prog)s ")
parser.add_argument("--deamon", action="store_true", default=False, help="Run as deamon.")
parser.add_argument("output_folder", help="Folder where images will be stored")
parser.add_argument("file", help="Key to file to open")

if __name__ == "__main__":
    # args = parser.parse_args(['--version']) # this exits automtically
    args = parser.parse_args(["folder/", "66"])
    print(args)
