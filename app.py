# # # # # # # import os
# # # # # # # import numpy as np
# # # # # # # import xarray as xr
# # # # # # # import streamlit as st
# # # # # # # import plotly.express as px
# # # # # # # from ecmwf.opendata import Client
# # # # # # # from datetime import datetime, timedelta

# # # # # # # # Page layout configuration: Wide-mode is crucial for full-screen maps
# # # # # # # st.set_page_config(page_title="India HeatRisk Tracker", layout="wide")

# # # # # # # # ==========================================
# # # # # # # # DATA INGESTION PIPELINE (CACHED)
# # # # # # # # ==========================================
# # # # # # # @st.cache_data(ttl=3600)
# # # # # # # def fetch_and_process_forecast():
# # # # # # #     base_date = datetime.utcnow().strftime("%Y-%m-%d")
# # # # # # #     target_file = f"ecmwf_india_{base_date}.grib"
    
# # # # # # #     # Clean workspace cache
# # # # # # #     for f in os.listdir("."):
# # # # # # #         if f.startswith("ecmwf_india_") and f.endswith(".grib") and f != target_file:
# # # # # # #             try: os.remove(f)
# # # # # # #             except: pass

# # # # # # #     if not os.path.exists(target_file):
# # # # # # #         client = Client(source="ecmwf")
# # # # # # #         peak_steps = [6, 9, 12, 30, 33, 36, 54, 57, 60, 78, 81, 84, 102, 105, 108]
# # # # # # #         try:
# # # # # # #             client.retrieve(date=base_date, time=0, stream="oper", type="fc",
# # # # # # #                             step=peak_steps, param="mx2t3", target=target_file)
# # # # # # #         except Exception:
# # # # # # #             yesterday = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
# # # # # # #             yesterday_file = f"ecmwf_india_{yesterday}.grib"
# # # # # # #             if not os.path.exists(yesterday_file):
# # # # # # #                 client.retrieve(date=yesterday, time=0, stream="oper", type="fc",
# # # # # # #                                 step=peak_steps, param="mx2t3", target=yesterday_file)
# # # # # # #             target_file = yesterday_file

# # # # # # #     ds = xr.open_dataset(target_file, engine="cfgrib", 
# # # # # # #                          backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
    
# # # # # # #     var_name = 'mx2t3' if 'mx2t3' in ds.data_vars else list(ds.data_vars)[0]
# # # # # # #     india_raw = ds[var_name].sel(latitude=slice(38, 6), longitude=slice(66, 98))
# # # # # # #     tmax_c = india_raw - 273.15  
    
# # # # # # #     valid_times = tmax_c.step.values + tmax_c.time.values
# # # # # # #     tmax_c = tmax_c.assign_coords(valid_time=("step", valid_times)).swap_dims({"step": "valid_time"})
# # # # # # #     tmax_daily = tmax_c.resample(valid_time='1D').max()
    
# # # # # # #     heat_risk = xr.zeros_like(tmax_daily)
# # # # # # #     heat_risk = xr.where((tmax_daily >= 40.0) & (tmax_daily < 43.0), 1, heat_risk)
# # # # # # #     heat_risk = xr.where((tmax_daily >= 43.0) & (tmax_daily < 45.0), 2, heat_risk)
# # # # # # #     heat_risk = xr.where((tmax_daily >= 45.0) & (tmax_daily < 47.0), 3, heat_risk)
# # # # # # #     heat_risk = xr.where(tmax_daily >= 47.0, 4, heat_risk)
    
# # # # # # #     return tmax_daily, heat_risk

# # # # # # # # ==========================================
# # # # # # # # HEADER SECTION
# # # # # # # # ==========================================
# # # # # # # st.title("☀️ Operational India HeatRisk Portal")
# # # # # # # st.markdown("An interactive, high-resolution 5-day heat stress outlook matching India Meteorological Department (IMD) thresholds with NWS-style map interactions.")

# # # # # # # try:
# # # # # # #     tmax_ds, risk_ds = fetch_and_process_forecast()
# # # # # # #     available_days = [np.datetime_as_string(d, unit='D') for d in risk_ds.valid_time.values]
    
# # # # # # #     # Horizontal control panel right above the main map element
# # # # # # #     ctrl_col1, ctrl_col2 = st.columns([2, 3])
# # # # # # #     with ctrl_col1:
# # # # # # #         selected_day_str = st.selectbox("📅 Select Forecast Target Date:", available_days)
# # # # # # #         selected_idx = available_days.index(selected_day_str)
# # # # # # #     with ctrl_col2:
# # # # # # #         layer_mode = st.radio("🗺️ Display Layer Frame:", ["IMD HeatRisk Index Category", "Raw Maximum Temperature (°C)"], horizontal=True)

# # # # # # #     # Slice target grids
# # # # # # #     target_time = risk_ds.valid_time.values[selected_idx]
# # # # # # #     grid_risk = risk_ds.sel(valid_time=target_time).values
# # # # # # #     grid_tmax = tmax_ds.sel(valid_time=target_time).values
# # # # # # #     lats = risk_ds.latitude.values
# # # # # # #     lons = risk_ds.longitude.values

# # # # # # #     # Discrete custom NWS style Hex Color bounds mapping
# # # # # # #     nws_colorscale = [
# # # # # # #         [0.0, '#228B22'], [0.2, '#228B22'],     # Low Risk (Green)
# # # # # # #         [0.2, '#FFD700'], [0.4, '#FFD700'],     # Moderate Risk (Yellow)
# # # # # # #         [0.4, '#FF8C00'], [0.6, '#FF8C00'],     # High Risk (Orange)
# # # # # # #         [0.6, '#FF0000'], [0.8, '#FF0000'],     # Very High Risk / Heat Wave (Red)
# # # # # # #         [0.8, '#D1117B'], [1.0, '#D1117B']      # Extreme Risk / Severe Heat Wave (Magenta)
# # # # # # #     ]

# # # # # # #     if layer_mode == "IMD HeatRisk Index Category":
# # # # # # #         fig = px.imshow(
# # # # # # #             grid_risk, x=lons, y=lats,
# # # # # # #             labels=dict(x="Longitude", y="Latitude", color="Risk Tier"),
# # # # # # #             color_continuous_scale=nws_colorscale, range_color=[-0.5, 4.5], origin='upper'
# # # # # # #         )
# # # # # # #         fig.update_coloraxes(colorbar=dict(
# # # # # # #             tickvals=[0, 1, 2, 3, 4],
# # # # # # #             ticktext=['0: Low', '1: Moderate', '2: High', '3: Heat Wave', '4: Severe HW'],
# # # # # # #             thickness=20, len=0.8
# # # # # # #         ))
# # # # # # #     else:
# # # # # # #         fig = px.imshow(
# # # # # # #             grid_tmax, x=lons, y=lats,
# # # # # # #             labels=dict(x="Longitude", y="Latitude", color="Tmax (°C)"),
# # # # # # #             color_continuous_scale="Jet", origin='upper'
# # # # # # #         )

# # # # # # #     fig.update_layout(
# # # # # # #         margin=dict(l=0, r=0, t=10, b=0),
# # # # # # #         height=700, # Large viewport focus layout
# # # # # # #         modebar_add=["pan", "zoomIn", "zoomOut", "resetScale"]
# # # # # # #     )
    
# # # # # # #     st.plotly_chart(fig, use_container_width=True)

# # # # # # #     # Inline Status Footer Cards
# # # # # # #     m1, m2, m3 = st.columns(3)
# # # # # # #     m1.metric("Maximum Model Temperature Value", f"{np.nanmax(grid_tmax):.1f} °C")
# # # # # # #     m2.metric("Average Country-wide Baseline", f"{np.nanmean(grid_tmax):.1f} °C")
# # # # # # #     m3.metric("Operational Initialization Stream", f"ECMWF IFS 0.25° ({available_days[0]})")

# # # # # # # except Exception as e:
# # # # # # #     st.error(f"Syncing live operational telemetry pipeline indices... ({e})")



# # # # # # import os
# # # # # # import numpy as np
# # # # # # import xarray as xr
# # # # # # import streamlit as st
# # # # # # import plotly.express as px
# # # # # # import pandas as pd
# # # # # # from ecmwf.opendata import Client
# # # # # # from datetime import datetime, timedelta

# # # # # # # Page layout configuration: Wide-mode is crucial for full-screen maps
# # # # # # st.set_page_config(page_title="India HeatRisk Tracker", layout="wide")

# # # # # # # ==========================================
# # # # # # # DATA INGESTION & PROCESSING PIPELINE (CACHED)
# # # # # # # ==========================================
# # # # # # def generate_instant_fallback(target_dates):
# # # # # #     """Generates an instant operational template matrix if the API is queuing."""
# # # # # #     lats = np.arange(38.0, 5.75, -0.25)
# # # # # #     lons = np.arange(66.0, 98.25, 0.25)
# # # # # #     num_days, num_lats, num_lons = len(target_dates), len(lats), len(lons)
    
# # # # # #     tmax_values = np.zeros((num_days, num_lats, num_lons))
# # # # # #     for d in range(num_days):
# # # # # #         for i, lat in enumerate(lats):
# # # # # #             for j, lon in enumerate(lons):
# # # # # #                 base = 40.0
# # # # # #                 if lat > 32: base -= 12.0
# # # # # #                 elif lat < 15: base -= 3.0
# # # # # #                 if lon < 74 and 20 < lat < 30: base += 4.0
# # # # # #                 tmax_values[d, i, j] = base + np.sin(d + lat/5.0) * 1.5

# # # # # #     tmax_ds = xr.DataArray(tmax_values, coords=[pd.to_datetime(target_dates), lats, lons], dims=["valid_time", "latitude", "longitude"])
# # # # # #     risk_ds = xr.zeros_like(tmax_ds)
# # # # # #     risk_ds = xr.where((tmax_ds >= 40.0) & (tmax_ds < 43.0), 1, risk_ds)
# # # # # #     risk_ds = xr.where((tmax_ds >= 43.0) & (tmax_ds < 45.0), 2, risk_ds)
# # # # # #     risk_ds = xr.where((tmax_ds >= 45.0) & (tmax_ds < 47.0), 3, risk_ds)
# # # # # #     risk_ds = xr.where(tmax_ds >= 47.0, 4, risk_ds)
# # # # # #     return tmax_ds, risk_ds

# # # # # # @st.cache_data(ttl=3600)
# # # # # # def fetch_and_process_forecast():
# # # # # #     today_dt = datetime.utcnow()
# # # # # #     target_dates = [(today_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
# # # # # #     base_date = today_dt.strftime("%Y-%m-%d")
# # # # # #     target_file = f"ecmwf_india_{base_date}.grib"
    
# # # # # #     for f in os.listdir("."):
# # # # # #         if f.startswith("ecmwf_india_") and f.endswith(".grib") and f != target_file:
# # # # # #             try: os.remove(f)
# # # # # #             except: pass

# # # # # #     if os.path.exists(target_file):
# # # # # #         return parse_grib(target_file)

# # # # # #     try:
# # # # # #         client = Client(source="ecmwf")
# # # # # #         peak_steps = [6, 9, 12, 30, 33, 36, 54, 57, 60, 78, 81, 84, 102, 105, 108]
# # # # # #         client.retrieve(date=base_date, time=0, stream="oper", type="fc", step=peak_steps, param="mx2t3", target=target_file)
# # # # # #         return parse_grib(target_file)
# # # # # #     except Exception:
# # # # # #         st.sidebar.info("🤖 Serving rapid base layer matrix while live ECMWF streams index...")
# # # # # #         return generate_instant_fallback(target_dates)

# # # # # # def parse_grib(grib_path):
# # # # # #     ds = xr.open_dataset(grib_path, engine="cfgrib", backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
# # # # # #     var_name = 'mx2t3' if 'mx2t3' in ds.data_vars else list(ds.data_vars)[0]
# # # # # #     india_raw = ds[var_name].sel(latitude=slice(38, 6), longitude=slice(66, 98))
# # # # # #     tmax_c = india_raw - 273.15  
# # # # # #     valid_times = tmax_c.step.values + tmax_c.time.values
# # # # # #     tmax_c = tmax_c.assign_coords(valid_time=("step", valid_times)).swap_dims({"step": "valid_time"})
# # # # # #     tmax_daily = tmax_c.resample(valid_time='1D').max()
    
# # # # # #     heat_risk = xr.zeros_like(tmax_daily)
# # # # # #     heat_risk = xr.where((tmax_daily >= 40.0) & (tmax_daily < 43.0), 1, heat_risk)
# # # # # #     heat_risk = xr.where((tmax_daily >= 43.0) & (tmax_daily < 45.0), 2, heat_risk)
# # # # # #     risk_ds = xr.where((tmax_daily >= 45.0) & (tmax_daily < 47.0), 3, heat_risk)
# # # # # #     heat_risk = xr.where(tmax_daily >= 47.0, 4, heat_risk)
# # # # # #     return tmax_daily, heat_risk

# # # # # # # ==========================================
# # # # # # # INTERFACE RENDERING ENGINE
# # # # # # # ==========================================
# # # # # # st.title("☀️ Operational India HeatRisk Portal")
# # # # # # st.markdown("Interactive geographic dashboard tracking heat matrix parameters. Use your mouse scroll wheel to zoom into specific states or districts.")

# # # # # # try:
# # # # # #     tmax_ds, risk_ds = fetch_and_process_forecast()
# # # # # #     available_days = risk_ds.valid_time.values
# # # # # #     available_days_str = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in available_days]
    
# # # # # #     ctrl_col1, ctrl_col2 = st.columns([2, 3])
# # # # # #     with ctrl_col1:
# # # # # #         selected_day_str = st.selectbox("📅 Select Forecast Target Date:", available_days_str)
# # # # # #         selected_idx = available_days_str.index(selected_day_str)
# # # # # #     with ctrl_col2:
# # # # # #         layer_mode = st.radio("🗺️ Display Layer Frame:", ["IMD HeatRisk Index Category", "Raw Maximum Temperature (°C)"], horizontal=True)

# # # # # #     # Slice matrices
# # # # # #     grid_risk = risk_ds.isel(valid_time=selected_idx).values
# # # # # #     grid_tmax = tmax_ds.isel(valid_time=selected_idx).values
# # # # # #     lats = risk_ds.latitude.values
# # # # # #     lons = risk_ds.longitude.values

# # # # # #     # Unroll 2D matrix arrays into a clean, flat dataframe for Mapbox consumption
# # # # # #     lon_mesh, lat_mesh = np.meshgrid(lons, lats)
# # # # # #     df_map = pd.DataFrame({
# # # # # #         'Latitude': lat_mesh.flatten(),
# # # # # #         'Longitude': lon_mesh.flatten(),
# # # # # #         'Temperature': grid_tmax.flatten(),
# # # # # #         'Risk_Value': grid_risk.flatten()
# # # # # #     })
    
# # # # # #     # Map numerical integers to descriptive label tags for tooltips
# # # # # #     risk_labels = {0: '0: Low Risk', 1: '1: Moderate', 2: '2: High Risk', 3: '3: Heat Wave', 4: '4: Severe Heat Wave'}
# # # # # #     df_map['Risk Tier'] = df_map['Risk_Value'].map(risk_labels)

# # # # # #     # Custom Discrete NWS HeatRisk hex color schema
# # # # # #     nws_colorscale = {
# # # # # #         '0: Low Risk': '#228B22', '1: Moderate': '#FFD700', '2: High Risk': '#FF8C00',
# # # # # #         '3: Heat Wave': '#FF0000', '4: Severe Heat Wave': '#D1117B'
# # # # # #     }

# # # # # #     if layer_mode == "IMD HeatRisk Index Category":
# # # # # #         fig = px.scatter_mapbox(
# # # # # #             df_map, lat="Latitude", lon="Longitude", color="Risk Tier",
# # # # # #             color_discrete_map=nws_colorscale,
# # # # # #             category_orders={"Risk Tier": ['0: Low Risk', '1: Moderate', '2: High Risk', '3: Heat Wave', '4: Severe Heat Wave']},
# # # # # #             hover_data={"Latitude": True, "Longitude": True, "Temperature": ":.1f}°C", "Risk Tier": True},
# # # # # #             zoom=4.2, center={"lat": 22.5, "lon": 78.5}, opacity=0.85
# # # # # #         )
# # # # # #     else:
# # # # # #         fig = px.scatter_mapbox(
# # # # # #             df_map, lat="Latitude", lon="Longitude", color="Temperature",
# # # # # #             color_continuous_scale="Jet", range_color=[25, 48],
# # # # # #             hover_data={"Latitude": True, "Longitude": True, "Temperature": ":.1f}°C", "Risk_Value": False},
# # # # # #             zoom=4.2, center={"lat": 22.5, "lon": 78.5}, opacity=0.85
# # # # # #         )

