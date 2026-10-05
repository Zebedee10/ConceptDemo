from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import streamlit as st

from components.ui import render_html


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "Sample_EBCM.csv"
)

ALIAS_PATTERN = re.compile(
    r"^\s*(\d+(?:\.\d+)*)\.?\s*(.*)\s*$"
)


@dataclass(frozen=True)
class Capability:
    code: str
    name: str
    level: int
    description: str
    inferred: bool = False

    @property
    def display_name(self) -> str:
        return f"{self.code} {self.name}".strip()


def _parse_alias(alias: str) -> tuple[str, str]:
    value = str(alias or "").strip()
    match = ALIAS_PATTERN.match(value)

    if not match:
        return value, ""

    return (
        match.group(1).strip(),
        match.group(2).strip(),
    )


def _expected_name(
    row: pd.Series,
    level: int,
    fallback_name: str,
) -> str:
    column = f"Level {level}"

    if column in row.index:
        value = row.get(column)

        if pd.notna(value):
            text = str(value).strip()

            if text:
                return text

    return fallback_name.strip()


@st.cache_data
def load_capabilities() -> dict[str, Capability]:
    df = pd.read_csv(DATA_FILE)

    required_columns = {
        "LeanIX Alias",
        "Level 1",
        "Level 2",
        "Level 3",
        "Level 4",
        "Description",
    }

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"Sample_EBCM.csv is missing required columns: {missing}"
        )

    capabilities: dict[str, Capability] = {}

    for _, row in df.iterrows():
        code, alias_name = _parse_alias(
            row["LeanIX Alias"]
        )

        if not code:
            continue

        level = len(code.split("."))
        name = _expected_name(
            row=row,
            level=level,
            fallback_name=alias_name,
        )

        description = ""

        if pd.notna(row.get("Description")):
            description = str(
                row["Description"]
            ).strip()

        candidate = Capability(
            code=code,
            name=name or alias_name or code,
            level=level,
            description=description,
            inferred=False,
        )

        # The sample extract contains duplicate aliases.
        # Keep the first complete record rather than rendering duplicates.
        existing = capabilities.get(code)

        if existing is None:
            capabilities[code] = candidate

        elif (
            not existing.description
            and candidate.description
        ):
            capabilities[code] = candidate

    # Build placeholder parents when an extract contains a child
    # but omits one of the intermediate hierarchy rows.
    existing_codes = list(capabilities.keys())

    for code in existing_codes:
        parts = code.split(".")

        for depth in range(1, len(parts)):
            parent_code = ".".join(
                parts[:depth]
            )

            if parent_code in capabilities:
                continue

            capabilities[parent_code] = Capability(
                code=parent_code,
                name=f"Capability {parent_code}",
                level=depth,
                description=(
                    "This hierarchy node is implied by child "
                    "capabilities but is not present as a separate "
                    "row in the supplied extract."
                ),
                inferred=True,
            )

    return dict(
        sorted(
            capabilities.items(),
            key=lambda item: [
                int(part)
                for part in item[0].split(".")
            ],
        )
    )


def _parent_code(code: str) -> str | None:
    parts = code.split(".")

    if len(parts) <= 1:
        return None

    return ".".join(parts[:-1])


def _children(
    capabilities: dict[str, Capability],
    parent_code: str | None,
    level: int,
) -> list[Capability]:

    children: list[Capability] = []

    for capability in capabilities.values():

        if capability.level != level:
            continue

        if level == 1:
            if parent_code is None:
                children.append(
                    capability
                )
            continue

        if (
            _parent_code(capability.code)
            == parent_code
        ):
            children.append(
                capability
            )

    return children


def _path_codes(code: str) -> list[str]:
    parts = code.split(".")

    return [
        ".".join(parts[:index])
        for index in range(
            1,
            len(parts) + 1,
        )
    ]


