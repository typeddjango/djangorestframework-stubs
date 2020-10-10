FIELD_FULLNAME = "rest_framework.fields.Field"
BASE_SERIALIZER_FULLNAME = "rest_framework.serializers.BaseSerializer"
SERIALIZER_FULLNAME = "rest_framework.serializers.Serializer"
LIST_SERIALIZER_FULLNAME = "rest_framework.serializers.ListSerializer"
MODEL_SERIALIZER_FULLNAME = "rest_framework.serializers.ModelSerializer"
SERIALIZER_FIELD_MAPPING = {
    "django.db.models.fields.AutoField": "rest_framework.serializers.IntegerField",
    "django.db.models.fields.BigIntegerField": "rest_framework.serializers.IntegerField",
    "django.db.models.fields.BooleanField": "rest_framework.serializers.BooleanField",
    "django.db.models.fields.CharField": "rest_framework.serializers.CharField",
    "django.db.models.fields.CommaSeparatedIntegerField": "rest_framework.serializers.CharField",
    "django.db.models.fields.DateField": "rest_framework.serializers.DateField",
    "django.db.models.fields.DateTimeField": "rest_framework.serializers.DateTimeField",
    "django.db.models.fields.DecimalField": "rest_framework.serializers.DecimalField",
    "django.db.models.fields.DurationField": "rest_framework.serializers.DurationField",
    "django.db.models.fields.EmailField": "rest_framework.serializers.EmailField",
    "django.db.models.fields.Field": "rest_framework.serializers.ModelField",
    "django.db.models.fields.FileField": "rest_framework.serializers.FileField",
    "django.db.models.fields.FilePathField": "rest_framework.serializers.FilePathField",
    "django.db.models.fields.FloatField": "rest_framework.serializers.FloatField",
    "django.db.models.fields.GenericIPAddressField": "rest_framework.serializers.IPAddressField",
    "django.db.models.fields.ImageField": "rest_framework.serializers.ImageField",
    "django.db.models.fields.IntegerField": "rest_framework.serializers.IntegerField",
    "django.db.models.fields.NullBooleanField": "rest_framework.serializers.BooleanField",
    "django.db.models.fields.PositiveIntegerField": "rest_framework.serializers.IntegerField",
    "django.db.models.fields.PositiveSmallIntegerField": "rest_framework.serializers.IntegerField",
    "django.db.models.fields.SlugField": "rest_framework.serializers.SlugField",
    "django.db.models.fields.SmallIntegerField": "rest_framework.serializers.IntegerField",
    "django.db.models.fields.TextField": "rest_framework.serializers.CharField",
    "django.db.models.fields.TimeField": "rest_framework.serializers.TimeField",
    "django.db.models.fields.URLField": "rest_framework.serializers.URLField",
    "django.db.models.fields.UUIDField": "rest_framework.serializers.UUIDField",
    "django.db.models.fields.JSONField": "rest_framework.serializers.JSONField",
}

ID_TYPE = "builtins.object"
