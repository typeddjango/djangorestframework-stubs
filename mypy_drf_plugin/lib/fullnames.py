FIELD_FULLNAME = 'rest_framework.fields.Field'
BASE_SERIALIZER_FULLNAME = 'rest_framework.serializers.BaseSerializer'
SERIALIZER_FULLNAME = 'rest_framework.serializers.Serializer'
LIST_SERIALIZER_FULLNAME = 'rest_framework.serializers.ListSerializer'
MODEL_SERIALIZER_FULLNAME = 'rest_framework.serializers.ModelSerializer'

# TODO: finish mapping
SERIALIZER_FIELD_MAPPING = {
    'django.db.models.fields.AutoField': 'rest_framework.serializers.IntegerField',
    'django.db.models.fields.BigIntegerField': 'rest_framework.serializers.IntegerField',
    'django.db.models.fields.BooleanField': 'rest_framework.serializers.BooleanField',
    'django.db.models.fields.CharField': 'rest_framework.serializers.CharField',
    'django.db.models.fields.CommaSeparatedIntegerField': 'rest_framework.serializers.CharField',
    'django.db.models.fields.DateField': 'rest_framework.serializers.DateField',
    'django.db.models.fields.DateTimeField': 'rest_framework.serializers.DateTimeField',
    'django.db.models.fields.DecimalField': 'rest_framework.serializers.DecimalField',
}
ID_TYPE = 'builtins.object'
