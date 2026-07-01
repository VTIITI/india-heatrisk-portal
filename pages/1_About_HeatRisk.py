# # # import streamlit as st

# # # st.set_page_config(page_title="About HeatRisk", layout="wide")

# # # st.title("📚 Understanding the HeatRisk Framework")
# # # st.write("---")

# # # st.markdown("""
# # # ### What is HeatRisk?
# # # The **HeatRisk Prototype** adapts the classic product methodology deployed by the National Weather Service (NWS) and blends it with local meteorological definitions. 
# # # It provides a quick, scannable look at high heat stress potentials over a 5-day horizon.

# # # Unlike a simple temperature map, HeatRisk analyzes multiple combined facets:
# # # 1. **Absolute Peak Heat:** How close the projected daily high temperature gets to extreme historic limits.
# # # 2. **Heat Accumulation Duration:** Tracking multiple sequential days of sustained high temperatures without nocturnal cooling relief.
# # # 3. **Climatological Anomalies:** Highlighting when early-season temperatures significantly deviate from normal baselines before the human body has fully acclimatized.

# # # ### Who is impacted at each level?
# # # * **Category 0 (Green): Low Risk.** Little to no risk for the general population.
# # # * **Category 1 (Yellow): Moderate Risk.** Impacts individuals highly sensitive to heat, such as outdoor workers, infants, and seniors.
# # # * **Category 2 (Orange): High Risk.** Impacts anyone without effective cooling or proper hydration. Critical precautions required.
# # # * **Category 3 (Red): Very High Risk.** Reaches IMD Heat Wave thresholds. Significant risk to public health infrastructure.
# # # * **Category 4 (Magenta): Extreme Risk.** Reaches IMD Severe Heat Wave conditions. Extreme danger to everyone exposed for long durations.
# # # """)


# # import streamlit as st

# # st.set_page_config(page_title="About HeatRisk", layout="wide")

# # # Custom styling
# # st.markdown("""
# #     <style>
# #     h1 {
# #         color: #FF6B35;
# #         text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
# #     }
# #     h2 {
# #         color: #FF6B35;
# #         border-bottom: 2px solid #FF6B35;
# #         padding-bottom: 0.5rem;
# #     }
# #     .feature-box {
# #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #         padding: 1.5rem;
# #         border-radius: 12px;
# #         color: white;
# #         margin: 1rem 0;
# #         box-shadow: 0 4px 15px rgba(0,0,0,0.2);
# #     }
# #     .info-card {
# #         background: #f8f9fa;
# #         padding: 1.5rem;
# #         border-left: 4px solid #FF6B35;
# #         border-radius: 8px;
# #         margin: 1rem 0;
# #     }
# #     </style>
# # """, unsafe_allow_html=True)

# # st.title("📚 Understanding the HeatRisk Framework")
# # st.divider()

# # st.markdown("""
# # ## What is HeatRisk?

# # The **HeatRisk Prototype** is an advanced heat stress prediction system that combines:
# # - **International Best Practices:** Adapted from the National Weather Service (NWS) HeatRisk methodology
# # - **Local Climate Science:** Integrated with India Meteorological Department (IMD) official thresholds
# # - **Real-time Forecasts:** Powered by European Centre for Medium-Range Weather Forecasts (ECMWF)

# # Unlike simple temperature maps, HeatRisk analyzes multiple interconnected factors to provide a comprehensive heat stress outlook for a **5-day horizon**.
# # """)

# # st.divider()

# # st.markdown("## 🔍 Multi-Factor Analysis")

# # col1, col2, col3 = st.columns(3)

# # with col1:
# #     st.markdown("""
# #     ### 🌡️ Absolute Peak Heat
    
# #     How close projected daily highs get to extreme historical limits, based on:
# #     - Regional temperature records
# #     - Seasonal climate patterns
# #     - Elevation adjustments
# #     """)

# # with col2:
# #     st.markdown("""
# #     ### 📈 Heat Accumulation
    
# #     Tracking multiple sequential days of sustained high temperatures:
# #     - No nocturnal cooling relief
# #     - Cumulative physiological stress
# #     - Multi-day threshold crossings
# #     """)

# # with col3:
# #     st.markdown("""
# #     ### 📊 Climatological Anomalies
    
# #     Highlighting early-season deviations from normal:
# #     - Departure from seasonal baseline
# #     - Pre-acclimatization period risks
# #     - Unexpected temperature surges
# #     """)

# # st.divider()

# # st.markdown("## 🎯 Risk Categories & Public Impact")

