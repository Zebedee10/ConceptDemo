import pandas as pd
import streamlit as st

from components.ui import render_html

from config.settings import (
    SAMPLE_COMMERCIAL_RENEWALS_FILE,
    SAMPLE_COMMERCIAL_DIVISION_ROADMAPS_FILE,
)


# ============================================================
# DATA
# ============================================================

@st.cache_data
def load_commercial_renewals():

    if not SAMPLE_COMMERCIAL_RENEWALS_FILE.exists():

        return pd.DataFrame()

    data = pd.read_csv(
        SAMPLE_COMMERCIAL_RENEWALS_FILE
    ).fillna("")

    data["Renewal Date"] = pd.to_datetime(
        data["Renewal Date"],
        errors="coerce",
    )

    return data.sort_values(
        "Renewal Date"
    )


@st.cache_data
def load_division_roadmaps():

    if not SAMPLE_COMMERCIAL_DIVISION_ROADMAPS_FILE.exists():

        return pd.DataFrame()

    return pd.read_csv(
        SAMPLE_COMMERCIAL_DIVISION_ROADMAPS_FILE
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
                Illustrative view of upcoming technology
                renewals and Division roadmap information.
            </div>

        </div>
        """
    )


# ============================================================
# KPI
# ============================================================

def render_kpi(
    title,
    value,
    description,
):

    render_html(
        f"""
        <div style="
            border:1px solid #DFE6EE;
            border-radius:10px;
            background:#FFFFFF;
            padding:15px 17px;
            min-height:105px;
        ">

            <div style="
                color:#718096;
                font-size:12px;
                margin-bottom:6px;
            ">
                {title}
            </div>

            <div style="
                color:#0B1F3A;
                font-size:26px;
                font-weight:750;
                margin-bottom:4px;
            ">
                {value}
            </div>

            <div style="
                color:#718096;
                font-size:12px;
            ">
                {description}
            </div>

        </div>
        """
    )


# ============================================================
# ROADMAP STATUS
# ============================================================

def get_roadmap_style(
    status,
):

    if status == "Confirmed":

        return (
            "#E8F6EC",
            "#23743B",
            "Roadmap confirmed",
        )

    return (
        "#FFF5E5",
        "#9A6500",
        "Roadmap required",
    )


# ============================================================
# DIVISION ROADMAP
# ============================================================

def render_division_roadmap(
    row,
    contract_id,
):

    status = (
        row["Roadmap Status"]
    )

    (
        status_bg,
        status_colour,
        status_label,
    ) = get_roadmap_style(
        status
    )

    render_html(
        f"""
        <div style="
            border:1px solid #E3E9F0;
            border-radius:9px;
            background:#FFFFFF;
            padding:13px 14px;
            margin-bottom:8px;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:14px;
                margin-bottom:7px;
            ">

                <div style="
                    color:#0B1F3A;
                    font-size:14px;
                    font-weight:700;
                ">
                    {row["Division"]}
                </div>

                <div style="
                    background:{status_bg};
                    color:{status_colour};
                    border-radius:12px;
                    padding:4px 9px;
                    font-size:10px;
                    font-weight:700;
                    text-transform:uppercase;
                    white-space:nowrap;
                ">
                    {status_label}
                </div>

            </div>
        """
    )

    if status == "Confirmed":

        roadmap_summary = (
            row["Roadmap Summary"]
            or "Roadmap information confirmed."
        )

        target_exit_date = (
            row["Target Exit Date"]
            or "Not currently planned"
        )

        render_html(
            f"""
                <div style="
                    color:#5F7085;
                    font-size:13px;
                    line-height:1.45;
                    margin-bottom:7px;
                ">
                    {roadmap_summary}
                </div>

                <div style="
                    color:#7A8797;
                    font-size:12px;
                ">
                    Target exit

                    <span style="
                        color:#30445D;
                        font-weight:650;
                        margin-left:5px;
                    ">
                        {target_exit_date}
                    </span>
                </div>

            </div>
            """
        )

    else:

        render_html(
            """
                <div style="
                    color:#6D7786;
                    font-size:13px;
                    line-height:1.45;
                    margin-bottom:9px;
                ">
                    Roadmap information has not yet been
                    confirmed by this Division.
                </div>

            </div>
            """
        )

        if st.button(
            f'Raise JIRA Request — {row["Division"]}',
            key=(
                f'jira_{contract_id}_'
                f'{row["Division"]}'
            ),
            use_container_width=True,
        ):

            st.info(
                f'Proof of Concept: a JIRA request would '
                f'be raised to {row["Division"]} to confirm '
                f'the roadmap for this contract.'
            )


# ============================================================
# CONTRACT CARD
# ============================================================

def render_contract_card(
    row,
    roadmap_data,
):

    renewal_date = (
        row["Renewal Date"].strftime(
            "%d %b %Y"
        )
        if not pd.isna(row["Renewal Date"])
        else "-"
    )

    contract_id = (
        row["Contract ID"]
    )

    contract_roadmaps = (
        roadmap_data[
            roadmap_data["Contract ID"]
            == contract_id
        ].copy()
    )

    render_html(
        f"""
        <div style="
            border:1px solid #DFE6EE;
            border-radius:11px;
            background:#FFFFFF;
            padding:17px 18px;
            margin-bottom:12px;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:18px;
            ">

                <div>

                    <div style="
                        color:#718096;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:0.04em;
                        margin-bottom:4px;
                    ">
                        {contract_id}
                    </div>

                    <div style="
                        color:#0B1F3A;
                        font-size:17px;
                        font-weight:750;
                        margin-bottom:3px;
                    ">
                        {row["Contract Name"]}
                    </div>

                    <div style="
                        color:#64768C;
                        font-size:13px;
                    ">
                        {row["Supplier"]}
                    </div>

                </div>

                <div style="
                    text-align:right;
                ">

                    <div style="
                        color:#718096;
                        font-size:11px;
                        margin-bottom:3px;
                    ">
                        Renewal date
                    </div>

                    <div style="
                        color:#0B1F3A;
                        font-size:14px;
                        font-weight:700;
                    ">
                        {renewal_date}
                    </div>

                </div>

            </div>

            <div style="
                display:grid;
                grid-template-columns:
                    minmax(150px, 1fr)
                    minmax(180px, 1.2fr);
                gap:16px;
                margin-top:15px;
                padding-top:14px;
                border-top:1px solid #EEF2F7;
            ">

                <div>

                    <div style="
                        color:#7A8797;
                        font-size:11px;
                        font-weight:650;
                        margin-bottom:5px;
                    ">
                        TECHNOLOGIES
                    </div>

                    <div style="
                        color:#263B57;
                        font-size:13px;
                        line-height:1.45;
                    ">
                        {row["Technologies"]}
                    </div>

                </div>

                <div>

                    <div style="
                        color:#7A8797;
                        font-size:11px;
                        font-weight:650;
                        margin-bottom:5px;
                    ">
                        CONSUMING DIVISIONS
                    </div>

                    <div style="
                        color:#263B57;
                        font-size:13px;
                        line-height:1.45;
                    ">
                        {row["Consuming Divisions"]}
                    </div>

                </div>

            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # DIVISION ROADMAPS
    # --------------------------------------------------------

    render_html(
        """
        <div style="
            margin-top:-2px;
            margin-bottom:8px;
            color:#0B1F3A;
            font-size:14px;
            font-weight:700;
        ">
            Division Roadmaps
        </div>
        """
    )

    if contract_roadmaps.empty:

        st.info(
            "No Division roadmap information "
            "has been recorded."
        )

    else:

        columns = st.columns(
            min(
                3,
                len(contract_roadmaps),
            ),
            gap="small",
        )

        for (
            column,
            (_, roadmap_row),
        ) in zip(
            columns,
            contract_roadmaps.iterrows(),
        ):

            with column:

                render_division_roadmap(
                    roadmap_row,
                    contract_id,
                )

    # --------------------------------------------------------
    # RENEWAL GUIDANCE
    # --------------------------------------------------------

    render_html(
        f"""
        <div style="
            border-top:1px solid #EEF2F7;
            margin-top:12px;
            padding-top:12px;
            margin-bottom:24px;
        ">

            <div style="
                color:#7A8797;
                font-size:11px;
                margin-bottom:3px;
            ">
                Indicative renewal guidance
            </div>

            <div style="
                color:#0B1F3A;
                font-size:15px;
                font-weight:750;
            ">
                {row["Indicative Renewal Guidance"]}
            </div>

        </div>
        """
    )


# ============================================================
# PAGE
# ============================================================

def render_page():

    st.title(
        "Commercial Renewals"
    )

    render_poc_banner()

    data = (
        load_commercial_renewals()
    )

    roadmap_data = (
        load_division_roadmaps()
    )

    if data.empty:

        st.info(
            "No commercial renewal information is available."
        )

        return

    # ========================================================
    # SUMMARY
    # ========================================================

    outstanding_roadmaps = (
        roadmap_data[
            roadmap_data["Roadmap Status"]
            != "Confirmed"
        ]
        if not roadmap_data.empty
        else roadmap_data
    )

    confirmed_exit_plans = (
        roadmap_data[
            roadmap_data["Target Exit Date"]
            != ""
        ]
        if not roadmap_data.empty
        else roadmap_data
    )

    col1, col2, col3 = st.columns(
        3,
        gap="small",
    )

    with col1:

        render_kpi(
            "Upcoming Renewals",
            len(data),
            "Contracts in the current renewal view",
        )

    with col2:

        render_kpi(
            "Division Roadmaps Required",
            len(outstanding_roadmaps),
            "Division responses still required",
        )

    with col3:

        render_kpi(
            "Known Exit Plans",
            len(confirmed_exit_plans),
            "Division roadmaps with a target exit date",
        )

    st.divider()

    # ========================================================
    # FILTERS
    # ========================================================

    filter_col1, filter_col2 = st.columns(
        [1, 1],
        gap="medium",
    )

    division_options = sorted(
        {
            division.strip()
            for value in data["Consuming Divisions"]
            for division in value.split(";")
            if division.strip()
        }
    )

    with filter_col1:

        selected_division = st.selectbox(
            "Consuming Division",
            options=[
                "All Divisions",
                *division_options,
            ],
        )

    with filter_col2:

        roadmap_filter = st.selectbox(
            "Roadmap Position",
            options=[
                "All",
                "All roadmaps confirmed",
                "Roadmap confirmation outstanding",
            ],
        )

    filtered = data.copy()

    if selected_division != "All Divisions":

        filtered = filtered[
            filtered[
                "Consuming Divisions"
            ].str.contains(
                selected_division,
                regex=False,
            )
        ]

    if roadmap_filter != "All":

        contract_status = {}

        for contract_id in filtered[
            "Contract ID"
        ]:

            contract_roadmaps = roadmap_data[
                roadmap_data["Contract ID"]
                == contract_id
            ]

            has_outstanding = (
                not contract_roadmaps.empty
                and (
                    contract_roadmaps[
                        "Roadmap Status"
                    ]
                    != "Confirmed"
                ).any()
            )

            contract_status[
                contract_id
            ] = has_outstanding

        if (
            roadmap_filter
            == "Roadmap confirmation outstanding"
        ):

            matching_contracts = [
                contract_id
                for contract_id, outstanding
                in contract_status.items()
                if outstanding
            ]

        else:

            matching_contracts = [
                contract_id
                for contract_id, outstanding
                in contract_status.items()
                if not outstanding
            ]

        filtered = filtered[
            filtered["Contract ID"].isin(
                matching_contracts
            )
        ]

    # ========================================================
    # RENEWALS
    # ========================================================

    render_html(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-top:10px;
            margin-bottom:12px;
        ">

            <div style="
                color:#0B1F3A;
                font-size:18px;
                font-weight:700;
            ">
                Upcoming Contract Renewals
            </div>

            <div class="category-badge">
                {len(filtered)} renewals
            </div>

        </div>
        """
    )

    if filtered.empty:

        st.info(
            "No renewals match the selected filters."
        )

        return

    for _, row in filtered.iterrows():

        render_contract_card(
            row,
            roadmap_data,
        )