# THEME MANAGER - Custom styling and UI components
import streamlit as st

class ThemeManager:
    """Manages light and dark theme CSS for the application"""
    
    LIGHT_COLORS = {
        "primary": "#0066cc",
        "secondary": "#dc3545",
        "background": "#ffffff",
        "text": "#000000",
        "box": "#f8f9fa",
        "border": "#e0e0e0"
    }
    
    DARK_COLORS = {
        "primary": "#4da6ff",
        "secondary": "#ff6b6b",
        "background": "#1a1a1a",
        "text": "#ffffff",
        "box": "#2d2d2d",
        "border": "#404040"
    }
    
    @staticmethod
    def get_css(is_light_mode: bool) -> str:
        """Generate custom CSS based on theme"""
        colors = ThemeManager.LIGHT_COLORS if is_light_mode else ThemeManager.DARK_COLORS
        
        return f"""
        <style>
            :root {{
                --primary-color: {colors['primary']};
                --secondary-color: {colors['secondary']};
                --text-color: {colors['text']};
                --bg-color: {colors['background']};
                --box-bg: {colors['box']};
                --border-color: {colors['border']};
            }}
            
            body, .main {{
                background-color: {colors['background']} !important;
                color: {colors['text']} !important;
            }}
            
            .main-title {{
                font-size: 4.5em !important;
                font-weight: bold;
                text-align: center;
                color: {colors['primary']};
                margin-bottom: 0.5em;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }}
            
            .section-header {{
                font-size: 3em !important;
                font-weight: bold;
                color: {colors['primary']};
                margin: 1em 0 0.5em 0;
                border-bottom: 4px solid {colors['primary']};
                padding-bottom: 0.5em;
            }}
            
            .facility-box {{
                background-color: {"#e7f3ff" if is_light_mode else "#1e3a5f"};
                padding: 2em;
                border-radius: 12px;
                margin: 1em 0;
                border-left: 6px solid {colors['primary']};
                color: {colors['text']};
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                font-size: 1.3em !important;
            }}
            
            .meal-box {{
                background-color: {"#fffacd" if is_light_mode else "#3d3a1a"};
                padding: 1.8em;
                border-radius: 12px;
                margin: 0.8em 0;
                border-left: 6px solid #ff9800;
                color: {colors['text']};
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                font-size: 1.2em !important;
            }}
            
            .stTabs [data-baseweb="tab-list"] {{
                gap: 10px;
                background-color: {colors['box']};
            }}
            
            .stTabs [role="tab"] {{
                font-size: 1.6em !important;
                font-weight: bold !important;
                padding: 15px 25px !important;
                color: {colors['text']} !important;
            }}
            
            input, textarea, select {{
                background-color: {colors['background']} !important;
                color: {colors['text']} !important;
                border: 2px solid {colors['primary']} !important;
                font-size: 1.2em !important;
            }}
            
            h1, h2, h3, h4, h5, h6 {{
                font-weight: bold !important;
            }}
        </style>
        """
    
    @staticmethod
    def apply_theme(is_light_mode: bool):
        """Apply theme to Streamlit app"""
        st.markdown(ThemeManager.get_css(is_light_mode), unsafe_allow_html=True)


def render_facility_box(content: str, title: str = "", emoji: str = ""):
    """Render a custom facility box"""
    return f"""
    <div class="facility-box">
    {f'<h3 style="margin-top: 0; color: #0066cc;">{emoji} {title}</h3>' if title else ''}
    {content}
    </div>
    """


def render_metric_card(label: str, value: str, emoji: str = ""):
    """Render a metric card"""
    return f"""
    <div class="facility-box" style="text-align: center; padding: 2em;">
    <div style="font-size: 2.5em; margin-bottom: 10px;">{emoji}</div>
    <h3 style="font-size: 1.5em; margin: 10px 0; color: #0066cc;">{label}</h3>
    <div style="font-size: 2.2em; font-weight: bold; color: #0066cc; margin: 15px 0;">{value}</div>
    </div>
    """
