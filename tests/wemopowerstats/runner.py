import wemopowerstats

if __name__ == "__main__":
    # args = parser.parse_args(['--version']) # this exits automtically
    wemopowerstats.cli()
    print(wemopowerstats.args)
