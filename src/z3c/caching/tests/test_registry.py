from zope.interface import Interface
from zope.interface import implements
from unittest import TestCase
from z3c.caching.registry import cleanupCacheRulesets
from z3c.caching.registry import _registry

class ITestView(Interface):
    pass


class TestView(object):
    implements(ITestView)



class TestRulesetRegistry(TestCase):
    def tearDown(self):
        cleanupCacheRulesets()


    def testRulesetForInstance(self):
        _registry.register(TestView, "frop")
        i=TestView()
        self.assertEqual(_registry[i], "frop")


    def testRulesetViaInterface(self):
        _registry.register(ITestView, "frop")
        i=TestView()
        self.assertEqual(_registry[i], "frop")


    def testUnknownRulesetReturnsNone(self):
        self.failUnless(_registry[None] is None)


    def testUnregister(self):
        _registry.register(TestView, "frop")
        _registry.unregister(TestView, "frop")
        self.failUnless(_registry[TestView] is None)


