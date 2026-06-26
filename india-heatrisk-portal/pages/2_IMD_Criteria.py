# import streamlit as st
# import pandas as pd

# st.set_page_config(page_title="IMD Threshold Metrics", layout="wide")

# st.title("📋 India Meteorological Department Threshold Matrix")
# st.write("---")

# st.markdown("""
# The color-coded index layers rendered on the primary dynamic dashboard conform directly to the statutory classifications established by the **India Meteorological Department (IMD)** for the plains regions:
# """)

# # Build an easy-to-read reference matrix table
# data = {
#     'Risk Tier ID': [0, 1, 2, 3, 4],
#     'Classification Name': ['Normal / Low Risk', 'Moderate Heat Risk', 'High Heat Stress', 'IMD Heat Wave', 'IMD Severe Heat Wave'],
#     'Temperature Cut-off Thresholds': ['< 40.0 °C', '40.0 °C - 42.9 °C', '43.0 °C - 44.9 °C', '45.0 °C - 46.9 °C', '≥ 47.0 °C'],
#     'Public Health Warning Action': ['No Special Actions Needed', 'Exercise Normal Cautious Awareness', 'Active Hydration Advised', 'Adhere to Official Heat Advisories', 'Extreme Emergency Protocols']
# }

# df = pd.DataFrame(data)
# st.table(df)

# st.markdown("""
# > **Note on Regional Variability:** The automated engine defaults to the standard 40.0°C cutoff for plains geographic domains. For specific coastal segments or elevated hilly terrain regions, heat waves may be triggered at slightly lower ambient thresholds based on departure metrics from native climatological normal means.
# """)


import streamlit as st
import pandas as pd

st.set_page_config(page_title="IMD Threshold Metrics", layout="wide")

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
    .threshold-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .threshold-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
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

st.title("📋 India Meteorological Department Threshold Matrix")
st.divider()

st.markdown("""
The color-coded risk layers rendered on the HeatRisk dashboard conform directly to the **statutory classifications** 
established by the **India Meteorological Department (IMD)** for plains regions across India.

This page details the precise temperature thresholds, regional variations, and the meteorological science behind each classification.
""")

st.divider()

# Main threshold table
st.markdown("## 📊 IMD Heat Risk Classification Thresholds")

data = {
    'Tier': [0, 1, 2, 3, 4],
    'Classification': ['Normal / Low Risk', 'Moderate Heat Risk', 'High Heat Stress', 'IMD Heat Wave', 'IMD Severe Heat Wave'],
    'Temperature Range': ['< 40.0 °C', '40.0 - 42.9 °C', '43.0 - 44.9 °C', '45.0 - 46.9 °C', '≥ 47.0 °C'],
    'Color Code': ['🟢 Green', '🟡 Yellow', '🟠 Orange', '🔴 Red', '🟣 Magenta'],
    'Public Health Alert': ['None', 'Caution', 'Warning', 'Severe Warning', 'Emergency']
}

df_thresholds = pd.DataFrame(data)

# Display as styled dataframe
st.dataframe(df_thresholds, use_container_width=True, hide_index=True)

st.divider()

st.markdown("## 🌡️ Threshold Details by Category")

# Display threshold cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🟢 Tier 0: Normal / Low Risk (< 40°C)
    
    **Characteristics:**
    - Temperatures below 40°C
    - No exceptional heat stress
    - General population safe
    - All outdoor activities permitted
    
    **Actions:**
    - No special precautions
    - Normal awareness
    - Routine operations continue
    """)

with col2:
    st.markdown("""
    ### 🟡 Tier 1: Moderate Heat Risk (40-42.9°C)
    
    **Characteristics:**
    - Temperatures in mid-40s range
    - Sensitive groups start to experience stress
    - Occasional heat-related illnesses
    
    **At-Risk Groups:**
    - Outdoor workers
    - Elderly populations
    - People with chronic conditions
    - Infants
    
    **Recommended Actions:**
    - Increase water intake
    - Limit outdoor exposure
    - Extend rest breaks
    """)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    ### 🟠 Tier 2: High Heat Stress (43-44.9°C)
    
    **Characteristics:**
    - Significantly above normal
    - Heat-related illnesses become common
    - Strain on public services
    - Infrastructure impacts possible
    
    **At-Risk Groups:**
    - Everyone without cooling
    - Unhoused populations
    - Construction/outdoor workers
    - Elderly and infants
    
    **Recommended Actions:**
    - Seek cooling centers
    - Avoid outdoor work
    - Monitor vulnerable persons
    - Ensure electricity/water supply
    """)

