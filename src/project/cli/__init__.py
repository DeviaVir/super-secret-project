import click
from .memcache import memcache_cmd

CMDS = (memcache_cmd,)
CLI = click.CommandCollection(sources=CMDS)
