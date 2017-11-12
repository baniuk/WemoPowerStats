"""Test unit for dataaccess.py."""
import unittest
import logging
from wemopowerstats import GeneratePlot

logging.basicConfig(level=logging.DEBUG)


class TestDataAccess(unittest.TestCase):
    """Test unit for dataaccess.py."""

    def test_listFiles(self):
        """
        Test of listFiles.

        Expect nonemty list of files.
        """
        o = GeneratePlot("client_secrets.json", "./plot.html")
        ret = o.listFiles("home")
        logging.debug(ret)
        self.assertTrue(ret)

    def test_listFiles1(self):
        """
        Test of listFiles no wildcard

        Expect one file, same as given on input.
        """
        o = GeneratePlot("client_secrets.json", "./plot.html")
        ret = o.listFiles("home.log", wildcards=False)
        logging.debug(ret)
        self.assertTrue(ret == ['home.log'])


if __name__ == '__main__':
    unittest.main()
