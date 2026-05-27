import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium
import folium

# 1. Page Configuration (Full Width, Custom Title)
st.set_page_config(
    page_title="Pak Land Watch | Earth Observation Platform",
    page_icon="🇵🇰",
    layout="wide"
)

# 2. Complete Custom CSS to match the premium dark theme
st.markdown("""
    <style>
    /* Dark Premium Theme Colors */
    .stApp {
        background-color: #0F141C !important;
        color: #FFFFFF !important;
    }
    
    /* Sidebar Styling Override */
    [data-testid="stSidebar"] {
        background-color: #1A2332 !important;
        border-right: 1px solid #2D3748;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    
    /* Hero Banner Section */
    .hero-container {
        background: linear-gradient(180deg, rgba(15,20,28,0.2) 0%, rgba(26,35,50,1) 100%), 
                    url('https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?q=80&w=1200&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        padding: 40px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        border: 1px solid #1A2332;
    }
    .hero-title { font-size: 34px; font-weight: bold; color: #FFFFFF; margin-bottom: 5px; }
    .hero-subtitle { font-size: 16px; color: #A0AEC0; margin-bottom: 15px; }
    
    /* Feature Section Blocks */
    .section-title { font-size: 24px; font-weight: bold; color: #FFFFFF; text-align: center; margin: 40px 0 20px 0; }
    .feature-card { 
        background-color: #1A2332; 
        padding: 20px; 
        border-radius: 8px; 
        border: 1px solid #2D3748;
        height: 100%;
    }
    .feature-card h4 { color: #FF7A00 !important; margin-top: 0; }
    
    /* Gradient CTA Box */
    .gradient-box {
        background: linear-gradient(90deg, #0D324D 0%, #FF7A00 100%);
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin: 40px 0;
    }
    
    /* Custom Footer Styling */
    .custom-footer {
        text-align: center;
        padding: 40px 20px 20px 20px;
        border-top: 1px solid #1A2332;
        color: #718096;
        font-size: 14px;
    }
    .watermark {
        color: #FF7A00;
        font-weight: bold;
        font-size: 16px;
        margin-top: 5px;
    }
    
    /* Map Legend Styling */
    .legend-title { font-size: 14px; font-weight: bold; margin-bottom: 8px; color: #FF7A00; }
    .legend-item { display: flex; align-items: center; margin-bottom: 4px; font-size: 13px; }
    .legend-color { width: 16px; height: 16px; margin-right: 8px; border-radius: 3px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR CONTROLS (Clean Layout)
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/external-flatart-icons-flat-flatarticons/64/external-satellite-space-flatart-icons-flat-flatarticons.png", width=50)
    st.markdown("### Control Pipeline")
    st.write("Configure your tracking engine:")
    st.write("---")
    
    regions = {
        "All Pakistan": {"center": [30.3753, 69.3451], "zoom": 5},
        "Punjab (Agriculture)": {"center": [31.1704, 72.7097], "zoom": 7},
        "Sindh (Indus Basin)": {"center": [25.8943, 68.5247], "zoom": 7},
        "KPK (Mountainous)": {"center": [34.9526, 72.3311], "zoom": 7},
        "Balochistan (Arid Zones)": {"center": [28.4907, 65.0958], "zoom": 6},
        "Gilgit-Baltistan (Glaciers)": {"center": [35.8026, 74.9843], "zoom": 8}
    }
    
    selected_region = st.selectbox("1. Focus Region Target", list(regions.keys()))
    analysis_type = st.selectbox(
        "2. Analytical Layer Index",
        ["Natural Color (True View)", "NDVI (Crop & Vegetation Health)", "NDWI (Flood & Water Mapping)"]
    )
    year = st.slider("3. Satellite Timeline Year", 2018, 2026, 2026)
    
    st.write("---")
    
    # Dynamic Map Legend Guide inside the Sidebar
    if analysis_type == "NDVI (Crop & Vegetation Health)":
        st.markdown('<div class="legend-title">🌿 NDVI Index Scale</div>', unsafe_allow_html=True)
        st.markdown('<div class="legend-item"><div class="legend-color" style="background:#228B22;"></div>Dense Forest / Healthy Crop</div>', unsafe_allow_html=True)
        st.markdown('<div class="legend-item"><div class="legend-color" style="background:#8FBC8F;"></div>Moderate / Sparse Brush</div>', unsafe_allow_html=True)
        st.markdown('<div class="legend-item"><div class="legend-color" style="background:#DEB887;"></div>Barren Soil / Urban Builtup</div>', unsafe_allow_html=True)
    elif analysis_type == "NDWI (Flood & Water Mapping)":
        st.markdown('<div class="legend-title">💧 NDWI Index Scale</div>', unsafe_allow_html=True)
        st.markdown('<div class="legend-item"><div class="legend-color" style="background:#00008B;"></div>Deep Water Channels / Rivers</div>', unsafe_