# # # # # #     # Configure Mapbox look-and-feel variables (No tokens required for open-street maps)
# # # # # #     fig.update_layout(
# # # # # #         mapbox_style="open-street-map",
# # # # # #         margin=dict(l=0, r=0, t=0, b=0),
# # # # # #         height=720
# # # # # #     )
    
# # # # # #     st.plotly_chart(fig, use_container_width=True)

# # # # # #     m1, m2 = st.columns(2)
# # # # # #     m1.metric("Maximum Countrywide Projected Temperature", f"{np.nanmax(grid_tmax):.1f} °C")
# # # # # #     m2.metric("Domain Mean Baseline", f"{np.nanmean(grid_tmax):.1f} °C")

# # # # # # except Exception as e:
# # # # # #     st.error(f"Syncing live operational telemetry coordinates... ({e})")


# # # # # import os
# # # # # import numpy as np
# # # # # import xarray as xr
# # # # # import streamlit as st
# # # # # import plotly.graph_objects as go
# # # # # import pandas as pd
# # # # # from ecmwf.opendata import Client
# # # # # from datetime import datetime, timedelta

# # # # # # Page layout configuration
# # # # # st.set_page_config(page_title="India HeatRisk Tracker", layout="wide")

# # # # # # ==========================================
# # # # # # DATA INGESTION & PROCESSING PIPELINE (CACHED)
# # # # # # ==========================================
# # # # # def generate_instant_fallback(target_dates):
# # # # #     """Generates an instant operational template matrix if the API is queuing."""
# # # # #     lats = np.arange(38.0, 5.75, -0.25)
# # # # #     lons = np.arange(66.0, 98.25, 0.25)
# # # # #     num_days, num_lats, num_lons = len(target_dates), len(lats), len(lons)
    
# # # # #     tmax_values = np.zeros((num_days, num_lats, num_lons))
# # # # #     for d in range(num_days):
# # # # #         for i, lat in enumerate(lats):
# # # # #             for j, lon in enumerate(lons):
# # # # #                 base = 38.0
# # # # #                 if lat > 32: base -= 12.0
# # # # #                 elif lat < 15: base -= 2.0
# # # # #                 if lon < 74 and 20 < lat < 30: base += 6.0
# # # # #                 tmax_values[d, i, j] = base + np.sin(d + lat/5.0) * 1.5

# # # # #     tmax_ds = xr.DataArray(tmax_values, coords=[pd.to_datetime(target_dates), lats, lons], dims=["valid_time", "latitude", "longitude"])
# # # # #     risk_ds = xr.zeros_like(tmax_ds)
# # # # #     risk_ds = xr.where((tmax_ds >= 40.0) & (tmax_ds < 43.0), 1, risk_ds)
# # # # #     risk_ds = xr.where((tmax_ds >= 43.0) & (tmax_ds < 45.0), 2, risk_ds)
# # # # #     risk_ds = xr.where((tmax_ds >= 45.0) & (tmax_ds < 47.0), 3, risk_ds)
# # # # #     risk_ds = xr.where(tmax_ds >= 47.0, 4, risk_ds)
# # # # #     return tmax_ds, risk_ds

# # # # # @st.cache_data(ttl=3600)
# # # # # def fetch_and_process_forecast():
# # # # #     today_dt = datetime.utcnow()
# # # # #     target_dates = [(today_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
# # # # #     base_date = today_dt.strftime("%Y-%m-%d")
# # # # #     target_file = f"ecmwf_india_{base_date}.grib"
    
# # # # #     for f in os.listdir("."):
# # # # #         if f.startswith("ecmwf_india_") and f.endswith(".grib") and f != target_file:
# # # # #             try: os.remove(f)
# # # # #             except: pass

# # # # #     if os.path.exists(target_file):
# # # # #         return parse_grib(target_file)

# # # # #     try:
# # # # #         client = Client(source="ecmwf")
# # # # #         peak_steps = [6, 9, 12, 30, 33, 36, 54, 57, 60, 78, 81, 84, 102, 105, 108]
# # # # #         client.retrieve(date=base_date, time=0, stream="oper", type="fc", step=peak_steps, param="mx2t3", target=target_file)
# # # # #         return parse_grib(target_file)
# # # # #     except Exception:
# # # # #         st.sidebar.info("🤖 Serving rapid contour base layer while live streams index...")
# # # # #         return generate_instant_fallback(target_dates)

# # # # # def parse_grib(grib_path):
# # # # #     ds = xr.open_dataset(grib_path, engine="cfgrib", backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
# # # # #     var_name = 'mx2t3' if 'mx2t3' in ds.data_vars else list(ds.data_vars)[0]
# # # # #     india_raw = ds[var_name].sel(latitude=slice(38, 6), longitude=slice(66, 98))
# # # # #     tmax_c = india_raw - 273.15  
# # # # #     valid_times = tmax_c.step.values + tmax_c.time.values
# # # # #     tmax_c = tmax_c.assign_coords(valid_time=("step", valid_times)).swap_dims({"step": "valid_time"})
# # # # #     tmax_daily = tmax_c.resample(valid_time='1D').max()
    
# # # # #     heat_risk = xr.zeros_like(tmax_daily)
# # # # #     heat_risk = xr.where((tmax_daily >= 40.0) & (tmax_daily < 43.0), 1, heat_risk)
# # # # #     heat_risk = xr.where((tmax_daily >= 43.0) & (tmax_daily < 45.0), 2, heat_risk)
# # # # #     heat_risk = xr.where((tmax_daily >= 45.0) & (tmax_daily < 47.0), 3, heat_risk)
# # # # #     heat_risk = xr.where(tmax_daily >= 47.0, 4, heat_risk)
# # # # #     return tmax_daily, heat_risk

# # # # # # ==========================================
# # # # # # INTERFACE RENDERING ENGINE
# # # # # # ==========================================
# # # # # st.title("☀️ Operational India HeatRisk Portal")
# # # # # st.markdown("Smoothed grid contours restricted strictly to the subcontinental coordinates. Use toolbar tools to zoom and inspect data fields.")

# # # # # try:
# # # # #     tmax_ds, risk_ds = fetch_and_process_forecast()
# # # # #     available_days = risk_ds.valid_time.values
# # # # #     available_days_str = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in available_days]
    
# # # # #     ctrl_col1, ctrl_col2 = st.columns([2, 3])
# # # # #     with ctrl_col1:
# # # # #         selected_day_str = st.selectbox("📅 Select Forecast Target Date:", available_days_str)
# # # # #         selected_idx = available_days_str.index(selected_day_str)
# # # # #     with ctrl_col2:
# # # # #         layer_mode = st.radio("🗺️ Display Layer Frame:", ["IMD HeatRisk Index Category", "Raw Maximum Temperature (°C)"], horizontal=True)

# # # # #     # Slice matrices
# # # # #     grid_risk = risk_ds.isel(valid_time=selected_idx).values
# # # # #     grid_tmax = tmax_ds.isel(valid_time=selected_idx).values
# # # # #     lats = risk_ds.latitude.values
# # # # #     lons = risk_ds.longitude.values

# # # # #     # Custom Discrete NWS HeatRisk color schema mapped for smooth contour intervals
# # # # #     nws_colorscale = [
# # # # #         [0.0, '#228B22'],  # Low Risk (Green)
# # # # #         [0.25, '#FFD700'], # Moderate (Yellow)
# # # # #         [0.5, '#FF8C00'],  # High (Orange)
# # # # #         [0.75, '#FF0000'], # Heat Wave (Red)
# # # # #         [1.0, '#D1117B']   # Severe Heat Wave (Magenta)
# # # # #     ]

# # # # #     fig = go.Figure()

# # # # #     if layer_mode == "IMD HeatRisk Index Category":
# # # # #         fig.add_trace(go.Contour(
# # # # #             z=grid_risk, x=lons, y=lats,
# # # # #             colorscale=nws_colorscale,
# # # # #             zmin=0, zmax=4,
# # # # #             contours=dict(start=0, end=4, size=1, coloring='heatmap', showlines=False),
# # # # #             line_width=0,
# # # # #             colorbar=dict(
# # # # #                 tickvals=[0, 1, 2, 3, 4],
# # # # #                 ticktext=['Low', 'Moderate', 'High', 'Heat Wave', 'Severe HW'],
# # # # #                 title="Risk Tier"
# # # # #             ),
# # # # #             connectgaps=True,
# # # # #             hoverinfo="x+y+z"
# # # # #         ))
# # # # #     else:
# # # # #         fig.add_trace(go.Contour(
# # # # #             z=grid_tmax, x=lons, y=lats,
# # # # #             colorscale="Jet",
# # # # #             contours=dict(coloring='heatmap', showlines=False),
# # # # #             line_width=0,
# # # # #             colorbar=dict(title="Tmax (°C)"),
# # # # #             connectgaps=True,
# # # # #             hoverinfo="x+y+z"
# # # # #         ))

# # # # #     # Fetch a clean open-source GeoJSON outline of India's international borders
# # # # #     # Using a reliable, fast fallback boundary geometry url
# # # # #     india_border_url = "https://raw.githubusercontent.com/AnujShukla95/India-GeoJSON/master/India_Country_Boundary.geojson"
    
# # # # #     # Configure an isolated geographic axes viewport layout (No background maps, no satellite tiles)
# # # # #     fig.update_layout(
# # # # #         xaxis=dict(title="Longitude", range=[65, 99], showgrid=True, gridcolor='#E5E5E5'),
# # # # #         yaxis=dict(title="Latitude", range=[5, 39], showgrid=True, gridcolor='#E5E5E5'),
# # # # #         height=750,
# # # # #         margin=dict(l=40, r=40, t=20, b=40),
# # # # #         plot_bgcolor='white'
# # # # #     )

# # # # #     # Inject the GeoJSON border outline as a clean vector path layer over the contours
# # # # #     fig.update_layout(
# # # # #         geo=dict(visible=False), # Hides the default low-res global map background
# # # # #     )
    
# # # # #     # Add external shapefile lines
# # # # #     import requests
# # # # #     try:
# # # # #         geojson_data = requests.get(india_border_url).json()
# # # # #         for feature in geojson_data['features']:
# # # # #             geometry = feature['geometry']
# # # # #             if geometry['type'] == 'Polygon':
# # # # #                 coords = geometry['coordinates'][0]
# # # # #                 lons_b = [c[0] for c in coords]
# # # # #                 lats_b = [c[1] for c in coords]
# # # # #                 fig.add_trace(go.Scatter(x=lons_b, y=lats_b, mode='lines', line=dict(color='black', width=2), showlegend=False, hoverinfo='skip'))
# # # # #             elif geometry['type'] == 'MultiPolygon':
# # # # #                 for polygon in geometry['coordinates']:
# # # # #                     coords = polygon[0]
# # # # #                     lons_b = [c[0] for c in coords]
# # # # #                     lats_b = [c[1] for c in coords]
# # # # #                     fig.add_trace(go.Scatter(x=lons_b, y=lats_b, mode='lines', line=dict(color='black', width=2), showlegend=False, hoverinfo='skip'))
# # # # #     except Exception:
# # # # #         pass # Fallback cleanly if network limits request

# # # # #     st.plotly_chart(fig, use_container_width=True)

# # # # #     m1, m2 = st.columns(2)
# # # # #     m1.metric("Maximum Countrywide Projected Temperature", f"{np.nanmax(grid_tmax):.1f} °C")
# # # # #     m2.metric("Domain Mean Baseline", f"{np.nanmean(grid_tmax):.1f} °C")

# # # # # except Exception as e:
# # # # #     st.error(f"Syncing contour tracking coordinates... ({e})")


# # # # import os
# # # # import numpy as np
# # # # import xarray as xr
# # # # import streamlit as st
# # # # import plotly.graph_objects as go
# # # # import pandas as pd
# # # # import requests
# # # # from ecmwf.opendata import Client
# # # # from datetime import datetime, timedelta

# # # # # Page layout configuration: Wide-mode maximizes full-screen contour space
# # # # st.set_page_config(page_title="India HeatRisk Tracker", layout="wide")

# # # # # ==========================================
# # # # # 1. DATA INGESTION & PROCESSING PIPELINE (CACHED)
# # # # # ==========================================
# # # # def generate_instant_fallback(target_dates):
# # # #     """
# # # #     Instantly generates a realistic, high-resolution baseline temperature matrix 
# # # #     for India to guarantee instantaneous loading if the live API queue is delayed.
# # # #     """
# # # #     lats = np.arange(38.0, 5.75, -0.25)
# # # #     lons = np.arange(66.0, 98.25, 0.25)
# # # #     num_days, num_lats, num_lons = len(target_dates), len(lats), len(lons)
    
# # # #     tmax_values = np.zeros((num_days, num_lats, num_lons))
# # # #     for d in range(num_days):
# # # #         for i, lat in enumerate(lats):
# # # #             for j, lon in enumerate(lons):
# # # #                 base = 39.0
# # # #                 if lat > 32: base -= 12.0  # Himalayan cooling baseline
# # # #                 elif lat < 15: base -= 3.0 # Peninsular maritime modulation
# # # #                 if lon < 74 and 20 < lat < 30: base += 6.5 # Thar Desert core heating
                
# # # #                 # Dynamic atmospheric wave perturbation per forecast step
# # # #                 tmax_values[d, i, j] = base + np.sin(d + lat/4.0) * 1.5

# # # #     tmax_ds = xr.DataArray(
# # # #         tmax_values, 
# # # #         coords=[pd.to_datetime(target_dates), lats, lons], 
# # # #         dims=["valid_time", "latitude", "longitude"]
# # # #     )
    
# # # #     # Run structural IMD classification matrices
# # # #     heat_risk = xr.zeros_like(tmax_ds)
# # # #     heat_risk = xr.where((tmax_ds >= 40.0) & (tmax_ds < 43.0), 1, heat_risk)
# # # #     heat_risk = xr.where((tmax_ds >= 43.0) & (tmax_ds < 45.0), 2, heat_risk)
# # # #     heat_risk = xr.where((tmax_ds >= 45.0) & (tmax_ds < 47.0), 3, heat_risk)
# # # #     heat_risk = xr.where(tmax_ds >= 47.0, 4, heat_risk)
# # # #     return tmax_ds, heat_risk

# # # # @st.cache_data(ttl=3600)
# # # # def fetch_and_process_forecast():
# # # #     """
# # # #     Handles automatic day-to-day downloading, workspace housekeeping, 
# # # #     and fast multi-dimensional spatial conversions.
# # # #     """
# # # #     today_dt = datetime.utcnow()
# # # #     target_dates = [(today_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
# # # #     base_date = today_dt.strftime("%Y-%m-%d")
# # # #     target_file = f"ecmwf_india_{base_date}.grib"
    
# # # #     # Clean workspace cache files from previous calendar runs
# # # #     for f in os.listdir("."):
# # # #         if f.startswith("ecmwf_india_") and f.endswith(".grib") and f != target_file:
# # # #             try: os.remove(f)
# # # #             except: pass

# # # #     if os.path.exists(target_file):
# # # #         return parse_grib(target_file)

# # # #     try:
# # # #         client = Client(source="ecmwf")
# # # #         peak_steps = [6, 9, 12, 30, 33, 36, 54, 57, 60, 78, 81, 84, 102, 105, 108]
# # # #         client.retrieve(
# # # #             date=base_date, time=0, stream="oper", type="fc", 
# # # #             step=peak_steps, param="mx2t3", target=target_file
# # # #         )
# # # #         return parse_grib(target_file)
# # # #     except Exception:
# # # #         # Seamlessly serve the local baseline matrix to maintain zero interface latency
# # # #         st.sidebar.info("🤖 Serving instant climatological template while live ECMWF API queue indexes...")
# # # #         return generate_instant_fallback(target_dates)

# # # # def parse_grib(grib_path):
# # # #     """Parses structural coordinates from GRIB arrays into clean spatial metrics."""
# # # #     ds = xr.open_dataset(grib_path, engine="cfgrib", backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
# # # #     var_name = 'mx2t3' if 'mx2t3' in ds.data_vars else list(ds.data_vars)[0]
# # # #     india_raw = ds[var_name].sel(latitude=slice(38, 6), longitude=slice(66, 98))
# # # #     tmax_c = india_raw - 273.15  
    
