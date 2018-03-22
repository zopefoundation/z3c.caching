import unittest
import zope.component.testing

from zope.interface import implementer

from zope.component import adapter
from zope.component import provideHandler
from zope.component.event import objectEventNotify

from zope.event import notify

from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectRemovedEvent
from zope.lifecycleevent import ObjectMovedEvent

from z3c.caching.interfaces import IPurgeEvent
from z3c.caching.interfaces import IPurgeable

from z3c.caching.purge import purgeOnModified
from z3c.caching.purge import purgeOnMovedOrRemoved


class Handler(object):

    def __init__(self):
        self.invocations = []

    @adapter(IPurgeEvent)
    def handler(self, event):
        self.invocations.append(event)


class FauxContainer(dict):
    pass


class FauxContext(object):

    def __init__(self, parent=None, name=None):
        self.__parent__ = parent
        self.__name__ = name


@implementer(IPurgeable)
class FauxMarkedContext(object):

    def __init__(self, parent=None, name=None):
        self.__parent__ = parent
        self.__name__ = name


class TestPurgeRedispatch(unittest.TestCase):

    def setUp(self):
        self.handler = Handler()
        provideHandler(self.handler.handler)

        provideHandler(objectEventNotify)
        provideHandler(purgeOnModified)
        provideHandler(purgeOnMovedOrRemoved)

    def tearDown(self):
        zope.component.testing.tearDown()

    def test_no_marker(self):
        context = FauxContext(FauxContainer(), 'new')

        notify(ObjectModifiedEvent(context))
        notify(ObjectAddedEvent(context))
        notify(ObjectRemovedEvent(context))

        self.assertEqual(0, len(self.handler.invocations))

    def test_modified(self):
        context = FauxMarkedContext()

        notify(ObjectModifiedEvent(context))

        self.assertEqual(1, len(self.handler.invocations))
        self.assertEqual(context, self.handler.invocations[0].object)

    def test_added(self):
        context = FauxMarkedContext(FauxContainer(), 'new')

        notify(ObjectAddedEvent(context, context.__parent__, 'new'))

        self.assertEqual(0, len(self.handler.invocations))

    def test_moved(self):
        context = FauxMarkedContext(FauxContainer(), 'new')

        notify(ObjectMovedEvent(context, FauxContainer(), 'old',
                                context.__parent__, 'new'))

        self.assertEqual(1, len(self.handler.invocations))
        self.assertEqual(context, self.handler.invocations[0].object)

    def test_renamed(self):
        context = FauxMarkedContext(FauxContainer(), 'new')

        notify(ObjectMovedEvent(context,
                                context.__parent__, 'old',
                                context.__parent__, 'new'))

        self.assertEqual(1, len(self.handler.invocations))
        self.assertEqual(context, self.handler.invocations[0].object)

    def test_removed(self):
        context = FauxMarkedContext(FauxContainer(), 'new')

        notify(ObjectRemovedEvent(context, context.__parent__, 'new'))

        self.assertEqual(1, len(self.handler.invocations))
        self.assertEqual(context, self.handler.invocations[0].object)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
