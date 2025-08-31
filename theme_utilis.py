# theme_manager.py
import streamlit as st
import plotly.io as pio

class ThemeManager:
    """
    Usage:
      tm = ThemeManager()
      tm.select_theme()   # renders the sidebar radio and sets session_state
      tm.apply_theme()    # injects css and sets plotly template
    """

    def __init__(self):
        if "theme" not in st.session_state:
            st.session_state["theme"] = "Light"

        # color palettes used by this manager
        self._palettes = {
            "Light": {
                "bg": "#FFFFFF",
                "text": "#0A0A0A",
                "panel": "#F8F9FA",
                "table_bg": "#FFFFFF",
                "table_text": "#0A0A0A",
                "plotly_template": "plotly_white",
            },
            "Dark": {
                "bg": "#0E1117",
                "text": "#F5F5F5",
                "panel": "#1E1E1E",
                "table_bg": "#161616",
                "table_text": "#F5F5F5",
                "plotly_template": "plotly_dark",
            },
        }

    def select_theme(self):
        """Render sidebar control and update session_state['theme'].""" 
        st.sidebar.subheader("🎨 Theme")
        choice = st.sidebar.radio(
            "Choose theme",
            ["Light", "Dark"],
            index=0 if st.session_state["theme"]=="Light" else 1
        )
        st.session_state["theme"] = choice

    def apply_theme(self):
        """Apply CSS and Plotly template based on current session_state['theme'].""" 
        theme = st.session_state.get("theme", "Light")
        pal = self._palettes.get(theme, self._palettes["Light"])

        # Set Plotly template
        tpl = pal["plotly_template"]
        try:
            pio.templates[tpl].layout.update(
                paper_bgcolor=pal["bg"],
                plot_bgcolor=pal["bg"],
                font=dict(color=pal["text"])
            )
            pio.templates.default = tpl
        except Exception:
            pio.templates.default = tpl

        # Inject CSS for app, sidebar, tables, dropdowns, metrics, plotly
        css = f"""
        <style>
        /* Main app + page container */
        [data-testid="stAppViewContainer"], .stApp {{
            background-color: {pal['bg']} !important;
            color: {pal['text']} !important;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {pal['panel']} !important;
            color: {pal['text']} !important;
        }}
        section[data-testid="stSidebar"] * {{
            color: {pal['text']} !important;
        }}

        /* Headings & markdown text */
        .stMarkdown, .stText, .stWrite, .css-1d391kg, .css-ffhzg2, h1, h2, h3, h4, h5, h6, p, span, label {{
            color: {pal['text']} !important;
        }}

        /* Metrics / big numbers */
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {pal['text']} !important;
        }}

        /* DataFrame & table */
        [data-testid="stDataFrame"] table, .stTable table {{
            background-color: {pal['table_bg']} !important;
            color: {pal['table_text']} !important;
        }}
        [data-testid="stDataFrame"] table th, .stTable thead th {{
            color: {pal['table_text']} !important;
            background-color: {pal['panel']} !important;
        }}
        [data-testid="stDataFrame"] table td, .stTable tbody td {{
            color: {pal['table_text']} !important;
            background-color: {pal['table_bg']} !important;
        }}

        /* Selectbox / dropdown (sidebar and main) */
        div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] {{
            background-color: #1e1e1e !important;
            color: #ffffff !important;
            border: 1px solid #444444 !important;
            box-shadow: none !important;
        }}

        /* Placeholder / selected text */
        div[data-baseweb="select"] span {{
            color: #ffffff !important;
        }}

        /* Dropdown container (opened options) */
        div[data-baseweb="popover"],
        div[data-testid="stSelectbox"] [role="listbox"] {{
            background-color: #1e1e1e !important;
            color: #ffffff !important;
            border: 1px solid #444444 !important;
            z-index: 9999 !important;
            box-shadow: none !important;
        }}

        /* Each option */
        div[data-baseweb="option"], div[role="option"] {{
            background-color: #1e1e1e !important;
            color: #ffffff !important;
        }}

        /* Hover effect */
        div[data-baseweb="option"]:hover, div[role="option"]:hover {{
            background-color: #333333 !important;
            color: #00e6e6 !important;
        }}

        /* Plotly container */
        .js-plotly-plot .plotly, .plot-container {{
            background-color: transparent !important;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

