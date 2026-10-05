from pathlib import Path

import streamlit as st

from components.theme import (
    apply_theme,
)

from components.ui import (
    render_html,
)

from config.settings import (
    APP_NAME,
    SAMPLE_DATA_FILE,
)

from repositories.csv_repository import (
    CsvTaxonomyRepository,
)

from services.taxonomy_service import (
    TaxonomyService,
)

from views.taxonomy_page import (
    render_page as render_taxonomy_page,
)

from views.ebcm_page import (
    render_page as render_ebcm_page,
)

from views.exceptions_page import (
    render_page as render_exceptions_page,
)

from views.adr_page import (
    render_page as render_adr_page,
)

from views.change_portfolios_page import (
    render_page as render_change_portfolios_page,
)

from views.triage_page import (
    render_page as render_triage_page,
)

from views.commercial_renewals_page import (
    render_page as render_commercial_renewals_page,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

GA_CONTROL_CENTRE_ICON = (
    BASE_DIR
    / "assets"
    / "ga_control_centre_sidebar.png"
)


# ============================================================
# STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon=str(GA_CONTROL_CENTRE_ICON),
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL THEME
# ============================================================

apply_theme()


# ============================================================
# DEPENDENCIES
# ============================================================

@st.cache_resource
def create_taxonomy_service():

    repository = CsvTaxonomyRepository(
        SAMPLE_DATA_FILE
    )

    return TaxonomyService(
        repository
    )


taxonomy_service = create_taxonomy_service()


# ============================================================
# PAGE STATE
# ============================================================

VALID_PAGES = [
    "STL Lookup",
    "Business Capabilities",
    "Change Portfolios",
    "Commercial Renewals",
    "Governance Triage",
    "STL Exceptions",
    "Architecture Decisions",
]


requested_page = (
    st.query_params.get(
        "page"
    )
)

if (
    requested_page
    and requested_page in VALID_PAGES
):

    st.session_state.selected_page = (
        requested_page
    )


if "selected_page" not in st.session_state:

    st.session_state.selected_page = (
        "STL Lookup"
    )


def set_page(
    page_name: str,
):

    st.session_state.selected_page = (
        page_name
    )

    st.query_params["page"] = (
        page_name
    )

    if (
        page_name
        != "Architecture Decisions"
        and "adr" in st.query_params
    ):

        del st.query_params["adr"]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # GROUP ARCHITECTURE CONTROL CENTRE BRAND
    # --------------------------------------------------------

    st.image(
        str(GA_CONTROL_CENTRE_ICON),
        use_container_width=True,
    )

    render_html(
        """
        <div style="
            height:8px;
        ">
        </div>
        """
    )

    # --------------------------------------------------------
    # EXPLORE
    # --------------------------------------------------------

    render_html(
        """
        <div style="
            color:#7A8797;
            font-size:11px;
            font-weight:700;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-bottom:8px;
        ">
            Explore
        </div>
        """
    )

    if st.button(
        "STL Lookup",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page
            == "STL Lookup"
            else "secondary"
        ),
        key="nav_stl_lookup",
    ):

        set_page(
            "STL Lookup"
        )

        st.rerun()

    if st.button(
        "Business Capabilities",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page
            == "Business Capabilities"
            else "secondary"
        ),
        key="nav_business_capabilities",
    ):

        set_page(
            "Business Capabilities"
        )

        st.rerun()

    # --------------------------------------------------------
    # CHANGE
    # --------------------------------------------------------

    render_html(
        """
        <div style="
            color:#7A8797;
            font-size:11px;
            font-weight:700;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-top:18px;
            margin-bottom:8px;
        ">
            Change
        </div>
        """
    )

    if st.button(
        "Change Portfolios",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page
            == "Change Portfolios"
            else "secondary"
        ),
        key="nav_change_portfolios",
    ):

        set_page(
            "Change Portfolios"
        )

        st.rerun()

    # --------------------------------------------------------
    # COMMERCIAL
    # --------------------------------------------------------

    render_html(
        """
        <div style="
            color:#7A8797;
            font-size:11px;
            font-weight:700;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-top:18px;
            margin-bottom:8px;
        ">
            Commercial
        </div>
        """
    )

    if st.button(
        "Commercial Renewals",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page
            == "Commercial Renewals"
            else "secondary"
        ),
        key="nav_commercial_renewals",
    ):

        set_page(
            "Commercial Renewals"
        )

        st.rerun()

    # --------------------------------------------------------
    # GOVERN
    # --------------------------------------------------------

    render_html(
        """
        <div style="
            color:#7A8797;
            font-size:11px;
            font-weight:700;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-top:18px;
            margin-bottom:8px;
        ">
            Govern
        </div>
        """
    )

    if st.button(
        "Governance Triage",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page
            == "Governance Triage"
            else "secondary"
        ),
        key="nav_governance_triage",
    ):

        set_page(
            "Governance Triage"
        )

        st.rerun()

    if st.button(
        "STL Exceptions",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page
            == "STL Exceptions"
            else "secondary"
        ),
        key="nav_stl_exceptions",
    ):

        set_page(
            "STL Exceptions"
        )

        st.rerun()

    if st.button(
        "Architecture Decisions",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.selected_page
            == "Architecture Decisions"
            else "secondary"
        ),
        key="nav_architecture_decisions",
    ):

        set_page(
            "Architecture Decisions"
        )

        st.rerun()


# ============================================================
# PAGE ROUTING
# ============================================================

if (
    st.session_state.selected_page
    == "STL Lookup"
):

    render_taxonomy_page(
        taxonomy_service
    )


elif (
    st.session_state.selected_page
    == "Business Capabilities"
):

    render_ebcm_page()


elif (
    st.session_state.selected_page
    == "Change Portfolios"
):

    render_change_portfolios_page()


elif (
    st.session_state.selected_page
    == "Commercial Renewals"
):

    render_commercial_renewals_page()


elif (
    st.session_state.selected_page
    == "Governance Triage"
):

    render_triage_page()


elif (
    st.session_state.selected_page
    == "STL Exceptions"
):

    render_exceptions_page(
        taxonomy_service
    )


elif (
    st.session_state.selected_page
    == "Architecture Decisions"
):

    render_adr_page()
