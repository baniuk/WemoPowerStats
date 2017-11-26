"""Application entry module."""
from . import cmd_parser as cp
import logging
from .dataaccess import GeneratePlot
args = None


def cli():
    global args
    args = cp.parser.parse_args()
    level = logging.INFO
    if getattr(args, 'debug', False):
        level = logging.DEBUG
    logging.basicConfig(level=level)
    logging.debug("Run with params: {0}".format(args))

    o = GeneratePlot(secret=getattr(args, 'secret'),
                     path=getattr(args, 'output_file_path'),
                     plotall=getattr(args, 'wildcard'))
    o(getattr(args, 'log_file'))