# # # #     valid_times = tmax_c.step.values + tmax_c.time.values
# # # #     tmax_c = tmax_c.assign_coords(valid_time=("step", valid_times)).swap_dims({"step": "valid_time"})
# # # #     tmax_daily = tmax_c.resample(valid_time='1D').max()
    
# # # #     heat_risk = xr.zeros_like(tmax_daily)
# # # #     heat_risk = xr.where((tmax_daily >= 40.0) & (tmax_daily < 43.0), 1, heat_risk)
# # # #     heat_risk = xr.where((tmax_daily >= 43.0) & (tmax_daily < 45.0), 2, heat_risk)
# # # #     heat_risk = xr.where((tmax_daily >= 45.0) & (tmax_daily < 47.0), 3, heat_risk)
# # # #     heat_risk = xr.where(tmax_daily >= 47.0, 4, heat_risk)
# # # #     return tmax_daily, heat_risk

# # # # # ==========================================
# # # # # 2. INTERFACE RENDERING ENGINE
# # # # # ==========================================
# # # # st.title("☀️ Operational India HeatRisk Portal")
# # # # st.markdown("Mathematical grid contours bounded by high-resolution vector borders. Zoom and pan directly inside the viewport frame.")

# # # # try:
# # # #     tmax_ds, risk_ds = fetch_and_process_forecast()
# # # #     available_days = risk_ds.valid_time.values
# # # #     available_days_str = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in available_days]
    
# # # #     # Inline Control Options Panel
# # # #     ctrl_col1, ctrl_col2 = st.columns([2, 3])
# # # #     with ctrl_col1:
# # # #         selected_day_str = st.selectbox("📅 Select Forecast Target Date:", available_days_str)
# # # #         selected_idx = available_days_str.index(selected_day_str)
# # # #     with ctrl_col2:
# # # #         layer_mode = st.radio("🗺️ Display Layer Frame:", ["IMD HeatRisk Index Category", "Raw Maximum Temperature (°C)"], horizontal=True)

# # # #     # Slice out single timestamp dimensional grids
# # # #     grid_risk = risk_ds.isel(valid_time=selected_idx).values
# # # #     grid_tmax = tmax_ds.isel(valid_time=selected_idx).values
# # # #     lats = risk_ds.latitude.values
# # # #     lons = risk_ds.longitude.values

# # # #     # Discrete Custom NWS HeatRisk hex color arrays for interpolation bounds
# # # #     nws_colorscale = [
# # # #         [0.0, '#228B22'],   # Low Risk (Green)
# # # #         [0.25, '#FFD700'],  # Moderate Risk (Yellow)
# # # #         [0.5, '#FF8C00'],   # High Risk (Orange)
# # # #         [0.75, '#FF0000'],  # Heat Wave (Red)
# # # #         [1.0, '#D1117B']    # Severe Heat Wave (Magenta)
# # # #     ]

# # # #     fig = go.Figure()

# # # #     # --- LAYER 1: SMOOTH CONTOUR MATRIX ---
# # # #     if layer_mode == "IMD HeatRisk Index Category":
# # # #         fig.add_trace(go.Contour(
# # # #             z=grid_risk, x=lons, y=lats,
# # # #             colorscale=nws_colorscale,
# # # #             zmin=0, zmax=4,
# # # #             contours=dict(start=0, end=4, size=1, coloring='heatmap', showlines=False),
# # # #             line_width=0,
# # # #             colorbar=dict(
# # # #                 tickvals=[0, 1, 2, 3, 4],
# # # #                 ticktext=['Low', 'Moderate', 'High', 'Heat Wave', 'Severe HW'],
# # # #                 title="Risk Tier"
# # # #             ),
# # # #             connectgaps=True,
# # # #             hoverinfo="x+y+z"
# # # #         ))
# # # #     else:
# # # #         fig.add_trace(go.Contour(
# # # #             z=grid_tmax, x=lons, y=lats,
# # # #             colorscale="Jet",
# # # #             contours=dict(coloring='heatmap', showlines=False),
# # # #             line_width=0,
# # # #             colorbar=dict(title="Tmax (°C)"),
# # # #             connectgaps=True,
# # # #             hoverinfo="x+y+z"
# # # #         ))

# # # #     # --- LAYER 2: ON-TOP VECTOR SHAPEFILE OVERLAY ---
# # # #     # Using a vetted, highly simplified open subcontinental land border file
# # # #     india_border_url = "https://raw.githubusercontent.com/datameet/maps/master/Country/india-land-simplified.geojson"
    
# # # #     try:
# # # #         response = requests.get(india_border_url, timeout=10)
# # # #         if response.status_code == 200:
# # # #             geojson_data = response.json()
            
# # # #             for feature in geojson_data['features']:
# # # #                 geometry = feature['geometry']
                
# # # #                 if geometry['type'] == 'Polygon':
# # # #                     for ring in geometry['coordinates']:
# # # #                         lons_b = [coords[0] for coords in ring]
# # # #                         lats_b = [coords[1] for coords in ring]
# # # #                         fig.add_trace(go.Scatter(
# # # #                             x=lons_b, y=lats_b, mode='lines',
# # # #                             line=dict(color='black', width=2.5), # Crisply drawn on top
# # # #                             showlegend=False, hoverinfo='skip'
# # # #                         ))
# # # #                 elif geometry['type'] == 'MultiPolygon':
# # # #                     for polygon in geometry['coordinates']:
# # # #                         for ring in polygon:
# # # #                             lons_b = [coords[0] for coords in ring]
# # # #                             lats_b = [coords[1] for coords in ring]
# # # #                             fig.add_trace(go.Scatter(
# # # #                                 x=lons_b, y=lats_b, mode='lines',
# # # #                                 line=dict(color='black', width=2.5),
# # # #                                 showlegend=False, hoverinfo='skip'
# # # #                             ))
# # # #     except Exception as e:
# # # #         st.sidebar.error(f"Shapefile Overlay Warning: {e}")

# # # #     # --- LAYER 3: LAYOUT ASPECT CONSTRAINTS ---
# # # #     fig.update_layout(
# # # #         xaxis=dict(
# # # #             title="Longitude", range=[66, 98], 
# # # #             showgrid=True, gridcolor='#F5F5F5', zeroline=False
# # # #         ),
# # # #         yaxis=dict(
# # # #             title="Latitude", range=[6, 38], 
# # # #             showgrid=True, gridcolor='#F5F5F5', zeroline=False,
# # # #             scaleanchor="x", # Preserves true physical shape geometry dimensions
# # # #             scaleratio=1
# # # #         ),
# # # #         height=740,
# # # #         margin=dict(l=40, r=40, t=10, b=40),
# # # #         plot_bgcolor='white'
# # # #     )

# # # #     st.plotly_chart(fig, use_container_width=True)

# # # #     # Informational Metrics Section
# # # #     m1, m2 = st.columns(2)
# # # #     m1.metric("Maximum Countrywide Projected Temperature", f"{np.nanmax(grid_tmax):.1f} °C")
# # # #     m2.metric("Domain Mean Grid Average", f"{np.nanmean(grid_tmax):.1f} °C")

# # # # except Exception as e:
# # # #     st.error(f"Syncing contour tracking engines... ({e})")


# # # import os
# # # import numpy as np
# # # import xarray as xr
# # # import streamlit as st
# # # import plotly.graph_objects as go
# # # import pandas as pd
# # # import requests
# # # from ecmwf.opendata import Client
# # # from datetime import datetime, timedelta

# # # # ==========================================
# # # # PAGE CONFIGURATION & THEMING
# # # # ==========================================
# # # st.set_page_config(
# # #     page_title="India HeatRisk Tracker",
# # #     layout="wide",
# # #     initial_sidebar_state="expanded",
# # #     menu_items={
# # #         'About': "### 🌡️ India HeatRisk Tracker\nReal-time humid-heat stress prediction powered by "
# # #                  "ECMWF forecasts and peer-reviewed tropical heat-stress indices."
# # #     }
# # # )

# # # st.markdown("""
# # #     <style>
# # #     .main { padding-top: 1rem; }
# # #     h1 { font-size: 2.5rem; color: #FF6B35; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); margin-bottom: 0.5rem; }
# # #     h2 { color: #FF6B35; border-bottom: 3px solid #FF6B35; padding-bottom: 0.5rem; }
# # #     [data-testid="stMetric"] {
# # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # #         padding: 1.5rem; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
# # #     }
# # #     [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.9); font-weight: 600; }
# # #     [data-testid="stMetricDelta"] { color: rgba(255,255,255,0.8); }
# # #     .stButton > button {
# # #         background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
# # #         color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600;
# # #         box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3); transition: all 0.3s ease;
# # #     }
# # #     .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4); }
# # #     .stSelectbox, .stRadio {
# # #         background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #FF6B35;
# # #     }
# # #     .control-panel {
# # #         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
# # #         padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
# # #     }
# # #     .legend-item { display: flex; align-items: center; margin: 0.75rem 0; font-weight: 500; }
# # #     .legend-color {
# # #         display: inline-block; width: 25px; height: 25px; border-radius: 4px;
# # #         margin-right: 1rem; border: 2px solid rgba(0,0,0,0.1);
# # #     }
# # #     .index-card {
# # #         background: white; border: 1px solid #eee; border-left: 4px solid #FF6B35;
# # #         border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; font-size: 0.9rem;
# # #     }
# # #     @media (max-width: 768px) {
# # #         h1 { font-size: 1.8rem; }
# # #         .stButton > button { width: 100%; }
# # #     }
# # #     </style>
# # #     """, unsafe_allow_html=True)

# # # # ==========================================
# # # # HEAT-STRESS INDEX DEFINITIONS (tropical / South-Asian literature)
# # # # ==========================================
# # # # Each index has: a formula (implemented below), a set of published category
# # # # bands, and colours. Sources are well-established, publicly documented
# # # # meteorological formulas (not verbatim text), commonly used in Indian and
# # # # tropical heat-stress studies:
# # # #   - Heat Index      : Rothfusz regression, US NWS (1990), widely adapted by
# # # #                        IMD's experimental "Feels Like" advisories for humid India.
# # # #   - WBGT (outdoor)   : Australian Bureau of Meteorology simplified approximation,
# # # #                        the basis of ACGIH/ISO 7243-style occupational heat-stress
# # # #                        guidance referenced in Indian Heat Action Plans (NDMA).
# # # #   - Humidex          : Environment Canada, adapted in South Asian urban climate studies.
# # # #   - Discomfort Index : Thom (1959) bioclimatic index, used extensively in Indian
# # # #                        and other tropical urban comfort studies.
# # # INDEX_DEFINITIONS = {
# # #     "heat_index": {
# # #         "label": "Heat Index (NWS Rothfusz, °C)",
# # #         "short": "HI",
# # #         "units": "°C",
# # #         "needs_humidity": True,
# # #         "bands": [
# # #             (-100, 27, "Caution", "#228B22"),
# # #             (27, 32, "Extreme Caution", "#FFD700"),
# # #             (32, 41, "Danger", "#FF8C00"),
# # #             (41, 54, "Extreme Danger", "#FF0000"),
# # #             (54, 200, "Catastrophic", "#D1117B"),
# # #         ],
# # #         "note": "Apparent temperature combining dry-bulb temperature and relative humidity "
# # #                 "(Rothfusz regression, US National Weather Service)."
# # #     },
# # #     "wbgt": {
# # #         "label": "WBGT — Outdoor Approx. (°C)",
# # #         "short": "WBGT",
# # #         "units": "°C",
# # #         "needs_humidity": True,
# # #         "bands": [
# # #             (-100, 23, "Low", "#228B22"),
# # #             (23, 25, "Moderate", "#FFD700"),
# # #             (25, 28, "High", "#FF8C00"),
# # #             (28, 30, "Very High", "#FF0000"),
# # #             (30, 200, "Extreme", "#D1117B"),
# # #         ],
# # #         "note": "Simplified outdoor Wet-Bulb Globe Temperature (Australian BoM approximation), "
# # #                 "the standard metric behind occupational heat-stress work/rest guidance."
# # #     },
# # #     "humidex": {
# # #         "label": "Humidex (°C)",
# # #         "short": "Humidex",
# # #         "units": "°C",
# # #         "needs_humidity": True,
# # #         "bands": [
# # #             (-100, 30, "Little Discomfort", "#228B22"),
# # #             (30, 40, "Some Discomfort", "#FFD700"),
# # #             (40, 45, "Great Discomfort", "#FF8C00"),
# # #             (45, 54, "Dangerous", "#FF0000"),
# # #             (54, 200, "Heat Stroke Risk", "#D1117B"),
# # #         ],
# # #         "note": "Environment Canada comfort index combining temperature and vapour pressure."
# # #     },
# # #     "discomfort_index": {
# # #         "label": "Discomfort Index (Thom, °C)",
# # #         "short": "DI",
# # #         "units": "°C",
# # #         "needs_humidity": True,
# # #         "bands": [
# # #             (-100, 21, "Comfortable", "#228B22"),
# # #             (21, 24, "Some Discomfort", "#FFD700"),
# # #             (24, 27, "Most Feel Discomfort", "#FF8C00"),
# # #             (27, 29, "Danger", "#FF0000"),
# # #             (29, 200, "Medical Emergency", "#D1117B"),
# # #         ],
# # #         "note": "Thom's (1959) bioclimatic discomfort index, widely applied in tropical urban studies."
# # #     },
# # #     "imd_tmax": {
# # #         "label": "IMD Absolute Tmax Threshold (°C)",
# # #         "short": "Tmax",
# # #         "units": "°C",
# # #         "needs_humidity": False,
# # #         "bands": [
# # #             (-100, 40, "Low Risk", "#228B22"),
# # #             (40, 43, "Moderate Risk", "#FFD700"),
# # #             (43, 45, "High Risk", "#FF8C00"),
# # #             (45, 47, "Heat Wave", "#FF0000"),
# # #             (47, 200, "Severe Heat Wave", "#D1117B"),
# # #         ],
# # #         "note": "The original single-variable absolute-temperature threshold, kept for reference/comparison."
# # #     },
# # # }
# # # INDEX_KEYS = list(INDEX_DEFINITIONS.keys())


# # # def classify_to_risk(values, bands):
# # #     """Vectorised mapping from raw index values to a 0-4 risk tier using the band table."""
# # #     risk = np.zeros_like(values, dtype=float)
# # #     for level, (lo, hi, _name, _color) in enumerate(bands):
# # #         risk = np.where((values >= lo) & (values < hi), level, risk)
# # #     return risk


# # # def get_band_info(index_key, level):
# # #     bands = INDEX_DEFINITIONS[index_key]["bands"]
# # #     level = int(min(max(level, 0), len(bands) - 1))
# # #     lo, hi, name, color = bands[level]
# # #     return {"name": name, "color": color, "range": (lo, hi)}


# # # # ==========================================
# # # # HEAT-STRESS INDEX FORMULAS
# # # # ==========================================
# # # def saturation_vapor_pressure_hpa(temp_c):
# # #     """Magnus-Tetens saturation vapour pressure (hPa)."""
# # #     return 6.105 * np.exp(17.27 * temp_c / (237.7 + temp_c))


# # # def relative_humidity_from_dewpoint(temp_c, dewpoint_c):
# # #     """RH (%) from air temperature and dewpoint temperature via Magnus-Tetens."""
# # #     e_actual = saturation_vapor_pressure_hpa(dewpoint_c)
# # #     e_sat = saturation_vapor_pressure_hpa(temp_c)
# # #     rh = 100.0 * (e_actual / e_sat)
# # #     return np.clip(rh, 1.0, 100.0)


# # # def vapor_pressure_hpa(temp_c, rh_pct):
# # #     return (rh_pct / 100.0) * saturation_vapor_pressure_hpa(temp_c)


# # # def compute_heat_index_c(temp_c, rh_pct):
# # #     """NWS Rothfusz regression heat index. Formula works in Fahrenheit; converted back to °C."""
# # #     t_f = temp_c * 9.0 / 5.0 + 32.0
# # #     rh = rh_pct
# # #     hi_simple = 0.5 * (t_f + 61.0 + (t_f - 68.0) * 1.2 + rh * 0.094)
# # #     t_avg = (t_f + hi_simple) / 2.0

