from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.schema import TextLine

from z3c.caching.registry import getGlobalRulesetRegistry


ORDER = 1000001


class IRuleset(Interface):
    for_ = GlobalObject(
        title="Object to be configured",
        description="The object for which the cache ruleset is to be defined",
        default=None,
        required=True)

    ruleset = TextLine(
        title="ruleset",
        description="The id of the cache ruleset to use",
        default=None,
        required=True)


def rulesetType(_context, name, title, description=""):
    # The order is 'late' so that we know getGlobalRulesetRegistry() will
    # return something real. The default order of a configuration action is
    # determined by a counter, so in systems with a large number of components
    # registered, a big number is called for to ensure that we occur after
    # z3c.caching has been configured.
    _context.action(
        discriminator=("declareCacheRuleSetType", name),
        callable=declareType,
        args=(name, title, description,),
        order=ORDER)


def ruleset(_context, for_, ruleset):
    # We need to ensure this has a higher order than rulesetType() always
    _context.action(
        discriminator=("registerCacheRule", for_),
        callable=register,
        args=(for_, ruleset,),
        order=ORDER + 1)


# Handlers
def declareType(name, title, description):
    getGlobalRulesetRegistry().declareType(name, title, description)


def register(for_, ruleset):
    getGlobalRulesetRegistry().register(for_, ruleset)
