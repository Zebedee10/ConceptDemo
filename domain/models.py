from dataclasses import dataclass, field


# ============================================================
# TAXONOMY CATEGORY
# ============================================================

@dataclass(frozen=True)
class TaxonomyCategory:
    """
    Represents a category within the architecture taxonomy.

    For the CSV prototype, the ID and display name may be the same.

    In future, the ID could instead be a persistent LeanIX Fact Sheet ID,
    while the name remains the user-friendly display value.
    """

    id: str
    name: str
    level: int
    description: str = ""


# ============================================================
# TECHNOLOGY
# ============================================================

@dataclass(frozen=True)
class Technology:
    """
    Represents a technology connected to a taxonomy category.
    """

    id: str
    name: str
    description: str = ""


# ============================================================
# TAXONOMY DETAIL
# ============================================================

@dataclass
class TaxonomyDetail:
    """
    Represents the information shown when a Level 3 category
    has been selected.
    """

    level_1: TaxonomyCategory
    level_2: TaxonomyCategory
    level_3: TaxonomyCategory

    technologies: list[Technology] = field(
        default_factory=list
    )