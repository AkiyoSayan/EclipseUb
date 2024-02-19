import os
from typing import Dict, List, Union 
import telethon
from eclipse import get_value, get_value_list
import asyncio
import datetime
import inspect
import re
import sys
import traceback
from pathlib import Path

from telethon import TelegramClient, events
from telethon.errors import (
    AlreadyInConversationError,
    BotInlineDisabledError,
    BotResponseTimeoutError,
    ChatSendInlineForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendStickersForbiddenError,
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
)

class Decorator:
    def __init__(
          self,
          eclipse,
          pattern: str = None,
          group: int = 1,
          only_private: bool = True,
          only_bots: bool = True,
          only_groups: bool = True,
          only_channels: bool = True,
          only_admin: bool = True,
          about: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]] = None,
          check_permission: bool = True,
          **kwargs,
    ):
        self.eclipse = eclipse
        def decorator(self):  
            async def wrapper(self, func):  
                
            return wrapper
        return decorator
        

