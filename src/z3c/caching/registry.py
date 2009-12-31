""" Rulesets are registered for entities, which can be a type, an interface or
even even a specific interface. This means the lookup mechanism needs to be
aware of all of those and deal with things like derived classes as well.
Luckily we have a framework which already implements that: zope.component.

We will (ab)use the zope.component registries by registering a dummy adapter
for the entity to a special ICacheRule interface and which will always return
the ruleset id. """
import warnings
from zope.interface import implements
from zope.component import adapts, getGlobalSiteManager
from zope.component.interfaces import IComponents

from interfaces import ICacheRule, IRulesetRegistry

class CacheRule(object):
    __slots__ = ("id")
    implements(ICacheRule)
    
    def __init__(self, identifier):
        self.id = identifier

def get_context_to_cacherule_adapter_factory(rule):
    """Given a cache rule return an adapter factory which expects an object 
    but only returns the pre-specified cache rule."""
    def CacheRuleFactory(context):
        return CacheRule(rule)
    CacheRuleFactory.id = rule
    return CacheRuleFactory

class RulesetRegistry(object):

    implements(IRulesetRegistry)
    adapts(IComponents)

    def __init__(self, registry):
        self.registry = registry

    def register(self, obj, rule):
        rule = str(rule) # We only want ascii, tyvm
        
        factory = get_context_to_cacherule_adapter_factory(rule)
        existing = self.directLookup(obj)
        if existing is None:
            # Only register if we haven't got this one already
            self.registry.registerAdapter(factory, provided=ICacheRule, required=(obj,))
        else:
            warnings.warn("Ignoring attempted to register caching rule %s for %s.  %s is already registered." % (rule, `obj`, existing))
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
        rule = ICacheRule(obj, None)
        if rule is not None:
            return rule.id
        return None
    
    def enumerate(self):
        seen = set()
        for reg in self.registry.registeredAdapters():
            if reg.provided == ICacheRule and reg.factory.id not in seen:
                yield reg.factory.id
                seen.add(reg.factory.id)
    
    def directLookup(self, obj):
        """Find a rule _directly_ assigned to `obj`"""
        for rule in self.registry.registeredAdapters():
            if rule.provided != ICacheRule:
                continue
            if rule.required == (obj, ):
                return rule.factory(None).id
        return None

    __getitem__ = lookup

def getGlobalRulesetRegistry():
    return IRulesetRegistry(getGlobalSiteManager())
