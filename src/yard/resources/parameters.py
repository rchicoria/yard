#!/usr/bin/env python
# encoding: utf-8

class ResourceParameters(dict):
    '''
    Dictionary with given resource parameters values
    '''   
    def __init__(self, params={}):
        self.__errors  = {}
        self.__path    = params
        self.validated = {}
        self.__update_nested( params )

    def __update_nested(self, params):
        for key,value in params.iteritems():
            self[key] = value
            self.validated[key] = unicode(value)

    def update(self, params):
        '''
        Updates parameters
        '''
        for key,value in params.iteritems():
            if isinstance(value, Exception):
                self.__errors[key] = unicode(value)
            else:
                self[key.alias] = value
                self.validated[key.name] = unicode(value)
    
    def from_path(self):
        '''
        Returns parameters of type path
        '''
        return self.__path
        
    def from_query(self):
        '''
        Returns parameters of type query
        '''
        return dict( [(k,v) for k,v in self.items() if k not in self.__path] )
    
    def is_valid(self):
        '''
        Were there any errors while processing the parameters
        '''
        return not bool(self.__errors)

    def errors(self):
        '''
        Returns JSON with evaluated errors 
        '''
        return {'Errors': self.__errors if self.__errors else {}}

