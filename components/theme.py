from components.ui import render_html


def apply_theme():

    render_html(
        """
        <style>

        .block-container {
            max-width: 1500px;
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.55rem;
        }

        section[data-testid="stSidebar"] {
            background: #F7F9FC;
            border-right: 1px solid #E3E8EF;
        }

        /*
        Keep the Streamlit sidebar collapse control, but reduce the
        vertical space reserved above the Group Architecture branding.
        */
        section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
            height: 2.5rem;
            min-height: 2.5rem;
        }

        /*
        Pull the sidebar content closer to the top while retaining
        a small amount of breathing room.
        */
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-top: 0.25rem;
        }

        h1 {
            color: #0B1F3A;
            font-size: 2.5rem !important;
            letter-spacing: -0.7px;
            margin-bottom: 0.15rem !important;
        }

        .breadcrumb {
            color: #6B7C91;
            font-size: 13px;
            margin-top: 8px;
            margin-bottom: 14px;
        }

        .breadcrumb strong {
            color: #263B57;
            font-weight: 650;
        }

        .panel-heading {
            font-size: 18px;
            font-weight: 700;
            color: #0B1F3A;
            margin-bottom: 2px;
        }

        .panel-subheading {
            color: #708198;
            font-size: 13px;
            margin-bottom: 8px;
        }

        .category-badge {
            background: #EEF4FD;
            color: #4D6890;
            font-size: 12px;
            border-radius: 14px;
            padding: 4px 9px;
            white-space: nowrap;
        }

        div.stButton > button {
            width: 100%;
            min-height: 48px;
            justify-content: flex-start;
            text-align: left;
            border-radius: 8px;
            border: 1px solid #D9E2EC;
            background: #FFFFFF;
            color: #263B57;
            padding-left: 0.9rem;
            font-size: 0.93rem;
        }

        div.stButton > button:hover {
            border-color: #3578E5;
            color: #155EC2;
            background: #F6F9FF;
        }

        div.stButton > button[kind="primary"] {
            background: #EEF5FF;
            border: 1px solid #2E78E8;
            color: #155EC2;
        }

        .detail-panel {
            border: 1px solid #DFE6EE;
            border-radius: 12px;
            background: #FFFFFF;
            padding: 18px 20px;
            margin-top: 4px;
        }

        .detail-title {
            color: #0B1F3A;
            font-size: 24px;
            font-weight: 750;
            margin-bottom: 4px;
        }

        .detail-description {
            color: #5D7088;
            font-size: 14px;
            line-height: 1.55;
        }

        .tech-card {
            border: 1px solid #DFE6EE;
            border-radius: 10px;
            background: #FFFFFF;
            padding: 16px;
            min-height: 88px;
        }

        .tech-name {
            color: #102A4C;
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 7px;
        }

        .tech-description {
            color: #60748B;
            font-size: 13px;
            line-height: 1.45;
        }

        hr {
            margin-top: 0.8rem !important;
            margin-bottom: 0.8rem !important;
        }

        </style>
        """
    )
