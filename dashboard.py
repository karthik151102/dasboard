import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
# Set page configuration
st.set_page_config(
    page_title="Company Dashboard",
    page_icon="📈",
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'https://www.streamlit-help',
        'Report a bug': "https://www.streamlit/bug",
        'About': '#Wolfzy is a premier sales company with a strong global presence, dedicated to delivering exceptional sales solutions that drive business growth and success. With branches in India, Canada, the USA, the UK, Germany, and beyond, we are committed to empowering businesses with innovative strategies and tools to excel in their respective markets'
    }
)
# Custom CSS styles for background, text, and fonts
st.markdown(
    """
    <style>
    /* Background and text styles */
    body {
        background-color: #f0f4f8;
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    
    /* Custom header styles */
    .header-container {
        background-color: #3498db;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    
    /* Custom KPI styles */
    .stMetric {
        background-color: #f1c40f;
        color: #fff;
        font-size: 1.2em;
        border-radius: 10px;
        padding: 10px;
    }

    /* Filters section */
    .filters-container {
        background-color: #ffffff;
        padding: 20px;
        margin-top: 20px;
        border-radius: 10px;
    }

    /* Tabs and visualizations */
    .tabs-container {
        background-color: #ffffff;
        padding: 20px;
        margin-top: 20px;
        border-radius: 10px;
    }
    
    /* General content container styling */
    .container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data
def load_data():
    try:
        df = pd.read_csv("C:/dasboard/venv/my_app/pages/comp.csv")
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("Error: CSV file not found. Please check the file path.")
        return None
    except pd.errors.EmptyDataError:
        st.error("Error: The CSV file is empty.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the data: {str(e)}")
        return None

df = load_data()

if df is not None and not df.empty:
    # Create a container for the dashboard
    container = st.container()

    # Create a header section
    with container:
        st.image("D:\download\Circle-wolf-logo-template-Graphics-5449673-1.jpg", width=100)  # Correct image path with forward slashes
        # Add a brief description of the dashboard
        st.header("Dashboard of Wolfzy")
        st.write("""
Wolfzy: Your Global Sales Partner
Company Overview: Wolfzy is a leading sales company with a robust global presence. With branches in India, Canada, the USA, the UK, Germany, and beyond, Wolfzy is committed to delivering exceptional sales solutions that drive business growth and success. Our mission is to empower businesses with innovative strategies and tools to excel in their respective markets.

Mission: At Wolfzy, our mission is to transform the sales landscape by providing tailored solutions that meet the unique needs of each client. We aim to build enduring relationships based on trust, transparency, and mutual success.

Vision: Our vision is to become the foremost global sales company, renowned for our innovative approaches, outstanding customer service, and unwavering dedication to excellence. We aspire to set new benchmarks in the sales industry and help our clients achieve their highest potential.

Core Values:

1.Integrity: We uphold the highest ethical standards in all our dealings.

2.Innovation: We embrace change and continuously seek new ways to improve.`Customer Focus: Our clients’ success is our top priority.

3.Collaboration: We believe in the power of teamwork and partnership.

4.Excellence: We strive for excellence in everything we do.

5.Global Presence: Wolfzy operates in multiple countries, providing localized support and insights to our clients. Our branches in India, Canada, the USA, the UK, and Germany enable us to understand and cater to diverse markets effectively.
""")

    # Create a filters section
    with container:
        st.subheader("Filters")
        country_filter = st.multiselect("Select Countries", options=df['Country'].unique(), default=df['Country'].unique())
        year_filter = st.slider("Select Year Range", 
                                min_value=int(df['Date'].dt.year.min()), 
                                max_value=int(df['Date'].dt.year.max()), 
                                value=(int(df['Date'].dt.year.min()), int(df['Date'].dt.year.max())))

    # Filter the data based on the selected countries and year range
    filtered_df = df[(df['Country'].isin(country_filter)) & (df['Date'].dt.year.between(year_filter[0], year_filter[1]))]

    # Create a KPIs section
    with container:
        st.subheader("Key Performance Indicators (KPIs)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Companies", len(filtered_df['Name'].unique()))
        col2.metric("Total Profits", f"${filtered_df['Profits'].sum():,.2f}")
        col3.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.2f}")
        col4.metric("Average Branches", f"{filtered_df['Branches'].mean():.2f}")

    # Create a visualizations section
    with container:
        st.subheader("Visualizations")
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Profits by Country", "Revenue vs Profits", "Employees by Branches", "Correlation Heat Map", "Profits Histogram", "Profits Time Series", "Profits Time Series with Moving Average"])

        with tab1:
            profits_by_country = filtered_df.groupby('Country')['Profits'].sum().reset_index()
            fig_map = px.choropleth(profits_by_country, 
                                    locations="Country", 
                                    locationmode="country names",
                                    color="Profits",
                                    hover_name="Country",
                                    color_continuous_scale=px.colors.sequential.Viridis,
                                    title="Total Profits by Country")
            fig_map.update_layout(geo=dict(showframe=False, 
                                           showcoastlines=True, 
                                           projection_type='natural earth'))
            st.plotly_chart(fig_map, use_container_width=True)

        with tab2:
            fig_scatter = px.scatter(filtered_df, x='Revenue', y='Profits', color='Country', hover_name='Name', title="Revenue vs Profits")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with tab3:
            branches = filtered_df['Branches'].value_counts()
            fig_donut = go.Figure(data=[go.Pie(labels=branches.index, values=branches.values, hole=.3)])
            fig_donut.update_layout(title_text="Employees by Branches")
            st.plotly_chart(fig_donut, use_container_width=True)

        with tab4:
            corr_matrix = filtered_df[['Profits', 'Revenue', 'Branches']].corr()
            fig_heatmap = px.imshow(corr_matrix, text_auto=True, title='Heat Map of Company')
            st.plotly_chart(fig_heatmap, use_container_width=True)

        with tab5:
            fig_histogram = px.histogram(filtered_df, x='Profits', title='Profits Histogram')
            st.plotly_chart(fig_histogram, use_container_width=True)

        with tab6:
            fig_time_series = px.line(filtered_df, x='Date', y='Profits', title='Profits Time Series')
            st.plotly_chart(fig_time_series, use_container_width=True)

        with tab7:
            filtered_df['Profits_ma'] = filtered_df['Profits'].rolling(window=3).mean()
            fig_time_series_ma = px.line(filtered_df, x='Date', y=['Profits', 'Profits_ma'], title='Profits Time Series with Moving Average')
            st.plotly_chart(fig_time_series_ma, use_container_width=True)
