from rest_framework.fields import (Field as Field,
                                   CharField as CharField,
                                   RegexField as RegexField,
                                   EmailField as EmailField,
                                   IntegerField as IntegerField,
                                   BooleanField as BooleanField,
                                   NullBooleanField as NullBooleanField,
                                   ListField as ListField,
                                   DictField as DictField,
                                   ChoiceField as ChoiceField,
                                   JSONField as JSONField,
                                   DateTimeField as DateTimeField)


class Serializer(Field):
    pass