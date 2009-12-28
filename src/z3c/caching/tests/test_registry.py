from unittest import TestCase
import warnings
from zope.interface import Interface
from zope.interface import implements

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
    
    def tearDown(self):
        self.registry.clear()

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
    
    def test_most_specific_interface_wins(self):
        self.registry.register(ITestView, "frop")
        self.registry.register(IMoreSpecificTestView, "fribble")
        i=OtherTestView()
        self.assertEqual(self.registry[i], "fribble")
    
    def test_direct_lookup_for_interface_works(self):
        self.registry.register(ITestView, "frop")
        self.assertEqual(self.registry.directLookup(ITestView), "frop")

    def test_direct_lookup_for_daughter_fails(self):
        self.registry.register(ITestView, "frop")
        self.assertEqual(self.registry.directLookup(IMoreSpecificTestView), None)
    
    def test_registration_on_class_ignores_any_interface_relationship(self):
        self.registry.register(TestView, "frop")
        
        i=OtherTestView()
        self.assertEqual(self.registry[i], None)

        i=TestView()
        self.assertEqual(self.registry[i], "frop")

    def test_registration_on_class_wins_over_interface_registration(self):
        self.registry.register(ITestView, "frop")
        self.registry.register(TestView, "fribble")
        
        i=TestView()
        self.assertEqual(self.registry[i], "fribble")

    def test_ruleset_registered_twice(self):
        self.registry.register(ITestView, "frop")

        # Hide the warning generated, that's for users, not tests.
        warnings.simplefilter("ignore")
        self.registry.register(ITestView, "fribble")
        warnings.simplefilter("default")

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
    