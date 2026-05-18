import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="Financial Data Pipeline Dashboard", layout="wide", page_icon="📊")

# Database connection
@st.cache_resource
def get_connection():
    return sqlite3.connect("pipeline.db", check_same_thread=False)

conn = get_connection()

# Load data with caching
@st.cache_data(ttl=60)
def load_cleaned_trades():
    return pd.read_sql_query("SELECT * FROM cleaned_trades", conn)

@st.cache_data(ttl=60)
def load_validation_errors():
    return pd.read_sql_query("SELECT * FROM validation_errors", conn)

@st.cache_data(ttl=60)
def load_audit_log():
    return pd.read_sql_query("SELECT * FROM audit_log ORDER BY timestamp DESC", conn)

@st.cache_data(ttl=60)
def load_lineage():
    return pd.read_sql_query("SELECT * FROM lineage", conn)

# Load data
cleaned_df = load_cleaned_trades()
errors_df = load_validation_errors()
audit_df = load_audit_log()
lineage_df = load_lineage()

# Convert date column to datetime
if not cleaned_df.empty and 'date' in cleaned_df.columns:
    cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])

# ---------- SIDEBAR FILTERS ----------
st.sidebar.title("🔍 Filters & Navigation")
page = st.sidebar.radio("Go to", ["📊 Overview", "📋 Cleaned Trades", "⚠️ Validation Errors", "📜 Audit Log", "🔗 Data Lineage"])

st.sidebar.markdown("---")
st.sidebar.subheader("Data Filters (applies to Overview & Cleaned Trades)")

# Date range filter
if not cleaned_df.empty:
    min_date = cleaned_df['date'].min().date()
    max_date = cleaned_df['date'].max().date()
    date_range = st.sidebar.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date)
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = cleaned_df[(cleaned_df['date'].dt.date >= start_date) & (cleaned_df['date'].dt.date <= end_date)]
    else:
        filtered_df = cleaned_df
else:
    filtered_df = cleaned_df
    start_date, end_date = None, None

# Symbol filter
all_symbols = cleaned_df['symbol'].unique() if not cleaned_df.empty else []
selected_symbols = st.sidebar.multiselect("Symbol(s)", all_symbols, default=all_symbols)
if selected_symbols:
    filtered_df = filtered_df[filtered_df['symbol'].isin(selected_symbols)]

# Client filter (optional)
all_clients = cleaned_df['client_id'].unique() if not cleaned_df.empty else []
selected_clients = st.sidebar.multiselect("Client ID(s)", all_clients)
if selected_clients:
    filtered_df = filtered_df[filtered_df['client_id'].isin(selected_clients)]

# Suspicious flag filter
suspicious_filter = st.sidebar.radio("Suspicious only", ["All", "Normal", "Suspicious"])
if suspicious_filter == "Suspicious":
    filtered_df = filtered_df[filtered_df['is_suspicious'] == 1]
elif suspicious_filter == "Normal":
    filtered_df = filtered_df[filtered_df['is_suspicious'] == 0]

# ---------- MAIN CONTENT ----------
if page == "📊 Overview":
    st.title("📊 Pipeline Overview")
    
    # Key metrics (using filtered data)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trades", f"{len(filtered_df):,}")
    with col2:
        suspicious_count = filtered_df['is_suspicious'].sum() if not filtered_df.empty else 0
        st.metric("Suspicious Trades", f"{suspicious_count:,}", delta=f"{suspicious_count/len(filtered_df)*100:.1f}%" if len(filtered_df)>0 else None)
    with col3:
        error_count = len(errors_df) if not errors_df.empty else 0
        st.metric("Validation Errors", f"{error_count:,}")
    with col4:
        if not filtered_df.empty:
            total_value = filtered_df['total_value'].sum()
            st.metric("Total Value (€)", f"{total_value:,.0f}")
        else:
            st.metric("Total Value (€)", "0")
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Trades per Symbol")
        if not filtered_df.empty:
            symbol_counts = filtered_df['symbol'].value_counts().reset_index()
            symbol_counts.columns = ['Symbol', 'Count']
            fig = px.bar(symbol_counts, x='Symbol', y='Count', color='Symbol', title="Number of Trades by Symbol")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data matching filters")
    
    with col2:
        st.subheader("💰 Daily Total Value")
        if not filtered_df.empty:
            daily_value = filtered_df.groupby(filtered_df['date'].dt.date)['total_value'].sum().reset_index()
            daily_value.columns = ['Date', 'Total Value (€)']
            fig = px.line(daily_value, x='Date', y='Total Value (€)', title="Total Value Over Time")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data matching filters")
    
    # Suspicious vs Normal pie chart
    st.subheader("🚨 Suspicious vs Normal Trades")
    if not filtered_df.empty:
        suspicious_counts = filtered_df['is_suspicious'].value_counts().reset_index()
        suspicious_counts.columns = ['Type', 'Count']
        suspicious_counts['Type'] = suspicious_counts['Type'].map({0: 'Normal', 1: 'Suspicious'})
        fig = px.pie(suspicious_counts, values='Count', names='Type', title="Trade Classification", color='Type', color_discrete_map={'Normal':'green','Suspicious':'red'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data")
    
    # Recent audit log summary
    st.subheader("🕒 Recent Pipeline Activity (Audit Log)")
    if not audit_df.empty:
        st.dataframe(audit_df.head(10), use_container_width=True)
    else:
        st.info("No audit records")

elif page == "📋 Cleaned Trades":
    st.title("📋 Cleaned Trades (Filtered View)")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button("Download as CSV", csv, "cleaned_trades.csv", "text/csv")

elif page == "⚠️ Validation Errors":
    st.title("⚠️ Validation Errors")
    if not errors_df.empty:
        st.dataframe(errors_df, use_container_width=True)
        # Summary by error type
        error_summary = errors_df['error_type'].value_counts().reset_index()
        error_summary.columns = ['Error Type', 'Count']
        st.subheader("Error Type Distribution")
        st.bar_chart(error_summary.set_index('Error Type'))
    else:
        st.success("No validation errors found! ✅")

elif page == "📜 Audit Log":
    st.title("📜 Audit Log (Full History)")
    st.dataframe(audit_df, use_container_width=True)

elif page == "🔗 Data Lineage":
    st.title("🔗 Data Lineage (Where Numbers Came From)")
    st.dataframe(lineage_df, use_container_width=True)
    st.caption("This table shows the origin of each value in the cleaned trades.")

# Close connection (optional, Streamlit handles it)
conn.close()