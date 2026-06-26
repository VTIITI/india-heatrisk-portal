# import streamlit as st

# st.set_page_config(page_title="About HeatRisk", layout="wide")

# st.title("📚 Understanding the HeatRisk Framework")
# st.write("---")

# st.markdown("""
# ### What is HeatRisk?
# The **HeatRisk Prototype** adapts the classic product methodology deployed by the National Weather Service (NWS) and blends it with local meteorological definitions. 
# It provides a quick, scannable look at high heat stress potentials over a 5-day horizon.

# Unlike a simple temperature map, HeatRisk analyzes multiple combined facets:
# 1. **Absolute Peak Heat:** How close the projected daily high temperature gets to extreme historic limits.
# 2. **Heat Accumulation Duration:** Tracking multiple sequential days of sustained high temperatures without nocturnal cooling relief.
# 3. **Climatological Anomalies:** Highlighting when early-season temperatures significantly deviate from normal baselines before the human body has fully acclimatized.

# ### Who is impacted at each level?
# * **Category 0 (Green): Low Risk.** Little to no risk for the general population.
# * **Category 1 (Yellow): Moderate Risk.** Impacts individuals highly sensitive to heat, such as outdoor workers, infants, and seniors.
# * **Category 2 (Orange): High Risk.** Impacts anyone without effective cooling or proper hydration. Critical precautions required.
# * **Category 3 (Red): Very High Risk.** Reaches IMD Heat Wave thresholds. Significant risk to public health infrastructure.
# * **Category 4 (Magenta): Extreme Risk.** Reaches IMD Severe Heat Wave conditions. Extreme danger to everyone exposed for long durations.
# """)


import streamlit as st

st.set_page_config(page_title="About HeatRisk", layout="wide")

# Custom styling
st.markdown("""
    <style>
    h1 {
        color: #FF6B35;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    h2 {
        color: #FF6B35;
        border-bottom: 2px solid #FF6B35;
        padding-bottom: 0.5rem;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-left: 4px solid #FF6B35;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Understanding the HeatRisk Framework")
st.divider()

st.markdown("""
## What is HeatRisk?

The **HeatRisk Prototype** is an advanced heat stress prediction system that combines:
- **International Best Practices:** Adapted from the National Weather Service (NWS) HeatRisk methodology
- **Local Climate Science:** Integrated with India Meteorological Department (IMD) official thresholds
- **Real-time Forecasts:** Powered by European Centre for Medium-Range Weather Forecasts (ECMWF)

Unlike simple temperature maps, HeatRisk analyzes multiple interconnected factors to provide a comprehensive heat stress outlook for a **5-day horizon**.
""")

st.divider()

st.markdown("## 🔍 Multi-Factor Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🌡️ Absolute Peak Heat
    
    How close projected daily highs get to extreme historical limits, based on:
    - Regional temperature records
    - Seasonal climate patterns
    - Elevation adjustments
    """)

with col2:
    st.markdown("""
    ### 📈 Heat Accumulation
    
    Tracking multiple sequential days of sustained high temperatures:
    - No nocturnal cooling relief
    - Cumulative physiological stress
    - Multi-day threshold crossings
    """)

with col3:
    st.markdown("""
    ### 📊 Climatological Anomalies
    
    Highlighting early-season deviations from normal:
    - Departure from seasonal baseline
    - Pre-acclimatization period risks
    - Unexpected temperature surges
    """)

st.divider()

st.markdown("## 🎯 Risk Categories & Public Impact")

# Risk category table
risk_data = {
    'Category': ['0 - Low', '1 - Moderate', '2 - High', '3 - Heat Wave', '4 - Severe HW'],
    'Temperature': ['< 40°C', '40-42.9°C', '43-44.9°C', '45-46.9°C', '≥ 47°C'],
    'Population Impact': [
        'No special risk',
        'Sensitive groups (outdoor workers, elderly)',
        'Anyone without cooling/hydration',
        'Significant public health concern',
        'Extreme danger to all populations'
    ],
    'Color': ['🟢', '🟡', '🟠', '🔴', '🟣']
}

