from zope.interface import Interface
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import PythonIdentifier
from z3c.caching.registry import register

class IRuleset(Interface):
    for_ = GlobalObject(
            title=u"Object to be configured",
            description=u"The object for which the cache ruleset is to be defined",
            default=None,
            required=True)

    ruleset = PythonIdentifier(
            title=u"ruleset",
            description=u"The id of the cache ruleset to use",
            default=None,
            required=True)


def ruleset(_context, for_, ruleset):
    _context.action(
            discriminator=("registerCacheRule", for_),
            callable = register,
            args = (for_, ruleset))


