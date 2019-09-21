# (C) Copyright 2019 Hewlett Packard Enterprise Development LP

import testtools
import logging

class TestBase(testtools.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(self):
        pass


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs.
    """

    def __init__(self, *args, **kwargs):
        self.messages = {'debug': [], 'info': [], 'warning': [], 'error': [],
                         'critical': []}
        super(MockLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        "Store a message from ``record`` in the instance's ``messages`` dict."
        try:
            self.messages[record.levelname.lower()].append(record.getMessage())
        except Exception:
            self.handleError(record)

    def reset(self):
        self.acquire()
        try:
            for message_list in self.messages.values():
                message_list.clear()
        finally:
            self.release()
