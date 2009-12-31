Introduction
============

Caching of web pages is a complicated process: there are many possible
policies to choose from, and the right policy can depend on factors such as
who is making the request, the URL is being retrieved and resource
negotiation settings such as accepted languages and encodings,

Hardcoding caching logic in an application is not desirable, especially for
reusable code. It is also not possible to allow an administrator to manually
configure the caching headers for every resource in an application. This
packages tries to address this problem by providing a cache ruleset
framework: it allows implementors to specify a ruleset for every component.
Administrators can then define a policy which dictates the correct caching
behaviour for each ruleset.

Depending on your environment there are different options for turning
the ruleset into HTTP caching headers.

* If you are using Plone_ 3 and CacheFu_ you can use `five.caching`_ to
  integrate with CacheSetup.
* If you are using Zope 2.12 or later, you can use `plone.caching`_ to
  integrate with the publisher events.
* If you are using Plone 4, you can also use `plone.app.caching`_, which
  provides UI and default operations.
* In a WSGI environment you could set the ruleset in `environ` or a response
  header and add a piece of middleware which acts on those hints.

Usage
=====

You can register rulesets using either zcml or direct python. If you
use zcml you can use the ``cache:ruleset`` directive::

  <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser"
      xmlns:cache="http://namespaces.zope.org/cache"/>

    <cache:ruleset
        for=".frontpage.FrontpageView"
        ruleset="plone-content-types"
        />

    <browser:page
        for="..interfaces.IFrontpage"
        class=".frontpage.FrontpageView"
        name="frontpage_view"
        template="templates/frontpage_view.pt"
        permission="zope2.View" />

  </configure>

This example sets up a browser view called ``frontpage_view`` and
associates it with the ``plone-content-types`` ruleset.

You can specify either a class or an interface in the ``for`` attribute. As
with an adapter registration, a more specific registration can be used to
override a more generic one.

If you prefer to use python directly you can do so::

   from z3c.caching.registry import register
   from frontpage import FrontpageView

   register(FrontpageView, "plone-content-types")

To find the ruleset for an object use the ``lookup`` method::

   from z3c.caching.registry import getGlobalRulesetRegistry
   registry = getGlobalRulesetRegistry()

   cacheRule = registry.lookup(FrontpageView)

Caching operations
------------------

This package does not directly include support for performing caching
operations such as setting response headers. However, it defines interfaces
which can be used by a framework such as `five.caching`_ or `plone.caching`_
for this purpose.

The basic principle is that a *cache rule* is looked up for the view or other
resource published, as shown above. This is a string, which can then be mapped
to a caching operation. Operations can be implemented using one of the
following two interfaces::

    class IResponseMutator(Interface):
        """Represents a caching operation, typically setting of response headers.
    
        Should be registered as a named multi-adapter from a cacheable object
        (e.g. a view, or just Interface for a general operation) and the request.
    
        A higher level framework is assumed to do something like this::
    
            registry  = getGlobalRulesetRegistry()
            published = getPublishiedView(request)
        
            cacheRule = registry.lookup(published)
            operation = getOperationFor(cacheRule)
        
            mutator   = queryMultiAdapter((published, request,),
                                            IResponseMutator, name=operation)
            mutator(response)
    
        Here, a cache rule is looked up for the published view. An operation is
        then looked up for the cache rule (presuming there exists some mapping
        from cache rules to operations) and invoked.
        """
    
        def __call__(response):
            """Mutate the response
            """

    class ICacheInterceptor(Interface):
        """Represents a caching intercept, typically for the purposes of sending
        a 304 response.
    
        Should be registered as a named multi-adapter from a cacheable object
        (e.g. a view, or just Interface for a general operation) and the request.
    
        A higher level framework is assumed to do something like this::
    
            registry  = getGlobalRulesetRegistry()
            published = getPublishiedView(request)
        
            cacheRule = registry.lookup(published)
            operation = getInterceptorFor(cacheRule)
        
            intercept = queryMultiAdapter((published, request,),
                                            ICacheInterceptor, name=operation)
            if intercept(response):
                return # abort rendering and return what we have
        
            # continue as normal
        """
    
        def __call__(response):
            """Mutate the response if required. Return True if the response should
            be intercepted. In this case, normal rendering may be aborted and the
            response returned as-is.
            """

In addition, a helper adapter interface is defined which can be used to
determine the last modified date of a given content item::

    class ILastModified(Interface):
        """An abstraction to help obtain a last-modified date for a published
        resource.
    
        Should be registered as an unnamed multi-adapter from a published object
        (e.g. a view) and the request.
        """
    
        def __call__():
            """Return the last-modified date, as a Python datetime object.
            """

One implementation exists for this interface: When looked up for a Zope
browser view, it will delegate to an ``ILastModified`` adapter on the view's
context.

.. _Plone: http://plone.org/
.. _CacheFu: http://plone.org/products/cachefu
.. _five.caching: http://pypi.python.org/pypi/five.caching
.. _plone.caching: http://pypi.python.org/pypi/plone.caching
.. _plone.app.caching: http://pypi.python.org/pypi/plone.app.caching
