import logging
import click

from project.lib import Memcached
from project.log import setup_logging

logger = logging.getLogger('project')


@click.group()
def memcache_cmd():  # pragma: no cover
    pass


@memcache_cmd.command(help='Execute something on the memcache')
@click.option('--action', type=click.Choice([
    'set', 'get', 'file_set', 'file_get']),
              help='Set or get, file_set or file_get')
@click.option('--key', prompt='Your key',
              help='The memcache key to use.')
@click.option('--value', default='',
              help='The value to set.')
@click.option('--filename', default='',
              help='The filename to read or write to.')
@click.option('--hostname', default='localhost', envvar='HOSTNAME',
              help='The memcached hostname to use.')
@click.option('--port', default=11211, envvar='PORT',
              help='The memcached port to use.')
def memcache(action, key, value, filename, hostname, port):  # pragma: no cover
    do_memcache(action, key, value, filename, hostname, port)


def do_memcache(action, key, value, filename, hostname, port):
    setup_logging(logging.INFO)

    memcached = Memcached(hostname, port)
    if action == 'set':
        memcached.set(key, value)
        logger.info('successfully set key %s.', key)
    if action == 'get':
        val = memcached.get(key)
        logger.info('returning %s value.', key)
        logger.info(val)
    if action == 'file_set':
        memcached.set_file(key, filename)
    if action == 'file_get':
        memcached.get_file(key, filename)
    if not action:
        logger.info('no action selected.')