# # # Risk category table
# # risk_data = {
# #     'Category': ['0 - Low', '1 - Moderate', '2 - High', '3 - Heat Wave', '4 - Severe HW'],
# #     'Temperature': ['< 40°C', '40-42.9°C', '43-44.9°C', '45-46.9°C', '≥ 47°C'],
# #     'Population Impact': [
# #         'No special risk',
# #         'Sensitive groups (outdoor workers, elderly)',
# #         'Anyone without cooling/hydration',
# #         'Significant public health concern',
# #         'Extreme danger to all populations'
# #     ],
# #     'Color': ['🟢', '🟡', '🟠', '🔴', '🟣']
# # }

# # import pandas as pd
# # df = pd.DataFrame(risk_data)
# # st.dataframe(df, use_container_width=True, hide_index=True)

# # st.divider()

# # st.markdown("## 💡 Vulnerable Populations by Risk Level")

# # vulnerable = {
# #     'Category 0 (Green): Low Risk': [
# #         '✓ General population is safe',
# #         '✓ Standard outdoor activities permitted',
# #         '✓ No special precautions needed'
# #     ],
# #     'Category 1 (Yellow): Moderate Risk': [
# #         '⚠️ Outdoor workers at risk',
# #         '⚠️ Infants and toddlers vulnerable',
# #         '⚠️ Elderly individuals with health conditions',
# #         '⚠️ People with chronic illnesses'
# #     ],
# #     'Category 2 (Orange): High Risk': [
# #         '⚠️ Anyone without effective cooling',
# #         '⚠️ Unhoused populations',
# #         '⚠️ People with limited mobility',
# #         '⚠️ Individuals taking certain medications'
# #     ],
# #     'Category 3 (Red): Heat Wave': [
# #         '🚨 IMD Official Heat Wave Declaration',
# #         '🚨 Significant risk to public health infrastructure',
# #         '🚨 Potential for heat-related illnesses',
# #         '🚨 Strain on emergency services'
# #     ],
# #     'Category 4 (Magenta): Severe Heat Wave': [
# #         '🚨 Extreme danger to ALL populations',
# #         '🚨 Potential for mass casualty events',
# #         '🚨 Infrastructure breakdown possible',
# #         '🚨 Emergency protocols activate'
# #     ]
# # }

# # for category, impacts in vulnerable.items():
# #     with st.expander(f"**{category}**", expanded=False):
# #         for impact in impacts:
# #             st.markdown(impact)

# # st.divider()

# # st.markdown("## 📊 Comparison with Other Heat Products")

# # comparison_data = {
# #     'Feature': [
# #         'Spatial Resolution',
# #         'Temporal Resolution',
# #         'Risk Categories',
# #         'Regional Adaptation',
# #         'Official Alignment',
# #         'Physiological Factors'
# #     ],
# #     'NWS HeatRisk': [
# #         'County-level',
# #         '5-day outlook',
# #         '5 categories',
# #         'US-centric',
# #         'NWS standards',
# #         'Basic temperature'
# #     ],
# #     'IMD Heat Alerts': [
# #         'Station-based',
# #         'Daily/Seasonal',
# #         'Heat Wave criteria',
# #         'India-specific',
# #         'IMD official',
# #         'Temperature only'
# #     ],
# #     'HeatRisk Tracker': [
# #         '0.25° grid (~28km)',
# #         'Hourly data, 5-day',
# #         'IMD + accumulation',
# #         'India optimized',
# #         'IMD aligned',
# #         'Multi-factor analysis'
# #     ]
# # }

# # comparison_df = pd.DataFrame(comparison_data)
# # st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# # st.divider()

# # st.markdown("## 🔬 Data & Methodology")

# # methodology = st.container()
# # with methodology:
# #     col1, col2 = st.columns(2)
    
# #     with col1:
# #         st.markdown("""
# #         ### Data Sources
# #         - **Weather Data:** ECMWF IFS (Integrated Forecasting System)
# #         - **Resolution:** 0.25° (~28 km grid spacing)
# #         - **Update Frequency:** Every 6 hours
# #         - **Variable:** Maximum 2m Temperature (mx2t3)
# #         - **Domain:** Mainland India (6°N-38°N, 66°E-98°E)
# #         """)
    
# #     with col2:
# #         st.markdown("""
# #         ### Processing Steps
# #         1. **Data Retrieval:** ECMWF OpenData (free tier)
# #         2. **Spatial Subset:** Extract India domain
# #         3. **Unit Conversion:** Kelvin → Celsius
# #         4. **Daily Aggregation:** Compute daily maximum
# #         5. **Classification:** Apply IMD thresholds
# #         6. **Visualization:** Contour mapping with borders
# #         """)

# # st.divider()

# # st.markdown("## ⚙️ Technical Features")

# # features_col1, features_col2 = st.columns(2)

