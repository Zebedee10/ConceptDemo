import pandas as pd
import streamlit as st

from components.ui import render_html

from config.settings import (
    SAMPLE_CHANGE_PORTFOLIOS_FILE,
    SAMPLE_DATA_FILE,
    SAMPLE_PATTERNS_FILE,
)


# ============================================================
# LOAD SAMPLE DATA
# ============================================================

@st.cache_data
def load_change_data():

    if not SAMPLE_CHANGE_PORTFOLIOS_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(
        SAMPLE_CHANGE_PORTFOLIOS_FILE
    ).fillna("")


@st.cache_data
def load_technology_data():

    if not SAMPLE_DATA_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(
        SAMPLE_DATA_FILE
    ).fillna("")


@st.cache_data
def load_pattern_data():

    if not SAMPLE_PATTERNS_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(
        SAMPLE_PATTERNS_FILE
    ).fillna("")


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
            margin-bottom:20px;
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
                Illustrative governance triage experience.
            </div>

        </div>
        """
    )


# ============================================================
# SECTION HEADING
# ============================================================

def render_section_heading(
    number,
    title,
    description,
):

    render_html(
        f"""
        <div style="
            display:flex;
            gap:12px;
            align-items:flex-start;
            margin-top:6px;
            margin-bottom:12px;
        ">

            <div style="
                width:28px;
                height:28px;
                flex:0 0 28px;
                border-radius:50%;
                background:#EAF2FF;
                color:#1769D2;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:12px;
                font-weight:750;
            ">
                {number}
            </div>

            <div>

                <div style="
                    color:#0B1F3A;
                    font-size:17px;
                    font-weight:700;
                    margin-bottom:2px;
                ">
                    {title}
                </div>

                <div style="
                    color:#718096;
                    font-size:13px;
                ">
                    {description}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# STATUS MESSAGE
# ============================================================

