from dataclasses import dataclass, field
from typing import Optional

@dataclass
class FieldConfig:
    order: int
    label: str                      # heading text shown above the box
    placeholder: str = ""           # pre-entered/greyed-out hint text
    field_type: str = "text"        # "text", "date", etc — lets you branch on behaviour
    default_value: str = ""         # optional pre-filled value (not just placeholder)

FIELD_CONFIG: dict[str, FieldConfig] = {
    "NAME": FieldConfig(
        order=0, label="Full Name", placeholder="Enter your full name"
    ),
    "DOB": FieldConfig(
        order=1, label="Date of Birth", field_type="date"
    ),
    "ADDRESS1": FieldConfig(
        order=2, label="Address Line 1", placeholder="House number and street"
    ),
    "ADDRESS2": FieldConfig(
        order=3, label="Address Line 2", placeholder="Town / city"
    ),
    "ADDRESS3": FieldConfig(
        order=4, label="Address Line 3", placeholder="County"
    ),
    "POSTCODE": FieldConfig(
        order=5, label="Postcode", placeholder="e.g. SO14 3AB"
    ),
    "PHONE_NUMBER": FieldConfig(
        order=6, label="Phone Number", placeholder="e.g. 07123 456789"
    ),
    "EMAIL_ADDRESS": FieldConfig(
        order=7, label="Email Address", placeholder="name@example.com"
    ),
    "SURGERY": FieldConfig(
        order=8, label="GP Surgery", placeholder="Enter surgery name"
    ),
    "PREFERRED_GP": FieldConfig(
        order=9, label="Preferred GP", placeholder="Enter GP name"
    ),
    "NOK_NAME": FieldConfig(
        order=10, label="Next of Kin Name", placeholder="Enter full name"
    ),
    "NOK_RELATIONSHIP": FieldConfig(
        order=11, label="Relationship to Patient", placeholder="e.g. Spouse, Parent"
    ),
    "NOK_PHONE": FieldConfig(
        order=12, label="Next of Kin Phone", placeholder="e.g. 07123 456789"
    ),
    "AGE": FieldConfig(
            order=13, label="Age", placeholder="e.g. 30"
        ),
    "GENDER": FieldConfig(
        order=14, label="Gender", placeholder="e.g. Male, Female, Other"
    ),
}

DEFAULT_ORDER = len(FIELD_CONFIG)

def _get_config(field_name: str) -> FieldConfig:
    """Fallback for fields not yet in the dictionary, so nothing crashes."""
    return FIELD_CONFIG.get(
        field_name,
        FieldConfig(order=DEFAULT_ORDER, label=field_name, placeholder=f"Enter {field_name}")
    )

def _sorted_fields( field_names: list[str]) -> list[str]:
    return sorted(field_names, key=lambda f: _get_config(f).order)