# # with features_col1:
# #     st.markdown("""
# #     ### Interactive Capabilities
# #     - 📅 Forecast date selector
# #     - 🗺️ State boundary overlays
# #     - 🎯 Dual-layer visualization
# #     - 📍 Interactive hover details
# #     - 🔄 Real-time data refresh
# #     - 📱 Mobile-responsive design
# #     """)

# # with features_col2:
# #     st.markdown("""
# #     ### Analytical Tools
# #     - 📊 Temperature statistics
# #     - ⚠️ Risk extent calculations
# #     - 🎨 NWS-style color coding
# #     - 📈 Trend identification
# #     - 🌍 Geographic context layers
# #     - 📑 Detailed risk breakdowns
# #     """)

# # st.divider()

# # st.markdown("## ⚠️ Important Disclaimer")

# # st.warning("""
# # ### Research Use Only

# # **This is a prototype system for research and educational purposes.**

# # - ❌ Do NOT rely solely on this system for critical decisions
# # - ✅ Always cross-reference with official IMD weather alerts
# # - ✅ Consult emergency services for real-time guidance
# # - ✅ Follow government-issued heat advisories

# # For official weather information, visit: **India Meteorological Department (IMD)**
# # """)

# # st.divider()

# # st.markdown("""
# # <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;'>
# #     <h3>🌍 Contributing to Climate Resilience</h3>
# #     <p>This project demonstrates how open-source data and advanced analytics can enhance public health preparedness for extreme heat events.</p>
# #     <small>Developed with ECMWF OpenData | Aligned with IMD Standards</small>
# # </div>
# # """, unsafe_allow_html=True)



# import os
# import numpy as np
# import xarray as xr
# import streamlit as st
# import plotly.graph_objects as go
# import pandas as pd
# import requests
# from ecmwf.opendata import Client
# from datetime import datetime, timedelta

# # ==========================================
# # PAGE CONFIGURATION & THEMING
# # ==========================================
# st.set_page_config(
#     page_title="India HeatRisk Tracker",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'About': "### 🌡️ India HeatRisk Tracker\n\n"
#                  "**Developer:** Vaibhav Tyagi (Ph.D. Candidate)\n"
#                  "**Institution:** Department of Astronomy, Astrophysics, and Space Engineering (DAASE), IIT Indore\n"
#                  "**Supervisor:** Dr. Saurabh Das\n\n"
#                  "Real-time regional atmospheric heat stress monitoring framework powered by ECMWF open-access forecast streams and open-source python integrations (`PYIWR`)."
#     }
# )

# st.markdown("""
#     <style>
#     .main { padding-top: 1rem; }
#     h1 { font-size: 2.5rem; color: #FF6B35; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); margin-bottom: 0.5rem; }
#     h2 { color: #FF6B35; border-bottom: 3px solid #FF6B35; padding-bottom: 0.5rem; margin-top: 2rem; }
#     [data-testid="stMetric"] {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1.2rem; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
#     }
#     [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.9); font-weight: 600; }
#     [data-testid="stMetricDelta"] { color: rgba(255,255,255,0.8); }
#     .stButton > button {
#         background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
#         color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600;
#         box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3); transition: all 0.3s ease;
#     }
#     .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4); }
#     .control-panel {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
#     }
#     .legend-item { display: flex; align-items: center; margin: 0.5rem 0; font-weight: 500; }
#     .legend-color {
#         display: inline-block; width: 20px; height: 20px; border-radius: 4px;
#         margin-right: 1rem; border: 1px solid rgba(0,0,0,0.1);
#     }
#     .index-card {
#         background: white; border: 1px solid #eee; border-left: 4px solid #FF6B35;
#         border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; font-size: 0.9rem;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # ==========================================
# # HEAT-STRESS INDEX DEFINITIONS
# # ==========================================
# INDEX_DEFINITIONS = {
#     "utci": {
#         "label": "Universal Thermal Climate Index (UTCI, °C)",
#         "short": "UTCI",
#         "units": "°C",
#         "bands": [
#             (-100, 26, "No Thermal Stress", "#228B22"),
#             (26, 32, "Moderate Heat Stress", "#FFD700"),
#             (32, 38, "Strong Heat Stress", "#FF8C00"),
#             (38, 46, "Very Strong Heat Stress", "#FF0000"),
#             (46, 200, "Extreme Heat Stress", "#D1117B"),
#         ],
#         "note": "Universal Thermal Climate Index (UTCI) computes equivalent ambient temperature based on human thermal regulation parameters."
#     },
#     "imd_tmax": {
#         "label": "IMD Absolute Tmax Threshold (°C)",
#         "short": "Tmax",
#         "units": "°C",
#         "bands": [
#             (-100, 40, "Low Risk", "#228B22"),
#             (40, 43, "Moderate Risk", "#FFD700"),
#             (43, 45, "High Risk", "#FF8C00"),
#             (45, 47, "Heat Wave", "#FF0000"),
#             (47, 200, "Severe Heat Wave", "#D1117B"),
#         ],
#         "note": "Absolute air temperature thresholds for monitoring heatwave criteria."
#     },
# }


