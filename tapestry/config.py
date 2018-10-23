"""
Configurations

* GalleryConfig, MenuConfig can read and parse configuration INI files
* TitlesConfig can read TXT file with titles for images in gallery
"""

import configparser
import os
import re


class BaseConfig:
    """
    Base config class with common methods.
    """
    filename = None

    def __init__(self, dirpath):
        self.dirpath = dirpath
        self.filepath = os.path.abspath(os.path.join(dirpath, self.filename))

    def exists(self):
        """
        Return True if file self.filename exists on given path.
        """
        return os.path.exists(self.filepath) and os.path.isfile(self.filepath)

    def process(self):
        """
        Main method returning (status, config_dict), where status=True represent fact that provided
        file was sucessfully processed. Value False tell us that default values was returned since
        there was some problem with config file.
        """
        raise NotImplemented


class BaseIniConfig(BaseConfig):
    """
    Base INI config class.
    """
    defaults = {}
    filename = 'config.ini'
    section = None

    def process(self):
        if not self.exists():
            return False, self.defaults

        config = configparser.ConfigParser()
        config.read(self.filepath)
        if self.section not in config:
            return False, self.defaults

        return True, dict(self.process_content(config[self.section]))

    def parse_item(self, section, key, method, parser=None):
        """
        Get key from given section with ConfigParser's method (like `getint`). If parser is provided,
        value from file are parsed with it.

        Return tuple (key, value).
        """
        fn = getattr(section, method)
        value = fn(key, None)
        if value is None:
            value = self.defaults[key]
        elif parser is not None:
            value = parser(value)
        return (key, value)

    def process_content(self, section):
        """
        Parse concrete config file. Return list of tuples [(key, value), ...].
        """
        raise NotImplemented

    @staticmethod
    def color_parser(value):
        if value.startswith('#'):
            value = value[1:]
        if len(value) != 6:
            raise RuntimeError
        return tuple([int(value[i:i+2], 16) for i in range(0, len(value), 2)])


class GalleryConfig(BaseIniConfig):
    """
    Configuration file for image gallery.

    Usage:
        gc = GalleryConfig(self.dirpath)
        status, config = gc.process()

    Returned config is dictionary with all configuration parameters, status is False if no config file was found
    (so config will be prepopulated by default values).
    """
    defaults = {
        'autoplay': False,
        'delay': 5000,
        'fontsize': 24,
        'margin': 20,
        'screen_background': (0, 0, 0),
        'screen_color': (255, 255, 255),
    }
    section = 'gallery'

    def process_content(self, section):
        return [
            self.parse_item(section, 'autoplay', 'getboolean'),
            self.parse_item(section, 'delay', 'getint'),
            self.parse_item(section, 'fontsize', 'getint'),
            self.parse_item(section, 'margin', 'getint'),
            self.parse_item(section, 'screen_background', 'get', self.color_parser),
            self.parse_item(section, 'screen_color', 'get', self.color_parser),
        ]


class MenuConfig(BaseIniConfig):
    """
    Configuration file for main menu.

    Usage:
        mc = MenuConfig(dirpath)
        status, menu_config = mc.process()

    Returned config is dictionary with all configuration parameters, status is False if no config file was found
    (so config will be prepopulated by default values).
    """
    defaults = {
        'fontsize': 24,
        'screen_background': (0, 0, 0),
        'screen_color': (255, 255, 255),
        'cursor_background': (255, 255, 255),
        'cursor_color': (0, 0, 0),
        'y_spacing': 10,
        'x_padding': 20,
        'y_padding': 3,
    }
    section = 'menu'

    def process_content(self, section):
        return [
            self.parse_item(section, 'fontsize', 'getint'),
            self.parse_item(section, 'screen_background', 'get', self.color_parser),
            self.parse_item(section, 'screen_color', 'get', self.color_parser),
            self.parse_item(section, 'cursor_background', 'get', self.color_parser),
            self.parse_item(section, 'cursor_color', 'get', self.color_parser),
            self.parse_item(section, 'y_spacing', 'getint'),
            self.parse_item(section, 'x_padding', 'getint'),
            self.parse_item(section, 'y_padding', 'getint'),
        ]


class TitlesConfig(BaseConfig):
    """
    Configuration file with image titles.

    Usage:
        tc = TitlesConfig(self.dirpath)
        status, config = tc.process()

    Returned config is dictionary with filenames and their titles, status is False if no titles file was found
    (and config will be empty dict).
    """
    title_row_format_re = re.compile(r'^([^:]+)\:(.+)$')
    filename = 'titles.txt'

    def process(self):
        out = {}
        if not self.exists():
            return False, out

        with open(self.filepath) as f:
            lines = [l for l in f.readlines() if l.strip()]

        for line in lines:
            m = self.title_row_format_re.match(line)
            if not m:
                continue
            out[m.group(1).strip()] = m.group(2).strip()

        return True, out
