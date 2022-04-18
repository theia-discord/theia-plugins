import logging
logging.basicConfig(level=logging.DEBUG)

from . import register_commands
from .dispatch import dispatcher

register_commands()
dispatcher.run()
