from unittest import TestCase
import zope.component.testing

from zope.interface import implements
from zope.component import adapts, provideAdapter, queryMultiAdapter
from zope.browser.interfaces import IView

from z3c.caching.interfaces import ILastModified
from z3c.caching.lastmodified import viewDelegateLastModified

class TestLastModified(TestCase):

    def setUp(self):
        provideAdapter(viewDelegateLastModified)
    
    def tearDown(self):
        zope.component.testing.tearDown()
    
    def test_no_adapter(self):
        
        class DummyView(object):
            implements(IView)
            
            def __init__(self, context, request):
                self.context = context
                self.request = request
        
        class DummyContext(object):
            pass
        
        class DummyRequest(dict):
            pass
        
        context = DummyContext()
        request = DummyRequest()
        
        lastModified = queryMultiAdapter((context, request,), ILastModified)
        self.assertEquals(None, lastModified)
    
    def test_with_adapter(self):
        
        class DummyView(object):
            implements(IView)
            
            def __init__(self, context, request):
                self.context = context
                self.request = request
        
        class DummyContext(object):
            pass
        
        class DummyRequest(dict):
            pass
        
        class DummyLastModified(object):
            implements(ILastModified)
            adapts(DummyContext, DummyRequest)
            
            def __init__(self, context, request):
                self.context = context
                self.request = request
        
        provideAdapter(DummyLastModified)
        
        context = DummyContext()
        request = DummyRequest()
        
        lastModified = queryMultiAdapter((context, request,), ILastModified)
        self.failUnless(isinstance(lastModified, DummyLastModified,))
        
        self.assertEquals(context, lastModified.context)
        self.assertEquals(request, lastModified.request)
    
def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
