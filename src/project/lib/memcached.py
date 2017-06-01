import logging
import os

from pymemcache.client.base import Client

logger = logging.getLogger('project')

CHUNK_SIZE = 1000000


class Memcached(object):
    def __init__(self, hostname='localhost', port=11211):
        self.client = Client((hostname, port))

    def set(self, key, value):
        return self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def set_file(self, key, file_obj_or_string):
        """store a file in memcache by its key"""
        if os.path.exists(file_obj_or_string):
            logger.info('file detected')
            with open(file_obj_or_string, 'rb') as f:

                byte = f.read(CHUNK_SIZE)
                if not byte:
                    logger.info('no chunks found')
                    return
                i = 0
                while byte != b'':
                    logger.info('writing part %i', i)
                    self.client.set('%s--%i' % (key, i), byte)

                    verify = self.client.get('%s--%i' % (key, i))
                    if not byte == verify:  # sha checksum instead?
                        logger.error('we wrote something insane. quit.')
                        return
                    byte = f.read(CHUNK_SIZE)
                    i += 1

                self.client.set('%s--parts' % key, i)
        else:
            logger.info('not a file, writing string')
            # TODO: should probably also split per megabyte..
            return self.set(key, file_obj_or_string)

    def get_file(self, key, filename='output.txt'):
        """retrieve a file from memcache by its key"""
        file = open(filename, 'w')
        parts = self.client.get('%s--parts' % key)
        for i in range(0, int(parts)):
            file.write(self.client.get('%s--%i' % (key, i)))
            logger.info('getting part %i', i)
        file.close()
        logger.info('written output to file %s', filename)
