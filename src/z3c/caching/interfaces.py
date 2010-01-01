from zope.interface import Interface

class IRulesetRegistry(Interface):
    
    def register(obj, rule):
        """Mark objects that are implementers of `obj` to use the caching 
        rule `rule`.  The value for `rule` MUST be a valid python identifier.
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
    
    def enumerate():
        """Return a sequence of all unique registered rule set ids (strings)
        """

class ILastModified(Interface):
    """An abstraction to help obtain a last-modified date for a published
    resource.
    
    Should be registered as an unnamed multi-adapter from a published object
    (e.g. a view) and the request.
    """
    
    def __call__():
        """Return the last-modified date, as a Python datetime object.
        """
