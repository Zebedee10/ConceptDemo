import pandas as pd
import streamlit as st

from components.ui import render_html

from config.settings import (
    SAMPLE_ADRS_FILE,
)


# ============================================================
# CONSTANTS
# ============================================================

DECIDING_AUTHORITIES = [
    "Enterprise Decision",
    "Division A",
    "Division B",
    "Division C",
]


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_adr_data():

    if not SAMPLE_ADRS_FILE.exists():

        return pd.DataFrame()

    data = pd.read_csv(
        SAMPLE_ADRS_FILE
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
# STATUS STYLE
# ============================================================

def get_status_style(
    status: str,
):

    status_lower = (
        status.lower()
    )

    if status_lower == "approved":

        return (
            "#E8F6EC",
            "#1E7A3B",
        )

    if status_lower == "proposed":

        return (
            "#FFF5E5",
            "#A66400",
        )

    if status_lower == "superseded":

        return (
            "#EEF2F7",
            "#677589",
        )

    return (
        "#EEF2F7",
        "#566476",
    )


# ============================================================
# ADR CARD
# ============================================================

def render_adr_card(
    row,
    highlighted=False,
):

    (
        status_bg,
        status_colour,
    ) = get_status_style(
        row["Status"]
    )

    border_colour = (
        "#1769D2"
        if highlighted
        else "#DFE6EE"
    )

    background = (
        "#F7FAFF"
        if highlighted
        else "#FFFFFF"
    )

    render_html(
        f"""
        <div style="
            border:1px solid {border_colour};
            border-radius:10px;
            background:{background};
            padding:16px 18px;
            margin-bottom:10px;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:16px;
            ">

                <div>

                    <div style="
                        color:#718096;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:0.04em;
                        margin-bottom:5px;
                    ">
                        {row["ADR ID"]}
                    </div>

                    <div style="
                        color:#0B1F3A;
                        font-size:16px;
                        font-weight:700;
                        margin-bottom:5px;
                    ">
                        {row["Title"]}
                    </div>

                    <div style="
                        color:#60748B;
                        font-size:13px;
                        line-height:1.5;
                    ">
                        {row["Summary"]}
                    </div>

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
                    {row["Status"]}
                </div>

            </div>

            <div style="
                display:flex;
                gap:26px;
                margin-top:13px;
                padding-top:11px;
                border-top:1px solid #EDF1F5;
                font-size:12px;
            ">

                <div>
                    <span style="color:#7A8797;">
                        Deciding authority
                    </span>

                    <span style="
                        color:#283E57;
                        font-weight:650;
                        margin-left:5px;
                    ">
                        {row["Deciding Authority"]}
                    </span>
                </div>

                <div>
                    <span style="color:#7A8797;">
                        Decision date
                    </span>

                    <span style="
                        color:#283E57;
                        font-weight:650;
                        margin-left:5px;
                    ">
                        {row["Decision Date"]}
                    </span>
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
        "Architecture Decision Records"
    )

    data = load_adr_data()

    if data.empty:

        st.info(
            "No Architecture Decision Records "
            "are available."
        )

        return

    selected_adr = (
        st.query_params.get(
            "adr"
        )
    )

    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    filter_column, count_column = (
        st.columns(
            [1.1, 3],
            gap="medium",
        )
    )

    with filter_column:

        selected_authority = (
            st.selectbox(
                "Deciding Authority",
                options=[
                    "All authorities",
                    *DECIDING_AUTHORITIES,
                ],
            )
        )

    if (
        selected_authority
        == "All authorities"
    ):

        filtered = (
            data.copy()
        )

    else:

        filtered = data[
            data["Deciding Authority"]
            == selected_authority
        ].copy()

    with count_column:

        render_html(
            f"""
            <div style="
                padding-top:30px;
                color:#7A8797;
                font-size:13px;
            ">
                Showing
                <strong style="color:#30445D;">
                    {len(filtered)}
                </strong>
                Architecture Decision Records
            </div>
            """
        )

    st.divider()

    # --------------------------------------------------------
    # SELECTED ADR FROM EXCEPTION LINK
    # --------------------------------------------------------

    if selected_adr:

        selected_records = data[
            data["ADR ID"]
            == selected_adr
        ]

        if not selected_records.empty:

            render_html(
                """
                <div style="
                    color:#1769D2;
                    font-size:12px;
                    font-weight:700;
                    margin-bottom:8px;
                    text-transform:uppercase;
                    letter-spacing:0.04em;
                ">
                    Selected Decision
                </div>
                """
            )

            render_adr_card(
                selected_records.iloc[0],
                highlighted=True,
            )

            st.divider()

    # --------------------------------------------------------
    # ALL FILTERED ADRS
    # --------------------------------------------------------

    render_html(
        """
        <div style="
            color:#0B1F3A;
            font-size:17px;
            font-weight:700;
            margin-bottom:10px;
        ">
            Decision Records
        </div>
        """
    )

    if filtered.empty:

        st.info(
            "No Architecture Decision Records "
            "match this authority."
        )

        return

    for _, row in filtered.iterrows():

        # Do not repeat the highlighted ADR
        # immediately underneath itself.

        if (
            selected_adr
            and row["ADR ID"]
            == selected_adr
        ):
            continue

        render_adr_card(
            row
        )