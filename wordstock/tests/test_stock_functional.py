# (C) Copyright 2019 Hewlett Packard Enterprise Development LP
import argparse
import os

from ddt import ddt, data
import pandas as pd
from unittest import mock
from wordstock import stock
from wordstock.tests import base as test_base

import logging


@ddt
class TestStockFunctional(test_base.TestBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        core_log = logging.getLogger(stock.__name__)
        cls._core_log_handler = test_base.MockLoggingHandler(level='DEBUG')
        core_log.addHandler(cls._core_log_handler)
        cls.core_log_messages = cls._core_log_handler.messages

    def setUp(self):
        super().setUp()
        self._core_log_handler.reset()  # So each test is independent

    @data('csv','json','unknown', '')
    def test_word_stock(self, formats):
        ns = {'datadir': os.path.join(os.getcwd(), 'tests', 'data', 'smoke'),
              'seeddir': os.path.join(os.getcwd(), 'tests', 'patterns', 'smoke'),
              'outputdir': os.path.join(os.getcwd(), 'tests', 'output'),
              'outputformat': formats}
        df = stock.word_stock(ns)
        self.assertIn(6, df.values)

    def test_word_stock_impossible_pattern(self,):
        ns = {'datadir': os.path.join(os.getcwd(), 'tests', 'data', 'smoke'),
              'seeddir': os.path.join(os.getcwd(), 'tests', 'patterns',
                                      'smoke', 'impossible_pattern'),
              'outputdir': os.path.join(os.getcwd(), 'tests', 'output'),
              'outputformat': 'csv'}
        df = stock.word_stock(ns)
        self.assertEqual(None, df)

    @mock.patch("sys.exit", side_effect=SystemExit)
    def test_word_stock_empty_data_file(self, sys_exit):
        ns = {'datadir': os.path.join(os.getcwd(), 'tests', 'data', 'smoke',
                                      'emptyfile'),
              'seeddir': os.path.join(os.getcwd(), 'tests', 'patterns',
                                      'smoke'),
              'outputdir': os.path.join(os.getcwd(), 'tests', 'output'),
              'outputformat': 'csv'}
        try:
            df = stock.word_stock(ns)
        except SystemExit:
            pass
        sys_exit.assert_called_once_with(1)

    @mock.patch("sys.exit", side_effect=SystemExit)
    def test_word_stock_empty_pattern_file(self, sys_exit):
        ns = {'datadir': os.path.join(os.getcwd(), 'tests', 'data', 'smoke'),
              'seeddir': os.path.join(os.getcwd(), 'tests', 'patterns',
                                      'smoke', 'emptyfile'),
              'outputdir': os.path.join(os.getcwd(), 'tests', 'output'),
              'outputformat': 'csv'}
        try:
            df = stock.word_stock(ns)
        except SystemExit:
            pass
        sys_exit.assert_called_once_with(1)

    @mock.patch("sys.exit", side_effect=SystemExit)
    def test_word_stock_empty_data_folder(self, sys_exit):
        ns = {'datadir': os.path.join(os.getcwd(), 'tests', 'data', 'smoke',
                                      'emptyfolder'),
              'seeddir': os.path.join(os.getcwd(), 'tests', 'patterns',
                                      'smoke'),
              'outputdir': os.path.join(os.getcwd(), 'tests', 'output'),
              'outputformat': 'csv'}
        try:
            df = stock.word_stock(ns)
        except SystemExit:
            pass
        sys_exit.assert_called_once_with(1)

    @data(None, {})
    @mock.patch("sys.exit", side_effect=SystemExit)
    def test_word_stock_empty(self,ns, sys_exit):
        try:
            stock.word_stock(ns)
        except SystemExit:
            pass
            # Assertions
            sys_exit.assert_called_once_with(1)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
