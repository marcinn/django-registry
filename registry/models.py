from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import registry

NUMERIC = 'N'
BOOLEAN = 'B'
TEXT = 'T'

TYPE_CHOICES = (
        (TEXT,'Text'), 
        (BOOLEAN,'Boolean'), 
        (NUMERIC, 'Numeric'),
        )


class EntryManager(models.Manager):

    def find_keys(self, key):
        return self.get_query_set().filter(key__istartswith=key)

    def delete_key(self, key):
        return self.find_keys(key).delete()

    def set(self, key, value, type=TEXT):
        obj = self.get_query_set().get_or_create(key=key)
        obj.value = value
        if not obj.type:
            obj.type = type
        obj.save()


class Entry(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value_bool = models.NullBooleanField(null=True, blank=True)
    value_text = models.CharField(null=True, blank=True, max_length=255)
    value_numeric = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=1, default=TEXT, choices=TYPE_CHOICES)
    objects = EntryManager()

    def _get_value(self):
        if self.type == NUMERIC:
            return self.value_numeric
        if self.type == TEXT:
            return self.value_text
        if self.type == BOOLEAN:
            return self.value_bool

    def _set_value(self, value):
        if self.type == NUMERIC:
            self.value_numeric = value
        if self.type == TEXT:
            self.value_text = value
        if self.type == BOOLEAN:
            self.value_bool = value
    value = property(_get_value, _set_value)

    def __repr__(self):
        return '[%s] %s:%s' % (self.type, self.key, self.value)

    def __str__(self):
        return '%s:%s' % (self.key, self.value)

    def __unicode__(self):
        return '%s:%s' % (self.key, self.value)


class ModelEntryManager(models.Manager):

    def get_for_model(self, instance):
        ct = ContentType.objects.get_for_model(instance)
        return self.get_query_set().filter(content_type=ct,
                object_id=instance.pk)

    def update_for_model(self, instance, data):
        ct = ContentType.objects.get_for_model(instance)
        for key, value in data:
            entry, created = self.get_or_create(content_type=ct,
                       object_id=instance.pk, key=key)
            entry.value = value
            entry.save()


class ModelEntry(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    key = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=1, default=TEXT, choices=TYPE_CHOICES)
    value_bool = models.NullBooleanField(null=True, blank=True)
    value_text = models.CharField(null=True, blank=True, max_length=255)
    value_numeric = models.IntegerField(null=True, blank=True)

    objects = ModelEntryManager()

    def _get_value(self):
        if self.type == NUMERIC:
            return self.value_numeric
        if self.type == TEXT:
            return self.value_text
        if self.type == BOOLEAN:
            return self.value_bool

    def _set_value(self, value):
        if self.type == NUMERIC:
            self.value_numeric = value
        if self.type == TEXT:
            self.value_text = value
        if self.type == BOOLEAN:
            self.value_bool = value
    value = property(_get_value, _set_value)

    def __repr__(self):
        return '[%s] %s:%s' % (self.type, self.key, self.value)

    def __str__(self):
        return '%s:%s' % (self.key, self.value)

    def __unicode__(self):
        return '%s:%s' % (self.key, self.value)


class RegistryDescriptor(object):
    def __init__(self):
        self.config = {}

    def __get__(self, instance, owner):
        if not instance:
            raise ValueError('Use registry on model instances, not class')
        if not instance in self.config:
            self.config[instance] = registry.open(instance)
        return self.config[instance]


def register(model, attribute_name='registry'):
    setattr(model, attribute_name, RegistryDescriptor())

