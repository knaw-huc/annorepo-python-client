# -*- coding: utf-8 -*-
import unittest

from annorepo import __version__
from annorepo.client import AnnoRepoClient


class AnnoRepoTestSuite(unittest.TestCase):

    def test_version(self):
        assert __version__ == '0.1.0'

    def test_client(self):
        c = AnnoRepoClient("http://localhost:8080/")
        c.hello("world")
