from zope.dublincore.interfaces import IDCTimes
from Products.CMFCore.interfaces import ICatalogableDublinCore


class ILastModified(Interface):
    def __call__(context):
        """Return the last modification date for an object.""" 


@adapter(ICatalogableDublinCore)
@implementer(ILastModified)
def CatalogableDublinCoreLastModified(obj):
    return obj.modified()


@adapter(IDCTimes)
@implementer(ILastModified)
def DCTimesLastModified(obj):
    return obj.modified()


@adapter(IBrowserView)
@implementer(ILastModified)
def BrowserViewLastModified(obj):
    if not has_attr(aq_base(self.context, "context")):
        return None

    context=aq_base(self.context.context)
    lm=ILastModified(context, None)
    if lm is not None:
        return lm(context)

    return None

