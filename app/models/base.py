from copy import deepcopy
import re
from typing import Any, ClassVar, get_args

from pydantic import BaseModel, ConfigDict, create_model, field_validator


class EntityModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

    table: ClassVar[str] = ""
    create_required: ClassVar[tuple[str, ...]] = ()
    create_defaults: ClassVar[dict[str, Any]] = {}
    order_by: ClassVar[str] = "id ASC"

    @classmethod
    def read_fields(cls) -> tuple[str, ...]:
        return tuple(
            name
            for name, field_info in cls.model_fields.items()
            if not field_info.exclude
        )

    @classmethod
    def payload_values(cls, payload: BaseModel) -> dict[str, Any]:
        values = payload.model_dump(exclude_unset=True)
        for field_name in payload.model_fields_set:
            field_info = payload.__class__.model_fields.get(field_name)
            if field_info is not None and field_info.exclude:
                values[field_name] = getattr(payload, field_name)
        values.pop("id", None)
        return values

    @field_validator("correo", check_fields=False)
    @classmethod
    def validate_correo(cls, value: str | None) -> str | None:
        if value is not None and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Ingresa un correo electrónico válido.")
        return value


def _without_none(annotation: Any) -> Any:
    arguments = get_args(annotation)
    non_none_arguments = tuple(argument for argument in arguments if argument is not type(None))
    if len(non_none_arguments) == 1:
        return non_none_arguments[0]
    return annotation


def _payload_schema(
    entity: type[EntityModel],
    *,
    name: str,
    module: str,
    create: bool,
) -> type[EntityModel]:
    definitions: dict[str, tuple[Any, Any]] = {}
    required = set(entity.create_required)
    defaults = entity.create_defaults if create else {}

    for field_name, field_info in entity.model_fields.items():
        if field_name == "id":
            continue

        copied_info = deepcopy(field_info)
        annotation = field_info.annotation

        if create and field_name in required:
            annotation = _without_none(annotation)
            copied_info.default = ...
        elif create and field_name in defaults:
            default_value = defaults[field_name]
            if default_value is not None:
                annotation = _without_none(annotation)
            copied_info.default = default_value
        elif not create:
            copied_info.default = None

        definitions[field_name] = (annotation, copied_info)

    return create_model(
        name,
        __base__=EntityModel,
        __module__=module,
        **definitions,
    )


def build_create_schema(
    entity: type[EntityModel],
    *,
    module: str = "app.api.schemas",
) -> type[EntityModel]:
    return _payload_schema(
        entity,
        name=f"{entity.__name__}Create",
        module=module,
        create=True,
    )


def build_update_schema(
    entity: type[EntityModel],
    *,
    module: str = "app.api.schemas",
) -> type[EntityModel]:
    return _payload_schema(
        entity,
        name=f"{entity.__name__}Update",
        module=module,
        create=False,
    )
