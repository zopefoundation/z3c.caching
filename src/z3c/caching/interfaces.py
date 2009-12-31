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

class IResponseMutator(Interface):
    """Represents a caching operation, typically setting of response headers.
    
    Should be registered as a named multi-adapter from a cacheable object
    (e.g. a view, or just Interface for a general operation) and the request.
    
    A higher level framework is assumed to do something like this::
    
        registry  = getGlobalRulesetRegistry()
        published = getPublishiedView(request)
        
        cacheRule = registry.lookup(published)
        operation = getOperationFor(cacheRule)
        
        mutator   = queryMultiAdapter((published, request,), IResponseMutator, name=operation)
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
        
        intercept = queryMultiAdapter((published, request,), ICacheInterceptor, name=operation)
        if intercept(response):
            return # abort rendering and return what we have
        
        # continue as normal
    """
    
    def __call__(response):
        """Mutate the response if required. Return True if the response should
        be intercepted. In this case, normal rendering may be aborted and the
        response returned as-is.
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
