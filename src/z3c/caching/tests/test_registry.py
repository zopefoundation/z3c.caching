from unittest import TestCase
import warnings
from zope.interface import Interface
from zope.interface import implementer

from zope.component import provideAdapter
from zope.component import provideUtility

from z3c.caching.registry import RulesetRegistry
from z3c.caching.registry import getGlobalRulesetRegistry

import zope.component.testing


class ITestView(Interface):
    pass


class IMoreSpecificTestView(ITestView):
    pass


@implementer(ITestView)
class TestView(object):
    pass


@implementer(IMoreSpecificTestView)
class OtherTestView(object):
    pass


class IDummy(Interface):
    pass


class TestRulesetRegistry(TestCase):

    def setUp(self):
        provideAdapter(RulesetRegistry)
        self.registry = getGlobalRulesetRegistry()

    def tearDown(self):
        self.registry.clear()
        zope.component.testing.tearDown()

    def test_no_ruleset_returned_if_unregistered(self):
        self.assertIsNone(self.registry[None])

    def test_ruleset_for_class(self):
        self.registry.register(TestView, "frop")
        i = TestView()
        self.assertEqual(self.registry[i], "frop")

    def test_ruleset_for_interface(self):
        self.registry.register(ITestView, "frop")
        i = TestView()
        self.assertEqual(self.registry[i], "frop")

    def test_most_specific_interface_wins(self):
        self.registry.register(ITestView, "frop")
        self.registry.register(IMoreSpecificTestView, "fribble")
        i = OtherTestView()
        self.assertEqual(self.registry[i], "fribble")

    def test_direct_lookup_for_interface_works(self):
        self.registry.register(ITestView, "frop")
        self.assertEqual(self.registry.directLookup(ITestView), "frop")

    def test_direct_lookup_for_daughter_fails(self):
        self.registry.register(ITestView, "frop")
        self.assertIsNone(self.registry.directLookup(IMoreSpecificTestView))

    def test_registration_on_class_ignores_any_interface_relationship(self):
        self.registry.register(TestView, "frop")

        i = OtherTestView()
        self.assertEqual(self.registry[i], None)

        i = TestView()
        self.assertEqual(self.registry[i], "frop")

    def test_registration_on_class_wins_over_interface_registration(self):
        self.registry.register(ITestView, "frop")
        self.registry.register(TestView, "fribble")

        i = TestView()
        self.assertEqual(self.registry[i], "fribble")

    def test_ruleset_registered_twice(self):
        self.registry.register(ITestView, "frop")

        # Hide the warning generated, that's for users, not tests.
        warnings.simplefilter("ignore")
        self.registry.register(ITestView, "fribble")
        warnings.simplefilter("default")

        i = TestView()
        self.assertEqual(self.registry[i], "frop")

    def test_unregistering_ruleset_removes_ruleset(self):
        self.registry.register(TestView, "frop")
        self.registry.unregister(TestView)
        self.assertIsNone(self.registry[TestView])

    def test_unregistering_nonexistant_ruleset_doesnt_error(self):
        self.assertIsNone(self.registry[TestView])
        self.registry.unregister(TestView)
        self.assertIsNone(self.registry[TestView])

    def test_clearing_registry_removes_rulesets(self):
        self.registry.register(ITestView, "frop")

        self.registry.clear()

        i = TestView()
        self.assertIsNone(self.registry[i])

    def test_clearing_ignores_other_utilities(self):

        @implementer(IDummy)
        class DummyUtility(object):
            pass

        provideUtility(DummyUtility())

        self.registry.register(ITestView, "frop")

        self.registry.clear()

        i = TestView()
        self.assertIsNone(self.registry[i])

    def test_clearing_registry_removes_types(self):
        self.registry.declareType("rule1", u"Rule 1", u"First rule")
        self.registry.declareType("rule2", u"Rule 2", u"Second rule")

        self.registry.register(ITestView, "frop")

        self.registry.clear()

        i = TestView()
        self.assertIsNone(self.registry[i])
        self.assertEqual(0, len(list(self.registry.enumerateTypes())))

    def test_declareType_overrides(self):
        self.registry.declareType("rule1", u"Rule 1", u"First rule")
        self.registry.declareType("rule2", u"Rule 2", u"Second rule")
        self.registry.declareType("rule1", u"Rule One", u"Rule uno")

        rules = list(self.registry.enumerateTypes())
        rules.sort(key=lambda x: x.name)

        self.assertEqual(2, len(rules))
        self.assertEqual("rule1", rules[0].name)
        self.assertEqual(u"Rule One", rules[0].title)
        self.assertEqual(u"Rule uno", rules[0].description)
        self.assertEqual("rule2", rules[1].name)
        self.assertEqual(u"Rule 2", rules[1].title)
        self.assertEqual(u"Second rule", rules[1].description)

    def test_enumerateTypes(self):
        self.registry.declareType("rule1", u"Rule 1", u"First rule")
        self.registry.declareType("rule2", u"Rule 2", u"Second rule")

        rules = list(self.registry.enumerateTypes())
        rules.sort(key=lambda x: x.title)

        self.assertEqual(2, len(rules))
        self.assertEqual("rule1", rules[0].name)
        self.assertEqual(u"Rule 1", rules[0].title)
        self.assertEqual(u"First rule", rules[0].description)
        self.assertEqual("rule2", rules[1].name)
        self.assertEqual(u"Rule 2", rules[1].title)
        self.assertEqual(u"Second rule", rules[1].description)

    def test_enumerate_empty(self):
        self.assertEqual(set([]), set(self.registry.enumerateTypes()))

    def test_set_explicit_mode(self):
        self.registry.explicit = True

        with self.assertRaises(LookupError):
            self.registry.register(TestView, "rule1")
        self.assertIsNone(self.registry.lookup(TestView()))

        self.registry.declareType("rule1", u"Rule 1", u"First rule")
        self.registry.register(TestView, "rule1")

        self.assertEqual("rule1", self.registry.lookup(TestView()))

    def test_disable_explicit_mode(self):
        self.registry.explicit = True

        with self.assertRaises(LookupError):
            self.registry.register(TestView, "rule1")
        self.assertIsNone(self.registry.lookup(TestView()))

        self.registry.explicit = False

        self.registry.register(TestView, "rule1")
        self.assertEqual("rule1", self.registry.lookup(TestView()))


