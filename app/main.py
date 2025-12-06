import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
from PIL import Image



@st.cache_data 

def load_data():
    return pd.read_csv("/Users/anaghanair/Downloads/youtube-pipeline/data/youtube_clean.csv")


#Title and data loading
# Title with YouTube Logo
st.markdown("""
    <style>
        .title-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .title-container img {
            width: 55px;
        }
        .title-text {
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0;
            padding: 0;
        }
    </style>

    <div class="title-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png">
        <span class="title-text">YouTube Video Data Insights Dashboard</span>
    </div>
""", unsafe_allow_html=True)

#st.title("Youtube Video Data Insights Dashboard")
st.markdown("An interactive dashboard to explore global and channel-level insights from top 100 trending Youtube videos in the US.")
df = load_data()

#filter options

st.sidebar.header("Filters")
channel_options = ["All"] + df["channel_title"].unique().tolist()
bucket_options = ["All"] + df["time_bucket"].unique().tolist()

#fallback copy of dataframe
df_filtered = df.copy()
#creating sidebar filters
selected_channel = st.sidebar.selectbox("Select a Channel", channel_options)
selected_bucket = st.sidebar.selectbox("Choose time bucket", bucket_options)

if selected_channel != "All":
    df_filtered = df_filtered[df_filtered["channel_title"]==selected_channel]
if selected_bucket != "All":
    df_filtered = df_filtered[df_filtered["time_bucket"]==selected_bucket]

# SECTION 1 - GLOBAL INSIGHTS
st.divider()
st.markdown("<h2 style='color:#4A90E2;'>🌍 Global Insights</h2>", unsafe_allow_html=True)
st.info("These insights are based on the entire dataset, regardless of any filters applied in the sidebar.")
colA,colB = st.columns(2)
with colA:
     st.subheader("Total Channels By Avg Views/Day")
     top_channels = (
            df.groupby("channel_title",as_index=False)["views_per_day"]
            .mean().head(10) 
            
        )
     figA = px.bar(top_channels,x="channel_title",y="views_per_day",title="Top Channels by Average Views/Day", 
                   labels={"channel_title":"Channel Title","views_per_day":"Average Views/Day"}
                   )
     st.plotly_chart(figA,use_container_width=True)
with colB:
     st.subheader("Global Views Distribution")
     figB = px.histogram(df,x="views_per_day",nbins=10,title="Distribution of Views/Day",
                         labels={"views_per_day":"Views/Day"} 
                         )
     st.plotly_chart(figB,use_container_width=True)

st.divider()
# SECTION 2 - correlation analysis
def interpret_correlation(value):
    abs_val = abs(value)
    if abs_val >= 0.8:
        return "🔴 **Highly Correlated**"
    elif abs_val >= 0.5:
        return "🟠 **Moderately Correlated**"
    elif abs_val >= 0.3:
        return "🟡 **Weakly Correlated**"
    else:
        return "🟢 **Not Correlated**"
    
st.markdown("<h2 style='color:#4A90E2;'>Correlated or Not?</h2>", unsafe_allow_html=True)
st.info("Do not select any filters from the sidebar!")
st.markdown("Choose any two numerical features from the dataset to see if they are correlated.")
numerical_columns = df.select_dtypes(include=["int64","float64"]).columns.tolist()
col3,col4 = st.columns(2)

with col3:
    num_cols = st.multiselect("Select Two Numerical Features", numerical_columns, default=numerical_columns[:2])
with col4:
     if len(num_cols) != 2:
        st.warning("⚠️ Please select exactly two numerical features.")
        st.stop()

     feature_x, feature_y = num_cols[0], num_cols[1]
     if df[feature_x].nunique() <= 1 or df[feature_y].nunique() <= 1:
        st.warning("⚠️ Not enough variation in the selected features to compute correlation.")
        st.stop()

     correlation_value = df[[feature_x,feature_y]].corr().iloc[0,1] 

     if np.isnan(correlation_value):
        st.warning("⚠️ Correlation could not be computed due to insufficient data.")
        st.stop()

     st.subheader(f"Correlation between {feature_x} and {feature_y}:")
     st.write(f"Correlation value: {correlation_value:.2f}")
     st.markdown(f"They are {interpret_correlation(correlation_value)}")

# SECTION 3 - FILTERED DATA VIEW AND DOWNLOAD
st.divider()

st.markdown("""
<div style="
    padding:12px;
    background-color:#F7F7F7;
    border-radius:10px;
    margin-bottom:20px;">
    <h3 style='margin:0;color:#333;'>Filtered Data Preview</h3>
</div>
""", unsafe_allow_html=True)
st.info("Use the sidebar filters to refine the data displayed below. You can also download the filtered dataset as a CSV file.")
st.subheader("Filtered Data Preview")
st.write(df_filtered.head())

col1,col2 = st.columns(2)

with col1:
    st.subheader("Duration vs Views/Day")
    fig1 = px.scatter(df_filtered,x="duration_parsed",y="views_per_day",log_y=True,
                      labels={"duration_parsed":"Duration (minutes)","views_per_day":"Views/Day"}
                      )
    st.plotly_chart(fig1,use_container_width=True)
    fig1.update_layout(template="plotly_white")


with col2:
    st.subheader("Likes vs Views/Day")
    fig2 = px.scatter(df_filtered,x="like_count",y="views_per_day",log_y=True,  labels={"like_count":"Like Count","views_per_day":"Views/Day"})
    st.plotly_chart(fig2,use_container_width=True)
    fig2.update_layout(template="plotly_white")


st.subheader("Filtered Average Views by Time Bucket")
avg_views_bucket = (
    df_filtered.groupby("time_bucket",as_index=True)["view_count"].median().reset_index()
)
fig3 = px.bar(avg_views_bucket,x="time_bucket",y="view_count",title="Median Views by Time Bucket", 
              labels={"time_bucket":"Time Bucket","view_count":"Median View Count"})
st.plotly_chart(fig3,use_container_width=True)
fig3.update_layout(template="plotly_white")

# Section 4: Download filtered data
st.divider()
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

st.markdown("""
<div style="
    padding:12px;
    background-color:#F7F7F7;
    border-radius:10px;
    margin-bottom:20px;">
    <h3 style='margin:0;color:#333;'>Tools and Downloads</h3>
</div>
""", unsafe_allow_html=True)
with st.expander("Download Filtered Data"):
    csv = convert_df_to_csv(df_filtered)
    st.download_button(
        label="Download Filtered Data as CSV", data=csv, file_name="filtered_date.csv", mime="text/csv")


    









