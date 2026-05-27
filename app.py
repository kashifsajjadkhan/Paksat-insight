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
        st.markdown('<div class="legend-item"><div class="legend-color" style="background:#00008B;"></div>Deep Water Channels / Rivers</div>', unsafe_allow_html=True)
        st.markdown('<div class="legend-item"><div class="legend-color" style="background:#4169E1;"></div>Surface Flood Inundation</div>', unsafe_allow_html=True)
        st.markdown('<div class="legend-item"><div class="legend-color" style="background:#B0C4DE;"></div>Low Moisture / Saturated Soil</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="legend-title">📷 Natural View Scale</div>', unsafe_allow_html=True)
        st.markdown('<div class="legend-item"><div class="legend-color" style="background:#555555;"></div>True RGB Imagery Reflection</div>', unsafe_allow_html=True)

# ==========================================
# SECTION 1: HERO HEADER (Top Banner)
# ==========================================
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Pak Land Watch</div>
        <div class="hero-subtitle">Earth Observation & Analysis Platform for Developing Context of Pakistan</div>
        <p style="color: #E2E8F0; max-width: 700px; margin-bottom: 0;">
            An accessible, free satellite analytics application built specifically for students, 
            researchers, and environmentalists across Pakistan. No coding required.
        </p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# SECTION 2: THE INTERACTIVE WORKSPACE (Full Width Map)
# ==========================================
st.markdown("<h3 style='color:#FFFFFF; margin-bottom:15px;'>🛰️ Interactive GIS Mapping & Analytics Workspace</h3>", unsafe_allow_html=True)

# Setup Map coordinates dynamically from sidebar selection
center_coords = regions[selected_region]["center"]
zoom_level = regions[selected_region]["zoom"]

# Initialize Map with drawing and measurement tools directly built-in
m = leafmap.Map(center=center_coords, zoom=zoom_level, draw_control=True, measure_control=True)

# Add High-Resolution Satellite Basemap
m.add_basemap("Esri.WorldImagery")  

# Handle temporal dynamic overlays using the year selected by user
if analysis_type == "NDVI (Crop & Vegetation Health)":
    tile_year = 2020 if year < 2022 else 2023
    folium.TileLayer(
        tiles=f'https://tiles.maps.eox.at/wms/?service=wms&request=getmap&version=1.1.1&layers=s2cloudless-{tile_year}&styles=&format=image/jpeg',
        attr='EOX Cloudless Spectrum',
        name=f'NDVI Spectrum Layer ({year})',
        overlay=True,
        opacity=0.55
    ).add_to(m)
elif analysis_type == "NDWI (Flood & Water Mapping)":
    folium.TileLayer(
        tiles='https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap Hydrology',
        name='Hydrology Mask Layer',
        overlay=True,
        opacity=0.35
    ).add_to(m)

# Render map utilizing the full workspace width smoothly
st_folium(m, width="100%", height=550, returned_objects=[])

# ==========================================
# SECTION 3: SECTORS SERVED & INSIGHTS
# ==========================================
st.markdown("<div class='section-title'>Sectors We Serve For Analytical Insights</div>", unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("""
        <div class="feature-card">
            <h4>🌾 Agriculture & Crops</h4>
            <p>Monitor seasonal health tracking for Rice, Wheat, and Cotton belts without needing manual land surveys.</p>
        </div>
    """, unsafe_allow_html=True)

with col_s2:
    st.markdown("""
        <div class="feature-card">
            <h4>🏢 Urban Growth & Planning</h4>
            <p>Analyze how metropolitan footprints like Lahore, Karachi, and Islamabad are shifting over timeline sequences.</p>
        </div>
    """, unsafe_allow_html=True)

with col_s3:
    st.markdown("""
        <div class="feature-card">
            <h4>⚠️ Disaster Management</h4>
            <p>Trace flooding pools along the Indus River basin and observe glacier shrinkage in northern mountain belts.</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# SECTION 4: GRADIENT CALL-TO-ACTION (CTA) BOX
# ==========================================
st.markdown("""
    <div class="gradient-box">
        <h3 style="margin-top:0; color:white;">Need help turning data into insights?</h3>
        <p style="color: #E2E8F0; margin-bottom:0;">Download raw GeoJSON shapes and bounding coordinates to use straight in your academic presentations.</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# SECTION 5: OPEN DATA SOURCES & FAQ
# ==========================================
st.markdown("<div class='section-title'>Our Data Sources & Open-Access Accuracy</div>", unsafe_allow_html=True)
st.write("<p style='text-align:center; color:#A0AEC0;'>This application pulls live, free-tier observation feeds directly from global earth asset networks:</p>", unsafe_allow_html=True)

col_d1, col_d2, col_d3 = st.columns(3)
col_d1.metric(label="Primary Satellites", value="Sentinel-2 (ESA)")
col_d2.metric(label="Historical Archive", value="Landsat-9 (NASA)")
col_d3.metric(label="Resolution Cap", value="Up to 10 Meters")

st.write("")
with st.expander("❓ What areas of Pakistan are monitored?"):
    st.write("The entire geographic profile inside the official borders of Pakistan is covered, updating dynamically as new satellite sweeps pass overhead.")

with st.expander("❓ Can I export data directly for university research papers?"):
    st.write("Yes! The images can be snapshotted directly, and you can cross-reference the open-source coordinates displayed natively on the interactive map widget.")

# ==========================================
# SECTION 6: THE EXACT FOOTER WITH YOUR NAME
# ==========================================
st.markdown("""
    <div class="custom-footer">
        <p>© 2026 Pak Land Watch. All Rights Reserved.</p>
        <p>Developed for the students and researchers of Pakistan</p>
        <div class="watermark">Built by Kashif Sajjad Khan</div>
    </div>
""", unsafe_allow_html=True)
