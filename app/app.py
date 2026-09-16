import os
import sys

import streamlit as st

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# APPLICATION IMPORTS
# ============================================================

from app.components.layout import (
    apply_theme,
    render_sidebar,
    render_footer,
)

from app.views.home import render_home
from app.views.data_management import render_data_management
from app.views.classroom_analytics import render_classroom_analytics
from app.views.decision_support import render_decision_support


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="InsightED | AI Decision Support",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        /* Hide Streamlit's automatic multipage navigation */
        [data-testid="stSidebarNav"] {
            display: none;
        }

        /* Hide the top app/home navigation links if present */
        [data-testid="stSidebarNavItems"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# GLOBAL THEME
# ============================================================

apply_theme()


# SIDEBAR NAVIGATION ======================================================

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

selected_page = render_sidebar()


# Store the page currently being displayed
#st.session_state["active_page"] = selected_page

# PAGE ROUTER =========================================================

if selected_page == "Home":
    render_home()

elif selected_page == "Classroom Overview":
    render_classroom_analytics()

elif selected_page == "Decision Support":
    render_decision_support()

elif selected_page == "Data Management":
    render_data_management()

# ============================================================
# FOOTER
# ============================================================

render_footer()