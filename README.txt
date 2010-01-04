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
    
    <cache:rulesetType
        name="plone-content-types"
        title="Plone content types"
        description="Non-folderish content types"
        />
    
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

Above, we also add some metadata about the type of ruleset using the
``<cache:rulesetType />`` directive. This is principally useful for UI support
and can be often be skipped.

If you prefer to use python directly you can do so::

   from z3c.caching.registry import register
   from frontpage import FrontpageView

   register(FrontpageView, "plone-content-types")

To find the ruleset for an object use the ``lookup()`` method::

   from z3c.caching.registry import lookup
   cacheRule = lookup(FrontpageView)

To declare the ruleset type metadata, use the ``declareType`` method::

   from z3c.caching.registry import declareType
   declareType = declareType(name="plone-content-types", \
                             title=u"Plone content types", \
                             description=u"Non-folderish content types")

If you want to get a list of all declared types, use the ``enumerateTypes()``
method::

    from z3c.caching.registry import enumerate
    for type_ in enumerateTypes():
        ...

The ``type_`` object provides ``IRulesetType`` and has attributes for
``name``, ``title`` and ``description``.

Strict mode
-----------

By default, you are not required to declare the type of a ruleset before using
it. This is convenient, but increases the risk of typos or a proliferation of
rulesets that are semantically equivalent. If you want to guard against this
case, you can put the ruleset into explicit mode, like this::

    from z3c.caching.registry import setExplicitMode
    setExplicitMode(True)

Last modified date/time
-----------------------

A helper adapter interface is defined which can be used to determine the last
modified date of a given published object::

    class ILastModified(Interface):
        """An abstraction to help obtain a last-modified date for a published
        resource.
    
        Should be registered as an unnamed adapter from a published object
        (e.g. a view).
        """
    
        def __call__():
            """Return the last-modified date, as a Python datetime object.
            """

One implementation exists for this interface: When looked up for a Zope
browser view, it will delegate to an ``ILastModified`` adapter on the view's
context. Higher level packages may choose to implement this adapter for
other types of publishable resources, and/or different types of view context.

.. _Plone: http://plone.org/
.. _CacheFu: http://plone.org/products/cachefu
.. _five.caching: http://pypi.python.org/pypi/five.caching
.. _plone.caching: http://pypi.python.org/pypi/plone.caching
.. _plone.app.caching: http://pypi.python.org/pypi/plone.app.caching
