IGNORED_MODULES = ["utils.py", "test_testing.py"]
MOCK_OBJECTS = [
    "MockQueryset",
    "MockRequest",
    "TypeErrorQueryset",
    "DataErrorQueryset",
    "ValueErrorQueryset",
    "DummyView",
    "NonTimeThrottle",
    "Dict[<nothing>, <nothing>]",
    "TestCustomTimezoneForDateTimeField",
    "TestDefaultTZDateTimeField",
    "TestTZWithDateTimeField",
    "MockQuerySet",
    "AuthRaisesAttributeError",
    "CursorPaginationTestsMixin",
    "MockRenderer",
    "MockResponse",
    "MockView",
    "MockView2",
    "MockLazyStr",
    "MockTimezone",
    "MockAPIView",
    "MockUser",
    "MockObject",
]
EXTERNAL_MODULES = ["requests"]
IGNORED_ERRORS = {
    "__common__": [
        "already defined",
        "Need type annotation for",
        "Cannot assign to a method",
        "Cannot determine type of",
        '"HttpResponse" has no attribute "data"',
        'has no attribute "initkwargs"',
        'has no attribute "mapping"',
        'Response" has no attribute "view"',
        "Cannot infer type",
        ' has no attribute "_context',
        '(expression has type "None", variable has type "ForeignKeyTarget")',
    ],
    "test_openapi.py": ['Incompatible types in assignment (expression has type "CharField", base class "Field" defined the type as "bool")'],
    "test_authtoken.py": ['Item "None" of "Optional[Token]" has no attribute "key"', 'Argument 1 to "get_fields" of "BaseModelAdmin" has incompatible type "object"; expected "HttpRequest"', 'Argument 1 to "TokenAdmin" has incompatible type "Token"; expected "Type[Model]"'],
    "test_bound_fields.py": ['Value of type "BoundField" is not indexable'],
    "test_decorators.py": ['Argument 1 to "api_view" has incompatible type "Callable[[Any], Any]"; expected "Optional[Sequence[str]]"'],
    "test_encoders.py": ['Argument "serializer" to "ReturnList" has incompatible type "None'],
    "test_fields.py": [
        '"ChoiceModel"',
        'Argument "validators" to "CharField" has incompatible type',
        "Dict entry",
        '"FieldValues"',
        'base class "Field" defined the type as "bool"',
        'Invalid index type "int" for "Union[str, List[Any], Dict[str, Any]]"; expected type "str"',
        'Item "str" of "Union[str, Any]" has no attribute "code"',
        'Argument "default" to "CharField" has incompatible type',
        '"MultipleChoiceField" has no attribute "partial"',
        '"Field[Any, Any, Any, Any]" has no attribute "method_name"',
        'Argument 1 to "ModelField" has incompatible type "None"',
        'Argument "params" to "ValidationError" has incompatible type "Tuple[str]"'
    ],
    "test_filters.py": [
        'Module has no attribute "coreapi"',
        'has incompatible type "Options[Any]"',
        'has incompatible type "None"',
    ],
    "test_generics.py": [
        'has incompatible type "str"',
        '"Response" has no attribute "serializer"',
        ' Incompatible types in assignment (expression has type "Type[SlugSerializer]", base class "InstanceView" defined the type as "Type[BasicSerializer]")',
    ],
    "test_htmlrenderer.py": [
        'to "get_template_names" of "TemplateHTMLRenderer" has incompatible type',
        "Incompatible types in assignment",
    ],
    "test_metadata.py": ['"BaseMetadata" has incompatible type "None"'],
    "test_middleware.py": ['"is_form_media_type" has incompatible type "Optional[str]"; expected "str"'],
    "test_model_serializer.py": [
        '"Field[Any, Any, Any, Any]" has no attribute',
        'Module has no attribute "JSONField"',
        'expected "OrderedDict[Any, Any]"',
        'base class "Meta" defined the type as',
        '"Field" has no attribute',
    ],
    "test_negotiation.py": ['has incompatible type "None"'],
    "test_pagination.py": [
        'Incompatible types in assignment (expression has type "None", base class "LimitOffsetPagination" defined the type as "int")',
        "(not iterable)",
        '(expression has type "None", variable has type "List[Any]")',
        'has incompatible type "range"',
        'expected "Iterable[Any]"',
    ],
    "test_parsers.py": ['"object" has no attribute', 'Argument 1 to "isnan" has incompatible type'],
    "test_permissions.py": [
        '"ResolverMatch" has incompatible type "str"; expected "Callable[..., Any]"',
        "_SupportsHasPermission",
    ],
    "test_relations.py": [
        'Invalid index type "int" for "Union[str, List[Any], Dict[str, Any]]"; expected type "str"',
        'Argument "queryset" to "HyperlinkedRelatedField" has incompatible type',
        'Incompatible return value type (got "None", expected "HttpResponseBase',
        'Argument 2 to "re_path" has incompatible type "Callable[[], None]"; expected "Callable[..., HttpResponseBase]"',
    ],
    "test_relations_pk.py": [
        '"Field" has no attribute "get_queryset"',
        '"OneToOneTarget" has no attribute "id"',
        '"Field[Any, Any, Any, Any]" has no attribute "get_queryset',
        'Argument "queryset" to "HyperlinkedRelatedField" has incompatible type',
    ],
    "test_renderers.py": [
        '(expression has type "Callable[[], str]", variable has type "Callable[[Optional[str]], str]")'
    ],
    "test_requests_client.py": ["Module 'rest_framework.compat' has no attribute 'requests'"],
    "test_request.py": [
        '"Request" has no attribute "inner_property"',
        'Argument 2 to "login" has incompatible type "Optional[AbstractBaseUser]"; expected "AbstractBaseUser"',
        'expression has type "Optional[AbstractBaseUser]',
    ],
    "test_response.py": [
        'Argument 2 to "get" of "Client" has incompatible type "**Dict[str, str]"',
    ],
    "test_routers.py": [
        'expression has type "List[RouterTestModel]"'
    ],
    "test_serializer.py": [
        '"update" of "SerializerProtocol" has incompatible type "None"',
        '"create" of "SerializerProtocol" has incompatible type "None"',
        "base class",
        '(expression has type "IntegerField", base class "Base" defined the type as "CharField")',
        '"CharField" has incompatible type "Collection[Any]"',
        "Name 'foo' is not defined",
    ],
    "test_serializer_lists.py": ['The type "Type[ListSerializer]" is not generic and not indexable'],
    "test_serializer_nested.py": [
        '(expression has type "NestedSerializer", base class "Field" defined the type as "bool")',
        "self.Serializer",
        '(expression has type "NonRelationalPersonDataSerializer", base class "Serializer" defined the type as "ReturnDict")',
    ],
    "test_settings.py": ['Argument 1 to "APISettings" has incompatible type "Dict[str, int]"; expected "Optional[DefaultsSettings]'],
    "test_templatetags.py": ['Module has no attribute "smart_urlquote"'],
    "test_throttling.py": [
        'has incompatible type "Dict[<nothing>, <nothing>]"',
        '"SimpleRateThrottle" has no attribute "num_requests',
        '"SimpleRateThrottle" has no attribute "duration"',
        "Cannot assign to a method",
        'Type[NonTimeThrottle]" has no attribute "called"',
    ],
    "test_utils.py": ["Unsupported left operand type for %"],
    "test_validation.py": ['Value of type "object" is not indexable'],
    "test_validators.py": [
        'has incompatible type "object"; expected "QuerySet[Any]"',
        'to "filter_queryset" of "BaseUniqueForValidator" has incompatible type "None"',
    ],
    "test_versioning.py": [
        '(expression has type "Type[FakeResolverMatch]", variable has type "ResolverMatch")',
        "rest_framework.decorators",
    ],
    "test_viewsets.py": [
        '(expression has type "None", variable has type "HttpRequest")',
        '(expression has type "None", variable has type "Request")',
    ],
}