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
the ruleset into HTTP caching headers. If you are using Plone_
you can use `five.caching`_ to integrate with CacheSetup. In a WSGI
environment you could set the ruleset in `environ` or a response header
and add a piece of middleware which acts on those hints.


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

If you prefer to use python directly you can do so::

   from z3c.caching.registry import register
   from frontpage import FrontpageView

   register(FrontpageView, "plone-content-types")

You can register a ruleset for objects, their interfaces or a base class.

To find the ruleset for an object use the ``lookup`` method::

   from z3c.caching.registry import lookup

   lookup(FrontpageView)


.. _Plone: http://plone.org/
.. _five.caching: http://pypi.python.org/pypi/five.caching

