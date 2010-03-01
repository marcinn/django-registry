django-registry app
===================

Intro
-----

This reusable app delivers registry-like configuration tool
with configurable backends. Currently provides two backends:
memory and database

Features
--------

  * store configuration in global environment accessed by name (keys),
    where dot (.) is used as separator (ie. "modules.something.show_labels")
  * simple admin model for easy management
  * automatic configuration refresh at runtime after registry changes
    (currently supported only with database backend)

Usage
-----

Reading config is a most used operation. Configuration can be
simply accessed by opening a key:

    import registry
    my_app_config = registry.open('application_name.global_config')


By simple dict-like interface you can access application settings now:

    print my_app_config.get('default_thumbnail_width', 110)
    print my_app_config.get('default_thumbnail_height', 80)

It is equivalent for accessing:
  - application_name.global_config.default_thumbnail_width
  - and application_name.global_config.default_thumbnail_height

Registry configuration instances are lazy (loaded after first access).
They are refreshed after every registry data change, but only
within opened key (ie. "application_name.global_config").


Model
-----

The low-level API is a classic Django models module.

EntryManager has some extra methods:

  * find_keys(key) - returns Entries which name begins with "key"
  * delete_key(key) - delete key and all subkeys found by find_keys()
  * set(key, value, type=TEXT) - create or update key with value, set type for new key


