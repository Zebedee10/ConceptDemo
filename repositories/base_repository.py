from abc import ABC, abstractmethod

from domain.models import (
    TaxonomyCategory,
    TaxonomyDetail,
)


class TaxonomyRepository(ABC):
    """
    Defines the data operations required by the taxonomy capability.

    The UI and service layers should not care whether these records
    come from CSV, JSON, LeanIX, or another source.

    Any future repository must implement this interface.
    """

    @abstractmethod
    def get_level_1_categories(
        self,
    ) -> list[TaxonomyCategory]:
        pass

    @abstractmethod
    def get_level_2_categories(
        self,
        level_1_id: str,
    ) -> list[TaxonomyCategory]:
        pass

    @abstractmethod
    def get_level_3_categories(
        self,
        level_1_id: str,
        level_2_id: str,
    ) -> list[TaxonomyCategory]:
        pass

    @abstractmethod
    def get_level_3_detail(
        self,
        level_1_id: str,
        level_2_id: str,
        level_3_id: str,
    ) -> TaxonomyDetail | None:
        pass