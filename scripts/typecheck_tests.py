import itertools
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from collections import defaultdict
from distutils import dir_util, spawn
from typing import Dict, List, Pattern, Union

from scripts.git_helpers import git_checkout_drf
from scripts.paths import DRF_SOURCE_DIRECTORY, PROJECT_DIRECTORY, STUBS_DIRECTORY

# django-rest-framework commit hash to check against (ignored with --drf_version)
# This should be updated periodically or after every DRF release.
DRF_GIT_REF = "22d206c1e0dbc03840c4d190f7eda537c0f2010a"

IGNORED_MODULES = []
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
    "MockFile",
]
EXTERNAL_MODULES = ["requests"]
IGNORED_ERRORS = {
    "__common__": [
        "already defined on line",
        "Need type annotation for",
        "Cannot assign to a method",
        "Cannot determine type of",
        'has no attribute "initkwargs"',
        'Response" has no attribute "view"',
        "Cannot infer type",
        ' has no attribute "_context',
        '(expression has type "None", variable has type "ForeignKeyTarget")',
        '"_MonkeyPatchedWSGIResponse" has no attribute "content"',
        '"_MonkeyPatchedWSGIResponse" has no attribute "data"',
        '" defined here',
        '" has no attribute "id"',
    ],
    "authentication": [
        'Argument 1 to "post" of "APIClient" has incompatible type "None"; expected "str',
        ' base class "BaseTokenAuthTests" defined the type as "None"',
        '"None" has no attribute "objects"',
        '"BaseTokenAuthTests" has no attribute "assertNumQueries"',
        'Module "django.middleware.csrf" has no attribute "_mask_cipher_secret"',
        "All conditional function variants must have identical signatures",
        "note:     def _get_new_csrf_token() ->",
        "note: Original:",
        "note: Redefinition:",
    ],
    "schemas": [
        '(expression has type "CharField", base class "Field" defined the type as "bool")',
        'SchemaGenerator" has no attribute "_initialise_endpoints"',
        'Argument 1 to "map_field" of "AutoSchema" has incompatible type "object"',
        'Argument 1 to "get_component_name" of "AutoSchema"',
        'Argument 1 to "get_schema_operation_parameters"',
        '"Callable[..., Any]" has no attribute "cls"',
        'Value of type "Optional[Any]" is not indexable',
        'Item "None" of "Optional[Any]" has no attribute',
        'List item 0 has incompatible type "Type[',
        'Value of type "Optional[str]" is not indexable',
        'Incompatible types in assignment (expression has type "AsView[GenericView]", variable has type "AsView[Callable[[HttpRequest], Any]]")',  # noqa: E501
        'Argument "patterns" to "SchemaGenerator" has incompatible type "List[object]"',
        'Argument 1 to "field_to_schema" has incompatible type "object"; expected "Field[Any, Any, Any, Any]"',
        '"Module rest_framework.schemas.coreapi" does not explicitly export attribute "coreapi"',
    ],
    "browsable_api": [
        'expression has type "List[Dict[str, Dict[str, int]]]"',
    ],
    "models.py": [
        '"ForeignKeyTarget" has no attribute "sources"',
        '"CustomManager" not callable',
        'Incompatible types in assignment (expression has type "Type[BaseManager[Any]]", variable has type "Type[CustomManager]")',  # noqa: E501
    ],
    "test_authtoken.py": [
        'Item "None" of "Optional[Token]" has no attribute "key"',
        'Argument 1 to "get_fields" of "BaseModelAdmin" has incompatible type "object"; expected "HttpRequest"',
        'Argument 1 to "TokenAdmin" has incompatible type "Token"',
    ],
    "test_bound_fields.py": ['Value of type "BoundField" is not indexable'],
    "test_decorators.py": [
        'Argument 1 to "api_view" has incompatible type "Callable[[Any], Any]"; expected "Optional[Sequence[str]]"',
    ],
    "test_encoders.py": ['Argument "serializer" to "ReturnList" has incompatible type "None'],
    "test_fields.py": [
        '"ChoiceModel"',
        'Argument "validators" to "CharField" has incompatible type',
        "Dict entry",
        '"FieldValues"',
        'base class "Field" defined the type as "bool"',
        'Invalid index type "int" for "Union[str, _StrPromise, List[Any], Dict[str, Any]]"; expected type "str"',
        'Item "str" of "Union[str, Any]" has no attribute "code"',
        'Argument "default" to "CharField" has incompatible type',
        '"MultipleChoiceField" has no attribute "partial"',
        '"Field[Any, Any, Any, Any]" has no attribute "method_name"',
        'Argument 1 to "ModelField" has incompatible type "None"',
        'Argument "params" to "ValidationError" has incompatible type "Tuple[str]"',
        'Argument 1 to "to_internal_value" of "Field" has incompatible type "Dict[str, str]"; expected "List[Any]"',
        'Module "rest_framework.fields" does not explicitly export attribute "DjangoImageField"',
        'Argument 1 to "ListField" has incompatible type "CharField"; expected "bool"',
    ],
    "test_filters.py": [
        'Module has no attribute "coreapi"',
        'has incompatible type "Options[Any]"',
        'has incompatible type "None"',
    ],
    "test_generics.py": [
        'has incompatible type "str"',
        '"Response" has no attribute "serializer"',
        'Incompatible types in assignment (expression has type "Type[SlugSerializer]", base class "InstanceView" defined the type as "Type[BasicSerializer]")',  # noqa: E501
        'Incompatible types in assignment (expression has type "_QuerySet[SlugBasedModel, SlugBasedModel]", base class "InstanceView" defined the type as "_QuerySet[BasicModel, BasicModel]")',  # noqa: E501
    ],
    "test_htmlrenderer.py": [
        'to "get_template_names" of "TemplateHTMLRenderer" has incompatible type',
        "Incompatible types in assignment",
    ],
    "test_metadata.py": ['"BaseMetadata" has incompatible type "None"'],
    "test_middleware.py": ['"is_form_media_type" has incompatible type "Optional[str]"; expected "str"'],
    "test_model_serializer.py": [
        '"Field[Any, Any, Any, Any]" has no attribute',
        'base class "Meta" defined the type as',
        '"OneFieldModel" has no attribute "additional_attr"',
    ],
    "test_negotiation.py": ['has incompatible type "None"'],
    "test_pagination.py": [
        "(not iterable)",
        'has incompatible type "range"',
        'expected "Iterable[Any]"',
        'Value of type variable "_MT" of "paginate_queryset" of "CursorPagination" cannot be "object"',
        'Value of type "Union[object, Any]" is not indexable',
    ],
    "test_parsers.py": ['"object" has no attribute', 'Argument 1 to "isnan" has incompatible type'],
    "test_permissions.py": [
        '"ResolverMatch" has incompatible type "str"; expected "Callable[..., Any]"',
        "_SupportsHasPermission",
        "Invalid type alias: expression is not a valid type",
        '"object" not callable',
        'Cannot assign multiple types to name "composed_perm" without an explicit "Type[...]" annotation',
        '"<typing special form>" not callable',
        "<nothing> not callable",
    ],
    "test_relations.py": [
        'Invalid index type "int" for "Union[str, _StrPromise, List[Any], Dict[str, Any]]"; expected type "str"',
        'Argument "queryset" to "HyperlinkedRelatedField" has incompatible type',
        'Incompatible return value type (got "None", expected "HttpResponseBase',
        'Argument 2 to "re_path" has incompatible type "Callable[[], None]"; expected "Callable[..., HttpResponseBase]"',  # noqa: E501
    ],
    "test_relations_pk.py": [
        '"Field[Any, Any, Any, Any]" has no attribute "get_queryset',
    ],
    "test_renderers.py": [
        '(expression has type "Callable[[], str]", variable has type "Callable[[Optional[str]], str]")'
    ],
    "test_request.py": [
        '"Request" has no attribute "inner_property"',
        'expression has type "Optional[AbstractBaseUser]',
    ],
    "test_response.py": [
        'Argument 2 to "get" of "Client" has incompatible type "**Dict[str, str]"',
    ],
    "test_routers.py": [
        'expression has type "List[RouterTestModel]"',
        'Item "URLResolver" of "Union[URLPattern, URLResolver]" has no attribute "name"',
        '"None" not callable',
        '"BasenameTestCase" has no attribute "router"',
        'Unexpected keyword argument "use_regex_path" for "SimpleRouter"',
    ],
    "test_serializer.py": [
        "base class",
        '"CharField" has incompatible type "Collection[Any]"',
        'Name "foo" is not defined',
        'Unsupported left operand type for | ("ReturnDict")',
        'Unsupported left operand type for | ("Dict[str, str]")',
    ],
    "test_serializer_lists.py": [
        'Name "foo" is not defined',
        'Unexpected keyword argument "max_length" for "IntegerSerializer"',
        'Unexpected keyword argument "min_length" for "IntegerSerializer"',
    ],
    "test_serializer_nested.py": [
        '(expression has type "NestedSerializer", base class "Field" defined the type as "bool")',
        "self.Serializer",
        '(expression has type "NonRelationalPersonDataSerializer", base class "Serializer" defined the type as "ReturnDict")',  # noqa: E501
    ],
    "test_settings.py": [
        'Argument 1 to "APISettings" has incompatible type "Dict[str, int]"; expected "Optional[DefaultsSettings]'
    ],
    "test_templatetags.py": ['Module has no attribute "smart_urlquote"'],
    "test_testing.py": [
        '"Client" has no attribute "force_authenticate"',
        '"Client" has no attribute "credentials"',
        'has no attribute "addClassCleanup"',
    ],
    "test_throttling.py": [
        'has incompatible type "Dict[<nothing>, <nothing>]"',
        '"SimpleRateThrottle" has no attribute "num_requests',
        '"SimpleRateThrottle" has no attribute "duration"',
        'Type[NonTimeThrottle]" has no attribute "called"',
    ],
    "test_utils.py": [
        "Unsupported left operand type for %",
        'incompatible type "List[Union[URLPattern, URLResolver]]"; expected "Iterable[URLPattern]"',
    ],
    "test_validation.py": [
        'Argument 1 to "to_internal_value" of "Field" has incompatible type "object"',
    ],
    "test_validation_error.py": [
        'Argument "detail" to "ValidationError" has incompatible type "Tuple[str, str]"; expected "Optional[Union[Union[str, _StrPromise], List[Any], Dict[str, Any]]]"',  # noqa: E501
    ],
    "test_validators.py": [
        'Argument "queryset" to "BaseUniqueForValidator" has incompatible type "object";'
        ' expected "_QuerySet[Any, Any]"',
        'to "filter_queryset" of "BaseUniqueForValidator" has incompatible type "None"',
        'Item "ForeignObjectRel" of "Union[Field[Any, Any], ForeignObjectRel, GenericForeignKey]" has no attribute "validators"',  # noqa: E501
        'Item "GenericForeignKey" of "Union[Field[Any, Any], ForeignObjectRel, GenericForeignKey]" has no attribute "validators"',  # noqa: E501
    ],
    "test_versioning.py": [
        "rest_framework.decorators",
        'Argument 1 to "include" has incompatible type "Tuple[List[object], str]"',
        'Incompatible types in assignment (expression has type "Type[FakeResolverMatch]", variable has type "Optional[ResolverMatch]"',  # noqa: E501
        '"None" not callable',
    ],
    "test_viewsets.py": [
        '(expression has type "None", variable has type "Request")',
    ],
    "utils.py": ['Invalid signature "Callable[[BadType], Any]"'],
}


