IGNORED_MODULES = {}

MOCK_OBJECTS = []
EXTERNAL_MODULES = []
IGNORED_ERRORS = {
    "test_viewsets.py": [
        '"Response" has no attribute "view"',
        'Incompatible types in assignment (expression has type "None", variable has type "HttpRequest")',
        '"HttpResponse" has no attribute "view"',
    ],
}
