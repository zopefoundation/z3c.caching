# Rulesets are registered for entities, which can be a type, an interface or even
# even a specific interface. This means the lookup mechanism needs to be aware
# of all of those and deal with things like derived classes as well. Luckily
# we have a framework which already implements that: zope.component.
#
# We will (ab)use the zope.component registries by registering a dummy adapter
# for the entity to a special ICacheRule interface and which will always
# return the ruleset id.

from zope.interface import Interface
from zope.component import getGlobalSiteManager


class _ICacheRule(Interface):
    pass


class RulesetRegistry(object):
    def __init__(self):
        self._rules=set()


    def register(self, obj, rule):
        if obj in self._rules:
            return

        gsm=getGlobalSiteManager()
        def r(context):
            return lambda r=rule:r
        gsm.registerAdapter(r, provided=_ICacheRule, required=(obj,))

        self._rules.add(obj)


    def unregister(self, obj, rule):
        if obj not in self._rules:
            return

        gsm=getGlobalSiteManager()
        gsm.unregisterAdapter(provided=_ICacheRule, required=(obj,))
        self._rules.remove(obj)


    def clear(self):
        gsm=getGlobalSiteManager()
        for obj in self._rules:
            gsm.unregisterAdapter(provided=_ICacheRule, required=(obj,))
        self._rules.clear()


    def lookup(self, obj):
        ruler=_ICacheRule(obj, None)
        if ruler is not None:
            return ruler()
        return None


    __getitem__ = lookup


_registry = RulesetRegistry()

unregister = _registry.unregister
register = _registry.register
lookup = _registry.lookup


def cleanupCacheRulesets():
    global _registry

    _registry.clear()

try:
    from zope.testing.cleanup import addCleanUp
except ImportError:
    # don't have that part of Zope
    pass
else:
    addCleanUp(cleanupCacheRulesets)
    del addCleanUp


__all__ = [ "register", "unregister" ]

