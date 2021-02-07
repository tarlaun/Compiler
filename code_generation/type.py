from typing import TYPE_CHECKING


class Type:
    double = "double"
    int = "int"
    bool = "bool"
    string = "string"
    array = "array"
    null = "null"


PRIMITIVE_TYPES = {"int", "double", "bool", "string"}


def is_class_type(type):
    non_class_types = [Type.double, Type.int, Type.bool, Type.string, Type.array]
    return type not in non_class_types


class ArrayType(Type):
    element_type: Type

    def __init__(self, element_type: Type):
        self.name = f"{element_type.name}[]"
        self.element_type = element_type

    def is_array(self) -> bool:
        return True
