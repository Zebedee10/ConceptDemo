import pandas as pd
import streamlit as st

from components.ui import render_html

from config.settings import (
    SAMPLE_EXCEPTIONS_FILE,
)

from services.taxonomy_service import (
    TaxonomyService,
)

from views.taxonomy_page import (
    get_domain_status,
    initialise_taxonomy_state,
    render_level_1,
    render_level_2,
    render_level_3,
)


# ============================================================
# LOAD EXCEPTION DATA
# ============================================================

@st.cache_data
def load_exceptions_data():

    if not SAMPLE_EXCEPTIONS_FILE.exists():

        return pd.DataFrame()

    data = pd.read_csv(
        SAMPLE_EXCEPTIONS_FILE
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


# ============================================================
# FILTER EXCEPTIONS
# ============================================================

def get_exceptions_for_selection():

    data = load_exceptions_data()

    if data.empty:

        return data

    selected_l1 = (
        st.session_state.taxonomy_selected_l1
    )

    selected_l2 = (
        st.session_state.taxonomy_selected_l2
    )

    selected_l3 = (
        st.session_state.taxonomy_selected_l3
    )

    filtered = data[
        (data["Level 1"] == selected_l1)
        & (data["Level 2"] == selected_l2)
        & (data["Level 3"] == selected_l3)
    ]

    return filtered.reset_index(
        drop=True
    )


# ============================================================
# PROOF OF CONCEPT BANNER
# ============================================================

def render_poc_banner():

    render_html(
        """
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
            border:1px solid #D8E6FA;
            background:#F3F7FD;
            border-radius:8px;
            padding:10px 14px;
            margin-top:4px;
            margin-bottom:18px;
        ">

            <div style="
                background:#1769D2;
                color:#FFFFFF;
                border-radius:5px;
                padding:4px 7px;
                font-size:10px;
                font-weight:750;
                letter-spacing:0.06em;
                text-transform:uppercase;
            ">
                Proof of Concept
            </div>

            <div style="
                color:#536B88;
                font-size:13px;
            ">
                Illustrative exception and Architecture
                Decision Record data.
            </div>

        </div>
        """
    )


# ============================================================
# STRATEGIC TECHNOLOGIES
# ============================================================

def render_strategic_technologies(
    service: TaxonomyService,
):

    selected_l1 = (
        st.session_state.taxonomy_selected_l1
    )

    selected_l2 = (
        st.session_state.taxonomy_selected_l2
    )

    selected_l3 = (
        st.session_state.taxonomy_selected_l3
    )

    detail = service.get_level_3_detail(
        selected_l1,
        selected_l2,
        selected_l3,
    )

    render_html(
        """
        <div style="
            margin-bottom:10px;
            font-size:17px;
            font-weight:700;
            color:#0B1F3A;
        ">
            Strategic Technologies
        </div>
        """
    )

    if (
        detail is None
        or not detail.technologies
    ):

        st.info(
            "No strategic technologies are recorded."
        )

        return

    for technology in detail.technologies:

        render_html(
            f"""
            <div class="tech-card"
                 style="
                    margin-bottom:10px;
                    min-height:auto;
                 ">

                <div class="tech-name">
                    {technology.name}
                </div>

                <div class="tech-description">
                    {technology.description}
                </div>

            </div>
            """
        )


# ============================================================
# EXCEPTIONS
# ============================================================

def render_exceptions():

    exceptions = (
        get_exceptions_for_selection()
    )

    render_html(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:12px;
            margin-bottom:10px;
        ">

            <div style="
                font-size:17px;
                font-weight:700;
                color:#0B1F3A;
            ">
                Exceptions
            </div>

            <div class="category-badge">
                {len(exceptions)} exceptions
            </div>

        </div>
        """
    )

    if exceptions.empty:

        st.info(
            "No exceptions are recorded "
            "for this category."
        )

        return

    for _, row in exceptions.iterrows():

        status = (
            row["Status"]
            or "Unknown"
        )

        adr_id = (
            row["ADR ID"]
            or ""
        )

        if status.lower() == "active":

            status_bg = "#E8F6EC"
            status_colour = "#1E7A3B"

        elif status.lower() == "expired":

            status_bg = "#FDECEC"
            status_colour = "#B64141"

        elif status.lower() == "under review":

            status_bg = "#FFF5E5"
            status_colour = "#A66400"

        else:

            status_bg = "#EEF2F7"
            status_colour = "#566476"

        render_html(
            f"""
            <div style="
                border:1px solid #DFE6EE;
                border-radius:10px;
                background:#FFFFFF;
                padding:15px 16px;
                margin-bottom:10px;
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:12px;
                    margin-bottom:7px;
                ">

                    <div style="
                        color:#102A4C;
                        font-size:15px;
                        font-weight:700;
                    ">
                        {row["Exception Technology"]}
                    </div>

                    <div style="
                        background:{status_bg};
                        color:{status_colour};
                        border-radius:12px;
                        padding:4px 9px;
                        font-size:10px;
                        font-weight:700;
                        text-transform:uppercase;
                    ">
                        {status}
                    </div>

                </div>

                <div style="
                    color:#78889B;
                    font-size:12px;
                    margin-bottom:9px;
                ">
                    {row["Exception ID"]}
                </div>

                <a
                    href="?page=Architecture%20Decisions&adr={adr_id}"
                    target="_self"
                    style="
                        color:#1769D2;
                        font-size:13px;
                        font-weight:650;
                        text-decoration:none;
                    "
                >
                    View {adr_id} →
                </a>

            </div>
            """
        )


# ============================================================
# DETAIL SECTION
# ============================================================

def render_detail_section(
    service: TaxonomyService,
):

    selected_l1 = (
        st.session_state.taxonomy_selected_l1
    )

    selected_l2 = (
        st.session_state.taxonomy_selected_l2
    )

    selected_l3 = (
        st.session_state.taxonomy_selected_l3
    )

    st.divider()

    if not selected_l3:

        st.info(
            "Select a category to see its details."
        )

        return

    domain_status = get_domain_status(
        selected_l1
    )

    if domain_status == "defining":

        render_html(
            """
            <div class="detail-panel">

                <div class="detail-title">
                    Strategic technologies still to be defined
                </div>

                <div class="detail-description">
                    Strategic technologies for this
                    domain are still being defined.
                </div>

            </div>
            """
        )

        return

    detail = service.get_level_3_detail(
        selected_l1,
        selected_l2,
        selected_l3,
    )

    if detail is None:

        st.warning(
            "No information is available "
            "for this category."
        )

        return

    render_html(
        f"""
        <div class="detail-panel">

            <div class="detail-title">
                {detail.level_3.name}
            </div>

            <div class="detail-description">
                {
                    detail.level_3.description
                    or
                    "No description has been provided."
                }
            </div>

        </div>
        """
    )

    left_column, right_column = (
        st.columns(
            [1, 1],
            gap="medium",
        )
    )

    with left_column:

        render_strategic_technologies(
            service
        )

    with right_column:

        render_exceptions()


# ============================================================
# PAGE ENTRY POINT
# ============================================================

def render_page(
    service: TaxonomyService,
):

    initialise_taxonomy_state(
        service
    )

    st.title(
        "STL Exceptions"
    )

    render_poc_banner()

    (
        navigator_l1,
        navigator_l2,
        navigator_l3,
    ) = st.columns(
        [1.35, 1, 1],
        gap="medium",
    )

    with navigator_l1:

        render_level_1(
            service
        )

    with navigator_l2:

        render_level_2(
            service
        )

    with navigator_l3:

        render_level_3(
            service
        )

    render_detail_section(
        service
    )