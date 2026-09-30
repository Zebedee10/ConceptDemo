import pandas as pd
import streamlit as st

from components.ui import render_html

from config.settings import (
    SAMPLE_CHANGE_PORTFOLIOS_FILE,
)


# ============================================================
# CONSTANTS
# ============================================================

PORTFOLIOS = [
    "Enterprise Change Portfolio",
    "Division A",
    "Division B",
    "Division C",
]


# ============================================================
# DATA
# ============================================================

@st.cache_data
def load_change_portfolio_data():

    if not SAMPLE_CHANGE_PORTFOLIOS_FILE.exists():
        return pd.DataFrame()

    data = pd.read_csv(
        SAMPLE_CHANGE_PORTFOLIOS_FILE
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

    status_lower = status.lower()

    if status_lower == "in delivery":

        return (
            "#E8F6EC",
            "#1E7A3B",
        )

    if status_lower == "mobilising":

        return (
            "#EEF4FD",
            "#1769D2",
        )

    if status_lower == "planned":

        return (
            "#FFF5E5",
            "#A66400",
        )

    return (
        "#EEF2F7",
        "#566476",
    )


# ============================================================
# INITIATIVE CARD
# ============================================================

def render_initiative_card(
    row,
):

    (
        status_bg,
        status_colour,
    ) = get_status_style(
        row["Status"]
    )

    render_html(
        f"""
        <div style="
            border:1px solid #DFE6EE;
            border-radius:10px;
            background:#FFFFFF;
            padding:15px 17px;
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
                        color:#75859A;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:0.04em;
                        margin-bottom:4px;
                    ">
                        {row["Initiative ID"]}
                    </div>

                    <div style="
                        color:#0B1F3A;
                        font-size:16px;
                        font-weight:700;
                        margin-bottom:4px;
                    ">
                        {row["Initiative Name"]}
                    </div>

                    <div style="
                        color:#64768C;
                        font-size:13px;
                    ">
                        {row["Business Area"]}
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
                margin-top:11px;
                padding-top:10px;
                border-top:1px solid #EEF2F7;
                color:#75859A;
                font-size:12px;
            ">
                Target date

                <span style="
                    color:#2A405A;
                    font-weight:650;
                    margin-left:5px;
                ">
                    {row["Target Date"]}
                </span>
            </div>

        </div>
        """
    )


# ============================================================
# PORTFOLIO VIEW
# ============================================================

def render_portfolio(
    data,
    portfolio_name,
):

    portfolio_data = data[
        data["Portfolio"]
        == portfolio_name
    ].copy()

    render_html(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:12px;
        ">

            <div>

                <div style="
                    color:#0B1F3A;
                    font-size:20px;
                    font-weight:700;
                ">
                    {portfolio_name}
                </div>

                <div style="
                    color:#718096;
                    font-size:13px;
                    margin-top:3px;
                ">
                    Technology-enabled change initiatives
                </div>

            </div>

            <div class="category-badge">
                {len(portfolio_data)} initiatives
            </div>

        </div>
        """
    )

    if portfolio_data.empty:

        st.info(
            "No initiatives are recorded "
            "for this portfolio."
        )

        return

    for _, row in portfolio_data.iterrows():

        render_initiative_card(
            row
        )


# ============================================================
# PAGE
# ============================================================

def render_page():

    st.title(
        "Change Portfolios"
    )

    data = load_change_portfolio_data()

    if data.empty:

        st.info(
            "No change portfolio data is available."
        )

        return

    tabs = st.tabs(
        PORTFOLIOS
    )

    for tab, portfolio_name in zip(
        tabs,
        PORTFOLIOS,
    ):

        with tab:

            render_portfolio(
                data,
                portfolio_name,
            )