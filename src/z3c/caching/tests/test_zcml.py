from unittest import TestCase

from zope.configuration import xmlconfig

from z3c.caching.registry import getGlobalRulesetRegistry
import z3c.caching.tests
from z3c.caching.tests.test_registry import TestView

class TestZCMLDeclarations(TestCase):

    def setUp(self):
        self.registry = getGlobalRulesetRegistry()
    
    def tearDown(self):
        xmlconfig._clearContext()
        self.registry.clear()

    def test_simple_registration(self):
        i = TestView()
        self.failUnless(self.registry[i] is None)
        
        zcml = xmlconfig.XMLConfig("test1.zcml", z3c.caching.tests)
        zcml()
        
        i = TestView()
        self.assertEqual(self.registry[i], "first")

    def test_conflicting_registrations(self):
        zcml = xmlconfig.XMLConfig("test2.zcml", z3c.caching.tests)
        self.assertRaises(Exception, zcml) # ZCML conflict error

def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
