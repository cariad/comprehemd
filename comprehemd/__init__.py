import importlib.resources as pkg_resources

with pkg_resources.open_text(__package__, "VERSION") as t:
    __version__ = t.readline().strip()
