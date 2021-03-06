import asyncio
import logging

from .aws.message_translator import SNSMessageTranslator

logger = logging.getLogger(__name__)


class Route(object):
    def __init__(self, source, message_handler, name='default', message_translator=None):
        self.name = name
        self.source = source
        self.message_handler = message_handler
        self.message_handler_name = type(message_handler).__name__

        if message_translator is None:
            self.message_translator = SNSMessageTranslator()
        else:
            self.message_translator = message_translator

    def __repr__(self):
        return '<Route(name={} queue={} message_handler={})>'.format(
            self.name, self.source, self.message_handler)

    async def deliver(self, content, loop=None):
        logger.info('Delivering message content to message_handler={}'.format(self.message_handler_name))

        if asyncio.iscoroutinefunction(self.message_handler):
            logger.debug('Handler is coroutine! {!r}'.format(self.message_handler_name))
            return await self.message_handler(content)
        else:
            logger.debug('Handler will run in a separate thread: {!r}'.format(self.message_handler_name))
            loop = loop or asyncio.get_event_loop()
            return await loop.run_in_executor(None, self.message_handler, content)

    def error_handler(self, message, exception):
        """Hook for unhandled exceptions raised from `message_handler` for a given
        message.
        If the returning value is True, the message will be acknowledged.
        By the default we return `False`.
        """
        logger.exception(exception)
        logger.error('Unhandled exception on {}'.format(self.message_handler))
        return False
