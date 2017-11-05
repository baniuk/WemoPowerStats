"""Application entry module."""
from . import cmd_parser as cp

args = None


def cli():
    global args
    args = cp.parser.parse_args()