def _initialise_state():
    defaults = {
        "ebcm_level_1": None,
        "ebcm_level_2": None,
        "ebcm_level_3": None,
        "ebcm_level_4": None,
        "ebcm_search": None,
        "ebcm_processed_search": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def _set_selected_capability(
    code: str,
):
    parts = code.split(".")

    values = {
        "ebcm_level_1": None,
        "ebcm_level_2": None,
        "ebcm_level_3": None,
        "ebcm_level_4": None,
    }

    for depth in range(
        1,
        min(len(parts), 4) + 1,
    ):
        level_code = ".".join(
            parts[:depth]
        )

        values[
            f"ebcm_level_{depth}"
        ] = level_code

    for key, value in values.items():
        st.session_state[key] = value


def _select_level(
    level: int,
    code: str,
):
    st.session_state[
        f"ebcm_level_{level}"
    ] = code

    for deeper_level in range(
        level + 1,
        5,
    ):
        st.session_state[
            f"ebcm_level_{deeper_level}"
        ] = None


def _search_changed():
    selected = st.session_state.get(
        "ebcm_search"
    )

    if not selected:
        return

    code = selected.split(
        " · ",
        maxsplit=1,
    )[0]

    _set_selected_capability(
        code
    )

    st.session_state[
        "ebcm_processed_search"
    ] = selected


def _selected_code() -> str | None:
    for level in range(
        4,
        0,
        -1,
    ):
        value = st.session_state.get(
            f"ebcm_level_{level}"
        )

        if value:
            return value

    return None


def _render_header(
    capabilities: dict[str, Capability],
):
    title_col, search_col = st.columns(
        [1.55, 1.0],
        gap="large",
    )

    with title_col:
        st.title(
            "Enterprise Business Capability Model"
        )

        render_html(
            """
            <div style="
                color:#667A92;
                font-size:14px;
                line-height:1.5;
                margin-top:-4px;
                margin-bottom:10px;
            ">
                Explore the enterprise capability hierarchy,
                understand how capabilities relate, and navigate
                directly to the area of the business you need.
            </div>
            """
        )

    search_options = []

    for capability in capabilities.values():
        search_options.append(
            (
                f"{capability.code} · "
                f"{capability.name} "
                f"— Level {capability.level}"
            )
        )

    with search_col:
        st.selectbox(
            "Search all business capabilities",
            options=search_options,
            index=None,
            placeholder="Search 841 capabilities...",
            key="ebcm_search",
            on_change=_search_changed,
        )


def _render_overview_stats(
    capabilities: dict[str, Capability],
):
    level_counts = {
        level: sum(
            1
            for capability
            in capabilities.values()
            if capability.level == level
        )
        for level in range(1, 5)
    }

    render_html(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
            flex-wrap:wrap;
            margin:2px 0 18px 0;
        ">
            <span class="category-badge">
                {len(capabilities)} capabilities in this extract
            </span>
            <span class="category-badge">
                {level_counts[1]} Level 1
            </span>
            <span class="category-badge">
                {level_counts[2]} Level 2
            </span>
            <span class="category-badge">
                {level_counts[3]} Level 3
            </span>
            <span class="category-badge">
                {level_counts[4]} Level 4
            </span>
        </div>
        """
    )


def _render_level_1(
    capabilities: dict[str, Capability],
):
    level_1 = _children(
        capabilities=capabilities,
        parent_code=None,
        level=1,
    )

    render_html(
        """
        <div class="panel-heading">
            Choose a Level 1 capability
        </div>
        <div class="panel-subheading">
            Start with the broad business area,
            then progressively drill into the capability model.
        </div>
        """
    )

    columns = st.columns(
        4,
        gap="small",
    )

    for index, capability in enumerate(
        level_1
    ):
        column = columns[
            index % 4
        ]

        with column:
            selected = (
                st.session_state[
                    "ebcm_level_1"
                ]
                == capability.code
            )

            label = (
                f"{capability.code}  "
                f"{capability.name}"
            )

            if st.button(
                label,
                key=(
                    f"ebcm_l1_"
                    f"{capability.code}"
                ),
                type=(
                    "primary"
                    if selected
                    else "secondary"
                ),
                use_container_width=True,
            ):
                _select_level(
                    1,
                    capability.code,
                )
                st.rerun()


def _render_breadcrumb(
    capabilities: dict[str, Capability],
):
    selected = _selected_code()

    if not selected:
        return

    path = []

    for code in _path_codes(
        selected
    ):
        capability = capabilities.get(
            code
        )

        if capability:
            path.append(
                (
                    capability.code,
                    capability.name,
                )
            )

    crumbs = []

    for code, name in path:
        crumbs.append(
            f"<strong>{code}</strong> "
            f"{name}"
        )

    render_html(
        f"""
        <div class="breadcrumb">
            {" &nbsp;›&nbsp; ".join(crumbs)}
        </div>
        """
    )


def _render_level_column(
    capabilities: dict[str, Capability],
    level: int,
    parent_code: str | None,
    title: str,
):
    children = _children(
        capabilities=capabilities,
        parent_code=parent_code,
        level=level,
    )

    render_html(
        f"""
        <div class="panel-heading">
            {title}
        </div>
        <div class="panel-subheading">
            {len(children)} capabilities
        </div>
        """
    )

    if not children:
        st.caption(
            "No capabilities at this level."
        )
        return

    for capability in children:
        selected = (
            st.session_state[
                f"ebcm_level_{level}"
            ]
            == capability.code
        )

        if st.button(
            (
                f"{capability.code}  "
                f"{capability.name}"
            ),
            key=(
                f"ebcm_l{level}_"
                f"{capability.code}"
            ),
            type=(
                "primary"
                if selected
                else "secondary"
            ),
            use_container_width=True,
        ):
            _select_level(
                level,
                capability.code,
            )
            st.rerun()


def _render_drilldown(
    capabilities: dict[str, Capability],
):
    level_1 = st.session_state[
        "ebcm_level_1"
    ]

    if not level_1:
        return

    st.divider()

    _render_breadcrumb(
        capabilities
    )

    level_2_col, level_3_col, level_4_col = (
        st.columns(
            3,
            gap="medium",
        )
    )

    with level_2_col:
        _render_level_column(
            capabilities=capabilities,
            level=2,
            parent_code=level_1,
            title="Level 2",
        )

    with level_3_col:
        level_2 = st.session_state[
            "ebcm_level_2"
        ]

        if level_2:
            _render_level_column(
                capabilities=capabilities,
                level=3,
                parent_code=level_2,
                title="Level 3",
            )
        else:
            render_html(
                """
                <div class="panel-heading">
                    Level 3
                </div>
                <div class="panel-subheading">
                    Select a Level 2 capability
                </div>
                """
            )

    with level_4_col:
        level_3 = st.session_state[
            "ebcm_level_3"
        ]

        if level_3:
            _render_level_column(
                capabilities=capabilities,
                level=4,
                parent_code=level_3,
                title="Level 4",
            )
        else:
            render_html(
                """
                <div class="panel-heading">
                    Level 4
                </div>
                <div class="panel-subheading">
                    Select a Level 3 capability
                </div>
                """
            )


def _render_detail(
    capabilities: dict[str, Capability],
):
    selected = _selected_code()

    if not selected:
        return

    capability = capabilities.get(
        selected
    )

    if not capability:
        return

    child_count = len(
        _children(
            capabilities=capabilities,
            parent_code=selected,
            level=capability.level + 1,
        )
    ) if capability.level < 4 else 0

    inferred_note = ""

    if capability.inferred:
        inferred_note = """
            <div style="
                margin-top:12px;
                padding:8px 10px;
                background:#FFF8E6;
                border:1px solid #F4D58A;
                border-radius:8px;
                color:#765A14;
                font-size:12px;
            ">
                This node was inferred from the hierarchy because
                the supplied sample does not contain a separate row
                for it.
            </div>
        """

    render_html(
        f"""
        <div class="detail-panel" style="
            margin-top:18px;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:18px;
            ">
                <div>
                    <div style="
                        color:#6B7C91;
                        font-size:12px;
                        font-weight:700;
                        letter-spacing:0.7px;
                        text-transform:uppercase;
                        margin-bottom:5px;
                    ">
                        Level {capability.level} capability
                    </div>

                    <div class="detail-title">
                        {capability.code}
                        &nbsp;{capability.name}
                    </div>
                </div>

                <div class="category-badge">
                    {child_count} direct children
                </div>
            </div>

            <div class="detail-description" style="
                margin-top:10px;
            ">
                {capability.description or "No description supplied."}
            </div>

            {inferred_note}
        </div>
        """
    )


def render_page():
    _initialise_state()

    try:
        capabilities = load_capabilities()

    except Exception as exc:
        st.error(
            "Unable to load the Enterprise Business "
            f"Capability Model: {exc}"
        )
        return

    _render_header(
        capabilities
    )

    _render_overview_stats(
        capabilities
    )

    _render_level_1(
        capabilities
    )

    _render_drilldown(
        capabilities
    )

    _render_detail(
        capabilities
    )