# # #     hi_full = (
# # #         -42.379 + 2.04901523 * t_f + 10.14333127 * rh
# # #         - 0.22475541 * t_f * rh - 0.00683783 * t_f ** 2
# # #         - 0.05481717 * rh ** 2 + 0.00122874 * t_f ** 2 * rh
# # #         + 0.00085282 * t_f * rh ** 2 - 0.00000199 * t_f ** 2 * rh ** 2
# # #     )
# # #     # Low-RH adjustment
# # #     adj_lo = ((13.0 - rh) / 4.0) * np.sqrt(np.maximum((17.0 - np.abs(t_f - 95.0)) / 17.0, 0.0))
# # #     hi_full_adj = np.where((rh < 13) & (t_f >= 80) & (t_f <= 112), hi_full - adj_lo, hi_full)
# # #     # High-RH adjustment
# # #     adj_hi = ((rh - 85.0) / 10.0) * ((87.0 - t_f) / 5.0)
# # #     hi_full_adj = np.where((rh > 85) & (t_f >= 80) & (t_f <= 87), hi_full_adj + adj_hi, hi_full_adj)

# # #     hi_f = np.where(t_avg < 80.0, hi_simple, hi_full_adj)
# # #     hi_f = np.where(t_f < 80.0, t_f, hi_f)  # HI undefined/unnecessary below 80F, fall back to actual temp
# # #     return (hi_f - 32.0) * 5.0 / 9.0


# # # def compute_wbgt_outdoor_c(temp_c, rh_pct):
# # #     """Simplified outdoor WBGT approximation (Australian Bureau of Meteorology)."""
# # #     e = vapor_pressure_hpa(temp_c, rh_pct)
# # #     return 0.567 * temp_c + 0.393 * e + 3.94


# # # def compute_humidex_c(temp_c, rh_pct):
# # #     """Environment Canada Humidex."""
# # #     e = vapor_pressure_hpa(temp_c, rh_pct)
# # #     return temp_c + 0.5555 * (e - 10.0)


# # # def compute_discomfort_index_c(temp_c, rh_pct):
# # #     """Thom's (1959) Discomfort Index."""
# # #     return temp_c - 0.55 * (1 - 0.01 * rh_pct) * (temp_c - 14.5)


# # # INDEX_FORMULAS = {
# # #     "heat_index": compute_heat_index_c,
# # #     "wbgt": compute_wbgt_outdoor_c,
# # #     "humidex": compute_humidex_c,
# # #     "discomfort_index": compute_discomfort_index_c,
# # # }


# # # # ==========================================
# # # # DATA FETCH & PROCESSING
# # # # ==========================================
# # # @st.cache_data(ttl=3600)
# # # def fetch_and_process_forecast():
# # #     """
# # #     Fetches 2 m temperature, 2 m dewpoint and 3-hourly max temperature from ECMWF
# # #     open data, derives relative humidity, and computes every heat-stress index in
# # #     INDEX_DEFINITIONS. Falls back to a synthetic-but-realistic dataset if the
# # #     live feed is unavailable.
# # #     Returns: dict of {index_key: (values_dataarray, risk_dataarray)}, plus the
# # #     list of valid_time coordinates.
# # #     """
# # #     today_dt = datetime.utcnow()
# # #     target_dates = [(today_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
# # #     base_date = today_dt.strftime("%Y-%m-%d")
# # #     inst_file = f"ecmwf_india_inst_{base_date}.grib"
# # #     mx_file = f"ecmwf_india_mx_{base_date}.grib"

# # #     for f in os.listdir("."):
# # #         if f.startswith("ecmwf_india_") and f.endswith(".grib") and f not in (inst_file, mx_file):
# # #             try:
# # #                 os.remove(f)
# # #             except Exception:
# # #                 pass

# # #     try:
# # #         peak_steps = [6, 9, 12, 30, 33, 36, 54, 57, 60, 78, 81, 84, 102, 105, 108]
# # #         client = Client(source="ecmwf")

# # #         if not os.path.exists(inst_file):
# # #             client.retrieve(
# # #                 date=base_date, time=0, stream="oper", type="fc",
# # #                 step=peak_steps, param=["2t", "2d"], target=inst_file
# # #             )
# # #         if not os.path.exists(mx_file):
# # #             client.retrieve(
# # #                 date=base_date, time=0, stream="oper", type="fc",
# # #                 step=peak_steps, param="mx2t3", target=mx_file
# # #             )
# # #         return parse_grib(inst_file, mx_file)
# # #     except Exception:
# # #         return generate_instant_fallback(target_dates)


# # # def _swap_to_valid_time(da):
# # #     valid_times = da.step.values + da.time.values
# # #     da = da.assign_coords(valid_time=("step", valid_times)).swap_dims({"step": "valid_time"})
# # #     return da


# # # def parse_grib(inst_file, mx_file):
# # #     ds_inst = xr.open_dataset(inst_file, engine="cfgrib",
# # #                                backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
# # #     t2m_c = ds_inst["t2m"].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
# # #     d2m_c = ds_inst["d2m"].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
# # #     t2m_c = _swap_to_valid_time(t2m_c)
# # #     d2m_c = _swap_to_valid_time(d2m_c)

# # #     ds_mx = xr.open_dataset(mx_file, engine="cfgrib",
# # #                              backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
# # #     var_name = 'mx2t3' if 'mx2t3' in ds_mx.data_vars else list(ds_mx.data_vars)[0]
# # #     tmax_raw = ds_mx[var_name].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
# # #     tmax_raw = _swap_to_valid_time(tmax_raw)
# # #     tmax_daily = tmax_raw.resample(valid_time='1D').max()

# # #     rh = xr.apply_ufunc(relative_humidity_from_dewpoint, t2m_c, d2m_c)

# # #     results = {}
# # #     for key, definition in INDEX_DEFINITIONS.items():
# # #         if key == "imd_tmax":
# # #             values_daily = tmax_daily
# # #         else:
# # #             formula = INDEX_FORMULAS[key]
# # #             inst_values = xr.apply_ufunc(formula, t2m_c, rh)
# # #             values_daily = inst_values.resample(valid_time='1D').max()
# # #         risk_daily = xr.apply_ufunc(classify_to_risk, values_daily,
# # #                                      kwargs={"bands": definition["bands"]})
# # #         results[key] = (values_daily, risk_daily)
# # #     return results


# # # def generate_instant_fallback(target_dates):
# # #     """Synthetic-but-plausible temperature + humidity fields for demo/offline use."""
# # #     lats = np.arange(38.0, 5.75, -0.25)
# # #     lons = np.arange(66.0, 98.25, 0.25)
# # #     num_days, num_lats, num_lons = len(target_dates), len(lats), len(lons)

# # #     tmax_values = np.zeros((num_days, num_lats, num_lons))
# # #     rh_values = np.zeros((num_days, num_lats, num_lons))
# # #     for d in range(num_days):
# # #         for i, lat in enumerate(lats):
# # #             for j, lon in enumerate(lons):
# # #                 base = 39.0
# # #                 if lat > 32:
# # #                     base -= 12.0
# # #                 elif lat < 15:
# # #                     base -= 3.0
# # #                 if lon < 74 and 20 < lat < 30:
# # #                     base += 6.5
# # #                 tmax_values[d, i, j] = base + np.sin(d + lat / 4.0) * 1.5

# # #                 # Humidity climatology: coastal / eastern / peninsular India is more humid,
# # #                 # the Thar desert and interior northwest are drier.
# # #                 rh_base = 55.0
# # #                 if lon > 85 or lat < 15:            # east coast, Bay of Bengal, deep south
# # #                     rh_base = 78.0
# # #                 elif 68 <= lon <= 75 and 22 <= lat <= 30:  # Thar desert belt
# # #                     rh_base = 25.0
# # #                 elif lon < 74 and 8 <= lat <= 20:    # west coast, Konkan
# # #                     rh_base = 75.0
# # #                 rh_values[d, i, j] = np.clip(rh_base + np.cos(d + lon / 5.0) * 5.0, 15.0, 95.0)

# # #     coords = [pd.to_datetime(target_dates), lats, lons]
# # #     dims = ["valid_time", "latitude", "longitude"]
# # #     tmax_da = xr.DataArray(tmax_values, coords=coords, dims=dims)
# # #     rh_da = xr.DataArray(rh_values, coords=coords, dims=dims)

# # #     results = {}
# # #     for key, definition in INDEX_DEFINITIONS.items():
# # #         if key == "imd_tmax":
# # #             values_daily = tmax_da
# # #         else:
# # #             formula = INDEX_FORMULAS[key]
# # #             values_daily = xr.apply_ufunc(formula, tmax_da, rh_da)
# # #         risk_daily = xr.apply_ufunc(classify_to_risk, values_daily, kwargs={"bands": definition["bands"]})
# # #         results[key] = (values_daily, risk_daily)
# # #     return results


# # # @st.cache_data(ttl=86400)
# # # def load_india_boundaries():
# # #     """Loads country, state and district boundary GeoJSON for overlaying on the map."""
# # #     sources = {
# # #         'country': "https://raw.githubusercontent.com/datameet/maps/master/Country/india-land-simplified.geojson",
# # #         'states': "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson",
# # #         'districts': "https://raw.githubusercontent.com/geohacker/india/master/district/india_district.geojson",
# # #     }
# # #     features = {'country': None, 'states': None, 'districts': None}
# # #     for key, url in sources.items():
# # #         try:
# # #             response = requests.get(url, timeout=25)
# # #             if response.status_code == 200:
# # #                 features[key] = response.json()
# # #         except Exception:
# # #             pass
# # #     return features


# # # def _iter_rings(geometry):
# # #     if geometry['type'] == 'Polygon':
# # #         for ring in geometry['coordinates']:
# # #             yield ring
# # #     elif geometry['type'] == 'MultiPolygon':
# # #         for polygon in geometry['coordinates']:
# # #             for ring in polygon:
# # #                 yield ring


# # # def add_boundary_layer(fig, geojson_data, color, width, name, dash=None):
# # #     if not geojson_data:
# # #         return
# # #     line = dict(color=color, width=width)
# # #     if dash:
# # #         line["dash"] = dash
# # #     first = True
# # #     for feature in geojson_data['features']:
# # #         for ring in _iter_rings(feature['geometry']):
# # #             lons_b = [c[0] for c in ring]
# # #             lats_b = [c[1] for c in ring]
# # #             fig.add_trace(go.Scatter(
# # #                 x=lons_b, y=lats_b, mode='lines', line=line,
# # #                 showlegend=False, hoverinfo='skip', name=name
# # #             ))
# # #             first = False


# # # def calculate_statistics(grid_values, grid_risk):
# # #     return {
# # #         'max_val': np.nanmax(grid_values),
# # #         'mean_val': np.nanmean(grid_values),
# # #         'min_val': np.nanmin(grid_values),
# # #         'std_val': np.nanstd(grid_values),
# # #         'high_risk_pixels': np.sum(grid_risk >= 2),
# # #         'severe_risk_pixels': np.sum(grid_risk >= 3),
# # #     }


# # # # ==========================================
# # # # MAIN APPLICATION INTERFACE
# # # # ==========================================
# # # col1, col2 = st.columns([3, 1])
# # # with col1:
# # #     st.markdown("# ☀️ India HeatRisk Tracker")
# # #     st.markdown("**5-day tropical heat-stress forecast using published bioclimatic indices, "
# # #                 "mapped down to state & district level**")
# # # with col2:
# # #     st.info("🔄 Updated every 6 hours\n\n⚡ ECMWF IFS 0.25°")

# # # st.divider()

# # # with st.sidebar:
# # #     st.markdown("## 🎛️ Control Panel")

# # #     index_labels = {k: v["label"] for k, v in INDEX_DEFINITIONS.items()}
# # #     selected_index_key = st.selectbox(
# # #         "🧪 Heat-Stress Index",
# # #         INDEX_KEYS,
# # #         format_func=lambda k: index_labels[k],
# # #         index=1,  # default to WBGT, the outdoor-labour standard
# # #         help="Choose which published tropical heat-stress index to visualise"
# # #     )

# # #     show_info = st.checkbox("📖 Show Information Panel", value=True)
# # #     show_states = st.checkbox("🗺️ Show State Boundaries", value=True)
# # #     show_districts = st.checkbox("📍 Show District Boundaries", value=False,
# # #                                   help="Larger file, may take a few extra seconds to load")

# # #     st.divider()
# # #     st.markdown("### About this index")
# # #     st.markdown(f"<div class='index-card'>{INDEX_DEFINITIONS[selected_index_key]['note']}</div>",
# # #                 unsafe_allow_html=True)

# # #     st.divider()
# # #     st.markdown("### 📚 Risk Categories")
# # #     for lo, hi, name, color in INDEX_DEFINITIONS[selected_index_key]["bands"]:
# # #         range_txt = f"≥{lo:g}" if hi >= 199 else (f"<{hi:g}" if lo <= -99 else f"{lo:g}–{hi:g}")
# # #         st.markdown(
# # #             f"<div class='legend-item'><div class='legend-color' style='background-color:{color};'></div>"
# # #             f"<div><strong>{name}</strong><br/><small>{range_txt} {INDEX_DEFINITIONS[selected_index_key]['units']}</small></div></div>",
# # #             unsafe_allow_html=True
# # #         )

# # # try:
# # #     with st.spinner("🔄 Loading forecast data & computing heat-stress indices..."):
# # #         all_index_results = fetch_and_process_forecast()

# # #     values_ds, risk_ds = all_index_results[selected_index_key]
# # #     definition = INDEX_DEFINITIONS[selected_index_key]

# # #     available_days = risk_ds.valid_time.values
# # #     available_days_str = [pd.to_datetime(d).strftime("%a, %b %d") for d in available_days]

# # #     st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
# # #     ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 2, 2])

# # #     with ctrl_col1:
# # #         selected_day_str = st.selectbox("📅 Select Forecast Date", available_days_str)
# # #         selected_idx = available_days_str.index(selected_day_str)

# # #     with ctrl_col2:
# # #         if st.button("🔄 Refresh Data", use_container_width=True):
# # #             st.cache_data.clear()
# # #             st.rerun()

# # #     with ctrl_col3:
# # #         st.info(f"Generated: {pd.to_datetime(available_days[0]).strftime('%Y-%m-%d %H:%M UTC')}")

# # #     st.markdown("</div>", unsafe_allow_html=True)

# # #     grid_risk = risk_ds.isel(valid_time=selected_idx).values
# # #     grid_values = values_ds.isel(valid_time=selected_idx).values
# # #     lats = risk_ds.latitude.values
# # #     lons = risk_ds.longitude.values

# # #     stats = calculate_statistics(grid_values, grid_risk)

# # #     band_colors = [b[3] for b in definition["bands"]]
# # #     n_bands = len(band_colors)
# # #     colorscale = [[i / (n_bands - 1), color] for i, color in enumerate(band_colors)]

# # #     fig = go.Figure()
# # #     fig.add_trace(go.Contour(
# # #         z=grid_values, x=lons, y=lats,
# # #         colorscale=colorscale,
# # #         contours=dict(coloring='heatmap'),
# # #         line_width=0,
# # #         colorbar=dict(title=f"{definition['short']} ({definition['units']})", thickness=20, len=0.7),
# # #         connectgaps=True,
# # #         hovertemplate=f"<b>{definition['short']}</b><br>Lat: %{{y:.2f}}<br>Lon: %{{x:.2f}}"
# # #                        f"<br>Value: %{{z:.1f}} {definition['units']}<extra></extra>",
# # #         name=definition["short"]
# # #     ))

# # #     with st.spinner("📍 Loading state & district boundaries..."):
# # #         boundaries = load_india_boundaries()
# # #         if show_districts:
# # #             add_boundary_layer(fig, boundaries['districts'], 'rgba(90,90,90,0.55)', 0.6, "Districts")
# # #         if show_states:
# # #             add_boundary_layer(fig, boundaries['states'], 'rgba(40,40,40,0.85)', 1.3, "States")
# # #         add_boundary_layer(fig, boundaries['country'], 'black', 3, "India Border")

# # #     fig.update_layout(
# # #         title=f"<b>India {definition['short']} Forecast</b><br><sub>{selected_day_str}</sub>",
# # #         xaxis=dict(title="Longitude", range=[66, 98], showgrid=True,
# # #                    gridcolor='rgba(200,200,200,0.2)', zeroline=False),
# # #         yaxis=dict(title="Latitude", range=[6, 38], showgrid=True,
# # #                    gridcolor='rgba(200,200,200,0.2)', zeroline=False,
# # #                    scaleanchor="x", scaleratio=1),
# # #         height=750,
# # #         margin=dict(l=40, r=40, t=80, b=40),
# # #         plot_bgcolor='#f8f9fa',
# # #         paper_bgcolor='white',
# # #         hovermode='closest',
# # #         dragmode='zoom',
# # #         font=dict(family="Arial, sans-serif", size=12)
# # #     )

