from pathlib import Path

import pandas as pd

from domain.models import (
    TaxonomyCategory,
    TaxonomyDetail,
    Technology,
)

from repositories.base_repository import (
    TaxonomyRepository,
)


class CsvTaxonomyRepository(TaxonomyRepository):
    """
    CSV implementation of the taxonomy repository.

    This is used only for the MVP / prototype.

    The rest of the application should not depend on CSV or pandas.
    """

    def __init__(
        self,
        file_path: Path,
    ):
        self.file_path = file_path

        self._data = self._load_data()


    # ========================================================
    # INTERNAL DATA LOADING
    # ========================================================

    def _load_data(self) -> pd.DataFrame:

        if not self.file_path.exists():

            raise FileNotFoundError(
                f"Could not find taxonomy data file: "
                f"{self.file_path}"
            )

        data = pd.read_csv(
            self.file_path
        )

        data = data.dropna(
            how="all"
        )

        for column in data.columns:

            if data[column].dtype == "object":

                data[column] = (
                    data[column]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        return data


    @staticmethod
    def _unique_values(
        series: pd.Series,
    ) -> list[str]:

        return list(
            dict.fromkeys(
                value
                for value in series.tolist()
                if value
                and value != "nan"
            )
        )


    # ========================================================
    # LEVEL 1
    # ========================================================

    def get_level_1_categories(
        self,
    ) -> list[TaxonomyCategory]:

        values = self._unique_values(
            self._data["Level 1"]
        )

        return [
            TaxonomyCategory(
                id=value,
                name=value,
                level=1,
            )
            for value in values
        ]


    # ========================================================
    # LEVEL 2
    # ========================================================

    def get_level_2_categories(
        self,
        level_1_id: str,
    ) -> list[TaxonomyCategory]:

        filtered = self._data[
            self._data["Level 1"]
            == level_1_id
        ]

        values = self._unique_values(
            filtered["Level 2"]
        )

        return [
            TaxonomyCategory(
                id=value,
                name=value,
                level=2,
            )
            for value in values
        ]


    # ========================================================
    # LEVEL 3
    # ========================================================

    def get_level_3_categories(
        self,
        level_1_id: str,
        level_2_id: str,
    ) -> list[TaxonomyCategory]:

        filtered = self._data[
            (
                self._data["Level 1"]
                == level_1_id
            )
            & (
                self._data["Level 2"]
                == level_2_id
            )
        ]

        values = self._unique_values(
            filtered["Level 3"]
        )

        categories = []

        for value in values:

            rows = filtered[
                filtered["Level 3"]
                == value
            ]

            descriptions = (
                self._unique_values(
                    rows[
                        "Level 3 Description"
                    ]
                )
            )

            description = (
                descriptions[0]
                if descriptions
                else ""
            )

            categories.append(
                TaxonomyCategory(
                    id=value,
                    name=value,
                    level=3,
                    description=description,
                )
            )

        return categories


    # ========================================================
    # LEVEL 3 DETAIL
    # ========================================================

    def get_level_3_detail(
        self,
        level_1_id: str,
        level_2_id: str,
        level_3_id: str,
    ) -> TaxonomyDetail | None:

        rows = self._data[
            (
                self._data["Level 1"]
                == level_1_id
            )
            & (
                self._data["Level 2"]
                == level_2_id
            )
            & (
                self._data["Level 3"]
                == level_3_id
            )
        ]

        if rows.empty:
            return None

        descriptions = self._unique_values(
            rows[
                "Level 3 Description"
            ]
        )

        level_3_description = (
            descriptions[0]
            if descriptions
            else ""
        )

        technologies = []

        technology_rows = (
            rows[
                [
                    "Strategic Technology",
                    "Strategic Technology Description",
                ]
            ]
            .drop_duplicates()
        )

        for _, row in technology_rows.iterrows():

            technology_name = (
                row[
                    "Strategic Technology"
                ]
            )

            if not technology_name:
                continue

            technology_description = (
                row[
                    "Strategic Technology Description"
                ]
            )

            technologies.append(
                Technology(
                    id=technology_name,
                    name=technology_name,
                    description=technology_description,
                )
            )

        return TaxonomyDetail(

            level_1=TaxonomyCategory(
                id=level_1_id,
                name=level_1_id,
                level=1,
            ),

            level_2=TaxonomyCategory(
                id=level_2_id,
                name=level_2_id,
                level=2,
            ),

            level_3=TaxonomyCategory(
                id=level_3_id,
                name=level_3_id,
                level=3,
                description=level_3_description,
            ),

            technologies=technologies,
        )