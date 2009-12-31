from zope.interface import implementer, Interface
from zope.component import adapter, queryMultiAdapter

from zope.browser.interfaces import IView
from z3c.caching.interfaces import ILastModified

@implementer(ILastModified)
@adapter(IView, Interface)
def viewDelegateLastModified(view, request):
    """When looking up an ILastModified for a view, look up an ILastModified
    for its context. May return None, in which case adaptation will fail.
    """
    return queryMultiAdapter((view.context, request), ILastModified)
