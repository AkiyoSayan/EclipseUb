import os
import yaml
from eclipse import config

class Language:
    def __init__(self, *args, **kwargs, eclipse):
        self.lang_code = "en"
        self.lang_strings = {}
        self.lang_strings_cache = {}
        self.eclipse = eclipse
      
    @functools.lru_cache(maxsize=None)
    def load_strings(self, lang_code: str = "en") -> Dict[str, str]:
        lang_file = os.path.join("langs", f"{lang_code}.yaml")
        if os.path.exists(lang_file):
            with open(lang_file, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        else:
            self.eclipse.log(f"Localization file not found for '{lang_code}'", level=logging.ERROR)
            return {}

    def get_string(self, key: str) -> str:
        lang_strings = self.lang_strings_cache.get(config.LANG)
        if lang_strings is None:
            lang_strings = self.load_strings(config.LANG)
            self.lang_strings_cache[config.LANG] = lang_strings
        return lang_strings.get(key, f"Missing translation for key '{key}'")

    def get_supported_languages(self) -> List[str]:
        lang_files = os.listdir("langs")
        return [lang_file.split(".")[0] for lang_file in lang_files if lang_file.endswith(".yaml")]

    def _setup_localization(self) -> None:
        lang_files = os.listdir("langs")
        self.eclipse.log("Setting up Languages.", level=logging.INFO)
        if not lang_files:
            self.eclipse.log("Localization files not found!", level=logging.ERROR)
            self.eclipse.log("Using the default language - English.", level=logging.INFO)
            self.load_strings()  # Load default language
        else:
            self.eclipse.log("Localization setup complete!", level=logging.INFO)