def get_unused_ignores(ignored_message_freq: Dict[str, Dict[Union[str, Pattern], int]]) -> List[str]:
    unused_ignores = []
    for root_key, patterns in IGNORED_ERRORS.items():
        for pattern in patterns:
            if ignored_message_freq[root_key][pattern] == 0 and pattern not in itertools.chain(
                EXTERNAL_MODULES, MOCK_OBJECTS
            ):
                unused_ignores.append(f"{root_key}: {pattern}")
    return unused_ignores


def is_pattern_fits(pattern: Union[Pattern, str], line: str):
    if isinstance(pattern, Pattern):
        if pattern.search(line):
            return True
    else:
        if pattern in line:
            return True
    return False


def is_ignored(line: str, filename: str, ignored_message_dict: Dict[str, Dict[str, int]]) -> bool:
    if "runtests" in line or filename in IGNORED_MODULES:
        return True
    for pattern in IGNORED_ERRORS["__common__"]:
        if pattern in line:
            return True
    for pattern in IGNORED_ERRORS.get(filename, []):
        if is_pattern_fits(pattern, line):
            ignored_message_dict[test_filename][pattern] += 1
            return True
    for mock_object in MOCK_OBJECTS:
        if mock_object in line:
            return True
    return False

    def update(self, op_code, cur_count, max_count=None, message=""):
        print(self._cur_line)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--drf_version", required=False)
    args = parser.parse_args()
    git_checkout_drf(args.drf_version or DRF_GIT_REF)
    if sys.version_info[1] > 7:
        shutil.copytree(STUBS_DIRECTORY, DRF_SOURCE_DIRECTORY / "rest_framework", dirs_exist_ok=True)
    else:
        dir_util.copy_tree(str(STUBS_DIRECTORY), str(DRF_SOURCE_DIRECTORY / "rest_framework"))
    mypy_config_file = (PROJECT_DIRECTORY / "mypy.ini").absolute()
    mypy_cache_dir = PROJECT_DIRECTORY / ".mypy_cache"
    tests_root = DRF_SOURCE_DIRECTORY / "tests"
    global_rc = 0

    try:
        mypy_options = [
            "--cache-dir",
            str(mypy_cache_dir),
            "--config-file",
            str(mypy_config_file),
            "--show-traceback",
            "--no-error-summary",
            "--hide-error-context",
        ]
        mypy_options += [str(tests_root)]
        mypy_executable = spawn.find_executable("mypy")
        mypy_argv = [mypy_executable, *mypy_options]
        completed = subprocess.run(
            mypy_argv,
            env={"PYTHONPATH": str(PROJECT_DIRECTORY)},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = completed.stdout.decode()
        ignored_message_freqs = defaultdict(lambda: defaultdict(int))
        sorted_lines = sorted(output.splitlines())
        for line in sorted_lines:
            try:
                path_to_error = line.split(":")[0]
                test_filename = path_to_error.split("/")[2]
            except IndexError:
                test_filename = "unknown"

            if not is_ignored(line, test_filename, ignored_message_dict=ignored_message_freqs):
                global_rc = 1
                print(line)

        unused_ignores = get_unused_ignores(ignored_message_freqs)
        if unused_ignores:
            print("UNUSED IGNORES ------------------------------------------------")
            print("\n".join(unused_ignores))

        sys.exit(global_rc)

    except BaseException as exc:
        shutil.rmtree(mypy_cache_dir, ignore_errors=True)
        raise exc
