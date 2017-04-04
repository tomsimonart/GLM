#!/usr/bin/env python3

import glob
if __name__ == "__main__" and __package__ == None:
    from libs.rainbow import color, msg
else:
    from .libs.rainbow import color, msg


VERSION = "0.0.2"
PLUGIN_PREFIX = "plugins"
PLUGIN_DIRECTORY = "./" + PLUGIN_PREFIX + "/"


def plugin_scan(_dir=PLUGIN_DIRECTORY):
    """Scans the plugin directory"""
    return [x.replace(_dir, '')
            for x in glob.glob(_dir + "*.py")
            if x.replace(_dir, '') != "__init__.py"]


def import_plugin(plugin):
    try:
        _temp = __import__(plugin)
        main_plugin = getattr(_temp, plugin.replace(
            PLUGIN_PREFIX + '.', ""))
        msg("plugin imported", 0, "import_plugin", plugin)
        return main_plugin

    except ImportError as ie:
        msg("Import error", 2, "import_plugin", ie)


def plugin_checker(main_plugin, matrix=True, show=False) -> bool:
    if not hasattr(main_plugin, "Plugin"):
        msg("Plugin outdated", 2, "plugin_checker")
        return False
    else:
        loaded_plugin = main_plugin.Plugin(matrix=matrix, show=show)
    if not hasattr(loaded_plugin, "start"):
        msg("Plugin outdated", 2, "plugin_checker")
        return False
    if not hasattr(loaded_plugin, "version"):
        msg("Plugin outdated", 2, "plugin_checker")
        return False
    else:
        if loaded_plugin.version != VERSION:
            msg("Plugin outdated", 2, "plugin_checker", loaded_plugin.version)
            return False
        else:
            msg("Plugin version ok", 0, "plugin_checker", loaded_plugin.version)
    return loaded_plugin


def plugin_loader(plugin, matrix=False, show=True) -> bool:
    main_plugin = import_plugin(PLUGIN_PREFIX + "." + plugin.replace(".py", ''))
    loaded_plugin = plugin_checker(main_plugin, matrix=matrix, show=show)
    if loaded_plugin is not False:
        print_plugin_info(loaded_plugin)
        loaded_plugin.start()

def print_plugin_info(plugin):
    if hasattr(plugin, "name"):
        print(color(plugin.name, "red"))
    else:
        msg("No name", 1, "print_plugin_info")
    if hasattr(plugin, "author"):
        print(color(plugin.author, "green"))
    else:
        msg("No author", 1, "print_plugin_info")
    if hasattr(plugin, "version"):
        print(color(plugin.version, "magenta"))
    else:
        msg("No version", 1, "print_plugin_info")
    input()


def plugin_selector(plugins) -> str:
    for num, plugin in enumerate(plugins):
        print(num, plugin, sep=") ")

    select = input("Select plugin: ")
    return plugins[int(select)]


def main():
    plugin_loader(plugin_selector(plugin_scan()))

if __name__ == '__main__':
    main()
