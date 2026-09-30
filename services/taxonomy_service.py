from domain.models import (
    TaxonomyCategory,
    TaxonomyDetail,
)

from repositories.base_repository import (
    TaxonomyRepository,
)


class TaxonomyService:
    """
    Application service for the Technology Taxonomy capability.

    The service sits between the presentation layer and the
    repository/data layer.

    Business rules relating to taxonomy navigation should
    progressively live here rather than in the Streamlit page.
    """

    def __init__(
        self,
        repository: TaxonomyRepository,
    ):
        self.repository = repository


    # ========================================================
    # CATEGORY RETRIEVAL
    # ========================================================

    def get_level_1_categories(
        self,
    ) -> list[TaxonomyCategory]:

        return (
            self.repository
            .get_level_1_categories()
        )


    def get_level_2_categories(
        self,
        level_1_id: str,
    ) -> list[TaxonomyCategory]:

        return (
            self.repository
            .get_level_2_categories(
                level_1_id
            )
        )


    def get_level_3_categories(
        self,
        level_1_id: str,
        level_2_id: str,
    ) -> list[TaxonomyCategory]:

        return (
            self.repository
            .get_level_3_categories(
                level_1_id,
                level_2_id,
            )
        )


    # ========================================================
    # DETAIL RETRIEVAL
    # ========================================================

    def get_level_3_detail(
        self,
        level_1_id: str,
        level_2_id: str,
        level_3_id: str,
    ) -> TaxonomyDetail | None:

        return (
            self.repository
            .get_level_3_detail(
                level_1_id,
                level_2_id,
                level_3_id,
            )
        )


    # ========================================================
    # NAVIGATION HELPERS
    # ========================================================

    def get_initial_path(
        self,
    ) -> tuple[
        str | None,
        str | None,
        str | None,
    ]:
        """
        Returns the first valid navigation path through
        the taxonomy.

        This is currently used when the application loads.
        """

        level_1 = (
            self.get_level_1_categories()
        )

        if not level_1:
            return None, None, None

        selected_l1 = level_1[0].id

        level_2 = (
            self.get_level_2_categories(
                selected_l1
            )
        )

        if not level_2:
            return (
                selected_l1,
                None,
                None,
            )

        selected_l2 = level_2[0].id

        level_3 = (
            self.get_level_3_categories(
                selected_l1,
                selected_l2,
            )
        )

        selected_l3 = (
            level_3[0].id
            if level_3
            else None
        )

        return (
            selected_l1,
            selected_l2,
            selected_l3,
        )


    def get_path_for_level_1(
        self,
        level_1_id: str,
    ) -> tuple[
        str,
        str | None,
        str | None,
    ]:
        """
        When Level 1 changes, calculate the first valid
        Level 2 and Level 3 selections.
        """

        level_2 = (
            self.get_level_2_categories(
                level_1_id
            )
        )

        selected_l2 = (
            level_2[0].id
            if level_2
            else None
        )

        if not selected_l2:

            return (
                level_1_id,
                None,
                None,
            )

        level_3 = (
            self.get_level_3_categories(
                level_1_id,
                selected_l2,
            )
        )

        selected_l3 = (
            level_3[0].id
            if level_3
            else None
        )

        return (
            level_1_id,
            selected_l2,
            selected_l3,
        )


    def get_path_for_level_2(
        self,
        level_1_id: str,
        level_2_id: str,
    ) -> tuple[
        str,
        str,
        str | None,
    ]:
        """
        When Level 2 changes, calculate the first valid
        Level 3 selection.
        """

        level_3 = (
            self.get_level_3_categories(
                level_1_id,
                level_2_id,
            )
        )

        selected_l3 = (
            level_3[0].id
            if level_3
            else None
        )

        return (
            level_1_id,
            level_2_id,
            selected_l3,
        )