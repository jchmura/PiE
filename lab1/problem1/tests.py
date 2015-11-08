import logging
import unittest
from unittest.mock import patch

from monitor import logger


class TestMonitor(unittest.TestCase):
    def test_logger_decorator(self):
        name = 'name'
        with patch.object(logging, 'getLogger', return_value=logging.RootLogger(logging.DEBUG)) as log1:
            with patch.object(logging.Logger, 'info', return_value=None) as log2:
                @logger(name)
                def fun():
                    return 3.1415

                fun()
                log1.assert_called_once_with(name)
                log2.assert_called_once_with('3.14%')


if __name__ == '__main__':
    unittest.main()