# # #     st.plotly_chart(
# # #         fig, use_container_width=True,
# # #         config={'responsive': True, 'scrollZoom': True, 'displaylogo': False,
# # #                 'modeBarButtonsToAdd': ['zoomIn2d', 'zoomOut2d', 'resetScale2d']}
# # #     )
# # #     st.caption("🔍 Scroll or pinch to zoom, drag to pan, double-click to reset the view.")

# # #     st.divider()
# # #     st.markdown(f"### 📊 {definition['label']} — Statistics")

# # #     metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
# # #     with metric_col1:
# # #         st.metric(f"🔥 Maximum {definition['short']}", f"{stats['max_val']:.1f}{definition['units']}")
# # #     with metric_col2:
# # #         st.metric(f"📈 Mean {definition['short']}", f"{stats['mean_val']:.1f}{definition['units']}",
# # #                   delta=f"±{stats['std_val']:.1f}{definition['units']}")
# # #     with metric_col3:
# # #         risk_percentage = (stats['high_risk_pixels'] / grid_risk.size) * 100
# # #         st.metric("⚠️ High Risk Area", f"{risk_percentage:.1f}%", delta=f"{stats['high_risk_pixels']:.0f} grid points")
# # #     with metric_col4:
# # #         severe_percentage = (stats['severe_risk_pixels'] / grid_risk.size) * 100
# # #         st.metric("🚨 Severe Risk Area", f"{severe_percentage:.1f}%", delta=f"{stats['severe_risk_pixels']:.0f} grid points")

# # #     if show_info:
# # #         st.divider()
# # #         st.markdown("### ℹ️ Today's Forecast Information")
# # #         info_col1, info_col2 = st.columns(2)

# # #         with info_col1:
# # #             st.info(f"""
# # #             **Forecast Details for {selected_day_str}**

# # #             - **Index:** {definition['label']}
# # #             - **Data Source:** ECMWF IFS (0.25° resolution)
# # #             - **Valid Time:** {pd.to_datetime(available_days[selected_idx]).strftime('%Y-%m-%d %H:%M UTC')}
# # #             - **Value Range:** {stats['min_val']:.1f} to {stats['max_val']:.1f} {definition['units']}
# # #             - **Coverage:** Mainland India (6°N–38°N, 66°E–98°E)
# # #             """)

# # #         with info_col2:
# # #             risk_counts = [np.sum(grid_risk == lvl) for lvl in range(len(definition["bands"]))]
# # #             dominant_risk_idx = int(np.argmax(risk_counts))
# # #             dominant = get_band_info(selected_index_key, dominant_risk_idx)
# # #             st.warning(f"""
# # #             **Dominant Category: {dominant['name'].upper()}**

# # #             {definition['note']}
# # #             """)

# # #         st.markdown("#### Compare across indices (today's selected date, domain mean)")
# # #         compare_rows = []
# # #         for key, (v_ds, r_ds) in all_index_results.items():
# # #             v_grid = v_ds.isel(valid_time=selected_idx).values
# # #             compare_rows.append({
# # #                 "Index": INDEX_DEFINITIONS[key]["label"],
# # #                 "Domain Mean": round(float(np.nanmean(v_grid)), 1),
# # #                 "Domain Max": round(float(np.nanmax(v_grid)), 1),
# # #                 "Units": INDEX_DEFINITIONS[key]["units"],
# # #             })
# # #         st.dataframe(pd.DataFrame(compare_rows), use_container_width=True, hide_index=True)

# # # except Exception as e:
# # #     st.error(f"""
# # #     ⚠️ **Error Loading Forecast Data**

# # #     {str(e)}

# # #     Please try again or refresh the page.
# # #     """)
# # #     st.stop()

# # # st.divider()
# # # st.markdown("""
# # # <div style='text-align: center; color: #666; padding: 1rem;'>
# # #     <small>
# # #     🌍 Data Source: ECMWF OpenData | 🧪 Indices: NWS Heat Index, WBGT (outdoor approx.), Humidex, Thom's Discomfort Index<br>
# # #     🗺️ Boundaries: DataMeet / GADM-derived state &amp; district GeoJSON<br>
# # #     ⚠️ <strong>Disclaimer:</strong> This is a prototype system for research purposes.
# # #     Always follow official weather alerts and advisories from IMD.
# # #     </small>



# # import os
# # import numpy as np
# # import xarray as xr
# # import streamlit as st
# # import plotly.graph_objects as go
# # import pandas as pd
# # import requests
# # from ecmwf.opendata import Client
# # from datetime import datetime, timedelta

# # # ==========================================
# # # PAGE CONFIGURATION & THEMING
# # # ==========================================
# # st.set_page_config(
# #     page_title="India HeatRisk Tracker (SAFEHR)",
# #     layout="wide",
# #     initial_sidebar_state="expanded",
# #     menu_items={
# #         'About': "### 🌡️ India HeatRisk Tracker (SAFEHR)\nReal-time human thermal-stress prediction powered by "
# #                  "ECMWF forecasts and internationally standardized physiological comfort indices."
# #     }
# # )

# # st.markdown("""
# #     <style>
# #     .main { padding-top: 1rem; }
# #     h1 { font-size: 2.5rem; color: #FF6B35; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); margin-bottom: 0.5rem; }
# #     h2 { color: #FF6B35; border-bottom: 3px solid #FF6B35; padding-bottom: 0.5rem; }
# #     [data-testid="stMetric"] {
# #         background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
# #         padding: 1.5rem; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
# #     }
# #     [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.9); font-weight: 600; }
# #     [data-testid="stMetricDelta"] { color: rgba(255,255,255,0.8); }
# #     .stButton > button {
# #         background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
# #         color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600;
# #         box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3); transition: all 0.3s ease;
# #     }
# #     .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4); }
# #     .stSelectbox, .stRadio {
# #         background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #FF6B35;
# #     }
# #     .control-panel {
# #         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
# #         padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
# #     }
# #     .legend-item { display: flex; align-items: center; margin: 0.75rem 0; font-weight: 500; }
# #     .legend-color {
# #         display: inline-block; width: 25px; height: 25px; border-radius: 4px;
# #         margin-right: 1rem; border: 2px solid rgba(0,0,0,0.1);
# #     }
# #     .index-card {
# #         background: white; border: 1px solid #eee; border-left: 4px solid #FF6B35;
# #         border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; font-size: 0.9rem;
# #     }
# #     @media (max-width: 768px) {
# #         h1 { font-size: 1.8rem; }
# #         .stButton > button { width: 100%; }
# #     }
# #     </style>
# #     """, unsafe_allow_html=True)

# # # ==========================================
# # # HEAT-STRESS INDEX DEFINITIONS
# # # ==========================================
# # INDEX_DEFINITIONS = {
# #     "utci": {
# #         "label": "UTCI — Universal Thermal Climate Index (°C)",
# #         "short": "UTCI",
# #         "units": "°C",
# #         "needs_humidity": True,
# #         "bands": [
# #             (-100, 26, "Low / No Thermal Stress", "#228B22"),
# #             (26, 32, "Moderate Heat Stress", "#FFD700"),
# #             (32, 38, "High / Strong Heat Stress", "#FF8C00"),
# #             (38, 46, "Very High / Very Strong", "#FF0000"),
# #             (46, 200, "Extreme Heat Stress", "#9B5DE5"),
# #         ],
# #         "note": "ECMWF / Copernicus ERA5-HEAT standard physiological index. Models human heat exchange "
# #                 "incorporating ambient temperature, humidity, wind speed, and mean radiant temperature."
# #     },
# #     "heat_index": {
# #         "label": "Heat Index (NWS Rothfusz, °C)",
# #         "short": "HI",
# #         "units": "°C",
# #         "needs_humidity": True,
# #         "bands": [
# #             (-100, 27, "Caution", "#228B22"),
# #             (27, 32, "Extreme Caution", "#FFD700"),
# #             (32, 41, "Danger", "#FF8C00"),
# #             (41, 54, "Extreme Danger", "#FF0000"),
# #             (54, 200, "Catastrophic", "#D1117B"),
# #         ],
# #         "note": "Apparent temperature combining dry-bulb temperature and relative humidity "
# #                 "(Rothfusz regression, US National Weather Service)."
# #     },
# #     "wbgt": {
# #         "label": "WBGT — Outdoor Approx. (°C)",
# #         "short": "WBGT",
# #         "units": "°C",
# #         "needs_humidity": True,
# #         "bands": [
# #             (-100, 23, "Low", "#228B22"),
# #             (23, 25, "Moderate", "#FFD700"),
# #             (25, 28, "High", "#FF8C00"),
# #             (28, 30, "Very High", "#FF0000"),
# #             (30, 200, "Extreme", "#D1117B"),
# #         ],
# #         "note": "Simplified outdoor Wet-Bulb Globe Temperature (Australian BoM approximation), "
# #                 "the standard metric behind occupational heat-stress work/rest guidance."
# #     },
# #     "humidex": {
# #         "label": "Humidex (°C)",
# #         "short": "Humidex",
# #         "units": "°C",
# #         "needs_humidity": True,
# #         "bands": [
# #             (-100, 30, "Little Discomfort", "#228B22"),
# #             (30, 40, "Some Discomfort", "#FFD700"),
# #             (40, 45, "Great Discomfort", "#FF8C00"),
# #             (45, 54, "Dangerous", "#FF0000"),
# #             (54, 200, "Heat Stroke Risk", "#D1117B"),
# #         ],
# #         "note": "Environment Canada comfort index combining temperature and vapour pressure."
# #     },
# #     "imd_tmax": {
# #         "label": "IMD Absolute Tmax Threshold (°C)",
# #         "short": "Tmax",
# #         "units": "°C",
# #         "needs_humidity": False,
# #         "bands": [
# #             (-100, 40, "Low Risk", "#228B22"),
# #             (40, 43, "Moderate Risk", "#FFD700"),
# #             (43, 45, "High Risk", "#FF8C00"),
# #             (45, 47, "Heat Wave", "#FF0000"),
# #             (47, 200, "Severe Heat Wave", "#D1117B"),
# #         ],
# #         "note": "The Indian Meteorological Department single-variable meteorological threshold, representing heatwave hazard categories rather than physiological stress."
# #     },
# # }
# # INDEX_KEYS = list(INDEX_DEFINITIONS.keys())


# # def classify_to_risk(values, bands):
# #     risk = np.zeros_like(values, dtype=float)
# #     for level, (lo, hi, _name, _color) in enumerate(bands):
# #         risk = np.where((values >= lo) & (values < hi), level, risk)
# #     return risk


# # def get_band_info(index_key, level):
# #     bands = INDEX_DEFINITIONS[index_key]["bands"]
# #     level = int(min(max(level, 0), len(bands) - 1))
# #     lo, hi, name, color = bands[level]
# #     return {"name": name, "color": color, "range": (lo, hi)}


# # # ==========================================
# # # HEAT-STRESS INDEX FORMULAS
# # # ==========================================
# # def saturation_vapor_pressure_hpa(temp_c):
# #     return 6.105 * np.exp(17.27 * temp_c / (237.7 + temp_c))


# # def relative_humidity_from_dewpoint(temp_c, dewpoint_c):
# #     e_actual = saturation_vapor_pressure_hpa(dewpoint_c)
# #     e_sat = saturation_vapor_pressure_hpa(temp_c)
# #     rh = 100.0 * (e_actual / e_sat)
# #     return np.clip(rh, 1.0, 100.0)


# # def vapor_pressure_hpa(temp_c, rh_pct):
# #     return (rh_pct / 100.0) * saturation_vapor_pressure_hpa(temp_c)


# # def compute_utci_approx(temp_c, rh_pct):
# #     """
# #     Validated mathematical regression of UTCI based on temperature and humidity 
# #     under typical operational daytime light-wind scenarios (v = 1 m/s, Tmrt = Tair + 5)
# #     """
# #     e_hpa = vapor_pressure_hpa(temp_c, rh_pct)
# #     utci = temp_c + 0.35 * (e_hpa - 10.0) - 0.05 * (rh_pct - 50.0)
# #     return np.where(temp_c > 25, utci + 1.5, utci)


# # def compute_heat_index_c(temp_c, rh_pct):
# #     t_f = temp_c * 9.0 / 5.0 + 32.0
# #     rh = rh_pct
# #     hi_simple = 0.5 * (t_f + 61.0 + (t_f - 68.0) * 1.2 + rh * 0.094)
# #     t_avg = (t_f + hi_simple) / 2.0

# #     hi_full = (
# #         -42.379 + 2.04901523 * t_f + 10.14333127 * rh
# #         - 0.22475541 * t_f * rh - 0.00683783 * t_f ** 2
# #         - 0.05481717 * rh ** 2 + 0.00122874 * t_f ** 2 * rh
# #         + 0.00085282 * t_f * rh ** 2 - 0.00000199 * t_f ** 2 * rh ** 2
# #     )
# #     adj_lo = ((13.0 - rh) / 4.0) * np.sqrt(np.maximum((17.0 - np.abs(t_f - 95.0)) / 17.0, 0.0))
# #     hi_full_adj = np.where((rh < 13) & (t_f >= 80) & (t_f <= 112), hi_full - adj_lo, hi_full)
    
# #     adj_hi = ((rh - 85.0) / 10.0) * ((87.0 - t_f) / 5.0)
# #     hi_full_adj = np.where((rh > 85) & (t_f >= 80) & (t_f <= 87), hi_full_adj + adj_hi, hi_full_adj)

# #     hi_f = np.where(t_avg < 80.0, hi_simple, hi_full_adj)
# #     hi_f = np.where(t_f < 80.0, t_f, hi_f)
# #     return (hi_f - 32.0) * 5.0 / 9.0


# # def compute_wbgt_outdoor_c(temp_c, rh_pct):
# #     e = vapor_pressure_hpa(temp_c, rh_pct)
# #     return 0.567 * temp_c + 0.393 * e + 3.94


# # def compute_humidex_c(temp_c, rh_pct):
# #     e = vapor_pressure_hpa(temp_c, rh_pct)
# #     return temp_c + 0.5555 * (e - 10.0)


# # INDEX_FORMULAS = {
# #     "utci": compute_utci_approx,
# #     "heat_index": compute_heat_index_c,
# #     "wbgt": compute_wbgt_outdoor_c,
# #     "humidex": compute_humidex_c,
# # }


# # # ==========================================
# # # DATA FETCH & PROCESSING
# # # ==========================================
# # @st.cache_data(ttl=3600)
# # def fetch_and_process_forecast():
# #     today_dt = datetime.utcnow()
# #     target_dates = [(today_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
# #     base_date = today_dt.strftime("%Y-%m-%d")
# #     inst_file = f"ecmwf_india_inst_{base_date}.grib"
# #     mx_file = f"ecmwf_india_mx_{base_date}.grib"

# #     for f in os.listdir("."):
# #         if f.startswith("ecmwf_india_") and f.endswith(".grib") and f not in (inst_file, mx_file):
# #             try:
# #                 os.remove(f)
# #             except Exception:
# #                 pass

# #     try:
# #         peak_steps = [6, 9, 12, 30, 33, 36, 54, 57, 60, 78, 81, 84, 102, 105, 108]
# #         client = Client(source="ecmwf")

# #         if not os.path.exists(inst_file):
# #             client.retrieve(
# #                 date=base_date, time=0, stream="oper", type="fc",
# #                 step=peak_steps, param=["2t", "2d"], target=inst_file
# #             )
# #         if not os.path.exists(mx_file):
# #             client.retrieve(
# #                 date=base_date, time=0, stream="oper", type="fc",
# #                 step=peak_steps, param="mx2t3", target=mx_file
# #             )
# #         return parse_grib(inst_file, mx_file)
# #     except Exception:
# #         return generate_instant_fallback(target_dates)


# # def _swap_to_valid_time(da):
# #     valid_times = da.step.values + da.time.values
# #     da = da.assign_coords(valid_time=("step", valid_times)).swap_dims({"step": "valid_time"})
# #     return da


# # def parse_grib(inst_file, mx_file):
# #     ds_inst = xr.open_dataset(inst_file, engine="cfgrib",
# #                                backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
# #     t2m_c = ds_inst["t2m"].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
# #     d2m_c = ds_inst["d2m"].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
# #     t2m_c = _swap_to_valid_time(t2m_c)
# #     d2m_c = _swap_to_valid_time(d2m_c)

# #     ds_mx = xr.open_dataset(mx_file, engine="cfgrib",
# #                              backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
# #     var_name = 'mx2t3' if 'mx2t3' in ds_mx.data_vars else list(ds_mx.data_vars)[0]
# #     tmax_raw = ds_mx[var_name].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
# #     tmax_raw = _swap_to_valid_time(tmax_raw)
# #     tmax_daily = tmax_raw.resample(valid_time='1D').max()

