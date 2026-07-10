import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STYLE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Retail Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom css to polish metrics and general card aesthetics
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #dee2e6;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #1e3d59;
    }
    .metric-label {
        font-size: 14px;
        color: #6c757d;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. EMBEDDED FALLBACK DATASETS
# -----------------------------------------------------------------------------
# Embedded Store Master reference dataset
STORE_MASTER_CSV = """store_id,store_name,region,city,store_format
ST-001,Delhi Retail Hub,North,Delhi,High Street
ST-002,Jaipur Retail Hub,North,Jaipur,Neighborhood
ST-003,Lucknow Retail Hub,North,Lucknow,Outlet
ST-004,Chandigarh Retail Hub,North,Chandigarh,Mall
ST-005,Bengaluru Retail Hub,South,Bengaluru,High Street
ST-006,Chennai Retail Hub,South,Chennai,Neighborhood
ST-007,Hyderabad Retail Hub,South,Hyderabad,Outlet
ST-008,Kochi Retail Hub,South,Kochi,Mall
ST-009,Kolkata Retail Hub,East,Kolkata,High Street
ST-010,Bhubaneswar Retail Hub,East,Bhubaneswar,Neighborhood
ST-011,Guwahati Retail Hub,East,Guwahati,Outlet
ST-012,Patna Retail Hub,East,Patna,Mall
ST-013,Mumbai Retail Hub,West,Mumbai,High Street
ST-014,Pune Retail Hub,West,Pune,Neighborhood
ST-015,Ahmedabad Retail Hub,West,Ahmedabad,Outlet
ST-016,Surat Retail Hub,West,Surat,Mall
ST-017,Bhopal Retail Hub,Central,Bhopal,High Street
ST-018,Indore Retail Hub,Central,Indore,Neighborhood
ST-019,Nagpur Retail Hub,Central,Nagpur,Outlet
ST-020,Raipur Retail Hub,Central,Raipur,Mall"""

# Embed partial data from your CSV string to provide an immediate out-of-the-box load
RETAIL_WEEKLY_SALES_CSV = """week_start_date,region,store_id,store_name,city,store_format,product_category,footfall,transactions,units_sold,gross_sales,discount_amount,net_sales,sales_target,inventory_on_hand,stockouts,returns_amount,customer_rating,marketing_spend
05-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Grocery,2315,648,972,18195.84,2001.54,15830.38,20743.26,736,0,363.92,5,1628
05-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Apparel,2243,561,1683,74220.3,5937.62,56926.97,79415.72,239,1,11355.71,3.5,1927
05-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Electronics,802,209,418,93046.8,4652.34,79601.53,93046.8,271,2,8792.93,3.9,2226
05-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Home,1625,569,569,39573.95,7914.79,29680.46,36803.77,745,3,1978.7,4.3,2525
05-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Beauty,2016,444,1110,33566.4,5706.29,26853.12,38937.02,248,4,1006.99,4.7,2824
05-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Sports,1007,272,408,24459.6,3424.34,20790.66,26660.96,501,5,244.6,3.2,3123
05-01-2026,North,ST-002,Jaipur Retail Hub,Jaipur,Neighborhood,Grocery,2719,789,789,14344.02,2008.16,11331.78,14774.34,195,5,1004.08,5,1875
05-01-2026,North,ST-002,Jaipur Retail Hub,Jaipur,Neighborhood,Apparel,1166,303,758,32472.72,3572,26140.53,31173.81,448,6,2760.19,3.5,2174
05-01-2026,North,ST-002,Jaipur Retail Hub,Jaipur,Neighborhood,Electronics,1012,273,410,88683,7094.64,77996.7,78927.87,386,7,3591.66,3.5,2473
05-01-2026,North,ST-002,Jaipur Retail Hub,Jaipur,Neighborhood,Home,1948,351,1053,71182.8,3559.14,66911.83,79724.74,204,0,711.83,4.3,2772
05-01-2026,North,ST-002,Jaipur Retail Hub,Jaipur,Neighborhood,Beauty,939,216,432,12700.8,2540.16,9144.58,13335.84,457,1,1016.06,4.7,3071
05-01-2026,North,ST-002,Jaipur Retail Hub,Jaipur,Neighborhood,Sports,1330,372,372,21687.6,3686.89,16699.45,21253.85,710,2,1301.26,3.2,3370
05-01-2026,North,ST-003,Lucknow Retail Hub,Lucknow,Outlet,Grocery,1372,412,1236,21803.04,3706.52,17442.43,20058.8,404,2,654.09,5,2122
05-01-2026,North,ST-003,Lucknow Retail Hub,Lucknow,Outlet,Apparel,1489,402,804,33430.32,4680.24,28181.77,38444.87,657,3,568.31,3.5,2421
05-01-2026,North,ST-003,Lucknow Retail Hub,Lucknow,Outlet,Electronics,1222,342,342,71820,7900.2,56163.24,77565.6,88,8,7756.56,3.5,2720
05-01-2026,North,ST-003,Lucknow Retail Hub,Lucknow,Outlet,Home,2271,431,1078,70770.7,5661.66,60862.8,71478.41,413,5,4246.24,4.3,3019
05-01-2026,North,ST-003,Lucknow Retail Hub,Lucknow,Outlet,Beauty,1262,303,454,12966.24,648.31,11799.28,12188.27,666,6,518.65,4.7,3318
05-01-2026,North,ST-003,Lucknow Retail Hub,Lucknow,Outlet,Sports,1653,479,1437,81406.05,16281.21,,95245.08,169,11,1628.12,2.8,3617
05-01-2026,North,ST-004,Chandigarh Retail Hub,Chandigarh,Mall,Grocery,1776,551,1378,23563.8,4712.76,16965.94,26155.82,613,7,1885.1,4.6,2369
05-01-2026,North,ST-004,Chandigarh Retail Hub,Chandigarh,Mall,Apparel,1812,507,760,30643.2,5209.34,22308.26,31868.93,866,0,3125.6,3.5,2668
05-01-2026,North,ST-004,Chandigarh Retail Hub,Chandigarh,Mall,Electronics,1432,415,1245,253606.5,35504.91,204406.84,245998.3,203,1,13694.75,3.9,2967
05-01-2026,North,ST-004,Chandigarh Retail Hub,Chandigarh,Mall,Home,1194,239,478,30448.6,3349.35,26490.28,27403.74,622,2,608.97,4.3,3266
05-01-2026,North,ST-004,Chandigarh Retail Hub,Chandigarh,Mall,Beauty,1585,396,396,10977.12,878.17,9111.01,12404.15,125,7,987.94,4.3,3565
05-01-2026,North,ST-004,Chandigarh Retail Hub,Chandigarh,Mall,Sports,1976,593,1482,81510,4075.5,71728.8,86400.6,378,4,5705.7,3.2,3864
05-01-2026,South,ST-005,Bengaluru Retail Hub,Bengaluru,High Street,Grocery,2180,698,1396,23117.76,1155.89,21037.16,23117.76,822,4,924.71,5,2616
05-01-2026,South,ST-005,Bengaluru Retail Hub,Bengaluru,High Street,Apparel,2135,619,619,24178.14,4835.63,18520.46,22485.67,325,5,822.05,3.5,2915
05-01-2026,South,ST-005,Bengaluru Retail Hub,Bengaluru,High Street,Electronics,732,220,550,108570,18456.9,76921.84,125941.2,318,6,13191.26,3.9,3214
05-01-2026,South,ST-005,Bengaluru Retail Hub,Bengaluru,High Street,Home,1517,319,478,29516.5,4132.31,23318.03,32172.98,831,7,2066.16,3.9,3513
05-01-2026,South,ST-005,Bengaluru Retail Hub,Bengaluru,High Street,Beauty,1908,496,1488,39997.44,4399.72,33597.85,40797.39,334,0,1999.87,4.7,3812
05-01-2026,South,ST-005,Bengaluru Retail Hub,Bengaluru,High Street,Sports,2299,713,1426,76077.1,6086.17,67708.62,72273.24,587,1,2282.31,3.2,4111
05-01-2026,South,ST-006,Chennai Retail Hub,Chennai,Neighborhood,Grocery,2584,853,1280,25574.4,2045.95,21226.75,22761.22,281,1,2301.7,5,2863
05-01-2026,South,ST-006,Chennai Retail Hub,Chennai,Neighborhood,Apparel,1058,317,951,44735.04,2236.75,37174.83,50103.24,534,2,5323.46,3.5,3162
05-01-2026,South,ST-006,Chennai Retail Hub,Chennai,Neighborhood,Electronics,942,292,584,138583.2,27716.64,101512.19,145512.36,433,3,9354.37,3.9,3461
05-01-2026,South,ST-006,Chennai Retail Hub,Chennai,Neighborhood,Home,1840,405,405,24219,4117.23,19375.2,23734.62,290,4,726.57,4.3,3760
05-01-2026,South,ST-006,Chennai Retail Hub,Chennai,Neighborhood,Beauty,2231,602,1505,39190.2,5486.63,33311.67,35663.08,543,5,391.9,4.7,4059
05-01-2026,South,ST-006,Chennai Retail Hub,Chennai,Neighborhood,Sports,1222,391,586,30296.2,3332.58,24539.92,34537.67,796,6,2423.7,3.2,4358
12-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Grocery,1351,392,980,17110.8,2395.51,13517.53,15570.83,393,3,1197.76,4.9,2109
12-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Apparel,1472,383,574,23625.84,2598.84,19018.81,26933.46,646,4,2008.19,3.4,2408
12-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Electronics,1211,327,981,203949.9,16315.99,179373.93,218226.39,82,9,8259.98,3.4,2707
12-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Home,2254,406,812,52780,2639,49613.2,52780,402,6,527.8,4.2,3006
12-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Beauty,1245,286,286,8088.08,1617.62,5823.41,7521.91,655,7,647.05,4.2,3305
12-01-2026,North,ST-001,Delhi Retail Hub,Delhi,High Street,Sports,1636,458,1145,64234.5,10919.87,49460.56,74512.02,158,4,3854.07,5,3604
12-01-2026,North,ST-004,Chandigarh Retail Hub,Chandigarh,Mall,Sports,1205,374,374,19130.1,1530.41,17025.79,21617.01,785,-1,573.9,4.6,4345
26-01-2026,South,ST-006,Chennai Retail Hub,Chennai,Neighborhood,Apparel,1823,602,602,not_available,5714.18,20913.91,29428.05,255,3,1942.83,3.2,4605
19-01-2026,Central,ST-020,Raipur Retail Hub,Raipur,Mall,Grocery,2809,871,1306,23272.92,4654.58,16756.51,23040.19,271,5,1861.83,4.8,7283
19-01-2026,Central,ST-020,Raipur Retail Hub,Raipur,Mall,Apparel,1238,347,1041,43722,7432.74,31829.62,40224.24,524,6,4459.64,3.3,1082
19-01-2026,Central,ST-020,Raipur Retail Hub,Raipur,Mall,Electronics,1059,307,614,130229.4,18232.12,104964.89,149763.81,427,7,7032.39,3.3,1381
26-01-2026,Central,ST-017,Bhopal Retail Hub,Bhopal,High Street,Home,1982,357,357,24133.2,2654.65,21237.22,21237.22,810,4,241.33,4,1420
26-01-2026,Central,ST-017,Bhopal Retail Hub,Bhopal,High Street,Beauty,2444,562,1405,41307,10739.82,27262.62,45850.77,313,5,3304.56,4.4,1719
02-02-2026,Central,ST-020,Raipur Retail Hub,Raipur,Mall,Sports,1487,476,476,29321.6,3225.38,23750.49,31667.33,850,0,2345.73,4.7,3240
09-02-2026,Central,ST-017,Bhopal Retail Hub,Bhopal,High Street,Grocery,2206,684,684,13420.08,2684.02,9662.45,12480.67,865,7,1073.61,4.1,1485
invalid-date,Central,ST-017,Bhopal Retail Hub,Bhopal,High Street,Beauty,1929,482,964,30500.96,2440.08,25315.79,28975.91,377,3,2745.09,4.2,2681
09-02-2026,Central,ST-017,Bhopal Retail Hub,Bhopal,High Street,Sports,920,276,276,13965.6,698.28,12289.73,12289.73,630,4,977.59,4.6,2980"""


# -----------------------------------------------------------------------------
# 3. DATA LOADING & CLEANING PIPELINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_preprocess_data(weekly_sales_file, store_master_file):
    # Load Weekly Sales Dataset
    if weekly_sales_file is not None:
        if weekly_sales_file.name.endswith('.xlsx'):
            weekly_raw = pd.read_excel(weekly_sales_file)
        else:
            weekly_raw = pd.read_csv(weekly_sales_file)
    else:
        weekly_raw = pd.read_csv(io.StringIO(RETAIL_WEEKLY_SALES_CSV))
    
    # Load Store Master Dataset
    if store_master_file is not None:
        if store_master_file.name.endswith('.xlsx'):
            store_raw = pd.read_excel(store_master_file)
        else:
            store_raw = pd.read_csv(store_master_file)
    else:
        store_raw = pd.read_csv(io.StringIO(STORE_MASTER_CSV))
        
    # Clean BOM or unicode anomalies if present in columns
    weekly_raw.columns = weekly_raw.columns.str.replace('^\ufeff', '', regex=True)
    store_raw.columns = store_raw.columns.str.replace('^\ufeff', '', regex=True)
    
    # Merge reference store metadata on 'store_id' to align classifications correctly
    metadata_cols = ['store_name', 'region', 'city', 'store_format']
    weekly_cleaned = weekly_raw.drop(columns=[c for c in metadata_cols if c in weekly_raw.columns], errors='ignore')
    df = pd.merge(weekly_cleaned, store_raw, on='store_id', how='left')

    # Data Anomaly Cleaning: handle dates
    df['week_start_date'] = df['week_start_date'].astype(str).replace('invalid-date', np.nan)
    df['week_start_date'] = df['week_start_date'].ffill() # propagating previous valid week start dates
    df['week_start_date_parsed'] = pd.to_datetime(df['week_start_date'], format='%d-%m-%Y', errors='coerce')
    df = df.sort_values('week_start_date_parsed')
    
    # Numeric column enforcement & string normalization
    numeric_cols = [
        'footfall', 'transactions', 'units_sold', 'gross_sales', 
        'discount_amount', 'net_sales', 'sales_target', 
        'inventory_on_hand', 'stockouts', 'returns_amount', 
        'customer_rating', 'marketing_spend'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            # Strip string flags like 'not_available' and clean thousands separator commas
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = df[col].replace('not_available', np.nan)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Resolve physical constraints anomalies: negative stockouts count becomes zero
    if 'stockouts' in df.columns:
        df['stockouts'] = df['stockouts'].clip(lower=0)
        
    # Standardize empty numeric metrics to zero to prevent analytical calculation crashes
    df['discount_amount'] = df['discount_amount'].fillna(0)
    df['returns_amount'] = df['returns_amount'].fillna(0)
    
    # Impute missing values dynamically via formulas
    # 1. Net Sales = Gross Sales - Discount Amount - Returns Amount
    if 'net_sales' in df.columns:
        missing_net_sales_mask = df['net_sales'].isna()
        if 'gross_sales' in df.columns:
            df.loc[missing_net_sales_mask, 'net_sales'] = (
                df.loc[missing_net_sales_mask, 'gross_sales'] 
                - df.loc[missing_net_sales_mask, 'discount_amount'] 
                - df.loc[missing_net_sales_mask, 'returns_amount']
            )
            
    # 2. Gross Sales = Net Sales + Discount Amount + Returns Amount
    if 'gross_sales' in df.columns:
        missing_gross_sales_mask = df['gross_sales'].isna()
        if 'net_sales' in df.columns:
            df.loc[missing_gross_sales_mask, 'gross_sales'] = (
                df.loc[missing_gross_sales_mask, 'net_sales'] 
                + df.loc[missing_gross_sales_mask, 'discount_amount'] 
                + df.loc[missing_gross_sales_mask, 'returns_amount']
            )
            
    # Final standard fill to catch any remaining gaps in target
    if 'sales_target' in df.columns:
        df['sales_target'] = df['sales_target'].fillna(0)
        
    return df

# -----------------------------------------------------------------------------
# 4. SIDEBAR PANEL: DATA INTEGRATION & GLOBAL FILTERS
# -----------------------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/000000/dashboard.png", width=60)
st.sidebar.title("Data Integration & Filters")

# Optional Excel File Uploaders
weekly_sales_file = st.sidebar.file_uploader(
    "Upload weekly sales dataset (.csv / .xlsx)", 
    type=["csv", "xlsx"], 
    key="weekly_sales"
)
store_master_file = st.sidebar.file_uploader(
    "Upload store reference master (.csv / .xlsx)", 
    type=["csv", "xlsx"], 
    key="store_master"
)

# Load data through the pre-processing pipeline
raw_data = load_and_preprocess_data(weekly_sales_file, store_master_file)

if weekly_sales_file is None or store_master_file is None:
    st.sidebar.info("💡 Running on preloaded dataset. Upload files to update analysis.")
else:
    st.sidebar.success("✅ Datasets linked and cleaned!")

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filter Panel")

# Chained filtering implementation
# 1. Date/Week filter selection
unique_weeks = sorted(raw_data['week_start_date'].unique())
selected_weeks = st.sidebar.multiselect("Select Weeks", unique_weeks, default=[])

# 2. Region selection
unique_regions = sorted(raw_data['region'].dropna().unique())
selected_regions = st.sidebar.multiselect("Select Regions", unique_regions, default=[])

# 3. Dynamic City Selection based on selected Regions
if selected_regions:
    cities_available = sorted(raw_data[raw_data['region'].isin(selected_regions)]['city'].dropna().unique())
else:
    cities_available = sorted(raw_data['city'].dropna().unique())
selected_cities = st.sidebar.multiselect("Select Cities", cities_available, default=[])

# 4. Dynamic Store Selection based on selected Regions and Cities
store_filter_mask = pd.Series(True, index=raw_data.index)
if selected_regions:
    store_filter_mask &= raw_data['region'].isin(selected_regions)
if selected_cities:
    store_filter_mask &= raw_data['city'].isin(selected_cities)
stores_available = sorted(raw_data[store_filter_mask]['store_name'].dropna().unique())
selected_stores = st.sidebar.multiselect("Select Stores", stores_available, default=[])

# 5. Format & Category Filters
unique_formats = sorted(raw_data['store_format'].dropna().unique())
selected_formats = st.sidebar.multiselect("Select Store Formats", unique_formats, default=[])

unique_categories = sorted(raw_data['product_category'].dropna().unique())
selected_categories = st.sidebar.multiselect("Select Product Categories", unique_categories, default=[])

# Apply Selected Filter Constraints to Dataset
filtered_df = raw_data.copy()
if selected_weeks:
    filtered_df = filtered_df[filtered_df['week_start_date'].isin(selected_weeks)]
if selected_regions:
    filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]
if selected_cities:
    filtered_df = filtered_df[filtered_df['city'].isin(selected_cities)]
if selected_stores:
    filtered_df = filtered_df[filtered_df['store_name'].isin(selected_stores)]
if selected_formats:
    filtered_df = filtered_df[filtered_df['store_format'].isin(selected_formats)]
if selected_categories:
    filtered_df = filtered_df[filtered_df['product_category'].isin(selected_categories)]

# -----------------------------------------------------------------------------
# 5. APP CONTAINER: HEADER SECTION
# -----------------------------------------------------------------------------
st.title("📊 Retail Sales Intelligence Dashboard")
st.markdown("Monitor multi-format performance, manage stockout risks, and analyze business targets dynamically.")

# -----------------------------------------------------------------------------
# 6. APP CONTAINER: KPI SUMMARY CARDS
# -----------------------------------------------------------------------------
# Calculating global dynamic summary metrics
total_net_sales = filtered_df['net_sales'].sum()
total_sales_target = filtered_df['sales_target'].sum()
total_gross_sales = filtered_df['gross_sales'].sum()
total_discount = filtered_df['discount_amount'].sum()
total_returns = filtered_df['returns_amount'].sum()
total_transactions = filtered_df['transactions'].sum()

target_achievement = (total_net_sales / total_sales_target * 100) if total_sales_target > 0 else 0.0
atv = (total_net_sales / total_transactions) if total_transactions > 0 else 0.0
return_rate = (total_returns / total_net_sales * 100) if total_net_sales > 0 else 0.0
discount_rate = (total_discount / total_gross_sales * 100) if total_gross_sales > 0 else 0.0

kpi_cols = st.columns(5)

with kpi_cols[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">₹{total_net_sales:,.2f}</div>
        <div class="metric-label">Net Sales</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    # color-coding logic based on target success rate
    metric_color = "#28a745" if target_achievement >= 100 else "#dc3545"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: {metric_color};">{target_achievement:.1f}%</div>
        <div class="metric-label">Target Achievement</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">₹{atv:,.2f}</div>
        <div class="metric-label">Avg Transaction Value</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[3]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{return_rate:.2f}%</div>
        <div class="metric-label">Return Rate</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[4]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{discount_rate:.2f}%</div>
        <div class="metric-label">Discount Rate</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. APP CONTAINER: CHARTS & VISUAL ANALYTICS
# -----------------------------------------------------------------------------
chart_tab1, chart_tab2 = st.tabs(["📈 Sales & Regional Trends", "🏷️ Categories, Leaders & Inventory Risks"])

with chart_tab1:
    col_trend, col_region = st.columns([2, 1])
    
    with col_trend:
        st.subheader("Weekly Trend Analysis")
        # Aggregate chronological weekly performance
        weekly_perf = filtered_df.groupby('week_start_date_parsed')[['net_sales', 'sales_target']].sum().reset_index()
        weekly_perf['week_str'] = weekly_perf['week_start_date_parsed'].dt.strftime('%d-%b-%Y')
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=weekly_perf['week_str'], 
            y=weekly_perf['net_sales'],
            mode='lines+markers',
            name='Net Sales Actual',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        fig_trend.add_trace(go.Scatter(
            x=weekly_perf['week_str'], 
            y=weekly_perf['sales_target'],
            mode='lines+markers',
            name='Target Projection',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
        fig_trend.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=10, b=10),
            height=350,
            xaxis_title="Week Commencing",
            yaxis_title="Amount (₹)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_region:
        st.subheader("Sales Distribution by Region")
        region_sales = filtered_df.groupby('region')['net_sales'].sum().reset_index()
        fig_region = px.pie(
            region_sales, 
            values='net_sales', 
            names='region', 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_region.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=350,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_region, use_container_width=True)

with chart_tab2:
    col_cat, col_leader = st.columns(2)
    
    with col_cat:
        st.subheader("Category Performance vs Target")
        cat_perf = filtered_df.groupby('product_category')[['net_sales', 'sales_target']].sum().reset_index()
        fig_cat = go.Figure(data=[
            go.Bar(name='Net Sales', x=cat_perf['product_category'], y=cat_perf['net_sales'], marker_color='#1e3d59'),
            go.Bar(name='Sales Target', x=cat_perf['product_category'], y=cat_perf['sales_target'], marker_color='#ffc13b')
        ])
        fig_cat.update_layout(
            barmode='group',
            margin=dict(l=10, r=10, t=20, b=10),
            height=320,
            xaxis_title="Category",
            yaxis_title="Amount (₹)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_leader:
        st.subheader("Store Performance Leaderboard")
        store_sales = filtered_df.groupby('store_name')['net_sales'].sum().reset_index()
        store_sales = store_sales.sort_values(by='net_sales', ascending=True).tail(10)
        
        fig_leader = px.bar(
            store_sales, 
            y='store_name', 
            x='net_sales', 
            orientation='h',
            labels={'store_name': 'Store', 'net_sales': 'Net Sales (₹)'},
            color='net_sales',
            color_continuous_scale='Blues'
        )
        fig_leader.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            height=320,
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_leader, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Stockout Risk Analysis")
    # Identify high risk combinations: high stockout instances alongside declining on-hand levels
    stockout_data = filtered_df.groupby(['product_category', 'store_name'])[['stockouts', 'inventory_on_hand', 'units_sold']].sum().reset_index()
    # Categorize severity level
    stockout_data['Risk Level'] = pd.cut(
        stockout_data['stockouts'],
        bins=[-1, 2, 7, np.inf],
        labels=['Low Risk', 'Moderate Risk', 'Critical Risk']
    )
    
    fig_stockout = px.scatter(
        stockout_data,
        x="inventory_on_hand",
        y="stockouts",
        size="units_sold",
        color="Risk Level",
        hover_name="store_name",
        facet_col="product_category",
        labels={
            "inventory_on_hand": "Total Stock Level (Units)",
            "stockouts": "Cumulative Stockouts (Occurrences)"
        },
        color_discrete_map={
            'Low Risk': '#28a745',
            'Moderate Risk': '#ffc13b',
            'Critical Risk': '#dc3545'
        },
        category_orders={"Risk Level": ["Critical Risk", "Moderate Risk", "Low Risk"]}
    )
    fig_stockout.update_layout(
        margin=dict(l=15, r=15, t=30, b=15),
        height=350,
        plot_bgcolor="rgba(240,242,246,0.5)"
    )
    st.plotly_chart(fig_stockout, use_container_width=True)

# -----------------------------------------------------------------------------
# 8. APP CONTAINER: AUTOMATED BUSINESS INSIGHTS
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("🧠 Automated Business Insights")

def generate_insights(df):
    if df.empty:
        return "Not enough data filtered to formulate diagnostic metrics."
        
    # Region analysis
    reg_perf = df.groupby('region')['net_sales'].sum().reset_index()
    best_region_str = "None"
    worst_region_str = "None"
    if not reg_perf.empty:
        best_reg = reg_perf.loc[reg_perf['net_sales'].idxmax()]
        worst_reg = reg_perf.loc[reg_perf['net_sales'].idxmin()]
        best_region_str = f"**{best_reg['region']}** (Net Sales: ₹{best_reg['net_sales']:,.2f})"
        worst_region_str = f"**{worst_reg['region']}** (Net Sales: ₹{worst_reg['net_sales']:,.2f})"
        
    # Missing targets analysis
    st_perf = df.groupby('store_name')[['net_sales', 'sales_target']].sum().reset_index()
    st_perf['achievement'] = (st_perf['net_sales'] / st_perf['sales_target'] * 100) if 'sales_target' in st_perf.columns else 0.0
    underperformers = st_perf[st_perf['net_sales'] < st_perf['sales_target']].sort_values('achievement')
    
    underperformed_list_str = ""
    if not underperformers.empty:
        for _, row in underperformers.iterrows():
            deficit = row['sales_target'] - row['net_sales']
            underperformed_list_str += f"- **{row['store_name']}** (Achieved {row['achievement']:.1f}% | Target Deficit: -₹{deficit:,.2f})\n"
    else:
        underperformed_list_str = "- No store locations are currently falling short of targets!"
        
    # Return rate analysis
    cat_perf = df.groupby('product_category')[['returns_amount', 'net_sales']].sum().reset_index()
    cat_perf['return_rate'] = (cat_perf['returns_amount'] / cat_perf['net_sales'] * 100)
    high_returns = cat_perf[cat_perf['return_rate'] > 0.0].sort_values('return_rate', ascending=False)
    
    returns_list_str = ""
    if not high_returns.empty:
        for _, row in high_returns.head(3).iterrows():
            returns_list_str += f"- **{row['product_category']}**: Return Rate of **{row['return_rate']:.2f}%** (Returns Volume: ₹{row['returns_amount']:,.2f})\n"
    else:
        returns_list_str = "- No product classifications registered any returned transactions."

    insight_output = f"""### Dynamic Executive Operations Report

#### 🌎 Regional Leaders & Laggards
*   **Top Performer**: {best_region_str}
*   **Lowest Performer**: {worst_region_str}

#### 🏬 Target Shortfall Alert (Stores Currently Missing Business Targets)
{underperformed_list_str}

#### 📦 Product Quality & Returns Risk (Top Return Rates by Category)
{returns_list_str}

---
*Disclaimer: Report auto-compiled based on live transaction registers and global dynamic filter parameters.*"""
    return insight_output

# Generate and Display Live Text Insights
live_insights = generate_insights(filtered_df)
st.markdown(live_insights)

# -----------------------------------------------------------------------------
# 9. DATA EXPORT & AUDIT TRAIL EXPANDER
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("📥 Data Export Options")

export_col1, export_col2 = st.columns(2)

with export_col1:
    # 1. Download Filtered Tabular CSV
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data Register (CSV)",
        data=csv_bytes,
        file_name="filtered_weekly_sales.csv",
        mime="text/csv"
    )

with export_col2:
    # 2. Download Live Executive Insights Text
    st.download_button(
        label="Download Executive Insights Report (TXT)",
        data=live_insights,
        file_name="executive_sales_insights.txt",
        mime="text/plain"
    )

# Clean Audit Trail Expander
with st.expander("📋 View Dynamic Cleaned Data Table"):
    st.dataframe(filtered_df.drop(columns=['week_start_date_parsed'], errors='ignore'), use_container_width=True)
