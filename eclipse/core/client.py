import sys
import os
import asyncio
import logging
from eclipse import config
import time
import functools
import yaml
import importlib
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .funcs import Functions

from typing import Dict, List, Optional, Union
from eclipse.helpers.tools import get_readable_time
from telethon import TelegramClient, __version__
from telethon.errors import (
    AccessTokenExpiredError,
    AccessTokenInvalidError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
)

class Eclipse(TelegramClient, Functions):
    """
    Main client to run Eclipse.

    """
    def __init__(self, *args, **kwargs):
        self.start_time = time.time()
        self.lang_code = "en"
        self.lang_strings = {}
        self.lang_strings_cache = {}
        kwargs = {
            'api_id': config.API_ID,
            'api_hash': config.API_HASH,
        }
        super().__init__(config.SESSION, **kwargs)

        if config.BOT_TOKEN:
            kwargs['bot_token'] = config.BOT_TOKEN
        
        self._init_log()
        self.run_in_loop(self._start(**kwargs))

    def log(
        self, 
        message: str, 
        level: int = logging.INFO
    ) -> None:
        logging.getLogger(__name__).log(level, message)

    def _init_log(self) -> None:
        logging.getLogger("telethon").setLevel(logging.WARNING)
        logging.basicConfig(
            format='[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
            datefmt='%d-%b-%y %H:%M:%S',
            handlers = [
                RotatingFileHandler(
                    'eclipse.log',
                    maxBytes=1024*1024,
                    backupCount=5
                    ),
                logging.StreamHandler()
                ],
            level=logging.INFO,
        )
        self.log("Initialized Logger Successfully", level=logging.INFO)

    def add_handler(self, func, *args, **kwargs):
        if func in [_[0] for _ in self.list_event_handlers()]:
            return
        self.add_event_handler(func, *args, **kwargs)

    async def _import_module(
        self,
        directory: str,
        include: Optional[Union[str, List[str]]] = None,
        exclude: Optional[Union[str, List[str]]] = None,
        log: bool = False
    ) -> List[str]:
        directory_path = Path(directory)

        if not directory_path.exists() or not directory_path.is_dir():
            self.log(f"Directory {directory_path} does not exist or is not accessible", level=logging.ERROR)
            return []

        loaded_plugins = []

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    plugin_path = Path(os.path.join(root, file))
                    plugin_name = plugin_path.stem
                    if include and plugin_name not in include:
                        continue
                    if exclude and plugin_name in exclude:
                        continue

                    try:
                        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                        plugin_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(plugin_module)
                        self._initialize_plugin(plugin_module)
                        if log:
                            self.log(f"Loaded \"{plugin_name}\" from \"{plugin_path}\"", level=logging.INFO)
                        loaded_plugins.append(plugin_name)
                    except Exception as e:
                        if log:
                            self.log(f"Error loading \"{plugin_name}\": {e}", level=logging.ERROR)

        if log:
            self.log(f'Successfully loaded {len(loaded_plugins)} plugin{"s" if len(loaded_plugins) != 1 else ""}', level=logging.INFO)
        return loaded_plugins

    def _initialize_modules(self, plugin_module):
        if hasattr(plugin_module, 'on_load') and callable(plugin_module.on_load):
            plugin_module.on_load(self)
        self._plugins[plugin_module.__name__] = plugin_module

    def reload_modules(self, directory: str):
        self._plugins = {}
        self._import_module(directory, log=True)

    def unload_modules(self, plugin_name: str):
        if plugin_name in self._plugins:
            plugin_module = self._plugins.pop(plugin_name)
            if hasattr(plugin_module, 'on_unload') and callable(plugin_module.on_unload):
                plugin_module.on_unload(self)

    async def _start(self, **kwargs):
        self.log("Trying to login.")
        try:
            await self.start(**kwargs) 
        except ApiIdInvalidError:
            self.log("API ID and API_HASH combination does not match!", level=logging.CRITICAL)

            sys.exit()
        except (AuthKeyDuplicatedError, EOFError) as er:
            
            self.log("String session expired.", level=logging.CRITICAL)
        except (AccessTokenExpiredError, AccessTokenInvalidError):
            self.log(
                "Bot token is expired or invalid. Create new from @Botfather and add in BOT_TOKEN config!",
                level=logging.CRITICAL,
            )
            sys.exit()
        self._setup_localization()

    async def load_all_modules(self):
        self._import_module("eclipse/modules/*.py", log=True)
        self.reload_module("eclipse/modules/*.py", log=True)
        
    async def _run(self):
        await self.load_all_modules()
        self.log(
            f"[Solar] Eclipse userbot has been started for user {await self.get_me().first_name}.",
            level=logging.INFO,
        )
        if self.lunar_mode is True:
            self.log(
                "[Lunar] Eclipse is running, Assistant is disabled check help to see how to enable it",
                level=logging.INFO,
            )
            
    def run(self):
        self.loop.run_until_complete(self._run())

    def run_in_loop(self, function):
        return self.loop.run_until_complete(function)
    
