from app.models import ENTITY_MODEL_TYPES, EntityModel
from app.models.base import build_create_schema, build_update_schema

ApiSchema = EntityModel

__all__ = ["ApiSchema"]

for _entity_model in ENTITY_MODEL_TYPES:
    _name = _entity_model.__name__
    globals()[f"{_name}Create"] = build_create_schema(_entity_model, module=__name__)
    globals()[f"{_name}Update"] = build_update_schema(_entity_model, module=__name__)
    globals()[f"{_name}Read"] = _entity_model
    __all__.extend(
        [
            f"{_name}Create",
            f"{_name}Update",
            f"{_name}Read",
        ]
    )

del _entity_model, _name