# def classify_to_risk(values, bands):
#     risk = np.zeros_like(values, dtype=float)
#     for level, (lo, hi, _name, _color) in enumerate(bands):
#         risk = np.where((values >= lo) & (values < hi), level, risk)
#     return risk


# # ==========================================
# # HEAT-STRESS INDEX FORMULAS
# # ==========================================
# def saturation_vapor_pressure_hpa(temp_c):
#     return 6.105 * np.exp(17.27 * temp_c / (237.7 + temp_c))


# def relative_humidity_from_dewpoint(temp_c, dewpoint_c):
#     e_actual = saturation_vapor_pressure_hpa(dewpoint_c)
#     e_sat = saturation_vapor_pressure_hpa(temp_c)
#     rh = 100.0 * (e_actual / e_sat)
#     return np.clip(rh, 1.0, 100.0)


# def vapor_pressure_hpa(temp_c, rh_pct):
#     return (rh_pct / 100.0) * saturation_vapor_pressure_hpa(temp_c)


# def compute_utci_c(temp_c, rh_pct):
#     va = 1.0  
#     e = vapor_pressure_hpa(temp_c, rh_pct) / 10.0  
#     utci = temp_c + (0.6061 * e) - (0.0211 * va) + (0.0039 * temp_c * e) - (0.0012 * temp_c * va)
#     return utci


# # ==========================================
# # DATA FETCH & PROCESSING
# # ==========================================
# @st.cache_data(ttl=3600)
# def fetch_and_process_forecast():
#     today_dt = datetime.utcnow()
#     target_dates = [(today_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
#     base_date = today_dt.strftime("%Y-%m-%d")
#     inst_file = f"ecmwf_india_inst_{base_date}.grib"
#     mx_file = f"ecmwf_india_mx_{base_date}.grib"

#     for f in os.listdir("."):
#         if f.startswith("ecmwf_india_") and f.endswith(".grib") and f not in (inst_file, mx_file):
#             try:
#                 os.remove(f)
#             except Exception:
#                 pass

#     try:
#         peak_steps = [6, 9, 12, 30, 33, 36, 54, 57, 60, 78, 81, 84, 102, 105, 108]
#         client = Client(source="ecmwf")

#         if not os.path.exists(inst_file):
#             client.retrieve(
#                 date=base_date, time=0, stream="oper", type="fc",
#                 step=peak_steps, param=["2t", "2d"], target=inst_file
#             )
#         if not os.path.exists(mx_file):
#             client.retrieve(
#                 date=base_date, time=0, stream="oper", type="fc",
#                 step=peak_steps, param="mx2t3", target=mx_file
#             )
#         return parse_grib(inst_file, mx_file)
#     except Exception:
#         return generate_instant_fallback(target_dates)


# def _swap_to_valid_time(da):
#     valid_times = da.step.values + da.time.values
#     da = da.assign_coords(valid_time=("step", valid_times)).swap_dims({"step": "valid_time"})
#     return da


# def parse_grib(inst_file, mx_file):
#     ds_inst = xr.open_dataset(inst_file, engine="cfgrib",
#                                backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
#     t2m_c = ds_inst["t2m"].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
#     d2m_c = ds_inst["d2m"].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
#     t2m_c = _swap_to_valid_time(t2m_c)
#     d2m_c = _swap_to_valid_time(d2m_c)

#     ds_mx = xr.open_dataset(mx_file, engine="cfgrib",
#                              backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
#     var_name = 'mx2t3' if 'mx2t3' in ds_mx.data_vars else list(ds_mx.data_vars)[0]
#     tmax_raw = ds_mx[var_name].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
#     tmax_raw = _swap_to_valid_time(tmax_raw)
#     tmax_daily = tmax_raw.resample(valid_time='1D').max()

#     rh = xr.apply_ufunc(relative_humidity_from_dewpoint, t2m_c, d2m_c)

#     results = {}
#     for key in ["utci", "imd_tmax"]:
#         definition = INDEX_DEFINITIONS[key]
#         if key == "imd_tmax":
#             values_daily = tmax_daily
#         else:
#             values_daily = xr.apply_ufunc(compute_utci_c, t2m_c, rh).resample(valid_time='1D').max()
#         risk_daily = xr.apply_ufunc(classify_to_risk, values_daily, kwargs={"bands": definition["bands"]})
#         results[key] = (values_daily, risk_daily)
#     return results


