class LanguageRules:
    name: str
    function_name_level: int
    parameter_level: int
    parameter_node: dict


class PythonRules(LanguageRules):
    name = 'Python'
    function_name_level = 1
    parameter_level = 2
    parameter_node = {'identifier', 'typed_parameter'}


class CppRules(LanguageRules):
    name = 'C++'
    function_name_level = 2
    parameter_level = 3
    parameter_node = {'parameter_declaration'}
