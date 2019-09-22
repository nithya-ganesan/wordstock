# (C) Copyright 2019 Hewlett Packard Enterprise Development LP

from ddt import ddt, data
import pandas as pd
from unittest import mock
from wordstock import stock
from wordstock.tests import base as test_base

import logging


@ddt
class TestStockUnit(test_base.TestBase):

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

    # Uses mocking to build unit tests
    @mock.patch("sys.exit", side_effect=SystemExit)
    def test_argparser_no_args(self, sys_exit):
        parser = stock.build_argparser()
        try:
            parser.parse_args()
        except SystemExit:
            pass
        # Assertions
        sys_exit.assert_called_once_with(2)

    # Uses Data driven testing to provide multiple input to the same test
    @data(["-i", "data", "-p", "pattern", "-o", "output", "-f", "json"],
          ["--datadir", "data", "--seeddir", "pattern",
          "--outputdir", "output", "--outputformat", "json"])
    def test_argparser(self, inputs):
        parser = stock.build_argparser()
        parsed = parser.parse_args(inputs)
        self.assertEqual(parsed.datadir, 'data')
        self.assertEqual(parsed.outputdir, 'output')
        self.assertEqual(parsed.seeddir, 'pattern')
        self.assertIn(parsed.outputformat, ["csv", "json"])

    def test_check_dir_none(self):
        stock.check_dir(None)

    def test_get_unique_words(self):
        test_frame = pd.DataFrame(data={'words': ["data1", "data2", "data1"]})
        unique_list = stock.get_unique_words(test_frame)
        self.assertEqual(2, len(unique_list))
        self.assertIn("data1", unique_list)
        self.assertIn("data2", unique_list)

    @data({'no_words': []},
          {'words': []})
    def test_get_unique_words_negative(self, inputs):
        test_frame = pd.DataFrame(data=inputs)
        unique_list = stock.get_unique_words(test_frame)
        self.assertEqual(0, len(unique_list))
        unique_list = stock.get_unique_words(None)
        self.assertEqual(0, len(unique_list))

    def test_get_word_count_negative(self):
        test_frame = pd.DataFrame(data={'words': ["data1", "data2", "data1"]})
        count_frame = stock.get_word_count(test_frame, [], 'words')
        self.assertEqual(None,count_frame)

    @mock.patch("sys.exit", side_effect=SystemExit)
    @mock.patch("os.path.isdir", return_value=False)
    def test_check_dir_nonexistence(self, mock_os_path_isdir, mock_sys_exit):
        try:
            stock.check_dir(["does_not_exist"])
        except SystemExit:
            pass
        mock_sys_exit.assert_called_once_with(1)
        mock_os_path_isdir.assert_called_once_with("does_not_exist")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