with col4:
    st.markdown("""
    ### 🔴 Tier 3: IMD Heat Wave (45-46.9°C)
    
    **Characteristics:**
    - **Official IMD Heat Wave declaration**
    - Significantly above normal seasonal patterns
    - Widespread heat-related illnesses
    - Multiple system failures possible
    
    **At-Risk Groups:**
    - Virtually all populations
    - Healthcare capacity strained
    - Agricultural sector affected
    
    **Recommended Actions:**
    - Adhere to government advisories
    - Activate emergency protocols
    - Medical surge capacity
    - Public communications
    """)

col5, _ = st.columns([1, 1])

with col5:
    st.markdown("""
    ### 🟣 Tier 4: Severe Heat Wave (≥ 47°C)
    
    **Characteristics:**
    - **Official IMD Severe Heat Wave**
    - Extreme danger threshold
    - Mass casualty risk
    - Infrastructure breakdown likely
    
    **Societal Impact:**
    - Healthcare system overwhelmed
    - Power grid failure risk
    - Agricultural losses
    - Fatalities possible
    
    **Recommended Actions:**
    - Extreme emergency protocols
    - Full government mobilization
    - Maximum public warnings
    - Emergency healthcare operations
    """)

st.divider()

st.markdown("## 🗺️ Regional Threshold Variations")

st.info("""
### Important: Regional Adaptation

The core temperature thresholds (40.0°C, 43.0°C, 45.0°C, 47.0°C) apply primarily to **plains regions** 
across India where the majority of the population resides.

**Regional exceptions are recognized:**
""")

regional_data = {
    'Region Type': [
        'Plains (Indo-Gangetic, Deccan Plateau)',
        'Coastal Areas',
        'Hilly/Mountainous Terrain',
        'Deserts (Thar, etc.)',
        'Island Territories'
    ],
    'Baseline Characteristics': [
        'High population density, major cities',
        'Maritime influence, moderate extremes',
        'Lower absolute temperatures',
        'Extreme heat normal seasonally',
        'Oceanic moderation'
    ],
    'Threshold Adjustment': [
        'Standard IMD thresholds apply',
        'May trigger at -1 to -2°C',
        'May trigger at -2 to -3°C',
        'Heat waves at higher absolute temps',
        'May trigger at -1°C'
    ],
    'Rationale': [
        'Population accustomed to heat patterns',
        'Lower climatological normal',
        'Lower seasonal baseline',
        'Different acclimatization',
        'Low variability from norm'
    ]
}

df_regional = pd.DataFrame(regional_data)
st.dataframe(df_regional, use_container_width=True, hide_index=True)

st.markdown("""
> **Note:** The automated engine in HeatRisk defaults to standard plains thresholds. 
> Coastal and elevated regions may experience **earlier heat wave declarations** 
> based on **departure from climatological normals** rather than absolute temperatures.
""")

st.divider()

st.markdown("## 📈 Temperature Anomaly Approach")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Absolute Temperature Method
    
    **Used for:** Plains regions
    
    **Thresholds:**
    - Heat Wave: ≥ 45.0°C (standard)
    - Severe Heat Wave: ≥ 47.0°C
    
    **Advantage:**
    - Simple, objective criteria
    - Population well-adapted
    - Clear communication
    
    **Best for:** Areas with consistent heat
    """)

with col2:
    st.markdown("""
    ### Anomaly/Departure Method
    
    **Used for:** Coastal & hilly regions
    
    **Thresholds:**
    - Heat Wave: 4-5°C above normal
    - Severe Heat Wave: 6-7°C above normal
    
    **Advantage:**
    - Accounts for regional climate
    - Better pre-acclimatization detection
    - More equitable public health response
    
    **Best for:** Variable climate regions
    """)

st.divider()

st.markdown("## 📊 Historical Heat Wave Statistics")

st.markdown("""
### IMD Heat Wave Occurrence Patterns

India experiences **significant seasonal variation** in heat wave frequency:

| Season | Frequency | Typical Months | Regions Affected |
|--------|-----------|---|---|
| **Pre-monsoon** | Highest | April-May | North, Central, West India |
| **Post-monsoon** | Moderate | Sept-Oct | North, Central regions |
| **Winter** | Rare | Dec-Feb | Some northern regions |
| **Monsoon** | Very rare | June-Sept | Northwest only |

