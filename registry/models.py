from django.db import models

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