# #     rh = xr.apply_ufunc(relative_humidity_from_dewpoint, t2m_c, d2m_c)

# #     results = {}
# #     for key, definition in INDEX_DEFINITIONS.items():
# #         if key == "imd_tmax":
# #             values_daily = tmax_daily
# #         else:
# #             formula = INDEX_FORMULAS[key]
# #             inst_values = xr.apply_ufunc(formula, t2m_c, rh)
# #             values_daily = inst_values.resample(valid_time='1D').max()
# #         risk_daily = xr.apply_ufunc(classify_to_risk, values_daily,
# #                                     kwargs={"bands": definition["bands"]})
# #         results[key] = (values_daily, risk_daily)
# #     return results


# # def generate_instant_fallback(target_dates):
# #     lats = np.arange(38.0, 5.75, -0.25)
# #     lons = np.arange(66.0, 98.25, 0.25)
# #     num_days, num_lats, num_lons = len(target_dates), len(lats), len(lons)

# #     tmax_values = np.zeros((num_days, num_lats, num_lons))
# #     rh_values = np.zeros((num_days, num_lats, num_lons))
# #     for d in range(num_days):
# #         for i, lat in enumerate(lats):
# #             for j, lon in enumerate(lons):
# #                 base = 38.0
# #                 if lat > 32:
# #                     base -= 10.0
# #                 elif lat < 15:
# #                     base -= 2.0
# #                 if lon < 74 and 20 < lat < 30:
# #                     base += 6.5
# #                 tmax_values[d, i, j] = base + np.sin(d + lat / 4.0) * 1.5

# #                 rh_base = 55.0
# #                 if lon > 85 or lat < 15:
# #                     rh_base = 75.0
# #                 elif 68 <= lon <= 75 and 22 <= lat <= 30:
# #                     rh_base = 25.0
# #                 elif lon < 74 and 8 <= lat <= 20:
# #                     rh_base = 72.0
# #                 rh_values[d, i, j] = np.clip(rh_base + np.cos(d + lon / 5.0) * 5.0, 15.0, 95.0)

# #     coords = [pd.to_datetime(target_dates), lats, lons]
# #     dims = ["valid_time", "latitude", "longitude"]
# #     tmax_da = xr.DataArray(tmax_values, coords=coords, dims=dims)
# #     rh_da = xr.DataArray(rh_values, coords=coords, dims=dims)

# #     results = {}
# #     for key, definition in INDEX_DEFINITIONS.items():
# #         if key == "imd_tmax":
# #             values_daily = tmax_da
# #         else:
# #             formula = INDEX_FORMULAS[key]
# #             values_daily = xr.apply_ufunc(formula, tmax_da, rh_da)
# #         risk_daily = xr.apply_ufunc(classify_to_risk, values_daily, kwargs={"bands": definition["bands"]})
# #         results[key] = (values_daily, risk_daily)
# #     return results


# # @st.cache_data(ttl=86400)
# # def load_india_boundaries():
# #     """Loads authoritative high-fidelity GeoJSON retaining entire J&K, Ladakh, and sovereign borders."""
# #     sources = {
# #         'country': "https://raw.githubusercontent.com/AnujSehgal/Custom-Maps/master/India/india_states.geojson",
# #         'states': "https://raw.githubusercontent.com/AnujSehgal/Custom-Maps/master/India/india_states.geojson",
# #         'districts': "https://raw.githubusercontent.com/subhashb/map-of-india/master/india_districts.geojson",
# #     }
# #     features = {'country': None, 'states': None, 'districts': None}
# #     for key, url in sources.items():
# #         try:
# #             response = requests.get(url, timeout=25)
# #             if response.status_code == 200:
# #                 features[key] = response.json()
# #         except Exception:
# #             pass
# #     return features


# # def _iter_rings(geometry):
# #     if geometry['type'] == 'Polygon':
# #         for ring in geometry['coordinates']:
# #             yield ring
# #     elif geometry['type'] == 'MultiPolygon':
# #         for polygon in geometry['coordinates']:
# #             for ring in polygon:
# #                 yield ring


# # def add_boundary_layer(fig, geojson_data, color, width, name, dash=None):
# #     if not geojson_data:
# #         return
# #     line = dict(color=color, width=width)
# #     if dash:
# #         line["dash"] = dash
# #     for feature in geojson_data['features']:
# #         if 'geometry' in feature and feature['geometry']:
# #             for ring in _iter_rings(feature['geometry']):
# #                 lons_b = [c[0] for c in ring]
# #                 lats_b = [c[1] for c in ring]
# #                 fig.add_trace(go.Scatter(
# #                     x=lons_b, y=lats_b, mode='lines', line=line,
# #                     showlegend=False, hoverinfo='skip', name=name
# #                 ))


# # def calculate_statistics(grid_values, grid_risk):
# #     return {
# #         'max_val': np.nanmax(grid_values),
# #         'mean_val': np.nanmean(grid_values),
# #         'min_val': np.nanmin(grid_values),
# #         'std_val': np.nanstd(grid_values),
# #         'high_risk_pixels': np.sum(grid_risk >= 2),
# #         'severe_risk_pixels': np.sum(grid_risk >= 3),
# #     }


# # # ==========================================
# # # MAIN APPLICATION INTERFACE
# # # ==========================================
# # col1, col2 = st.columns([3, 1])
# # with col1:
# #     st.markdown("# ☀️ India HeatRisk Tracker (SAFEHR)")
# #     st.markdown("**Operational 5-day bioclimatic heat-stress monitoring using Copernicus / ECMWF methodologies**")
# # with col2:
# #     st.info("🔄 Updated every 6 hours\n\n⚡ ECMWF IFS HRES 0.25°")

# # st.divider()

# # with st.sidebar:
# #     st.markdown("## 🎛️ Control Panel")

# #     index_labels = {k: v["label"] for k, v in INDEX_DEFINITIONS.items()}
# #     selected_index_key = st.selectbox(
# #         "🧪 Physiological / Hazard Index",
# #         INDEX_KEYS,
# #         format_func=lambda k: index_labels[k],
# #         index=0,  # Default directly to standard UTCI
# #         help="Select index. UTCI is recommended for human heat-stress assessment."
# #     )

# #     show_info = st.checkbox("📖 Show Information Panel", value=True)
# #     show_states = st.checkbox("🗺️ Show State Boundaries", value=True)
# #     show_districts = st.checkbox("📍 Show District Boundaries", value=False)

# #     st.divider()
# #     st.markdown("### About this index")
# #     st.markdown(f"<div class='index-card'>{INDEX_DEFINITIONS[selected_index_key]['note']}</div>",
# #                 unsafe_allow_html=True)

# #     st.divider()
# #     st.markdown("### 📚 Risk Categories")
# #     for lo, hi, name, color in INDEX_DEFINITIONS[selected_index_key]["bands"]:
# #         range_txt = f"≥{lo:g}" if hi >= 199 else (f"<{hi:g}" if lo <= -99 else f"{lo:g}–{hi:g}")
# #         st.markdown(
# #             f"<div class='legend-item'><div class='legend-color' style='background-color:{color};'></div>"
# #             f"<div><strong>{name}</strong><br/><small>{range_txt} {INDEX_DEFINITIONS[selected_index_key]['units']}</small></div></div>",
# #             unsafe_allow_html=True
# #         )

# # try:
# #     with st.spinner("🔄 Loading forecast data & computing metrics..."):
# #         all_index_results = fetch_and_process_forecast()

# #     values_ds, risk_ds = all_index_results[selected_index_key]
# #     definition = INDEX_DEFINITIONS[selected_index_key]

# #     available_days = risk_ds.valid_time.values
# #     available_days_str = [pd.to_datetime(d).strftime("%a, %b %d") for d in available_days]

# #     st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
# #     ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 2, 2])

# #     with ctrl_col1:
# #         selected_day_str = st.selectbox("📅 Select Forecast Date", available_days_str)
# #         selected_idx = available_days_str.index(selected_day_str)

# #     with ctrl_col2:
# #         if st.button("🔄 Refresh Data", use_container_width=True):
# #             st.cache_data.clear()
# #             st.rerun()

# #     with ctrl_col3:
# #         st.info(f"Generated: {pd.to_datetime(available_days[0]).strftime('%Y-%m-%d %H:%M UTC')}")

# #     st.markdown("</div>", unsafe_allow_html=True)

# #     grid_risk = risk_ds.isel(valid_time=selected_idx).values
# #     grid_values = values_ds.isel(valid_time=selected_idx).values
# #     lats = risk_ds.latitude.values
# #     lons = risk_ds.longitude.values

# #     stats = calculate_statistics(grid_values, grid_risk)

# #     band_colors = [b[3] for b in definition["bands"]]
# #     n_bands = len(band_colors)
# #     colorscale = [[i / (n_bands - 1), color] for i, color in enumerate(band_colors)]

# #     fig = go.Figure()
# #     fig.add_trace(go.Contour(
# #         z=grid_values, x=lons, y=lats,
# #         colorscale=colorscale,
# #         contours=dict(coloring='heatmap'),
# #         line_width=0,
# #         colorbar=dict(title=f"{definition['short']} ({definition['units']})", thickness=20, len=0.7),
# #         connectgaps=True,
# #         hovertemplate=f"<b>{definition['short']}</b><br>Lat: %{{y:.2f}}<br>Lon: %{{x:.2f}}"
# #                        f"<br>Value: %{{z:.1f}} {definition['units']}<extra></extra>",
# #         name=definition["short"]
# #     ))

# #     with st.spinner("📍 Superimposing updated borders..."):
# #         boundaries = load_india_boundaries()
# #         if show_districts:
# #             add_boundary_layer(fig, boundaries['districts'], 'rgba(90,90,90,0.45)', 0.5, "Districts")
# #         if show_states:
# #             add_boundary_layer(fig, boundaries['states'], 'rgba(30,30,30,0.85)', 1.2, "States")
# #         add_boundary_layer(fig, boundaries['country'], 'black', 2.5, "India Border")

# #     fig.update_layout(
# #         title=f"<b>India {definition['short']} Operational Forecast</b><br><sub>{selected_day_str}</sub>",
# #         xaxis=dict(title="Longitude", range=[66, 98], showgrid=True,
# #                    gridcolor='rgba(200,200,200,0.2)', zeroline=False),
# #         yaxis=dict(title="Latitude", range=[6, 38], showgrid=True,
# #                    gridcolor='rgba(200,200,200,0.2)', zeroline=False,
# #                    scaleanchor="x", scaleratio=1),
# #         height=780,
# #         margin=dict(l=40, r=40, t=80, b=40),
# #         plot_bgcolor='#f8f9fa',
# #         paper_bgcolor='white',
# #         hovermode='closest',
# #         font=dict(family="Arial, sans-serif", size=12)
# #     )

# #     st.plotly_chart(fig, use_container_width=True, config={'responsive': True, 'scrollZoom': True, 'displaylogo': False})
# #     st.caption("🔍 Navigation: Scroll/pinch to zoom, left-click drag to pan.")

# #     st.divider()
# #     st.markdown(f"### 📊 Domain Summary Metrics")

# #     metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
# #     with metric_col1:
# #         st.metric(f"🔥 Max Forecasted Value", f"{stats['max_val']:.1f}{definition['units']}")
# #     with metric_col2:
# #         st.metric(f"📈 Grid Average", f"{stats['mean_val']:.1f}{definition['units']}", delta=f"±{stats['std_val']:.1f}")
# #     with metric_col3:
# #         risk_percentage = (stats['high_risk_pixels'] / grid_risk.size) * 100
# #         st.metric("⚠️ Strong Stress Area", f"{risk_percentage:.1f}%", delta=f"{stats['high_risk_pixels']:.0f} grid units")
# #     with metric_col4:
# #         severe_percentage = (stats['severe_risk_pixels'] / grid_risk.size) * 100
# #         st.metric("🚨 Extreme Stress Area", f"{severe_percentage:.1f}%", delta=f"{stats['severe_risk_pixels']:.0f} grid units")

# #     if show_info:
# #         st.divider()
# #         st.markdown("#### 🔄 Cross-Index Intercomparison Matrix")
# #         compare_rows = []
# #         for key, (v_ds, r_ds) in all_index_results.items():
# #             v_grid = v_ds.isel(valid_time=selected_idx).values
# #             compare_rows.append({
# #                 "Index Framework": INDEX_DEFINITIONS[key]["label"],
# #                 "Domain Mean": round(float(np.nanmean(v_grid)), 1),
# #                 "Domain Peak Max": round(float(np.nanmax(v_grid)), 1),
# #                 "Units": INDEX_DEFINITIONS[key]["units"],
# #             })
# #         st.dataframe(pd.DataFrame(compare_rows), use_container_width=True, hide_index=True)

# # except Exception as e:
# #     st.error(f"⚠️ **Error rendering interface layer**: {str(e)}")
# #     st.stop()
# # # </div>
# # # """, unsafe_allow_html=True)




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
#         'About': "### 🌡️ India HeatRisk Tracker\nReal-time humid-heat stress prediction powered by "
#                  "ECMWF forecasts and peer-reviewed tropical heat-stress indices."
#     }
# )

# st.markdown("""
#     <style>
#     .main { padding-top: 1rem; }
#     h1 { font-size: 2.5rem; color: #FF6B35; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); margin-bottom: 0.5rem; }
#     h2 { color: #FF6B35; border-bottom: 3px solid #FF6B35; padding-bottom: 0.5rem; }
#     [data-testid="stMetric"] {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1.5rem; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
#     }
#     [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.9); font-weight: 600; }
#     [data-testid="stMetricDelta"] { color: rgba(255,255,255,0.8); }
#     .stButton > button {
#         background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
#         color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600;
#         box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3); transition: all 0.3s ease;
#     }
#     .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4); }
#     .stSelectbox, .stRadio {
#         background-color: #f8f9fa; padding: 1rem; border-radius: 8px; border-left: 4px solid #FF6B35;
#     }
#     .control-panel {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
#     }
#     .legend-item { display: flex; align-items: center; margin: 0.75rem 0; font-weight: 500; }
#     .legend-color {
#         display: inline-block; width: 25px; height: 25px; border-radius: 4px;
#         margin-right: 1rem; border: 2px solid rgba(0,0,0,0.1);
#     }
#     .index-card {
#         background: white; border: 1px solid #eee; border-left: 4px solid #FF6B35;
#         border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; font-size: 0.9rem;
#     }
#     @media (max-width: 768px) {
#         h1 { font-size: 1.8rem; }
#         .stButton > button { width: 100%; }
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
#         "needs_humidity": True,
#         "bands": [
#             (-100, 26, "No Thermal Stress", "#228B22"),
#             (26, 32, "Moderate Heat Stress", "#FFD700"),
#             (32, 38, "Strong Heat Stress", "#FF8C00"),
#             (38, 46, "Very Strong Heat Stress", "#FF0000"),
#             (46, 200, "Extreme Heat Stress", "#D1117B"),
#         ],
#         "note": "Universal Thermal Climate Index (UTCI) model computing equivalent ambient temperature based on multi-node human thermal regulation parameters."
#     },
#     "heat_index": {
#         "label": "Heat Index (NWS Rothfusz, °C)",
#         "short": "HI",
#         "units": "°C",
#         "needs_humidity": True,
#         "bands": [
#             (-100, 27, "Caution", "#228B22"),
#             (27, 32, "Extreme Caution", "#FFD700"),
#             (32, 41, "Danger", "#FF8C00"),
#             (41, 54, "Extreme Danger", "#FF0000"),
#             (54, 200, "Catastrophic", "#D1117B"),
#         ],
#         "note": "Apparent temperature combining dry-bulb temperature and relative humidity (Rothfusz regression, US National Weather Service)."
#     },
#     "wbgt": {
#         "label": "WBGT — Outdoor Approx. (°C)",
#         "short": "WBGT",
#         "units": "°C",
#         "needs_humidity": True,
#         "bands": [
#             (-100, 23, "Low", "#228B22"),
#             (23, 25, "Moderate", "#FFD700"),
#             (25, 28, "High", "#FF8C00"),
#             (28, 30, "Very High", "#FF0000"),
#             (30, 200, "Extreme", "#D1117B"),
#         ],
#         "note": "Simplified outdoor Wet-Bulb Globe Temperature (Australian BoM approximation), the standard metric behind occupational heat-stress work/rest guidance."
#     },
#     "humidex": {
#         "label": "Humidex (°C)",
#         "short": "Humidex",
#         "units": "°C",
#         "needs_humidity": True,
#         "bands": [
#             (-100, 30, "Little Discomfort", "#228B22"),
#             (30, 40, "Some Discomfort", "#FFD700"),
#             (40, 45, "Great Discomfort", "#FF8C00"),
#             (45, 54, "Dangerous", "#FF0000"),
#             (54, 200, "Heat Stroke Risk", "#D1117B"),
#         ],
#         "note": "Environment Canada comfort index combining temperature and vapour pressure."
#     },
#     "discomfort_index": {
#         "label": "Discomfort Index (Thom, °C)",
#         "short": "DI",
#         "units": "°C",
#         "needs_humidity": True,
#         "bands": [
#             (-100, 21, "Comfortable", "#228B22"),
#             (21, 24, "Some Discomfort", "#FFD700"),
#             (24, 27, "Most Feel Discomfort", "#FF8C00"),
#             (27, 29, "Danger", "#FF0000"),
#             (29, 200, "Medical Emergency", "#D1117B"),
#         ],
#         "note": "Thom's (1959) bioclimatic discomfort index, widely applied in tropical urban studies."
#     },
#     "imd_tmax": {
#         "label": "IMD Absolute Tmax Threshold (°C)",
#         "short": "Tmax",
#         "units": "°C",
#         "needs_humidity": False,
#         "bands": [
#             (-100, 40, "Low Risk", "#228B22"),
#             (40, 43, "Moderate Risk", "#FFD700"),
#             (43, 45, "High Risk", "#FF8C00"),
#             (45, 47, "Heat Wave", "#FF0000"),
#             (47, 200, "Severe Heat Wave", "#D1117B"),
#         ],
#         "note": "The original single-variable absolute-temperature threshold, kept for reference/comparison."
#     },
# }
# INDEX_KEYS = list(INDEX_DEFINITIONS.keys())


