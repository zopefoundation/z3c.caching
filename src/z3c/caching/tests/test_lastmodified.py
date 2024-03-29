from unittest import TestCase

import zope.component.testing
from zope.browser.interfaces import IView
from zope.component import adapter
from zope.component import provideAdapter
from zope.interface import implementer

from z3c.caching.interfaces import ILastModified
from z3c.caching.lastmodified import viewDelegateLastModified


class TestLastModified(TestCase):

    def setUp(self):
        provideAdapter(viewDelegateLastModified)

    def tearDown(self):
        zope.component.testing.tearDown()

    def test_no_adapter(self):

        @implementer(IView)
        class DummyView:

            def __init__(self, context, request):
                self.context = context
                self.request = request

        class DummyContext:
            pass

        class DummyRequest(dict):
            pass

        context = DummyContext()
        request = DummyRequest()

        view = DummyView(context, request)

        lastModified = ILastModified(view, None)
        self.assertIsNone(lastModified)

    def test_with_adapter(self):

        @implementer(IView)
        class DummyView:

            def __init__(self, context, request):
                self.context = context
                self.request = request

        class DummyContext:
            pass

        class DummyRequest(dict):
            pass

        @implementer(ILastModified)
        @adapter(DummyContext)
        class DummyLastModified:

            def __init__(self, context):
                self.context = context
                self.request = request

        provideAdapter(DummyLastModified)

        context = DummyContext()
        request = DummyRequest()

        view = DummyView(context, request)

        lastModified = ILastModified(view)
        self.assertIsInstance(lastModified, DummyLastModified)

        self.assertEqual(context, lastModified.context)
        self.assertEqual(request, lastModified.request)


def test_suite():
    import unittest
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
