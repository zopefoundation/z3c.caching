""" Rulesets are registered for entities, which can be a type, an interface or
even even a specific interface. This means the lookup mechanism needs to be
aware of all of those and deal with things like derived classes as well.
Luckily we have a framework which already implements that: zope.component.

We will (ab)use the zope.component registries by registering a dummy adapter
for the entity to a special ICacheRule interface and which will always return
the ruleset id. """

from zope.interface import implements
from zope.component import adapts, getGlobalSiteManager
from zope.component.interfaces import IComponents

from interfaces import ICacheRule, IRulesetRegistry

class CacheRule(object):
    __slots__ = ("id")
    implements(ICacheRule)
    
    def __init__(self, identifier):
        self.id = identifier

class RulesetRegistry(object):

    implements(IRulesetRegistry)
    adapts(IComponents)

    def __init__(self, registry):
        self.registry = registry

    def register(self, obj, rule):
        def r(context):
            return lambda r=rule:r
        self.registry.registerAdapter(r, provided=ICacheRule, required=(obj,))
        return None


    def unregister(self, obj):
        self.registry.unregisterAdapter(provided=ICacheRule, required=(obj,))
        return None


    def clear(self):
        # We force the iterator to be evaluated to start with as the backing
        # storage will be changing size
        for rule in list(self.registry.registeredAdapters()):
            if rule.provided != ICacheRule:
                continue # Not our responsibility
            else:
                self.registry.unregisterAdapter(factory=rule.factory,
                                                provided=rule.provided, 
                                                required=rule.required)
        return None

    def lookup(self, obj):
        ruler=ICacheRule(obj, None)
        if ruler is not None:
            return ruler()
        return None


    __getitem__ = lookup

# Set up RulesetRegistry as an adapter for component roots
getGlobalSiteManager().registerAdapter(RulesetRegistry)

def getGlobalRulesetRegistry():
    return IRulesetRegistry(getGlobalSiteManager())