### Recent Trends
- ⚠️ Increasing frequency of heat waves
- ⚠️ Extended duration events (5-10 days)
- ⚠️ Earlier onset in spring
- ⚠️ Rising baseline temperatures
""")

st.divider()

st.markdown("## 🔬 Meteorological Definitions")

with st.expander("**What defines an IMD Heat Wave?**", expanded=True):
    st.markdown("""
    According to India Meteorological Department official criteria:
    
    ### For Plains Regions:
    
    **Heat Wave:** Maximum temperature of **45°C or above**
    
    **Severe Heat Wave:** Maximum temperature of **47°C or above**
    
    ### For Hilly Regions:
    
    **Heat Wave:** When **4-5°C above normal** from climatological baseline
    
    **Severe Heat Wave:** When **6°C or more above normal**
    
    ### For Coastal Regions:
    
    **Heat Wave:** When temperatures are **2-3°C above normal**
    
    **Severe Heat Wave:** When **4°C or more above normal**
    
    ### Duration Requirement:
    
    - Heat wave conditions must persist for **at least 2 consecutive days**
    - If extreme temperatures occur on isolated days, they may not be formally declared
    - Multi-wave patterns increase public health severity
    """)

st.divider()

st.markdown("## 💡 Public Health Guidelines by Tier")

health_guidelines = {
    'Tier 0 (Green)': {
        'General Public': 'Normal activities, stay hydrated',
        'Vulnerable Groups': 'Take normal precautions',
        'Healthcare System': 'Normal operations',
        'Emergency Services': 'Standard readiness'
    },
    'Tier 1 (Yellow)': {
        'General Public': 'Reduce outdoor exposure, drink water regularly',
        'Vulnerable Groups': 'Minimize outdoor activities, stay indoors during peak hours',
        'Healthcare System': 'Increase awareness among medical staff',
        'Emergency Services': 'Alert status - monitor heat-related cases'
    },
    'Tier 2 (Orange)': {
        'General Public': 'Avoid outdoor work, seek air-conditioned spaces',
        'Vulnerable Groups': 'Essential access to cooling centers',
        'Healthcare System': 'Prepare for increased heat-related admissions',
        'Emergency Services': 'Ready response teams for medical emergencies'
    },
    'Tier 3 (Red)': {
        'General Public': 'Follow government advisories, minimize all outdoor activities',
        'Vulnerable Groups': 'Ensure access to cooling, regular monitoring',
        'Healthcare System': 'Activate contingency protocols, arrange ICU capacity',
        'Emergency Services': 'Full mobilization, mass casualty preparedness'
    },
    'Tier 4 (Magenta)': {
        'General Public': 'Emergency protocols - shelter in place if necessary',
        'Vulnerable Groups': 'Mandatory shelter in cooling centers',
        'Healthcare System': 'Maximum capacity surge, crisis standards',
        'Emergency Services': 'Full-scale emergency response, all resources active'
    }
}

for tier, guidelines in health_guidelines.items():
    with st.expander(f"**{tier} Public Health Guidelines**"):
        for group, action in guidelines.items():
            st.markdown(f"**{group}:** {action}")

st.divider()

st.markdown("## 📖 References & Data Sources")

st.info("""
### Official Sources

- **India Meteorological Department (IMD):** www.imd.gov.in
  - Heat Wave Advisory Standards
  - Threshold Definitions and Regional Variations
  
- **National Disaster Management Authority (NDMA):** www.ndma.gov.in
  - Heat Wave Management Guidelines
  - Public Health Response Protocols

### Data Infrastructure

- **ECMWF OpenData:** Real-time weather forecasts (0.25° resolution)
- **Historical Climate Data:** IMD climate normal datasets
- **Satellite Observations:** For validation and validation

### Further Reading

- WHO Guidelines on Heat and Health
- CDC Heat Stress Prevention Guidelines
- WMO Guidelines on Extreme Heat
""")

st.divider()

st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #FFD700 0%, #FF8C00 100%); border-radius: 12px; color: white;'>
    <h3>⚠️ Always Follow Official IMD Advisories</h3>
    <p>For the most current and authoritative heat wave information, consult the India Meteorological Department directly.</p>
    <p><strong>Your safety depends on accurate, official weather information.</strong></p>
</div>
""", unsafe_allow_html=True)



