from zope.interface import Interface
from zope.interface import implements
from unittest import TestCase

from z3c.caching.registry import getGlobalRulesetRegistry

class ITestView(Interface):
    pass

class IMoreSpecificTestView(ITestView):
    pass

class TestView(object):
    implements(ITestView)

class OtherTestView(object):
    implements(IMoreSpecificTestView)


class TestRulesetRegistry(TestCase):

    def setUp(self):
        self.registry = getGlobalRulesetRegistry()

    def test_no_ruleset_returned_if_unregistered(self):
        self.failUnless(self.registry[None] is None)

    def test_ruleset_for_class(self):
        self.registry.register(TestView, "frop")
        i=TestView()
        self.assertEqual(self.registry[i], "frop")

    def test_ruleset_for_interface(self):
        self.registry.register(ITestView, "frop")
        i=TestView()
        self.assertEqual(self.registry[i], "frop")

    def test_ruleset_registered_twice(self):
        self.registry.register(ITestView, "frop")
        self.registry.register(ITestView, "fribble")
        i=TestView()
        self.assertEqual(self.registry[i], "frop")

    def test_unregistering_ruleset_removes_ruleset(self):
        self.registry.register(TestView, "frop")
        self.registry.unregister(TestView)
        self.failUnless(self.registry[TestView] is None)

    def test_unregistering_nonexistant_ruleset_doesnt_error(self):
        self.failUnless(self.registry[TestView] is None)
        self.registry.unregister(TestView)
        self.failUnless(self.registry[TestView] is None)

    def test_clearing_registry_removes_rulesets(self):
        self.registry.register(ITestView, "frop")
        i = TestView()
        self.registry.clear()
        self.failUnless(self.registry[i] is None)
