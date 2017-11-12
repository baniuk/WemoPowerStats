import logging
from wemopowerstats import cmd_parser as p

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    logging.debug(p.parser.parse_args(["folder/", "66"]))
    logging.debug(p.parser.parse_args(['--version']))