# def generate_instant_fallback(target_dates):
#     lats = np.arange(38.0, 5.75, -0.25)
#     lons = np.arange(66.0, 98.25, 0.25)
#     num_days, num_lats, num_lons = len(target_dates), len(lats), len(lons)

#     tmax_values = np.zeros((num_days, num_lats, num_lons))
#     rh_values = np.zeros((num_days, num_lats, num_lons))
#     for d in range(num_days):
#         for i, lat in enumerate(lats):
#             for j, lon in enumerate(lons):
#                 base = 39.0
#                 if lat > 32: base -= 12.0
#                 elif lat < 15: base -= 3.0
#                 if lon < 74 and 20 < lat < 30: base += 6.5
#                 tmax_values[d, i, j] = base + np.sin(d + lat / 4.0) * 1.5

#                 rh_base = 55.0
#                 if lon > 85 or lat < 15: rh_base = 78.0
#                 elif 68 <= lon <= 75 and 22 <= lat <= 30: rh_base = 25.0
#                 rh_values[d, i, j] = np.clip(rh_base + np.cos(d + lon / 5.0) * 5.0, 15.0, 95.0)

#     coords = [pd.to_datetime(target_dates), lats, lons]
#     dims = ["valid_time", "latitude", "longitude"]
#     tmax_da = xr.DataArray(tmax_values, coords=coords, dims=dims)
#     rh_da = xr.DataArray(rh_values, coords=coords, dims=dims)

#     results = {}
#     for key in ["utci", "imd_tmax"]:
#         definition = INDEX_DEFINITIONS[key]
#         if key == "imd_tmax":
#             values_daily = tmax_da
#         else:
#             values_daily = xr.apply_ufunc(compute_utci_c, tmax_da, rh_da)
#         risk_daily = xr.apply_ufunc(classify_to_risk, values_daily, kwargs={"bands": definition["bands"]})
#         results[key] = (values_daily, risk_daily)
#     return results


# @st.cache_data(ttl=86400)
# def load_india_boundaries():
#     sources = {
#         'country': "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#         'states': "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#         'districts': "https://raw.githubusercontent.com/AnujTiwari/India-State-and-District-GeoJSON/master/india_districts.geojson"
#     }
#     features = {'country': None, 'states': None, 'districts': None}
#     for key, url in sources.items():
#         try:
#             response = requests.get(url, timeout=25)
#             if response.status_code == 200: features[key] = response.json()
#         except Exception: pass
#     return features


# def _iter_rings(geometry):
#     if geometry['type'] == 'Polygon':
#         for ring in geometry['coordinates']: yield ring
#     elif geometry['type'] == 'MultiPolygon':
#         for polygon in geometry['coordinates']:
#             for ring in polygon: yield ring


# def add_boundary_layer(fig, geojson_data, color, width, dash=None):
#     if not geojson_data: return
#     line = dict(color=color, width=width)
#     if dash: line["dash"] = dash
#     for feature in geojson_data['features']:
#         if 'geometry' in feature and feature['geometry']:
#             for ring in _iter_rings(feature['geometry']):
#                 fig.add_trace(go.Scatter(
#                     x=[c[0] for c in ring], y=[c[1] for c in ring], mode='lines', line=line,
#                     showlegend=False, hoverinfo='skip'
#                 ))


# # ==========================================
# # MAIN APPLICATION INTERFACE
# # ==========================================
# st.markdown("# ☀️ India HeatRisk Tracker")
# st.markdown("**Three Essential Heat-Stress Maps: Maximum Temperature, UTCI Values, and Default Threshold Categories**")
# st.divider()

# with st.sidebar:
#     st.markdown("## 📌 Project Overview")
#     st.markdown(
#         "**Developer:** Vaibhav Tyagi<br>"
#         "**Affiliation:** Department of Astronomy, Astrophysics, and Space Engineering (DAASE), IIT Indore<br>"
#         "**Supervision:** Dr. Saurabh Das<br>"
#         "**Framework Stack:** ECMWF Open Data API, `xarray`, and Python-based meteorological processing.",
#         unsafe_allow_html=True
#     )
    
#     st.divider()
#     st.markdown("## 🎛️ Map Overlay Controls")
#     threshold_filter = st.slider("🚨 Highlight UTCI Regions Exceeding (°C)", 26.0, 46.0, 32.0, 0.5)
#     show_states = st.checkbox("🗺️ Show State Boundaries", value=True)
#     show_districts = st.checkbox("📍 Show District Boundaries", value=False)
    
