from zope.interface import Interface
from zope import schema

class IRulesetRegistry(Interface):
    
    def register(obj, rule):
        """Mark objects that are implementers of `obj` to use the caching 
        rule `rule`.
        """
    
    def unregister(obj):
        """Remove any prior rule registration attached to obj in this 
        registry. N.B. registries are hierarchical, a parent may still 
        provide rules.
        """
    
    def clear():
        """Remove all rule registrations in this registry.
        """
    
    def lookup(obj):
        """Return the id of the rule associated with `obj`.  If no rule has 
        been registered `None` is returned.
        """
    
    def __getitem__(obj):
        """Convenience spelling for `lookup(obj)`.
        """
    
    def declareType(name, type, description):
        """Declare a new ruleset type. This will put a new `IRulesetType`
        into the list of objects returned by `enumerate`.
        """
    
    def enumerateTypes():
        """Return a sequence of all unique registered rule set types, as
        ``IRuleSetType`` objects.
        """
    
    explicit = schema.Bool(
            title=u"Explicit mode",
            description=u"If true, ruleset types must be declared before being used.",
            required=True,
            default=False
        )

class IRulesetType(Interface):
    """A ruleset type. The name can be used in a <cache:ruleset /> directive.
    The title and description are used for UI support.
    """
    
    name        = schema.ASCIILine(title=u"Ruleset name")
    title       = schema.TextLine(title=u"Title")
    description = schema.TextLine(title=u"Description", required=False)

class ILastModified(Interface):
    """An abstraction to help obtain a last-modified date for a published
    resource.
    
    Should be registered as an unnamed multi-adapter from a published object
    (e.g. a view) and the request.
    """
    
    def __call__():
        """Return the last-modified date, as a Python datetime object.
        """
