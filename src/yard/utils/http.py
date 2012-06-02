#!/usr/bin/env python
# encoding: utf-8

from django.http import HttpResponse
import json, mimetypes

class HttpResponseUnauthorized(HttpResponse):
    '''
    Http Response for status 401
    '''
    status_code = 401


class FileResponse(HttpResponse):
    '''
    Http Response with file content
    '''
    def __init__(self, content='', status=None, content_type=None):
        HttpResponse.__init__(self, content      = content, 
                                    mimetype     = mimetypes.guess_type(content.name)[0], 
                                    status       = status, 
                                    content_type = content_type, )
        self['Content-Disposition'] = 'attachment; filename=' + content.name


class JsonResponse(HttpResponse):
    '''
    Http Response with Json content type
    '''
    def __init__(self, content='', mimetype=None, status=None):
        HttpResponse.__init__(self, content      = json.dumps( content or [], indent=2 ), 
                                    mimetype     = mimetype, 
                                    status       = status, 
                                    content_type = 'application/json', )


class JsonpResponse(HttpResponse):
    '''
    Http Response with Jsonp content type
    '''
    def __init__(self, content='', mimetype=None, status=None, param='callback'):
        content = json.dumps( content or [], indent=2 )
        HttpResponse.__init__(self, content      = "%s(%s)" %(param, content), 
                                    mimetype     = mimetype,
                                    status       = status, 
                                    content_type = 'text/javascript; charset=utf-8', )


class ProperJsonResponse:
    '''
    Json or Jsonp Response according to request
    '''    
    def __init__(self, request):
        self.__jsonp_param = None
        for param in ['callback', 'jsonp']:
            if param in request.GET:
                self.__jsonp_param = param
                
    def __call__(self, *args, **kwargs):
        if self.__jsonp_param:
            return JsonpResponse(*args, param=self.__jsonp_param, **kwargs) 
        return JsonResponse(*args, **kwargs)
