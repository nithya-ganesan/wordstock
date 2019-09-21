# (C) Copyright 2019 Hewlett Packard Enterprise Development LP

from ddt import ddt, data
from wordstock.tests import base as test_base
from unittest import mock
from wordstock import stock

import logging


@ddt
class TestStock(test_base.TestBase):

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
    @data(["-d", "-i", "data", "-p", "pattern", "-o", "output", "-f", "json"],
          ["--debug", "--datadir", "data", "--seeddir", "pattern",
          "--outputdir", "output", "--outputformat", "json"])
    def test_argparser(self, inputs):
        parser = stock.build_argparser()
        parsed = parser.parse_args(inputs)
        self.assertEqual(parsed.datadir, 'data')
        self.assertEqual(parsed.outputdir, 'output')
        self.assertEqual(parsed.seeddir, 'pattern')
        self.assertIn(parsed.outputformat, ["csv", "json"])
        self.assertTrue(parsed.debug)

    def test_check_dir_none(self):
        stock.check_dir(None)

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
