from wemopowerstats import entry
import logging

# logger = logging.getLogger("runner")
# logger.setLevel(logging.DEBUG)
# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# # create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# # add formatter to ch
# ch.setFormatter(formatter)
# # add ch to logger
# logger.addHandler(ch)

# https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
# can be used simple logger, see logging.basicConfig
# python tests\wemopowerstats\wemopowerstats.py client_secrets.json c:/Users/baniu/Downloads/ homenewver.log
if __name__ == "__main__":
    # args = parser.parse_args(['--version']) # this exits automtically
    entry.cli()
