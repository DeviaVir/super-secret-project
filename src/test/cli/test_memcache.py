from mock import MagicMock, patch
import unittest

from project.cli.memcache import do_memcache
from project.lib.memcached import Memcached


class TestMemcacheClient(unittest.TestCase):
    @patch('project.cli.memcache.Memcached')
    def test_memcache_set(self, memcache_constructor):
        self._setup_mocks(memcache_constructor)

        do_memcache('set', 'test', 'value', '', 'localhost', '11211')

        self.memcache_constructor.set.assert_called_with(
            'test', 'value')

    @patch('project.cli.memcache.Memcached')
    def test_memcache_get(self, memcache_constructor):
        self._setup_mocks(memcache_constructor)

        do_memcache('get', 'test', '', '', 'localhost', '11211')

        self.memcache_constructor.get.assert_called_with('test')

    @patch('project.cli.memcache.Memcached')
    def test_memcache_no_action(self, memcache_constructor):
        self._setup_mocks(memcache_constructor)

        do_memcache('', 'test', '', '', 'localhost', '11211')

        self.memcache_constructor.get.assert_not_called()
        self.memcache_constructor.set.assert_not_called()

    def _setup_mocks(self, memcache_constructor):
        self.memcache_constructor = MagicMock(spec=Memcached)
        memcache_constructor.return_value = self.memcache_constructor
