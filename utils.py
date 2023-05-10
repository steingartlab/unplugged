from dataclasses import fields
from typing import Type


def dataclass_from_dict(dataclass_: Type, dict_: dict) -> Type:
    """Populated dataclass from a dictionary.
    
    Used to parse incoming http dicts to a dataclass.

    Args:
        dataclass_ (Type): Dataclass object, i.e. not an instance of it.
        dict_ (dict): Dict that matches keys of dataclass_ **exactly**.

    Returns:
        Type: Dataclass instance, populated by values from dict.
    """

    field_set = {f.name for f in fields(dataclass_) if f.init}
    filtered_arg_dict = {k : v for k, v in dict_.items() if k in field_set}
    
    return dataclass_(**filtered_arg_dict)
