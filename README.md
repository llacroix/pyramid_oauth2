Pyramid oauth2
==============

Easy way to integrate oauth2 in your project.
It currently only support authentication, and access_token reception

Installing
-----------

    pip install pyramid_oauth2

Using
=====

When configuring pyramid, you can use the new function `add_oauth2_provider`

    config.add_oauth2_provider(provider)

The provider class can be imported from `pyramid_oauth2`. 

    from pyramid_oauth2 import Provider

    provider = Provider(name, client_id, client_secret, auth_url, access_token_url, callback_callable)

The callback callable is called when you receive your access token. By default, it does nothing. But you can add a callback
to handle the access token received. 
