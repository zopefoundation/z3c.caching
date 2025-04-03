Changelog
=========


3.1 (2025-04-03)
----------------

* Add support for Python 3.12, 3.13.

* Drop support for Python 3.7, 3.8.


3.0 (2023-02-08)
----------------

- Drop support for Python 2.7, 3.5, 3.6.
  [icemac]

- Add support for Python 3.9, 3.10, 3.11.
  [icemac]


2.2 (2019-10-16)
----------------

- Fix DeprecationWarnings: import moves from ``zope.component`` to ``zope.interface``.
  Depend on zope.interface >= 3.8.0.
  [jensens]

- Add support for Python 3.8a3.
  [icemac]

2.1 (2018-11-06)
----------------

- Changed ruleset of IRuleset to TextLine to work with
  `zope.configuration >= 4.2`. See
  `Products.CMFPlone#2591 <https://github.com/plone/Products.CMFPlone/issues/2591>`_.
  [pbauer]


2.0 (2018-03-22)
----------------

* Add support for Python 3.5, 3.6, 3.7, PyPy2 and PyPy3.
  [icemac]


2.0a1 - April 22, 2010
----------------------

* Added `Purge`` event and ``IPurgeable` and ``IPurgePaths`` interfaces.
  Although this package doesn't provide any purging support, it is convenient
  to keep the interfaces necessary for other packages to describe their cache
  purging behaviour here. This allows a relatively harmless dependency on
  z3c.caching, even in generic code, as distinct from a higher-level,
  application server specific framework.
  [optilude]

* Added concept of an explicitly declare ruleset type. Optional by default,
  but can be made required by setting `explicit` to `True`.
  [optilude]

* Added ``ILastModified`` implementation for a view which delegates to the
  view's context.
  [optilude]

* Added ``enumerateTypes()`` method to the registry, used to list all currently
  used cache rule ids.
  [optilude]

* Made the registry use the ZCA more directly.
  [matthewwilkes]


1.0b1 - October 15, 2008
------------------------

* Initial release
  [wichert]


