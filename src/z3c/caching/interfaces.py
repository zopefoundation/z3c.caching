from zope.interface import Interface, Attribute

class ICacheRule(Interface):
    """Represents the cache rule applied to an object."""
    
    id = Attribute("The identifier of this cache rule")
    

class IRulesetRegistry(Interface):
    
    def register(obj, rule):
        """Mark objects that are implementers of `obj` to use the caching 
        rule `rule`.  The value for `rule` MUST be a valid python identifier.
        """
    
    def unregister(obj):
        """Remove any prior rule registration attached to obj in this 
        registry. N.B. registries are hierarchical, a parent may still 
        provide rules."""
    
    def clear():
        """Remove all rule registrations in this registry."""
    
    def lookup(obj):
        """Return the id of the rule associated with `obj`.  If no rule has 
        been registered `None` is returned.
        """