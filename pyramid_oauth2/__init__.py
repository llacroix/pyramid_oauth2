''' 
Oauth2 pyramid
==============

Pyramid addons intended to support completely the oauth2 flows.

It currently only supports one of them. It should be possible
to create a oauth2 provider in the future using this addons.
'''

import urllib
import urllib2

from pyramid.path import DottedNameResolver
from pyramid.view import view_config
from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound

ENABLED_CLIENTS = 'oauth2.clients'
CLIENT_ID = 'oauth2.%s.client_id'
SECRET = 'oauth2.%s.secret'
AUTHORIZE_ENDPOINT = 'oauth2.%s.authorize_endpoint'
TOKEN_ENDPOINT = 'oauth2.%s.token_endpoint'
SCOPE = 'oauth2.%s.scope'
CALLBACK = 'oauth2.%s.callback'

class Provider(object):
    ''' Provider class for when using the client flow.
        This class has for purpopse to keep all the necessary information
        to get a token from a provider. 

        The provider is passed to `config.add_view`

        It as a special __call__ method that will get called once 
        you receive an access_token
    '''

    def __init__(self,name, client_id, secret, authorize_url, access_token_url, callback=None, **kargs):
        self.name = name
        self.client_id = client_id
        self.secret = secret
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.callback = callback
        self.extra = kargs

    def __call__(self, request, data):
        ''' Execute the callback method sent to the provider
        '''
        if self.callback:
            self.callback(request, data)

        raise HTTPFound('/')

    def access_url(self, request):
        ''' Returns an url to get the access token using a request
            code.
        '''
        code = request.params.get('code')

        params = dict()
        params['client_id'] = self.client_id
        params['client_secret'] = self.secret
        params['redirect_uri'] = request.route_url('oauth_callback',
                                                   provider=self.name)
        params['code'] = code
        params['grant_type'] = 'authorization_code'

        #result = "%s?%s" % (self.access_token_url, urllib.urlencode(params))
        params = urllib.urlencode(params)

        return self.access_token_url, params

    def authenticate_url(self, request):
        ''' Returns an url for autentication. It will authenticate you
            to a provider that will return you a request code
        '''
        params = dict(**self.extra)

        params['client_id'] =  self.client_id
        params['redirect_uri'] = request.route_url('oauth_callback',
                                                   provider=self.name)
        params['response_type'] = 'code'

        return "%s?%s" % (self.authorize_url, urllib.urlencode(params))

def authenticate(request):
    ''' Authenticate view that starts the authentication
        flow.
        grant_type [authorization_code]
    '''
    provider = get_provider(request)

    if provider:
        # If provider is defined
        raise HTTPFound(provider.authenticate_url(request))
    else:
        raise NotFound()

def view_callback(request):
    ''' Callback view that receives the request code.
        grant_type [authorization_code]
    '''
    provider = get_provider(request)

    if not provider:
        raise NotFound()

    url, data = provider.access_url(request)
    req = urllib2.Request(url, data)

    data = urllib2.urlopen(req).read()

    provider(request, data)

def get_provider(request):
    ''' Returns a registered provider if exists
    '''
    provider = request.matchdict.get('provider')
    if provider:
        return request.registry.oauth2_providers.get(provider)
    else:
        return None

def add_oauth2_provider(config, provider):
    ''' Adds a provider to the registry in the oauth2_providers
        namespace.
    '''
    config.registry.oauth2_providers[provider.name] = provider

def load_providers(config):
    ''' Loads provider from the config files.

        Each providers should be enabled in 
        oauth2.clients = ...

        And each config should be defined as such.

        For example:
        ============

        oauth2.clients = facebook
        oauth2.facebook.client_id = client_id
        oauth2.facebook.secret = secret_text
        oauth2.facebook.authorize_endpoint = authorization url
        oauth2.facebook.token_endpoint = token url
        oauth2.facebook.scope = scope you want to use
        oauth2.facebook.callback = dotted.string.to.callback:func

    '''
    resolver = DottedNameResolver()
    config.registry.oauth2_providers = dict()
    settings = config.registry.settings

    clients = config.registry.settings.get(ENABLED_CLIENTS)
    for client in clients.split(','):
        scope = settings.get(SCOPE % client)
        authorize_endpoint = settings.get(AUTHORIZE_ENDPOINT % client)
        token_endpoint = settings.get(TOKEN_ENDPOINT % client)
        client_id = settings.get(CLIENT_ID % client)
        secret = settings.get(SECRET % client)
        callback = settings.get(CALLBACK % client)

        if callback:
            callback = resolver.resolve(callback)

        provider = Provider(client, client_id, secret, 
                            authorize_endpoint, token_endpoint, 
                            callback, scope=scope)
        config.add_oauth2_provider(provider)

    

def includeme(config):
    ''' Adds routes and views to pyramid.
    '''
    config.add_route('oauth_authenticate', '/oauth/{provider}/authenticate')
    config.add_view(authenticate, route_name='oauth_authenticate')

    config.add_route('oauth_callback', '/oauth/{provider}/callback')
    config.add_view(view_callback, route_name='oauth_callback')

    config.add_directive('add_oauth2_provider', add_oauth2_provider)

    load_providers(config)