class TestConvenienceAPI(TestCase):

    def setUp(self):
        provideAdapter(RulesetRegistry)
        self.registry = getGlobalRulesetRegistry()

    def tearDown(self):
        self.registry.clear()
        zope.component.testing.tearDown()

    def test_no_ruleset_returned_if_unregistered(self):
        from z3c.caching.registry import lookup
        self.assertIsNone(lookup(None))

    def test_ruleset_for_class(self):
        from z3c.caching.registry import register, lookup
        register(TestView, "frop")
        i = TestView()
        self.assertEqual(lookup(i), "frop")

    def test_ruleset_for_interface(self):
        from z3c.caching.registry import register, lookup
        register(ITestView, "frop")
        i = TestView()
        self.assertEqual(lookup(i), "frop")

    def test_most_specific_interface_wins(self):
        from z3c.caching.registry import register, lookup
        register(ITestView, "frop")
        register(IMoreSpecificTestView, "fribble")
        i = OtherTestView()
        self.assertEqual(lookup(i), "fribble")

    def test_unregistering_ruleset_removes_ruleset(self):
        from z3c.caching.registry import register, unregister, lookup
        register(TestView, "frop")
        unregister(TestView)
        self.assertIsNone(lookup(TestView))

    def test_unregistering_nonexistant_ruleset_doesnt_error(self):
        from z3c.caching.registry import unregister, lookup
        self.assertIsNone(lookup(TestView))
        unregister(TestView)
        self.assertIsNone(lookup(TestView))

    def test_declareType_enumerateTypes(self):
        from z3c.caching.registry import declareType, enumerateTypes
        declareType("rule1", u"Rule 1", u"Rule one")

        rules = list(enumerateTypes())
        rules.sort(key=lambda x: x.name)

        self.assertEqual(1, len(rules))
        self.assertEqual("rule1", rules[0].name)
        self.assertEqual(u"Rule 1", rules[0].title)
        self.assertEqual(u"Rule one", rules[0].description)

    def test_set_explicit_mode(self):
        from z3c.caching.registry import setExplicitMode

        self.assertFalse(self.registry.explicit)
        setExplicitMode()
        self.assertTrue(self.registry.explicit)
        setExplicitMode(False)
        self.assertFalse(self.registry.explicit)
        setExplicitMode(True)
        self.assertTrue(self.registry.explicit)


class TestNotSetUp(TestCase):

    def test_getGlobalRulesetRegistry(self):
        from z3c.caching.registry import getGlobalRulesetRegistry
        self.assertIsNone(getGlobalRulesetRegistry())

    def test_register(self):
        from z3c.caching.registry import register
        with self.assertRaises(LookupError):
            register(TestView, 'testrule')

    def test_unregister(self):
        from z3c.caching.registry import unregister
        with self.assertRaises(LookupError):
            unregister(TestView)

    def test_lookup(self):
        from z3c.caching.registry import lookup
        self.assertIsNone(lookup(TestView))

    def test_enumerateTypes(self):
        from z3c.caching.registry import enumerateTypes
        with self.assertRaises(LookupError):
            enumerateTypes()

    def test_declareType(self):
        from z3c.caching.registry import declareType
        with self.assertRaises(LookupError):
            declareType('name', 'title', 'description')

    def test_setExplicitMode(self):
        from z3c.caching.registry import setExplicitMode
        with self.assertRaises(LookupError):
            setExplicitMode()


def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
