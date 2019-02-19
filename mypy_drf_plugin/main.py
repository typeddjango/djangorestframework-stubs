from mypy.plugin import Plugin


class DRFPlugin(Plugin):
    pass


def plugin(version):
    return DRFPlugin