def render_status(
    status,
    title,
    description,
):

    if status == "good":

        background = "#F1F8F3"
        border = "#CEE8D5"
        title_colour = "#23743B"
        symbol = "✓"

    elif status == "warning":

        background = "#FFF9EE"
        border = "#F0DCA8"
        title_colour = "#956200"
        symbol = "!"

    else:

        background = "#F8FAFC"
        border = "#DFE6EE"
        title_colour = "#526377"
        symbol = "•"

    render_html(
        f"""
        <div style="
            display:flex;
            gap:10px;
            align-items:flex-start;
            border:1px solid {border};
            background:{background};
            border-radius:8px;
            padding:10px 12px;
            margin-top:8px;
        ">

            <div style="
                color:{title_colour};
                font-size:15px;
                font-weight:750;
            ">
                {symbol}
            </div>

            <div>

                <div style="
                    color:{title_colour};
                    font-size:13px;
                    font-weight:700;
                    margin-bottom:2px;
                ">
                    {title}
                </div>

                <div style="
                    color:#617286;
                    font-size:12px;
                    line-height:1.4;
                ">
                    {description}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# GOVERNANCE SUMMARY
# ============================================================

def render_governance_summary(
    unmanaged_change,
    non_strategic_required,
    no_pattern,
):

    render_html(
        """
        <div style="
            color:#0B1F3A;
            font-size:20px;
            font-weight:750;
            margin-bottom:3px;
        ">
            Governance Position
        </div>

        <div style="
            color:#718096;
            font-size:13px;
            margin-bottom:14px;
        ">
            Illustrative assessment based on the information provided.
        </div>
        """
    )

    col1, col2, col3 = st.columns(
        3,
        gap="small",
    )

    with col1:

        if unmanaged_change:

            render_status(
                "warning",
                "Managed Change",
                "No associated change initiative. "
                "This should be understood as an exception.",
            )

        else:

            render_status(
                "good",
                "Managed Change",
                "The change is associated with "
                "a recognised change initiative.",
            )

    with col2:

        if non_strategic_required:

            render_status(
                "warning",
                "Strategic Technology",
                "A non-strategic technology "
                "has been identified.",
            )

        else:

            render_status(
                "good",
                "Strategic Technology",
                "Selected technologies are "
                "Strategic Technologies.",
            )

    with col3:

        if no_pattern:

            render_status(
                "warning",
                "Approved Pattern",
                "No approved pattern applies. "
                "The project will need to produce one.",
            )

        else:

            render_status(
                "good",
                "Approved Pattern",
                "An approved pattern can be "
                "selected for the design.",
            )

    if non_strategic_required:

        render_html(
            """
            <div style="
                border:1px solid #E9CACA;
                background:#FFF7F7;
                border-radius:9px;
                padding:14px 16px;
                margin-top:14px;
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:16px;
                ">

                    <div>

                        <div style="
                            color:#A43D3D;
                            font-size:14px;
                            font-weight:750;
                            margin-bottom:3px;
                        ">
                            EDA Approval Required
                        </div>

                        <div style="
                            color:#6E5C5C;
                            font-size:12px;
                        ">
                            Use of a non-strategic technology
                            constitutes an exception requiring
                            Enterprise Design Authority approval.
                        </div>

                    </div>

                    <div style="
                        background:#FBE5E5;
                        color:#A43D3D;
                        border-radius:14px;
                        padding:5px 10px;
                        font-size:11px;
                        font-weight:750;
                        white-space:nowrap;
                    ">
                        REQUIRED
                    </div>

                </div>

            </div>
            """
        )

    else:

        render_html(
            """
            <div style="
                border:1px solid #D7E8DB;
                background:#F6FBF7;
                border-radius:9px;
                padding:14px 16px;
                margin-top:14px;
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:16px;
                ">

                    <div>

                        <div style="
                            color:#297143;
                            font-size:14px;
                            font-weight:750;
                            margin-bottom:3px;
                        ">
                            EDA Approval
                        </div>

                        <div style="
                            color:#617267;
                            font-size:12px;
                        ">
                            No Strategic Technology exception
                            has currently been identified.
                        </div>

                    </div>

                    <div style="
                        background:#E4F3E8;
                        color:#297143;
                        border-radius:14px;
                        padding:5px 10px;
                        font-size:11px;
                        font-weight:750;
                        white-space:nowrap;
                    ">
                        NOT CURRENTLY REQUIRED
                    </div>

                </div>

            </div>
            """
        )


# ============================================================
# PAGE
# ============================================================

def render_page():

    st.title(
        "Governance Triage"
    )

    render_poc_banner()

    change_data = (
        load_change_data()
    )

    technology_data = (
        load_technology_data()
    )

    pattern_data = (
        load_pattern_data()
    )

    # ========================================================
    # 1. CHANGE INITIATIVE
    # ========================================================

    render_section_heading(
        "1",
        "Change Initiative",
        "Confirm the managed change initiative "
        "associated with the proposed design.",
    )

    initiatives = []

    if not change_data.empty:

        initiatives = (
            change_data[
                "Initiative Name"
            ]
            .drop_duplicates()
            .tolist()
        )

    selected_initiative = (
        st.selectbox(
            "Associated change initiative",
            options=[
                "Select a change initiative...",
                *initiatives,
            ],
            label_visibility="collapsed",
        )
    )

    unmanaged_change = st.checkbox(
        "This change is not associated with "
        "a managed change initiative",
        key="triage_no_change",
    )

    if unmanaged_change:

        render_status(
            "warning",
            "Change Portfolio Exception",
            "The proposed change is not associated "
            "with a managed change initiative and "
            "requires further governance review.",
        )

    elif (
        selected_initiative
        != "Select a change initiative..."
    ):

        render_status(
            "good",
            "Change Initiative Confirmed",
            f"{selected_initiative} is recorded "
            "within the change portfolio.",
        )

    st.divider()

    # ========================================================
    # 2. TECHNOLOGIES
    # ========================================================

    render_section_heading(
        "2",
        "Technologies",
        "Identify the technologies that will "
        "form part of the solution.",
    )

    technologies = []

    if not technology_data.empty:

        technologies = (
            technology_data[
                "Strategic Technology"
            ]
            .drop_duplicates()
            .tolist()
        )

        technologies = [
            value
            for value in technologies
            if value
        ]

    selected_technologies = (
        st.multiselect(
            "Strategic Technologies",
            options=technologies,
            placeholder=(
                "Select the technologies "
                "used by the solution"
            ),
        )
    )

    non_strategic_required = (
        st.checkbox(
            "A technology not on the "
            "Strategic Technology List is required",
            key="triage_non_strategic",
        )
    )

    if non_strategic_required:

        st.text_input(
            "Non-strategic technology",
            placeholder=(
                "Enter the technology requiring "
                "an exception"
            ),
        )

        render_status(
            "warning",
            "Strategic Technology Exception",
            "Use of a non-strategic technology "
            "requires an exception and will "
            "trigger EDA approval.",
        )

    elif selected_technologies:

        render_status(
            "good",
            "Strategic Technologies Confirmed",
            "The selected technologies are "
            "recorded Strategic Technologies.",
        )

    st.divider()

    # ========================================================
    # 3. PATTERNS
    # ========================================================

    render_section_heading(
        "3",
        "Architecture Patterns",
        "Identify the approved patterns "
        "that will be used by the design.",
    )

    available_patterns = (
        pattern_data.copy()
    )

    if (
        selected_technologies
        and not pattern_data.empty
    ):

        available_patterns = (
            pattern_data[
                pattern_data[
                    "Strategic Technology"
                ].isin(
                    selected_technologies
                )
            ]
        )

    pattern_options = []

    if not available_patterns.empty:

        pattern_options = [
            (
                f'{row["Pattern ID"]} — '
                f'{row["Pattern Name"]}'
            )
            for _, row
            in available_patterns.iterrows()
        ]

    selected_patterns = (
        st.multiselect(
            "Applicable approved patterns",
            options=pattern_options,
            placeholder=(
                "Select the patterns "
                "used by the solution"
            ),
        )
    )

    no_pattern = st.checkbox(
        "No approved pattern applies",
        key="triage_no_pattern",
    )

    if no_pattern:

        render_status(
            "warning",
            "Pattern Required",
            "The project will need to create "
            "and agree the required architecture "
            "pattern as part of the engagement.",
        )

    elif selected_patterns:

        render_status(
            "good",
            "Approved Pattern Selected",
            "The solution will use an "
            "existing approved pattern.",
        )

    elif (
        selected_technologies
        and not pattern_options
    ):

        render_status(
            "warning",
            "No Approved Pattern Found",
            "No existing pattern is associated "
            "with the selected technology. "
            "A pattern may need to be produced.",
        )

    st.divider()

    # ========================================================
    # GOVERNANCE POSITION
    # ========================================================

    render_governance_summary(
        unmanaged_change,
        non_strategic_required,
        no_pattern,
    )

    st.divider()

    # ========================================================
    # DESIGN DOCUMENT
    # ========================================================

    render_html(
        """
        <div style="
            text-align:center;
            max-width:760px;
            margin:8px auto 14px auto;
        ">

            <div style="
                color:#0B1F3A;
                font-size:20px;
                font-weight:750;
                margin-bottom:5px;
            ">
                Generate Design Document
            </div>

            <div style="
                color:#718096;
                font-size:13px;
                line-height:1.5;
            ">
                Future capability: use the change context,
                selected technologies, architecture patterns
                and governance information to generate an
                initial design document for the architect
                to review and build upon.
            </div>

        </div>
        """
    )

    centre_left, centre, centre_right = (
        st.columns(
            [1, 1.5, 1]
        )
    )

    with centre:

        if st.button(
            "Generate Design Document",
            type="primary",
            use_container_width=True,
            key="generate_design_document",
        ):

            st.info(
                "Proof of Concept: future versions "
                "will use an LLM to generate an "
                "initial design document from the "
                "available architecture information."
            )