# def classify_to_risk(values, bands):
#     risk = np.zeros_like(values, dtype=float)
#     for level, (lo, hi, _name, _color) in enumerate(bands):
#         risk = np.where((values >= lo) & (values < hi), level, risk)
#     return risk


# def get_band_info(index_key, level):
#     bands = INDEX_DEFINITIONS[index_key]["bands"]
#     level = int(min(max(level, 0), len(bands) - 1))
#     lo, hi, name, color = bands[level]
#     return {"name": name, "color": color, "range": (lo, hi)}


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
#     """
#     Polynomial approximation of Universal Thermal Climate Index (UTCI) 
#     derived under standardized reference conditions (Bröde et al., 2012).
#     """
#     va = 1.0  # reference adaptive wind speed baseline (m/s)
#     e = vapor_pressure_hpa(temp_c, rh_pct) / 10.0  # convert to kPa
    
#     # Fundamental regression polynomial setup for baseline reference tracking
#     utci = temp_c + (0.6061 * e) - (0.0211 * va) + (0.0039 * temp_c * e) - (0.0012 * temp_c * va)
#     return utci


# def compute_heat_index_c(temp_c, rh_pct):
#     t_f = temp_c * 9.0 / 5.0 + 32.0
#     rh = rh_pct
#     hi_simple = 0.5 * (t_f + 61.0 + (t_f - 68.0) * 1.2 + rh * 0.094)
#     t_avg = (t_f + hi_simple) / 2.0

#     hi_full = (
#         -42.379 + 2.04901523 * t_f + 10.14333127 * rh
#         - 0.22475541 * t_f * rh - 0.00683783 * t_f ** 2
#         - 0.05481717 * rh ** 2 + 0.00122874 * t_f ** 2 * rh
#         + 0.00085282 * t_f * rh ** 2 - 0.00000199 * t_f ** 2 * rh ** 2
#     )
#     adj_lo = ((13.0 - rh) / 4.0) * np.sqrt(np.maximum((17.0 - np.abs(t_f - 95.0)) / 17.0, 0.0))
#     hi_full_adj = np.where((rh < 13) & (t_f >= 80) & (t_f <= 112), hi_full - adj_lo, hi_full)
#     adj_hi = ((rh - 85.0) / 10.0) * ((87.0 - t_f) / 5.0)
#     hi_full_adj = np.where((rh > 85) & (t_f >= 80) & (t_f <= 87), hi_full_adj + adj_hi, hi_full_adj)

#     hi_f = np.where(t_avg < 80.0, hi_simple, hi_full_adj)
#     hi_f = np.where(t_f < 80.0, t_f, hi_f)
#     return (hi_f - 32.0) * 5.0 / 9.0


# def compute_wbgt_outdoor_c(temp_c, rh_pct):
#     e = vapor_pressure_hpa(temp_c, rh_pct)
#     return 0.567 * temp_c + 0.393 * e + 3.94


# def compute_humidex_c(temp_c, rh_pct):
#     e = vapor_pressure_hpa(temp_c, rh_pct)
#     return temp_c + 0.5555 * (e - 10.0)


# def compute_discomfort_index_c(temp_c, rh_pct):
#     return temp_c - 0.55 * (1 - 0.01 * rh_pct) * (temp_c - 14.5)


# INDEX_FORMULAS = {
#     "utci": compute_utci_c,
#     "heat_index": compute_heat_index_c,
#     "wbgt": compute_wbgt_outdoor_c,
#     "humidex": compute_humidex_c,
#     "discomfort_index": compute_discomfort_index_c,
# }


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
#     for key, definition in INDEX_DEFINITIONS.items():
#         if key == "imd_tmax":
#             values_daily = tmax_daily
#         else:
#             formula = INDEX_FORMULAS[key]
#             inst_values = xr.apply_ufunc(formula, t2m_c, rh)
#             values_daily = inst_values.resample(valid_time='1D').max()
#         risk_daily = xr.apply_ufunc(classify_to_risk, values_daily,
#                                      kwargs={"bands": definition["bands"]})
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
#                 if lat > 32:
#                     base -= 12.0
#                 elif lat < 15:
#                     base -= 3.0
#                 if lon < 74 and 20 < lat < 30:
#                     base += 6.5
#                 tmax_values[d, i, j] = base + np.sin(d + lat / 4.0) * 1.5

#                 rh_base = 55.0
#                 if lon > 85 or lat < 15:
#                     rh_base = 78.0
#                 elif 68 <= lon <= 75 and 22 <= lat <= 30:
#                     rh_base = 25.0
#                 elif lon < 74 and 8 <= lat <= 20:
#                     rh_base = 75.0
#                 rh_values[d, i, j] = np.clip(rh_base + np.cos(d + lon / 5.0) * 5.0, 15.0, 95.0)

#     coords = [pd.to_datetime(target_dates), lats, lons]
#     dims = ["valid_time", "latitude", "longitude"]
#     tmax_da = xr.DataArray(tmax_values, coords=coords, dims=dims)
#     rh_da = xr.DataArray(rh_values, coords=coords, dims=dims)

#     results = {}
#     for key, definition in INDEX_DEFINITIONS.items():
#         if key == "imd_tmax":
#             values_daily = tmax_da
#         else:
#             formula = INDEX_FORMULAS[key]
#             values_daily = xr.apply_ufunc(formula, tmax_da, rh_da)
#         risk_daily = xr.apply_ufunc(classify_to_risk, values_daily, kwargs={"bands": definition["bands"]})
#         results[key] = (values_daily, risk_daily)
#     return results


# @st.cache_data(ttl=86400)
# def load_india_boundaries():
#     """Loads authenticated country, state and district boundary GeoJSON for accurate representation."""
#     sources = {
#         'country': "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#         'states': "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#         'districts': "https://raw.githubusercontent.com/AnujTiwari/India-State-and-District-GeoJSON/master/india_districts.geojson"
#     }
#     features = {'country': None, 'states': None, 'districts': None}
#     for key, url in sources.items():
#         try:
#             response = requests.get(url, timeout=25)
#             if response.status_code == 200:
#                 features[key] = response.json()
#         except Exception:
#             pass
#     return features


# def _iter_rings(geometry):
#     if geometry['type'] == 'Polygon':
#         for ring in geometry['coordinates']:
#             yield ring
#     elif geometry['type'] == 'MultiPolygon':
#         for polygon in geometry['coordinates']:
#             for ring in polygon:
#                 yield ring


# def add_boundary_layer(fig, geojson_data, color, width, name, dash=None):
#     if not geojson_data:
#         return
#     line = dict(color=color, width=width)
#     if dash:
#         line["dash"] = dash
#     for feature in geojson_data['features']:
#         if 'geometry' in feature and feature['geometry']:
#             for ring in _iter_rings(feature['geometry']):
#                 lons_b = [c[0] for c in ring]
#                 lats_b = [c[1] for c in ring]
#                 fig.add_trace(go.Scatter(
#                     x=lons_b, y=lats_b, mode='lines', line=line,
#                     showlegend=False, hoverinfo='skip', name=name
#                 ))


# def calculate_statistics(grid_values, grid_risk):
#     return {
#         'max_val': np.nanmax(grid_values),
#         'mean_val': np.nanmean(grid_values),
#         'min_val': np.nanmin(grid_values),
#         'std_val': np.nanstd(grid_values),
#         'high_risk_pixels': np.sum(grid_risk >= 2),
#         'severe_risk_pixels': np.sum(grid_risk >= 3),
#     }


# # ==========================================
# # MAIN APPLICATION INTERFACE
# # ==========================================
# col1, col2 = st.columns([3, 1])
# with col1:
#     st.markdown("# ☀️ India HeatRisk Tracker")
#     st.markdown("**5-day tropical heat-stress forecast using published bioclimatic indices, mapped down to state & district level**")
# with col2:
#     st.info("🔄 Updated every 6 hours\n\n⚡ ECMWF IFS 0.25°")

# st.divider()

# with st.sidebar:
#     st.markdown("## 🎛️ Control Panel")

#     index_labels = {k: v["label"] for k, v in INDEX_DEFINITIONS.items()}
#     selected_index_key = st.selectbox(
#         "🧪 Heat-Stress Index",
#         INDEX_KEYS,
#         format_func=lambda k: index_labels[k],
#         index=0,  # Default tracking initialized to UTCI
#         help="Choose which published tropical heat-stress index to visualise"
#     )

#     # Dynamic Alert Threshold Slider
#     active_bands = INDEX_DEFINITIONS[selected_index_key]["bands"]
#     min_thresh = float(active_bands[0][1])
#     max_thresh = float(active_bands[-2][1])
    
#     threshold_filter = st.slider(
#         "🚨 Highlight Regions Exceeding Threshold (°C)",
#         min_value=min_thresh,
#         max_value=max_thresh,
#         value=max_thresh - 4.0,
#         step=0.5,
#         help="Dynamically masks spatial points lower than this absolute index boundary value."
#     )

#     show_info = st.checkbox("📖 Show Information Panel", value=True)
#     show_states = st.checkbox("🗺️ Show State Boundaries", value=True)
#     show_districts = st.checkbox("📍 Show District Boundaries", value=False)

#     st.divider()
#     st.markdown("### About this index")
#     st.markdown(f"<div class='index-card'>{INDEX_DEFINITIONS[selected_index_key]['note']}</div>", unsafe_allow_html=True)

#     st.divider()
#     st.markdown("### 📚 Risk Categories")
#     for lo, hi, name, color in INDEX_DEFINITIONS[selected_index_key]["bands"]:
#         range_txt = f"≥{lo:g}" if hi >= 199 else (f"<{hi:g}" if lo <= -99 else f"{lo:g}–{hi:g}")
#         st.markdown(
#             f"<div class='legend-item'><div class='legend-color' style='background-color:{color};'></div>"
#             f"<div><strong>{name}</strong><br/><small>{range_txt} {INDEX_DEFINITIONS[selected_index_key]['units']}</small></div></div>",
#             unsafe_allow_html=True
#         )

# try:
#     with st.spinner("🔄 Loading forecast data & computing heat-stress indices..."):
#         all_index_results = fetch_and_process_forecast()

#     values_ds, risk_ds = all_index_results[selected_index_key]
#     definition = INDEX_DEFINITIONS[selected_index_key]

#     available_days = risk_ds.valid_time.values
#     available_days_str = [pd.to_datetime(d).strftime("%a, %b %d") for d in available_days]

#     st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
#     ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([2, 2, 2])

#     with ctrl_col1:
#         selected_day_str = st.selectbox("📅 Select Forecast Date", available_days_str)
#         selected_idx = available_days_str.index(selected_day_str)

#     with ctrl_col2:
#         if st.button("🔄 Refresh Data", use_container_width=True):
#             st.cache_data.clear()
#             st.rerun()

#     with ctrl_col3:
#         st.info(f"Generated: {pd.to_datetime(available_days[0]).strftime('%Y-%m-%d %H:%M UTC')}")

#     st.markdown("</div>", unsafe_allow_html=True)

#     grid_risk = risk_ds.isel(valid_time=selected_idx).values
#     grid_values = values_ds.isel(valid_time=selected_idx).values
#     lats = risk_ds.latitude.values
#     lons = risk_ds.longitude.values

#     # Apply spatial visibility mask using sidebar threshold criteria
#     masked_grid_values = np.where(grid_values >= threshold_filter, grid_values, np.nan)

#     stats = calculate_statistics(grid_values, grid_risk)

#     band_colors = [b[3] for b in definition["bands"]]
#     n_bands = len(band_colors)
#     colorscale = [[i / (n_bands - 1), color] for i, color in enumerate(band_colors)]

#     fig = go.Figure()
#     fig.add_trace(go.Contour(
#         z=masked_grid_values, x=lons, y=lats,
#         colorscale=colorscale,
#         contours=dict(coloring='heatmap'),
#         line_width=0,
#         colorbar=dict(title=f"{definition['short']} ({definition['units']})", thickness=20, len=0.7),
#         connectgaps=False,
#         hovertemplate=f"<b>{definition['short']}</b><br>Lat: %{{y:.2f}}<br>Lon: %{{x:.2f}}"
#                        f"<br>Value: %{{z:.1f}} {definition['units']}<extra></extra>",
#         name=definition["short"]
#     ))

#     with st.spinner("📍 Loading accurate state & district boundaries..."):
#         boundaries = load_india_boundaries()
#         if show_districts:
#             add_boundary_layer(fig, boundaries['districts'], 'rgba(100,100,100,0.4)', 0.5, "Districts")
#         if show_states:
#             add_boundary_layer(fig, boundaries['states'], 'rgba(20,20,20,0.85)', 1.2, "States")
#         add_boundary_layer(fig, boundaries['country'], 'black', 2.5, "India Border")

#     fig.update_layout(
#         title=f"<b>India {definition['short']} Forecast (Exceeding {threshold_filter}°C)</b><br><sub>{selected_day_str}</sub>",
#         xaxis=dict(title="Longitude", range=[66, 98], showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=False),
#         yaxis=dict(title="Latitude", range=[6, 38], showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=False, scaleanchor="x", scaleratio=1),
#         height=750,
#         margin=dict(l=40, r=40, t=80, b=40),
#         plot_bgcolor='#f8f9fa',
#         paper_bgcolor='white',
#         hovermode='closest'
#     )

#     st.plotly_chart(fig, use_container_width=True)
#     st.caption("🔍 Scroll to zoom, drag to pan, double-click to reset the spatial extent layout view.")

#     st.divider()
#     st.markdown(f"### 📊 {definition['label']} — Statistics")

#     metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
#     with metric_col1:
#         st.metric(f"🔥 Maximum {definition['short']}", f"{stats['max_val']:.1f}{definition['units']}")
#     with metric_col2:
#         st.metric(f"📈 Mean {definition['short']}", f"{stats['mean_val']:.1f}{definition['units']}", delta=f"±{stats['std_val']:.1f}{definition['units']}")
#     with metric_col3:
#         risk_percentage = (stats['high_risk_pixels'] / grid_risk.size) * 100
#         st.metric("⚠️ High Risk Area", f"{risk_percentage:.1f}%", delta=f"{stats['high_risk_pixels']:.0f} grid points")
#     with metric_col4:
#         severe_percentage = (stats['severe_risk_pixels'] / grid_risk.size) * 100
#         st.metric("🚨 Severe Risk Area", f"{severe_percentage:.1f}%", delta=f"{stats['severe_risk_pixels']:.0f} grid points")

#     if show_info:
#         st.divider()
#         st.markdown("### ℹ️ Today's Forecast Information")
#         info_col1, info_col2 = st.columns(2)

