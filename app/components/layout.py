import streamlit as st

def apply_theme():
    st.markdown(
        """
        <link rel="stylesheet"
             href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">

        <style>
        
        /* =========================================================
           GLOBAL
           Uses Streamlit's live theme variables so Light / Dark /
           System all work. These update automatically when the
           user changes theme in Settings — no page reload needed.
           ========================================================= */

        .stApp {
            background: var(--background-color);
            color: var(--text-color);
        }

        .main .block-container {
            max-width: 1400px;
            padding-top: 0.5rem;
            padding-bottom: 3rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }

        /* =========================================================
           SIDEBAR
           ========================================================= */
        
        /* Sidebar width */
        section[data-testid="stSidebar"] {
            width: 250px;
            min-width: 250px;
        }
           
        section[data-testid="stSidebar"] {
            background: var(--secondary-background-color);
            background-image: linear-gradient(rgba(128,128,128,0.05), rgba(128,128,128,0.05));
            border-right: 1px solid rgba(128, 128, 128, 0.18);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 0.5rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }

        /* Brand */

        .sidebar-brand {
            padding: 0.6rem 0.7rem 1.4rem 0.7rem;
        }

        .sidebar-brand-title {
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--text-color);
            letter-spacing: -0.4px;
        }

        .sidebar-brand-subtitle {
            font-size: 0.73rem;
            color: rgba(128, 128, 128, 0.9);
            margin-top: 4px;
            line-height: 1.4;
        }

        /* Section title */

        .sidebar-section {
            font-size: 0.66rem;
            font-weight: 750;
            color: rgba(128, 128, 128, 0.85);
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin: 1.1rem 0 0.55rem 0.45rem;
        }

        /* SIDEBAR NAVIGATION*/

        section[data-testid="stSidebar"] .stButton {
            width: 100%;
            margin: 0 !important;
            padding: 0 !important;
        }

        section[data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            justify-content: flex-start !important;

            text-align: left !important;

            background: transparent !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;

            color: var(--text-color) !important;

            padding: 6px 12px !important;
            margin: 1px 0 !important;

            min-height: 38px !important;
            border-radius: 9px !important;

            font-size: 0.88rem !important;
            font-weight: 550 !important;

            transform: none !important;
        }

        /* Force every inner wrapper (div/p/span) to left align and
           not re-center the label text */
        section[data-testid="stSidebar"] .stButton > button * {
            text-align: left !important;
            justify-content: flex-start !important;
            width: auto !important;
        }

        section[data-testid="stSidebar"] .stButton > button span[data-testid="stIconMaterial"] {
            font-size: 22px !important;
            font-weight: 700 !important;
            margin-right: 10px !important;
        }

        section[data-testid="stSidebar"] .stButton > button p {
            margin: 0 !important;
        }

        /* ---------------------------------------------------
           ACTIVE / INACTIVE NAV ITEM BASE STATES
           st.button(type="primary") renders kind="primary";
           inactive buttons render kind="secondary".
           Active state uses var(--primary-color) so it adapts
           to whatever accent color the active theme defines.
           These must come BEFORE the hover rules below so
           hover can win the cascade on equal specificity.
           --------------------------------------------------- */

        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: rgba(99, 102, 241, 0.16) !important;
            color: var(--primary-color) !important;
            font-weight: 700 !important;
            border: 1px solid transparent !important;
        }

        section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
            background: transparent !important;
            color: var(--text-color) !important;
            font-weight: 550 !important;
            border: 1px solid transparent !important;
        }

        /* HOVER — must come last so it wins over the base
           kind rules above at equal specificity */

        section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
            background: rgba(128, 128, 128, 0.14) !important;
            color: var(--text-color) !important;
            border-color: transparent !important;
            transform: none !important;
        }

        section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
            background: rgba(99, 102, 241, 0.26) !important;
            color: var(--primary-color) !important;
            border-color: transparent !important;
        }

        /* =========================================================
           SYSTEM STATUS
           ========================================================= */

        .system-card {
            padding: 12px 13px;
            background: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 10px;
            margin-top: 1.5rem;
        }

        .system-title {
            font-size: 0.8rem;
            font-weight: 650;
            color: var(--text-color);
        }

        .system-subtitle {
            font-size: 0.6rem;
            color: rgba(128, 128, 128, 0.9);
            margin-top: 4px;
        }

        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #22C55E;
            border-radius: 50%;
            margin-right: 7px;
        }

        .sidebar-description {
            margin-top: 1.8rem;
            padding: 0 10px;
            color: rgba(128, 128, 128, 0.85);
            font-size: 0.68rem;
            line-height: 1.55;
        }

        /* =========================================================
           PAGE TYPOGRAPHY
           ========================================================= */

        .page-eyebrow {
            font-size: 0.68rem;
            font-weight: 750;
            color: rgba(128, 128, 128, 0.95);
            text-transform: uppercase;
            letter-spacing: 1.3px;
        }

        .page-title {
            font-size: 2rem;
            font-weight: 800;
            color: var(--text-color);
            margin-top: 0.25rem;
            letter-spacing: -0.5px;
        }

        .page-description {
            color: rgba(128, 128, 128, 0.95);
            font-size: 0.94rem;
            line-height: 1.6;
            margin-bottom: 2rem;
        }

        /* Streamlit headings */

        h1 {
            color: var(--text-color) !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        h2 {
            color: var(--text-color) !important;
            font-weight: 750 !important;
        }

        h3 {
            color: var(--text-color) !important;
            font-weight: 700 !important;
        }

        .increasing-risk {
            color: #D32F2F !important;
            font-weight: 700 !important;
        }

        .reducing-risk {
            color: #2E7D32 !important;
            font-weight: 700 !important;
        }

        .increasing-risk-icon {
            color: #D32F2F !important;
            font-size: 18px;
        }

        .reducing-risk-icon {
            color: #2E7D32 !important;
            font-size: 18px;
        }

        /* =========================================================
           METRICS
           ========================================================= */

        div[data-testid="stMetric"] {
            background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 12px;
            padding: 15px 17px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: rgba(37, 99, 235, 0.35);
            box-shadow: 0 12px 22px rgba(37, 99, 235, 0.10), 0 4px 8px rgba(0, 0, 0, 0.05);
        }

        div[data-testid="stMetricLabel"] {
            color: rgba(128, 128, 128, 0.95);
            font-size: 0.78rem;
        }

        div[data-testid="stMetricValue"] {
            color: var(--text-color);
            font-weight: 750;
        }

        /*-------BUTTONS---------*/

        .stButton > button {
            border-radius: 9px;
            min-height: 42px;
            font-weight: 650;
            border: 1px solid rgba(128, 128, 128, 0.3);
            transition: all 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: var(--primary-color);
        }

        /* Main page primary buttons */

        .stButton > button[kind="primary"] {
            background: #2563EB !important;
            color: white !important;
            border: 1px solid #2563EB !important;
            font-weight: 700 !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: #1D4ED8 !important;
            color: white !important;
            border-color: #1D4ED8 !important;
            transform: translateY(-1px);
        }

        /* =====INPUTS ================ */

        div[data-baseweb="select"] > div {
            border-radius: 8px;
            border-color: rgba(128, 128, 128, 0.3);
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }

        /* Selectbox hover / open / focus states — force blue instead
           of Streamlit's default red accent */
        .stSelectbox div[data-baseweb="select"] > div:hover,
        .stMultiSelect div[data-baseweb="select"] > div:hover {
            border-color: rgba(37, 99, 235, 0.55) !important;
        }

        .stSelectbox div[data-baseweb="select"]:focus-within > div,
        .stMultiSelect div[data-baseweb="select"]:focus-within > div {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 1px #2563EB !important;
        }

        /* Dropdown list: selected option highlight + checkmark tick */
        ul[data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"],
        div[data-baseweb="menu"] li[aria-selected="true"],
        div[data-baseweb="popover"] li[aria-selected="true"] {
            background: rgba(37, 99, 235, 0.12) !important;
        }

        ul[data-testid="stSelectboxVirtualDropdown"] li:hover,
        div[data-baseweb="menu"] li:hover,
        div[data-baseweb="popover"] li:hover {
            background: rgba(37, 99, 235, 0.08) !important;
        }

        ul[data-testid="stSelectboxVirtualDropdown"] svg,
        div[data-baseweb="menu"] svg,
        div[data-baseweb="popover"] svg,
        .stSelectbox svg,
        .stMultiSelect svg {
            fill: #2563EB !important;
            color: #2563EB !important;
        }

        /* Multiselect selected-item tags */
        .stMultiSelect span[data-baseweb="tag"] {
            background-color: #2563EB !important;
        }

        textarea,
        input {
            border-radius: 8px !important;
        }

        textarea:focus,
        input:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 1px #2563EB !important;
        }

        /* =========================================================
           CHECKBOXES, RADIO BUTTONS, SLIDERS
           Streamlit renders these as custom SVG/div controls (not
           plain native inputs), with colours often set as inline
           styles rather than the --primary-color variable — so we
           target Streamlit's own stable widget classes (.stCheckbox,
           .stRadio, .stSlider) plus BaseWeb's role/aria attributes,
           which beat inline styles because of !important.
           ========================================================= */

        input[type="checkbox"],
        input[type="radio"] {
            accent-color: #2563EB !important;
        }

        .stCheckbox svg,
        .stRadio svg {
            fill: #2563EB !important;
        }

        .stCheckbox [role="checkbox"],
        .stCheckbox [data-baseweb="checkbox"] > div:first-child {
            border-color: #2563EB !important;
        }

        .stCheckbox [role="checkbox"][aria-checked="true"],
        .stCheckbox [data-baseweb="checkbox"] > div:first-child:has(svg) {
            background-color: #2563EB !important;
            border-color: #2563EB !important;
        }

        .stRadio [role="radio"],
        .stRadio [data-baseweb="radio"] > div:first-child {
            border-color: #2563EB !important;
        }

        .stRadio [role="radio"][aria-checked="true"],
        .stRadio [data-baseweb="radio"] > div:first-child[aria-checked="true"] {
            border-color: #2563EB !important;
        }

        .stRadio [role="radio"][aria-checked="true"] > div,
        .stRadio [data-baseweb="radio"] > div:first-child[aria-checked="true"] > div {
            background-color: #2563EB !important;
        }

        .stSlider div[role="slider"] {
            background-color: #2563EB !important;
            border-color: #2563EB !important;
        }

        .stSlider div[data-baseweb="slider"] > div > div {
            background: #2563EB !important;
        }

        /* =========================================================
           DATAFRAME
           ========================================================= */

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 10px;
            overflow: hidden;
        }

        /* Hide the row-selection checkbox column */
        div[data-testid="stDataFrame"] [data-testid="stDataFrameResizable"]
            div[role="columnheader"]:first-child,
        div[data-testid="stDataFrame"] div[role="row"] > div[role="gridcell"]:first-child:has(input[type="checkbox"]) {
            display: none !important;
        }

        div[data-testid="stDataFrame"] input[type="checkbox"] {
            display: none !important;
        }

        /* Full-row hover highlight instead of single-cell highlight */
        div[data-testid="stDataFrame"] div[role="row"]:hover > div[role="gridcell"] {
            background-color: rgba(99, 102, 241, 0.08) !important;
            cursor: pointer;
        }

        /* =========================================================
           CLICKABLE STUDENT ROW LIST (Classroom Overview)
           Header labels
           ========================================================= */

        .student-row-header {
            font-size: 0.72rem;
            font-weight: 700;
            color: rgba(128, 128, 128, 0.95);
            text-transform: uppercase;
            letter-spacing: 0.6px;
            padding: 6px 10px;
            border-bottom: 1px solid rgba(128, 128, 128, 0.25);
        }

        /* Row buttons: full width, left aligned, no border,
           no background change on hover (plain clickable row) */

        div[class*="st-key-student_row_"] .stButton > button {
            width: 100% !important;
            display: flex !important;
            justify-content: flex-start !important;
            text-align: left !important;

            background: transparent !important;
            border: none !important;
            border-bottom: 1px solid rgba(128, 128, 128, 0.14) !important;
            border-radius: 0 !important;
            box-shadow: none !important;

            color: var(--text-color) !important;
            font-weight: 450 !important;
            font-size: 0.88rem !important;

            padding: 10px 10px !important;
            margin: 0 !important;
            min-height: 38px !important;
            transform: none !important;
        }

        div[class*="st-key-student_row_"] .stButton > button:hover {
            background: transparent !important;
            border-color: rgba(128, 128, 128, 0.14) !important;
            color: var(--text-color) !important;
            transform: none !important;
            cursor: pointer;
        }

        div[class*="st-key-student_row_"] .stButton > button * {
            text-align: left !important;
            justify-content: flex-start !important;
        }

        /* =========================================================
           DIVIDERS
           A soft gradient "fade" break instead of a flat grey line.
           ========================================================= */

        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(
                90deg,
                rgba(128, 128, 128, 0) 0%,
                rgba(128, 128, 128, 0.3) 20%,
                rgba(128, 128, 128, 0.3) 80%,
                rgba(128, 128, 128, 0) 100%
            ) !important;
            margin-top: 2.4rem !important;
            margin-bottom: 2.4rem !important;
        }

        /* =========================================================
           FOOTER
           ========================================================= */

        .app-footer {
            margin-top: 4rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(128, 128, 128, 0.2);
            color: rgba(128, 128, 128, 0.85);
            font-size: 0.72rem;
            text-align: center;
        }


        /* Remove excessive vertical spacing */

        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.05rem;
        }

        /* =========================================================
           HOME PAGE — FEATURE CARDS (About InsightED)
           ========================================================= */

        .feature-card {
            background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 16px;
            padding: 24px 22px;
            width: 100%;
            height: 100%;
            flex: 1 1 auto;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04), 0 1px 8px rgba(0, 0, 0, 0.03);
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            border-color: rgba(37, 99, 235, 0.45);
            box-shadow: 0 18px 30px rgba(37, 99, 235, 0.14), 0 4px 10px rgba(0, 0, 0, 0.06);
        }

        .feature-card-icon {
            font-size: 1.9rem;
            line-height: 1;
            margin-bottom: 12px;
            display: inline-block;
        }

        .feature-card-title {
            font-size: 1.08rem;
            font-weight: 750;
            color: var(--text-color);
            margin-bottom: 8px;
            letter-spacing: -0.2px;
        }

        .feature-card-desc {
            font-size: 0.87rem;
            color: rgba(128, 128, 128, 0.95);
            line-height: 1.6;
            flex: 1 1 auto;
        }

        /* =========================================================
           HOME PAGE — WORKFLOW CARDS
           ========================================================= */

        .workflow-card {
            background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-left: 3px solid #2563EB;
            border-radius: 14px;
            padding: 20px 20px;
            width: 100%;
            height: 100%;
            flex: 1 1 auto;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04), 0 1px 8px rgba(0, 0, 0, 0.03);
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-left-color 0.22s ease, background 0.22s ease;
        }

        .workflow-card:hover {
            transform: translateY(-5px);
            border-left-color: #1D4ED8;
            background: rgba(37, 99, 235, 0.05);
            box-shadow: 0 18px 30px rgba(0, 0, 0, 0.10), 0 4px 10px rgba(0, 0, 0, 0.05);
        }

        .workflow-step-number {
            font-size: 0.7rem;
            font-weight: 800;
            color: #2563EB;
            letter-spacing: 1.4px;
        }

        .workflow-card-title {
            font-size: 1rem;
            font-weight: 750;
            color: var(--text-color);
            margin: 8px 0 6px 0;
            letter-spacing: -0.2px;
        }

        .workflow-card-desc {
            font-size: 0.82rem;
            color: rgba(128, 128, 128, 0.92);
            line-height: 1.55;
            flex: 1 1 auto;
        }

        /* =========================================================
           HOME PAGE — SYSTEM STATUS CARDS (blue, matches feature cards)
           ========================================================= */

        .status-pill-card {
            background: rgba(37, 99, 235, 0.06);
            border: 1px solid rgba(37, 99, 235, 0.24);
            border-radius: 14px;
            padding: 16px 17px;
            width: 100%;
            height: 100%;
            flex: 1 1 auto;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease, border-color 0.2s ease;
        }

        .status-pill-card:hover {
            transform: translateY(-4px);
            background: rgba(37, 99, 235, 0.11);
            border-color: rgba(37, 99, 235, 0.5);
            box-shadow: 0 14px 24px rgba(37, 99, 235, 0.14);
        }

        .status-pill-title {
            font-size: 0.85rem;
            font-weight: 700;
            color: #2563EB;
            display: flex;
            align-items: center;
            gap: 7px;
        }

        .status-pill-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #2563EB;
            border-radius: 50%;
        }

        .status-pill-desc {
            font-size: 0.72rem;
            color: rgba(128, 128, 128, 0.9);
            margin-top: 5px;
            line-height: 1.5;
            flex: 1 1 auto;
        }

        /* =========================================================
           HOME PAGE — GET STARTED (plain section, no card box)
           ========================================================= */

        .get-started-desc {
            color: rgba(128, 128, 128, 0.95);
            font-size: 0.94rem;
            line-height: 1.6;
        }

        /* Longer, centered "Start" button on the Home page */
        div[class*="st-key-home_start_data_management"] .stButton {
            display: flex !important;
            justify-content: center !important;
        }

        div[class*="st-key-home_start_data_management"] .stButton > button {
            min-width: 280px !important;
            padding: 13px 36px !important;
            font-size: 0.98rem !important;
            margin-top: 6px !important;
        }

        /* =========================================================
           HOME PAGE — EQUAL WIDTH & HEIGHT CARD GRIDS
           Scoped to the "home_page" container so other pages are
           unaffected. Streamlit columns are already equal width;
           this stretches every card in a row to match the tallest.
           Both old and new Streamlit testid names are covered since
           they changed across versions (column/stColumn,
           element-container/stElementContainer).
           ========================================================= */

        div[class*="st-key-home_page"] div[data-testid="stHorizontalBlock"] {
            align-items: stretch !important;
        }

        div[class*="st-key-home_page"] div[data-testid="column"],
        div[class*="st-key-home_page"] div[data-testid="stColumn"] {
            display: flex !important;
            flex-direction: column !important;
        }

        div[class*="st-key-home_page"] div[data-testid="column"] > div,
        div[class*="st-key-home_page"] div[data-testid="stColumn"] > div {
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
        }

        div[class*="st-key-home_page"] div[data-testid="stVerticalBlock"] {
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
        }

        div[class*="st-key-home_page"] div[data-testid="element-container"],
        div[class*="st-key-home_page"] div[data-testid="stElementContainer"] {
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
        }

        div[class*="st-key-home_page"] div[data-testid="stMarkdown"] {
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
        }

        div[class*="st-key-home_page"] div[data-testid="stMarkdown"] > div {
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
        }

        /* =========================================================
           CLASSROOM ANALYTICS PAGE — PANEL CARDS
           Applied to st.container(border=True, key="cra_panel_...")
           wrappers so charts/tables/filters sit inside a shadowed,
           hoverable card matching the rest of the app.
           ========================================================= */

        div[class*="st-key-cra_panel"] {
            border-radius: 16px !important;
            border: 0px solid rgba(128, 128, 128, 0.18) !important;
            padding: 0px 0px !important;
            background: var(--secondary-background-color) !important;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        /* =========================================================
           CLASSROOM ANALYTICS PAGE — RISK STAT CARDS
           Traffic-light colour coding for High / Moderate / Lower
           attention metrics (semantic, not decorative — kept as
           red / amber / green on purpose).
           ========================================================= */

        div[class*="st-key-cra_risk_high"] {
            border-radius: 16px !important;
            border: 1px solid rgba(220, 38, 38, 0.32) !important;
            background: rgba(220, 38, 38, 0.06) !important;
            padding: 16px 18px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease, background 0.22s ease;
        }

        div[class*="st-key-cra_risk_high"]:hover {
            transform: translateY(-4px);
            border-color: rgba(220, 38, 38, 0.6) !important;
            background: rgba(220, 38, 38, 0.10) !important;
            box-shadow: 0 14px 26px rgba(220, 38, 38, 0.16) !important;
        }

        div[class*="st-key-cra_risk_high"] div[data-testid="stMetricValue"] {
            color: #DC2626 !important;
        }

        div[class*="st-key-cra_risk_moderate"] {
            border-radius: 16px !important;
            border: 1px solid rgba(217, 119, 6, 0.32) !important;
            background: rgba(217, 119, 6, 0.06) !important;
            padding: 16px 18px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease, background 0.22s ease;
        }

        div[class*="st-key-cra_risk_moderate"]:hover {
            transform: translateY(-4px);
            border-color: rgba(217, 119, 6, 0.6) !important;
            background: rgba(217, 119, 6, 0.10) !important;
            box-shadow: 0 14px 26px rgba(217, 119, 6, 0.16) !important;
        }

        div[class*="st-key-cra_risk_moderate"] div[data-testid="stMetricValue"] {
            color: #D97706 !important;
        }

        div[class*="st-key-cra_risk_low"] {
            border-radius: 16px !important;
            border: 1px solid rgba(22, 163, 74, 0.32) !important;
            background: rgba(22, 163, 74, 0.06) !important;
            padding: 16px 18px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease, background 0.22s ease;
        }

        div[class*="st-key-cra_risk_low"]:hover {
            transform: translateY(-4px);
            border-color: rgba(22, 163, 74, 0.6) !important;
            background: rgba(22, 163, 74, 0.10) !important;
            box-shadow: 0 14px 26px rgba(22, 163, 74, 0.16) !important;
        }

        div[class*="st-key-cra_risk_low"] div[data-testid="stMetricValue"] {
            color: #16A34A !important;
        }

        /* Metrics inside risk/panel cards don't need their own
           border+shadow since the card already provides it */
        div[class*="st-key-cra_risk_high"] div[data-testid="stMetric"],
        div[class*="st-key-cra_risk_moderate"] div[data-testid="stMetric"],
        div[class*="st-key-cra_risk_low"] div[data-testid="stMetric"] {
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            background: transparent !important;
        }

        div[class*="st-key-cra_risk_high"] div[data-testid="stMetric"]:hover,
        div[class*="st-key-cra_risk_moderate"] div[data-testid="stMetric"]:hover,
        div[class*="st-key-cra_risk_low"] div[data-testid="stMetric"]:hover {
            transform: none !important;
            box-shadow: none !important;
        }

        /* =========================================================
        MOBILE RESPONSIVE SIDEBAR
        Keep the desktop sidebar unchanged, but let Streamlit
        handle the sidebar normally on small screens.
        ========================================================= */

        @media (max-width: 768px) {

            /* Let Streamlit control the sidebar width on mobile */
            section[data-testid="stSidebar"] {
                width: auto !important;
                min-width: 0 !important;
            }

            /* Give the opened mobile sidebar a solid background
            so page content cannot visually show through it */
            section[data-testid="stSidebar"] > div {
                background: var(--secondary-background-color) !important;
            }

            /* Reduce main content side padding */
            .main .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                padding-top: 0.5rem !important;
                padding-bottom: 2rem !important;
            }

            /* Smaller page headings on phones */
            .page-title {
                font-size: 1.6rem !important;
            }

            .page-description {
                font-size: 0.88rem !important;
            }

            /* Prevent footer from becoming too wide */
            .app-footer {
                margin-top: 2.5rem;
                padding: 1.2rem 0.5rem;
                font-size: 0.68rem;
            }

            .app-footer h3 {
                font-size: 0.8rem !important;
                line-height: 1.4 !important;
            }

            .app-footer p {
                line-height: 1.5 !important;
            }
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():

    with st.sidebar:

        # ----------------------------------------------------
        # BRAND
        # ----------------------------------------------------

        st.markdown(
            '<div class="sidebar-brand">'
            '<div class="sidebar-brand-title">InsightED</div>'
            '<div class="sidebar-brand-subtitle">AI Student Decision Support</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        st.markdown(
            '<div class="sidebar-section"></div>',
            unsafe_allow_html=True,
        )

        pages = {
            "Home": "Home",
            "Data Management": "Data Management",
            "Classroom Overview": "Classroom Overview",
            "Decision Support": "Decision Support",
            
        }

        icons = {
            "Home": ":material/home:",
            "Data Management": ":material/database:",
            "Classroom Overview": ":material/school:",
            "Decision Support": ":material/lightbulb:",
        }

        # ----------------------------------------------------
        # HANDLE PROGRAMMATIC NAVIGATION
        # ----------------------------------------------------

        if "navigate_to" in st.session_state:

            target_page = st.session_state["navigate_to"]

            if target_page in pages:
                st.session_state["current_page"] = target_page

            del st.session_state["navigate_to"]

        # ----------------------------------------------------
        # CURRENT PAGE
        # ----------------------------------------------------

        current_page = st.session_state.get(
            "current_page",
            "Home"
        )

        if current_page not in pages:
            current_page = "Home"

        # ----------------------------------------------------
        # NAVIGATION BUTTONS
        # ----------------------------------------------------

        for page_name in pages:

            is_active = page_name == current_page

            button_label = (
                f"{icons[page_name]}  {page_name}"
            )

            if st.button(
                button_label,
                key=f"sidebar_{page_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):

                st.session_state["current_page"] = page_name

                st.rerun()

        # ----------------------------------------------------
        # SYSTEM STATUS
        # ----------------------------------------------------

        st.markdown(
            "---"
        )

        st.markdown(
            '<div class="sidebar-section">System</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="system-card">'
            '<div class="system-title">'
            '<span class="status-dot"></span>'
            'AI Engine Online'
            '</div>'
            #'<div class="system-subtitle">'
            #'ML · XAI · Recommendations'
            #'</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        #st.markdown(
        #    '<div class="sidebar-description">'
        #    'InsightED supports lecturers by combining '
        #    'machine learning, explainable AI and '
        #    'actionable intervention recommendations.'
        #    '</div>',
        #    unsafe_allow_html=True,
        #)

    return current_page

def page_header(eyebrow, title, description):

    st.markdown(
        f'<div class="page-eyebrow">{eyebrow}</div>'
        f'<div class="page-title">{title}</div>'
        f'<div class="page-description">{description}</div>',
        unsafe_allow_html=True,
    )


def render_footer():

    st.markdown(
        '<div class="app-footer">'
        '<h5>© 2026 InsightED · AI-Powered Academic Decision Support</h5>'
        '<br>'
        '<p>Machine Learning · Explainable AI · Actionable Pedagogical Recommendations · Human Feedback</p>'
        '</div>',
        unsafe_allow_html=True,
    )