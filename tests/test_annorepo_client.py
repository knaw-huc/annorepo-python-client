# -*- coding: utf-8 -*-
import unittest

from annorepo import __version__
from annorepo.client import AnnoRepoClient


class AnnoRepoTestSuite(unittest.TestCase):

    def test_version(self):
        self.assertIsNot(__version__, '')

    def test_client(self):
        c = AnnoRepoClient("http://localhost:8080/")
        self.assertIsNotNone(c)
