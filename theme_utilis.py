import streamlit as st
import plotly.io as pio

class ThemeManager:
    """
    Usage:
      tm = ThemeManager()
      tm.apply_theme()    # Call at top of script to inject styles
      tm.select_theme()   # Call in sidebar to allow user to switch theme
    """

    def __init__(self):
        if "theme" not in st.session_state:
            st.session_state["theme"] = "Dark"  # default dark theme

        self._palettes = {
            "Light": {
                "bg": "#FFFFFF",         # main page and header
                "text": "#0A0A0A",
                "panel": "#F0F2F6",      # slightly different sidebar
                "table_bg": "#FFFFFF",
                "table_text": "#0A0A0A",
                "plotly_template": "plotly_white",
            },
            "Dark": {
                "bg": "#0E1117",         # main page and header
                "text": "#F5F5F5",
                "panel": "#1A1A1A",      # slightly different sidebar
                "table_bg": "#161616",
                "table_text": "#F5F5F5",
                "plotly_template": "plotly_dark",
            },
        }

    def select_theme(self, key="theme_radio"):
        """Render theme radio and update session_state['theme']"""
        st.sidebar.subheader("🎨 Theme")
        choice = st.sidebar.radio(
            "Choose theme",
            ["Light", "Dark"],
            index=0 if st.session_state["theme"] == "Light" else 1,
            key=key
        )
        st.session_state["theme"] = choice

    def apply_theme(self):
        """Apply CSS and Plotly template based on current session_state['theme']"""
        theme = st.session_state.get("theme", "Dark")
        pal = self._palettes.get(theme, self._palettes["Dark"])

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

        # Dropdown styling
        if theme == "Dark":
            dropdown_bg = "#1e1e1e"
            dropdown_text = "#ffffff"
            dropdown_border = "#444444"
            dropdown_hover = "#333333"
            dropdown_hover_text = "#00e6e6"
        else:  # Light theme
            dropdown_bg = "#ffffff"
            dropdown_text = "#000000"
            dropdown_border = "#cccccc"
            dropdown_hover = "#f0f0f0"
            dropdown_hover_text = "#000000"

        # Inject CSS including Streamlit header
        css = f"""
        <style>
        /* Main app + header */
        [data-testid="stAppViewContainer"], .stApp, header[data-testid="stHeader"] {{
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

        /* Headings, markdown, labels */
        .stMarkdown, .stText, .stWrite, h1, h2, h3, h4, h5, h6, p, span, label {{
            color: {pal['text']} !important;
        }}

        /* Metrics */
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {pal['text']} !important;
        }}

        /* Tables */
        [data-testid="stDataFrame"] table, .stTable table {{
            background-color: {pal['table_bg']} !important;
            color: {pal['table_text']} !important;
        }}
        [data-testid="stDataFrame"] table th, .stTable thead th {{
            background-color: {pal['panel']} !important;
            color: {pal['table_text']} !important;
        }}
        [data-testid="stDataFrame"] table td, .stTable tbody td {{
            background-color: {pal['table_bg']} !important;
            color: {pal['table_text']} !important;
        }}

        /* Dropdown / Selectbox styling */
        div[data-baseweb="select"] > div,
        div[data-testid="stSelectbox"] {{
            background-color: {dropdown_bg} !important;
            color: {dropdown_text} !important;
            border: 1px solid {dropdown_border} !important;
            box-shadow: none !important;
        }}
        div[data-baseweb="select"] span {{
            color: {dropdown_text} !important;
        }}
        div[data-baseweb="popover"],
        div[data-testid="stSelectbox"] [role="listbox"] {{
            background-color: {dropdown_bg} !important;
            color: {dropdown_text} !important;
            border: 1px solid {dropdown_border} !important;
            z-index: 9999 !important;
            box-shadow: none !important;
        }}
        div[data-baseweb="option"], div[role="option"] {{
            background-color: {dropdown_bg} !important;
            color: {dropdown_text} !important;
        }}
        div[data-baseweb="option"]:hover, div[role="option"]:hover {{
            background-color: {dropdown_hover} !important;
            color: {dropdown_hover_text} !important;
        }}

        /* Plotly transparency fix */
        .js-plotly-plot .plotly, .plot-container {{
            background-color: transparent !important;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
