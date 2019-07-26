MOCK_OBJECTS = ['MockRequest', 'MockView', 'MockTimezone', 'MockLazyStr', 'MockQueryset']

IGNORED_ERRORS = [
    *MOCK_OBJECTS,
    'Need type annotation for',
    'URLPattern',  # moved in django 2.0+
    'URLResolver',  # moved in django 2.0+
    'Invalid signature "def (self: Any) -> Any"',
    'already defined on line',
    'already defined (possibly by an import)',
    # 'variable has type Module',
    # 'Invalid base class',
    # 'Invalid type "self"',
    # re.compile(r'Item "None" of "Optional\[[a-zA-Z0-9]+\]" has no attribute'),
    # 'Optional[List[_Record]]',
    # '"Callable[..., Any]" has no attribute "initkwargs"',
    # 'Cannot assign to a type',
    # 'Cannot assign to a method',
    # '"Type[NonTimeThrottle]" has no attribute "called"',
    # 'BaseTokenAuthTests',
    # re.compile(r'Dict entry [0-9] has incompatible type "[a-zA-Z]+": "None"; expected "object": "bool"'),
    # 'Incompatible types in assignment (expression has type "None", variable has type "List[Any]")',
    # 'Value of type "Optional[str]" is not indexable',
    # 'Argument 1 to "QueryDict" has incompatible type "Dict[<nothing>, <nothing>]";'
    # 'Argument "queryset" to "BaseUniqueForValidator" has incompatible type "object"; expected "QuerySet[Any]"',
    # 'has incompatible type "Dict[<nothing>, <nothing>]"; expected "Request"',
    # 'Argument 1 to "render" has incompatible type "Dict[<nothing>, <nothing>]"; expected "HttpRequest"',
    'Cannot infer type of lambda',
    '"type" has no attribute',
]