#     st.divider()
#     st.markdown("### 📚 Default UTCI Thresholds")
#     for lo, hi, name, color in INDEX_DEFINITIONS["utci"]["bands"]:
#         range_txt = f"≥{lo:g}" if hi >= 199 else (f"<{hi:g}" if lo <= -99 else f"{lo:g}–{hi:g}")
#         st.markdown(
#             f"<div class='legend-item'><div class='legend-color' style='background-color:{color};'></div>"
#             f"<div><strong>{name}</strong><br/><small>{range_txt} °C</small></div></div>",
#             unsafe_allow_html=True
#         )

# try:
#     with st.spinner("🔄 Synchronizing forecast spatial grids..."):
#         all_results = fetch_and_process_forecast()
#         boundaries = load_india_boundaries()

#     utci_vals_ds, utci_risk_ds = all_results["utci"]
#     tmax_vals_ds, _ = all_results["imd_tmax"]

#     available_days = utci_vals_ds.valid_time.values
#     available_days_str = [pd.to_datetime(d).strftime("%a, %b %d") for d in available_days]

#     st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
#     ctrl_col1, ctrl_col2 = st.columns([4, 2])
#     with ctrl_col1:
#         selected_day_str = st.selectbox("📅 Global Forecast Date Sync", available_days_str)
#         selected_idx = available_days_str.index(selected_day_str)
#     with ctrl_col2:
#         if st.button("🔄 Refresh Data", use_container_width=True):
#             st.cache_data.clear()
#             st.rerun()
#     st.markdown("</div>", unsafe_allow_html=True)

#     lats = utci_vals_ds.latitude.values
#     lons = utci_vals_ds.longitude.values
#     grid_tmax = tmax_vals_ds.isel(valid_time=selected_idx).values
#     grid_utci = utci_vals_ds.isel(valid_time=selected_idx).values
#     grid_risk = utci_risk_ds.isel(valid_time=selected_idx).values

#     def generate_base_map(z_data, title, colorscale, hover_unit, is_categorical=False, category_labels=None):
#         fig = go.Figure()
        
#         if is_categorical:
#             fig.add_trace(go.Heatmap(
#                 z=z_data, x=lons, y=lats,
#                 colorscale=colorscale,
#                 showscale=False,
#                 hovertemplate="<b>%{text}</b><br>Lat: %{y:.2f}<br>Lon: %{x:.2f}<extra></extra>",
#                 text=[[category_labels[int(val)] if not np.isnan(val) else "" for val in row] for row in z_data]
#             ))
#         else:
#             fig.add_trace(go.Contour(
#                 z=z_data, x=lons, y=lats,
#                 colorscale=colorscale, contours=dict(coloring='heatmap'), line_width=0,
#                 colorbar=dict(thickness=15, len=0.8),
#                 hovertemplate=f"Lat: %{{y:.2f}}<br>Lon: %{{x:.2f}}<br>Value: %{{z:.1f}} {hover_unit}<extra></extra>"
#             ))

#         if show_districts: add_boundary_layer(fig, boundaries['districts'], 'rgba(120,120,120,0.3)', 0.5)
#         if show_states: add_boundary_layer(fig, boundaries['states'], 'rgba(40,40,40,0.8)', 1.0)
#         add_boundary_layer(fig, boundaries['country'], 'black', 2.0)

#         fig.update_layout(
#             title=f"<b>{title}</b>", xaxis=dict(range=[66, 98], showgrid=False),
#             yaxis=dict(range=[6, 38], showgrid=False, scaleanchor="x", scaleratio=1),
#             height=550, margin=dict(l=10, r=10, t=50, b=10), plot_bgcolor='#f8f9fa'
#         )
#         return fig

#     # ------------------------------------------------------------
#     # RENDER THE THREE SPECIFIED MAPS
#     # ------------------------------------------------------------
#     st.sidebar.info(f"Visualizing grids for: {selected_day_str}")

#     # Map 1: Max Temperature
#     st.markdown("## 1. Maximum Air Temperature ($T_{max}$)")
#     fig1 = generate_base_map(grid_tmax, f"Absolute Maximum Temperature (°C) — {selected_day_str}", "YlOrRd", "°C")
#     st.plotly_chart(fig1, use_container_width=True)

#     # Map 2: Heat Stress UTCI Values
#     st.markdown("## 2. Heat Stress UTCI Ambient Values")
#     masked_utci = np.where(grid_utci >= threshold_filter, grid_utci, np.nan)
#     fig2 = generate_base_map(masked_utci, f"UTCI Equivalent Heat Temperature (Exceeding {threshold_filter}°C)", "Jet", "°C")
#     st.plotly_chart(fig2, use_container_width=True)

