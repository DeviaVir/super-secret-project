from mock import patch

from pymemcache.client.base import Client
from project.lib import Memcached

HOSTNAME = 'localhost'
PORT = '11211'


class TestMemcached():
    @patch('project.lib.memcached.Client', spec=Client)
    def setUp(self, mock_client):
        self.hostname = HOSTNAME
        self.port = PORT
        self.client = mock_client((self.hostname, self.port))
        self.memcached = Memcached(self.hostname, self.port)

    def test_get(self):
        self.memcached.get('key')
        self.client.get.assert_called_with('key')

    def test_set(self):
        self.memcached.set('key', 'value')
        self.client.set.assert_called_with('key', 'value')
