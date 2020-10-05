IGNORED_MODULES = ["utils.py", "test_testing.py"]
MOCK_OBJECTS = [
    "MockQueryset",
    "TypeErrorQueryset",
    "DataErrorQueryset",
    "ValueErrorQueryset",
    "DummyView",
    "NonTimeThrottle",
    "Dict[<nothing>, <nothing>]",
    "CursorPaginationTestsMixin",
    "TestCustomTimezoneForDateTimeField",
    "TestDefaultTZDateTimeField",
    "TestTZWithDateTimeField",
    "MockQuerySet",
    "AuthRaisesAttributeError",
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
        'Cannot infer type',
        '"Model" has no attribute "name"'
    ],
    "test_request.py": ['"Request" has no attribute "inner_property"', 'Argument 2 to "login" has incompatible type "Optional[AbstractBaseUser]"; expected "AbstractBaseUser"'],
    "test_response.py": [
        'Argument 2 to "get" of "Client" has incompatible type "**Dict[str, str]"',
    ],
    "test_routers.py": ['(expression has type "List[RouterTestModel]", base class "GenericAPIView" defined the type as "Union[QuerySet[Any], Manager[Any], None]")'],
    "test_serializer.py": [
        '"update" of "BaseSerializer"',
        '"create" of "BaseSerializer"',
        "base class",
        '(expression has type "IntegerField", base class "Base" defined the type as "CharField")',
        '"CharField" has incompatible type "Collection[Any]"',
    ],
    "test_serializer_nested.py": [
        '(expression has type "NestedSerializer", base class "Field" defined the type as "bool")',
        "self.Serializer",
    ],
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
        '"HyperlinkedRelatedField" has no attribute "_context"',
        "rest_framework.decorators",
    ],
    "test_viewsets.py": [
        '(expression has type "None", variable has type "HttpRequest")',
        '(expression has type "None", variable has type "Request")',
    ],
}