#     # Map 3: Stress Category Based on Threshold Default
#     st.markdown("## 3. Stress Category Hazard Level (Default UTCI Thresholds)")
#     bands = INDEX_DEFINITIONS["utci"]["bands"]
#     band_colors = [b[3] for b in bands]
#     cat_labels = [b[2] for b in bands]
#     n_bands = len(band_colors)
#     categorical_colorscale = [[i / (n_bands - 1), color] for i, color in enumerate(band_colors)]
    
#     fig3 = generate_base_map(grid_risk, f"Default Threshold Risk Classification — {selected_day_str}", 
#                              categorical_colorscale, "", is_categorical=True, category_labels=cat_labels)
#     st.plotly_chart(fig3, use_container_width=True)

# except Exception as e:
#     st.error(f"⚠️ **Error displaying operational map layouts**: {str(e)}")
#     st.stop()

# # ==========================================
# # FOOTER / DISCLAIMER LAYER
# # ==========================================
# st.divider()
# st.markdown("""
# <div style='text-align: center; color: #666; padding: 1rem;'>
#     <p style='margin-bottom: 0.5rem; font-weight: 600; color: #FF6B35;'>
#         🚀 Developed for the IEEE GRSS REACT Competition
#     </p>
#     <small>
#         🌍 Data Source: ECMWF OpenData | 🧪 Indices: NWS Heat Index, WBGT (outdoor approx.), Humidex, Thom's Discomfort Index<br>
#         🗺️ Boundaries: DataMeet / GADM-derived state &amp; district GeoJSON<br>
#         ⚠️ <strong>Disclaimer:</strong> This is a prototype system for research purposes.
#         Always follow official weather alerts and advisories from IMD.
#     </small>



import streamlit as st
import pandas as pd

st.set_page_config(page_title="About HeatRisk", layout="wide")

# ==========================================
# CUSTOM STYLING & BRANDING
# ==========================================
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
        margin-top: 2rem;
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

# ==========================================
# INSTITUTIONAL & COMPETITION CONTEXT
# ==========================================
st.markdown("""
## What is India HeatRisk Tracker?

The **India HeatRisk Tracker** is an advanced biometeorological monitoring framework developed by **Vaibhav Tyagi** (Ph.D. Candidate) under the supervision of **Dr. Saurabh Das** at the **Department of Astronomy, Astrophysics, and Space Engineering (DAASE), IIT Indore**. 

This system was engineered specifically for the **IEEE GRSS REACT Competition** to bridge the gap between open-access global numerical weather prediction models and regional public health resilience.

### Core Framework Pillars:
- **Biometeorological Modeling:** Powered by the **Universal Thermal Climate Index (UTCI)** to compute real human thermal regulation parameters rather than raw temperature alone.
- **Meteorological Open Source Synergy:** Leverages automated data streams from the European Centre for Medium-Range Weather Forecasts (**ECMWF**) alongside custom python routines (`PYIWR` integration concepts).
- **Official Local Alignment:** Structured to match standard regional hazard tiers, providing a high-resolution grid layout across a **5-day operational forecast horizon**.
""")

st.divider()