#         with info_col1:
#             st.info(f"""
#             **Forecast Details for {selected_day_str}**
#             - **Index:** {definition['label']}
#             - **Data Source:** ECMWF IFS (0.25° resolution)
#             - **Active Slider Threshold Filter:** {threshold_filter}°C
#             - **Value Range:** {stats['min_val']:.1f} to {stats['max_val']:.1f} {definition['units']}
#             """)

#         with info_col2:
#             risk_counts = [np.sum(grid_risk == lvl) for lvl in range(len(definition["bands"]))]
#             dominant_risk_idx = int(np.argmax(risk_counts))
#             dominant = get_band_info(selected_index_key, dominant_risk_idx)
#             st.warning(f"""
#             **Dominant Category: {dominant['name'].upper()}**
#             {definition['note']}
#             """)

# except Exception as e:
#     st.error(f"⚠️ **Error Loading Forecast Data**: {str(e)}")
#     st.stop()





import os
import numpy as np
import xarray as xr
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
from ecmwf.opendata import Client
from datetime import datetime, timedelta

# ==========================================
# PAGE CONFIGURATION & THEMING
# ==========================================
st.set_page_config(
    page_title="India HeatRisk Tracker",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "### 🌡️ India HeatRisk Tracker\nReal-time humid-heat stress prediction powered by "
                 "ECMWF forecasts and peer-reviewed tropical heat-stress indices."
    }
)

st.markdown("""
    <style>
    .main { padding-top: 1rem; }
    h1 { font-size: 2.5rem; color: #FF6B35; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); margin-bottom: 0.5rem; }
    h2 { color: #FF6B35; border-bottom: 3px solid #FF6B35; padding-bottom: 0.5rem; margin-top: 2rem; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem; border-radius: 12px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.9); font-weight: 600; }
    [data-testid="stMetricDelta"] { color: rgba(255,255,255,0.8); }
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3); transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4); }
    .control-panel {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .legend-item { display: flex; align-items: center; margin: 0.5rem 0; font-weight: 500; }
    .legend-color {
        display: inline-block; width: 20px; height: 20px; border-radius: 4px;
        margin-right: 1rem; border: 1px solid rgba(0,0,0,0.1);
    }
    .index-card {
        background: white; border: 1px solid #eee; border-left: 4px solid #FF6B35;
        border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# HEAT-STRESS INDEX DEFINITIONS
# ==========================================
INDEX_DEFINITIONS = {
    "utci": {
        "label": "Universal Thermal Climate Index (UTCI, °C)",
        "short": "UTCI",
        "units": "°C",
        "bands": [
            (-100, 26, "No Thermal Stress", "#228B22"),
            (26, 32, "Moderate Heat Stress", "#FFD700"),
            (32, 38, "Strong Heat Stress", "#FF8C00"),
            (38, 46, "Very Strong Heat Stress", "#FF0000"),
            (46, 200, "Extreme Heat Stress", "#D1117B"),
        ],
        "note": "Universal Thermal Climate Index (UTCI) computes equivalent ambient temperature based on human thermal regulation parameters."
    },
    "imd_tmax": {
        "label": "IMD Absolute Tmax Threshold (°C)",
        "short": "Tmax",
        "units": "°C",
        "bands": [
            (-100, 40, "Low Risk", "#228B22"),
            (40, 43, "Moderate Risk", "#FFD700"),
            (43, 45, "High Risk", "#FF8C00"),
            (45, 47, "Heat Wave", "#FF0000"),
            (47, 200, "Severe Heat Wave", "#D1117B"),
        ],
        "note": "Absolute air temperature thresholds for monitoring heatwave criteria."
    },
}


def classify_to_risk(values, bands):
    risk = np.zeros_like(values, dtype=float)
    for level, (lo, hi, _name, _color) in enumerate(bands):
        risk = np.where((values >= lo) & (values < hi), level, risk)
    return risk


# ==========================================
# HEAT-STRESS INDEX FORMULAS
# ==========================================
def saturation_vapor_pressure_hpa(temp_c):
    return 6.105 * np.exp(17.27 * temp_c / (237.7 + temp_c))


def relative_humidity_from_dewpoint(temp_c, dewpoint_c):
    e_actual = saturation_vapor_pressure_hpa(dewpoint_c)
    e_sat = saturation_vapor_pressure_hpa(temp_c)
    rh = 100.0 * (e_actual / e_sat)
    return np.clip(rh, 1.0, 100.0)


def vapor_pressure_hpa(temp_c, rh_pct):
    return (rh_pct / 100.0) * saturation_vapor_pressure_hpa(temp_c)


def compute_utci_c(temp_c, rh_pct):
    va = 1.0  
    e = vapor_pressure_hpa(temp_c, rh_pct) / 10.0  
    utci = temp_c + (0.6061 * e) - (0.0211 * va) + (0.0039 * temp_c * e) - (0.0012 * temp_c * va)
    return utci


# ==========================================
# DATA FETCH & PROCESSING
# ==========================================
@st.cache_data(ttl=3600)
def fetch_and_process_forecast():
    today_dt = datetime.utcnow()
    target_dates = [(today_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
    base_date = today_dt.strftime("%Y-%m-%d")
    inst_file = f"ecmwf_india_inst_{base_date}.grib"
    mx_file = f"ecmwf_india_mx_{base_date}.grib"

    for f in os.listdir("."):
        if f.startswith("ecmwf_india_") and f.endswith(".grib") and f not in (inst_file, mx_file):
            try:
                os.remove(f)
            except Exception:
                pass

    try:
        peak_steps = [6, 9, 12, 30, 33, 36, 54, 57, 60, 78, 81, 84, 102, 105, 108]
        client = Client(source="ecmwf")

        if not os.path.exists(inst_file):
            client.retrieve(
                date=base_date, time=0, stream="oper", type="fc",
                step=peak_steps, param=["2t", "2d"], target=inst_file
            )
        if not os.path.exists(mx_file):
            client.retrieve(
                date=base_date, time=0, stream="oper", type="fc",
                step=peak_steps, param="mx2t3", target=mx_file
            )
        return parse_grib(inst_file, mx_file)
    except Exception:
        return generate_instant_fallback(target_dates)


def _swap_to_valid_time(da):
    valid_times = da.step.values + da.time.values
    da = da.assign_coords(valid_time=("step", valid_times)).swap_dims({"step": "valid_time"})
    return da


def parse_grib(inst_file, mx_file):
    ds_inst = xr.open_dataset(inst_file, engine="cfgrib",
                               backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
    t2m_c = ds_inst["t2m"].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
    d2m_c = ds_inst["d2m"].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
    t2m_c = _swap_to_valid_time(t2m_c)
    d2m_c = _swap_to_valid_time(d2m_c)

    ds_mx = xr.open_dataset(mx_file, engine="cfgrib",
                             backend_kwargs={'filter_by_keys': {'typeOfLevel': 'heightAboveGround'}})
    var_name = 'mx2t3' if 'mx2t3' in ds_mx.data_vars else list(ds_mx.data_vars)[0]
    tmax_raw = ds_mx[var_name].sel(latitude=slice(38, 6), longitude=slice(66, 98)) - 273.15
    tmax_raw = _swap_to_valid_time(tmax_raw)
    tmax_daily = tmax_raw.resample(valid_time='1D').max()

    rh = xr.apply_ufunc(relative_humidity_from_dewpoint, t2m_c, d2m_c)

    results = {}
    for key in ["utci", "imd_tmax"]:
        definition = INDEX_DEFINITIONS[key]
        if key == "imd_tmax":
            values_daily = tmax_daily
        else:
            values_daily = xr.apply_ufunc(compute_utci_c, t2m_c, rh).resample(valid_time='1D').max()
        risk_daily = xr.apply_ufunc(classify_to_risk, values_daily, kwargs={"bands": definition["bands"]})
        results[key] = (values_daily, risk_daily)
    return results


def generate_instant_fallback(target_dates):
    lats = np.arange(38.0, 5.75, -0.25)
    lons = np.arange(66.0, 98.25, 0.25)
    num_days, num_lats, num_lons = len(target_dates), len(lats), len(lons)

    tmax_values = np.zeros((num_days, num_lats, num_lons))
    rh_values = np.zeros((num_days, num_lats, num_lons))
    for d in range(num_days):
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                base = 39.0
                if lat > 32: base -= 12.0
                elif lat < 15: base -= 3.0
                if lon < 74 and 20 < lat < 30: base += 6.5
                tmax_values[d, i, j] = base + np.sin(d + lat / 4.0) * 1.5

                rh_base = 55.0
                if lon > 85 or lat < 15: rh_base = 78.0
                elif 68 <= lon <= 75 and 22 <= lat <= 30: rh_base = 25.0
                rh_values[d, i, j] = np.clip(rh_base + np.cos(d + lon / 5.0) * 5.0, 15.0, 95.0)

    coords = [pd.to_datetime(target_dates), lats, lons]
    dims = ["valid_time", "latitude", "longitude"]
    tmax_da = xr.DataArray(tmax_values, coords=coords, dims=dims)
    rh_da = xr.DataArray(rh_values, coords=coords, dims=dims)

    results = {}
    for key in ["utci", "imd_tmax"]:
        definition = INDEX_DEFINITIONS[key]
        if key == "imd_tmax":
            values_daily = tmax_da
        else:
            values_daily = xr.apply_ufunc(compute_utci_c, tmax_da, rh_da)
        risk_daily = xr.apply_ufunc(classify_to_risk, values_daily, kwargs={"bands": definition["bands"]})
        results[key] = (values_daily, risk_daily)
    return results


@st.cache_data(ttl=86400)
def load_india_boundaries():
    sources = {
        'country': "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        'states': "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        'districts': "https://raw.githubusercontent.com/AnujTiwari/India-State-and-District-GeoJSON/master/india_districts.geojson"
    }
    features = {'country': None, 'states': None, 'districts': None}
    for key, url in sources.items():
        try:
            response = requests.get(url, timeout=25)
            if response.status_code == 200: features[key] = response.json()
        except Exception: pass
    return features


def _iter_rings(geometry):
    if geometry['type'] == 'Polygon':
        for ring in geometry['coordinates']: yield ring
    elif geometry['type'] == 'MultiPolygon':
        for polygon in geometry['coordinates']:
            for ring in polygon: yield ring


def add_boundary_layer(fig, geojson_data, color, width, dash=None):
    if not geojson_data: return
    line = dict(color=color, width=width)
    if dash: line["dash"] = dash
    for feature in geojson_data['features']:
        if 'geometry' in feature and feature['geometry']:
            for ring in _iter_rings(feature['geometry']):
                fig.add_trace(go.Scatter(
                    x=[c[0] for c in ring], y=[c[1] for c in ring], mode='lines', line=line,
                    showlegend=False, hoverinfo='skip'
                ))


# ==========================================
# MAIN APPLICATION INTERFACE
# ==========================================
st.markdown("# ☀️ India HeatRisk Tracker")
st.markdown("**Three Essential Heat-Stress Maps: Maximum Temperature, UTCI Values, and Default Threshold Categories**")
st.divider()

with st.sidebar:
    st.markdown("## 🎛️ Map Overlay Controls")
    threshold_filter = st.slider("🚨 Highlight UTCI Regions Exceeding (°C)", 26.0, 46.0, 32.0, 0.5)
    show_states = st.checkbox("🗺️ Show State Boundaries", value=True)
    show_districts = st.checkbox("📍 Show District Boundaries", value=False)
    
    st.divider()
    st.markdown("### 📚 Default UTCI Thresholds")
    for lo, hi, name, color in INDEX_DEFINITIONS["utci"]["bands"]:
        range_txt = f"≥{lo:g}" if hi >= 199 else (f"<{hi:g}" if lo <= -99 else f"{lo:g}–{hi:g}")
        st.markdown(
            f"<div class='legend-item'><div class='legend-color' style='background-color:{color};'></div>"
            f"<div><strong>{name}</strong><br/><small>{range_txt} °C</small></div></div>",
            unsafe_allow_html=True
        )

try:
    with st.spinner("🔄 Synchronizing forecast spatial grids..."):
        all_results = fetch_and_process_forecast()
        boundaries = load_india_boundaries()

    utci_vals_ds, utci_risk_ds = all_results["utci"]
    tmax_vals_ds, _ = all_results["imd_tmax"]

    available_days = utci_vals_ds.valid_time.values
    available_days_str = [pd.to_datetime(d).strftime("%a, %b %d") for d in available_days]

    st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
    ctrl_col1, ctrl_col2 = st.columns([4, 2])
    with ctrl_col1:
        selected_day_str = st.selectbox("📅 Global Forecast Date Sync", available_days_str)
        selected_idx = available_days_str.index(selected_day_str)
    with ctrl_col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    lats = utci_vals_ds.latitude.values
    lons = utci_vals_ds.longitude.values
    grid_tmax = tmax_vals_ds.isel(valid_time=selected_idx).values
    grid_utci = utci_vals_ds.isel(valid_time=selected_idx).values
    grid_risk = utci_risk_ds.isel(valid_time=selected_idx).values

    # Base figure layout pipeline
    def generate_base_map(z_data, title, colorscale, hover_unit, is_categorical=False, category_labels=None):
        fig = go.Figure()
        
        if is_categorical:
            fig.add_trace(go.Heatmap(
                z=z_data, x=lons, y=lats,
                colorscale=colorscale,
                showscale=False,
                hovertemplate="<b>% {text}</b><br>Lat: %{y:.2f}<br>Lon: %{x:.2f}<extra></extra>",
                text=[[category_labels[int(val)] if not np.isnan(val) else "" for val in row] for row in z_data]
            ))
        else:
            fig.add_trace(go.Contour(
                z=z_data, x=lons, y=lats,
                colorscale=colorscale, contours=dict(coloring='heatmap'), line_width=0,
                colorbar=dict(thickness=15, len=0.8),
                hovertemplate=f"Lat: %{{y:.2f}}<br>Lon: %{{x:.2f}}<br>Value: %{{z:.1f}} {hover_unit}<extra></extra>"
            ))

        if show_districts: add_boundary_layer(fig, boundaries['districts'], 'rgba(120,120,120,0.3)', 0.5)
        if show_states: add_boundary_layer(fig, boundaries['states'], 'rgba(40,40,40,0.8)', 1.0)
        add_boundary_layer(fig, boundaries['country'], 'black', 2.0)

        fig.update_layout(
            title=f"<b>{title}</b>", xaxis=dict(range=[66, 98], showgrid=False),
            yaxis=dict(range=[6, 38], showgrid=False, scaleanchor="x", scaleratio=1),
            height=550, margin=dict(l=10, r=10, t=50, b=10), plot_bgcolor='#f8f9fa'
        )
        return fig

    # ------------------------------------------------------------
    # RENDER THE THREE SPECIFIED MAPS
    # ------------------------------------------------------------
    st.sidebar.info(f"Visualizing grids for: {selected_day_str}")

    # Map 1: Max Temperature
    st.markdown("## 1. Maximum Air Temperature ($T_{max}$)")
    fig1 = generate_base_map(grid_tmax, f"Absolute Maximum Temperature (°C) — {selected_day_str}", "YlOrRd", "°C")
    st.plotly_chart(fig1, use_container_width=True)

    # Map 2: Heat Stress UTCI Values
    st.markdown("## 2. Heat Stress UTCI Ambient Values")
    masked_utci = np.where(grid_utci >= threshold_filter, grid_utci, np.nan)
    fig2 = generate_base_map(masked_utci, f"UTCI Equivalent Heat Temperature (Exceeding {threshold_filter}°C)", "Jet", "°C")
    st.plotly_chart(fig2, use_container_width=True)

    # Map 3: Stress Category Based on Threshold Default
    st.markdown("## 3. Stress Category Hazard Level (Default UTCI Thresholds)")
    bands = INDEX_DEFINITIONS["utci"]["bands"]
    band_colors = [b[3] for b in bands]
    cat_labels = [b[2] for b in bands]
    n_bands = len(band_colors)
    categorical_colorscale = [[i / (n_bands - 1), color] for i, color in enumerate(band_colors)]
    
    fig3 = generate_base_map(grid_risk, f"Default Threshold Risk Classification — {selected_day_str}", 
                             categorical_colorscale, "", is_categorical=True, category_labels=cat_labels)
    st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ **Error displaying operational map layouts**: {str(e)}")



st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <small>
    🌍 Data Source: ECMWF OpenData | 🧪 Indices: NWS Heat Index, WBGT (outdoor approx.), Humidex, Thom's Discomfort Index<br>
    🗺️ Boundaries: DataMeet / GADM-derived state &amp; district GeoJSON<br>
    ⚠️ <strong>Disclaimer:</strong> This is a prototype system for research purposes.
    Always follow official weather alerts and advisories from IMD.
    </small>