import pandas as pd
df = pd.DataFrame(risk_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

st.markdown("## 💡 Vulnerable Populations by Risk Level")

vulnerable = {
    'Category 0 (Green): Low Risk': [
        '✓ General population is safe',
        '✓ Standard outdoor activities permitted',
        '✓ No special precautions needed'
    ],
    'Category 1 (Yellow): Moderate Risk': [
        '⚠️ Outdoor workers at risk',
        '⚠️ Infants and toddlers vulnerable',
        '⚠️ Elderly individuals with health conditions',
        '⚠️ People with chronic illnesses'
    ],
    'Category 2 (Orange): High Risk': [
        '⚠️ Anyone without effective cooling',
        '⚠️ Unhoused populations',
        '⚠️ People with limited mobility',
        '⚠️ Individuals taking certain medications'
    ],
    'Category 3 (Red): Heat Wave': [
        '🚨 IMD Official Heat Wave Declaration',
        '🚨 Significant risk to public health infrastructure',
        '🚨 Potential for heat-related illnesses',
        '🚨 Strain on emergency services'
    ],
    'Category 4 (Magenta): Severe Heat Wave': [
        '🚨 Extreme danger to ALL populations',
        '🚨 Potential for mass casualty events',
        '🚨 Infrastructure breakdown possible',
        '🚨 Emergency protocols activate'
    ]
}

for category, impacts in vulnerable.items():
    with st.expander(f"**{category}**", expanded=False):
        for impact in impacts:
            st.markdown(impact)

st.divider()

st.markdown("## 📊 Comparison with Other Heat Products")

comparison_data = {
    'Feature': [
        'Spatial Resolution',
        'Temporal Resolution',
        'Risk Categories',
        'Regional Adaptation',
        'Official Alignment',
        'Physiological Factors'
    ],
    'NWS HeatRisk': [
        'County-level',
        '5-day outlook',
        '5 categories',
        'US-centric',
        'NWS standards',
        'Basic temperature'
    ],
    'IMD Heat Alerts': [
        'Station-based',
        'Daily/Seasonal',
        'Heat Wave criteria',
        'India-specific',
        'IMD official',
        'Temperature only'
    ],
    'HeatRisk Tracker': [
        '0.25° grid (~28km)',
        'Hourly data, 5-day',
        'IMD + accumulation',
        'India optimized',
        'IMD aligned',
        'Multi-factor analysis'
    ]
}

comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

st.divider()

st.markdown("## 🔬 Data & Methodology")

methodology = st.container()
with methodology:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Data Sources
        - **Weather Data:** ECMWF IFS (Integrated Forecasting System)
        - **Resolution:** 0.25° (~28 km grid spacing)
        - **Update Frequency:** Every 6 hours
        - **Variable:** Maximum 2m Temperature (mx2t3)
        - **Domain:** Mainland India (6°N-38°N, 66°E-98°E)
        """)
    
    with col2:
        st.markdown("""
        ### Processing Steps
        1. **Data Retrieval:** ECMWF OpenData (free tier)
        2. **Spatial Subset:** Extract India domain
        3. **Unit Conversion:** Kelvin → Celsius
        4. **Daily Aggregation:** Compute daily maximum
        5. **Classification:** Apply IMD thresholds
        6. **Visualization:** Contour mapping with borders
        """)

st.divider()

st.markdown("## ⚙️ Technical Features")

features_col1, features_col2 = st.columns(2)

with features_col1:
    st.markdown("""
    ### Interactive Capabilities
    - 📅 Forecast date selector
    - 🗺️ State boundary overlays
    - 🎯 Dual-layer visualization
    - 📍 Interactive hover details
    - 🔄 Real-time data refresh
    - 📱 Mobile-responsive design
    """)

with features_col2:
    st.markdown("""
    ### Analytical Tools
    - 📊 Temperature statistics
    - ⚠️ Risk extent calculations
    - 🎨 NWS-style color coding
    - 📈 Trend identification
    - 🌍 Geographic context layers
    - 📑 Detailed risk breakdowns
    """)

st.divider()

st.markdown("## ⚠️ Important Disclaimer")

st.warning("""
### Research Use Only

**This is a prototype system for research and educational purposes.**

- ❌ Do NOT rely solely on this system for critical decisions
- ✅ Always cross-reference with official IMD weather alerts
- ✅ Consult emergency services for real-time guidance
- ✅ Follow government-issued heat advisories

For official weather information, visit: **India Meteorological Department (IMD)**
""")

st.divider()

st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;'>
    <h3>🌍 Contributing to Climate Resilience</h3>
    <p>This project demonstrates how open-source data and advanced analytics can enhance public health preparedness for extreme heat events.</p>
    <small>Developed with ECMWF OpenData | Aligned with IMD Standards</small>
</div>
""", unsafe_allow_html=True)