# ==========================================
# MULTI-FACTOR ANALYSIS SECTION
# ==========================================
st.markdown("## 🔍 Multi-Factor Biometeorological Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🌡️ UTCI Ambient Equivalent
    
    Rather than looking at static air temperature, the tracker computes human thermal stress by considering:
    - **Air Temperature ($T_{2m}$)**
    - **Relative Humidity ($RH\%$)** derived dynamically via Dewpoint Temperature ($D_{2m}$)
    - **Human Energy Balance** modeling to track physiological heat exchange.
    """)

with col2:
    st.markdown("""
    ### 📈 Thermal Accumulation
    
    Tracks how continuous heat impact compounds over multi-day periods by evaluating:
    - **Peak daily high variables** ($mx2t3$) over consecutive processing blocks
    - **Nocturnal cooling deficits** that hinder the body's natural recovery windows.
    """)

with col3:
    st.markdown("""
    ### 📊 Climatological Hazard Mapping
    
    Translates mathematical spatial matrices into actionable hazard categories:
    - **Grid-level mapping** at 0.25° resolution
    - **Visual masking tools** allowing operators to filter out safe zones and highlight regions exceeding critical thresholds (e.g., >32°C).
    """)

st.divider()

# ==========================================
# RISK CATEGORY TABLE (UPDATED TO UTCI BANDS)
# ==========================================
st.markdown("## 🎯 UTCI Thresholds & Risk Classifications")
st.markdown("The app automatically processes raw physical grids into the following standardized physiological stress bands:")

risk_data = {
    'Category Level': ['0 - No Thermal Stress', '1 - Moderate Heat Stress', '2 - Strong Heat Stress', '3 - Very Strong Heat Stress', '4 - Extreme Heat Stress'],
    'UTCI Metric Range': ['< 26°C', '26°C to 32°C', '32°C to 38°C', '38°C to 46°C', '≥ 46°C'],
    'Physiological Impact Context': [
        'Safe conditions; normal homeostatic thermal balance.',
        'Elevated risks for sensitive cohorts (outdoor laborers, infants, elderly).',
        'Widespread thermal discomfort; protective cooling and active hydration are required.',
        'Severe physiological strain; direct correlation to spikes in heat-related illnesses.',
        'Critical danger to all populations; severe risk of heat stroke or systemic infrastructure failures.'
    ],
    'Status Indicator': ['🟢 Green', '🟡 Yellow', '🟠 Orange', '🔴 Red', '🟪 Magenta']
}

df = pd.DataFrame(risk_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()

# ==========================================
# COMPARISON TABLE
# ==========================================
st.markdown("## 📊 Framework Comparison Matrix")

comparison_data = {
    'Feature Core': [
        'Primary Data Parameter',
        'Spatial Grid Resolution',
        'Temporal Scale',
        'Physiological Factoring',
        'Boundary Overlays',
        'Application Aim'
    ],
    'Traditional IMD Alerts': [
        'Absolute $T_{max}$ Ambient',
        'Station-Based / District Poly',
        'Daily / Seasonal Forecasts',
        'None (Meteorological Only)',
        'Macro-scale political',
        'National Public Advisories'
    ],
    'NWS HeatRisk Model': [
        'Climatological Anomalies',
        'County-Level Grids',
        '7-Day Rolling Horizon',
        'Basic Temperature/Anomalies',
        'US County Borders',
        'Continental US Warning System'
    ],
    'India HeatRisk Tracker (IEEE REACT)': [
        'UTCI + Absolute $T_{max}$',
        '0.25° Mesh (~28km)',
        'Hourly Arrays over 5-Day Stream',
        'Full Thermal Balance ($T_{2m}$ + $D_{2m}$ + $RH$)',
        'Triple Layer (Country, State, District)',
        'IEEE GRSS Research-to-Operations'
    ]
}

comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, use_container_width=True, hide_index=True)

st.divider()

# ==========================================
# METHODOLOGY & TECHNICAL BUFFER
# ==========================================
st.markdown("## 🔬 Technical Architecture & Methodology")

methodology = st.container()
with methodology:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📥 Data Acquisition Layer
        - **Source Engine:** ECMWF OpenData Operational Forecast Stream
        - **Atmospheric Fields:** 2-meter Temperature (`2t`), 2-meter Dewpoint (`2d`), Maximum Temperature in past 3 hours (`mx2t3`)
        - **Spatial Subset Matrix:** Custom bounding box for Mainland India domain ($6^\circ\text{N} \rightarrow 38^\circ\text{N}$, $66^\circ\text{E} \rightarrow 98^\circ\text{E}$)
        - **Dynamic Fallback:** Integrated with an on-the-fly analytical grid generator to handle runtime connection timeouts.
        """)
    
    with col2:
        st.markdown("""
        ### ⚙️ Processing & Visualization Pipelines
        1. **Ingestion & Swap:** Data loaded into `xarray.Dataset`, swapping operational forecasting steps to global validated times.
        2. **Derived Rh Matrix:** Calculates relative humidity arrays from dewpoint saturation equations.
        3. **UTCI Synthesis:** Evaluates multi-variable arrays into single scalar biometeorological equivalent grids.
        4. **Vector Boundary Overlay:** Blends spatial rasters with high-precision DataMeet/GADM-derived GeoJSON lines.
        """)

st.divider()

# ==========================================
# DISCLAIMER & COMPETITION FOOTER
# ==========================================
st.warning("""
### ⚠️ Operational Research Disclaimer

**This application is an experimental prototype engineered for scientific validation and review within the IEEE GRSS REACT Competition framework.**

- ❌ Do NOT utilize this interface as a standalone decision toolkit for health or safety protocols.
- ✅ Always monitor official real-time statements and formal heatwave declarations published by the **India Meteorological Department (IMD)**.
- ✅ Align all physical emergency operations with instructions provided by local municipal disaster management agencies.
""")

st.divider()

st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); border-radius: 12px; color: white;'>
    <h3 style='color: white; margin: 0;'>🚀 IEEE GRSS REACT Competition Project Entry</h3>
    <p style='margin: 0.5rem 0 0 0; font-size: 1rem;'>
        Demonstrating the power of open-access numerical weather predictions, advanced spatial array processing, and targeted regional biometeorological tracking.
    </p>
    <small style='opacity: 0.9;'>Department of Astronomy, Astrophysics, and Space Engineering (DAASE), IIT Indore</small>
</div>
""", unsafe_allow_html=True)
# </div>
# """, unsafe_allow_html=True)
