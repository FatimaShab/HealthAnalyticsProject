import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import numpy as np

# Initialize session state for password
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Page configuration
st.set_page_config(
    page_title="Student Depression Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main color palette */
    :root {
        --primary-color: #03045E;
        --secondary-color: #0077B6;
        --tertiary-color: #00B4D8;
        --quaternary-color: #90E0EF;
        --quinary-color: #CAF0F8;
    }
    
    /* Metric boxes styling */
    div[data-testid="metric-container"] {
        background-color: var(--quinary-color);
        border: 2px solid var(--tertiary-color);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--quaternary-color);
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: var(--primary-color);
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom metric styling */
    .metric-box {
        background-color: #CAF0F8;
        border: 2px solid #00B4D8;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #03045E;
        margin-top: 10px;
    }
    
    .metric-label {
        font-size: 1.1em;
        color: #0077B6;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Only apply zero padding CSS after authentication
if st.session_state.authenticated:
    st.markdown("""
    <style>
        /* Remove default Streamlit padding for dashboard only */
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Password protection
if not st.session_state.authenticated:
    # Professional password page with healthcare theme
    st.markdown("""
    <style>
        /* Password page specific styling */
        .header-text {
            text-align: center;
            color: #03045E;
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 10px;
            line-height: 1.2;
        }
        
        .subtitle-text {
            text-align: center;
            color: #0077B6;
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        
        .warning-box {
            background-color: #FFF3CD;
            border: 2px solid #FFC107;
            border-radius: 10px;
            padding: 20px;
            margin: 30px auto;
            max-width: 600px;
        }
        
        .warning-icon {
            color: #FF6B35;
            font-size: 1.5em;
            margin-right: 10px;
        }
        
        .warning-text {
            color: #856404;
            font-size: 1em;
            line-height: 1.6;
        }
        
        .author-text {
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 20px;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)

    # Add logo at the top
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            logo = Image.open(
                'aub_logo.png')
            st.image(logo, width=200)
        except:
            st.write("Logo not found")

    # Header
    st.markdown("""
    <h1 class="header-text">Student Depression in India<br>Healthcare Analytics Dashboard</h1>
    """, unsafe_allow_html=True)

    # Author
    st.markdown('<p class="subtitle-text">Developed by Fatima Shab</p>',
                unsafe_allow_html=True)

    # Warning notice
    st.markdown("""
    <div class="warning-box">
        <span class="warning-icon">⚠️</span>
        <span class="warning-text">
            <strong>CONFIDENTIAL</strong><br>
            This dashboard contains sensitive healthcare data and statistical information 
            about student mental health. Access is restricted to authorized personnel only. 
            Unauthorized access or distribution of this information is strictly prohibited.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Password input
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 10px;'>Please enter your credentials to access the dashboard</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input(
            "", type="password", placeholder="Enter password", key="password_input")

        if st.button("🔓 Access Dashboard", use_container_width=True, type="primary"):
            if password == "healthcare2025":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error(
                    "❌ Invalid credentials. Please verify your password and try again.")

    # Footer
    st.markdown("""
    <p class="author-text">
        © 2025 Healthcare Analytics Platform<br>
        All rights reserved. Data protection protocols in effect.
    </p>
    """, unsafe_allow_html=True)
else:
    # Load data
    @st.cache_data
    def load_data():
        df = pd.read_csv(
            'IP_Student_Depression.csv')
        return df

    df = load_data()

    # Sidebar with logo and filters
    with st.sidebar:
        # Add university logo
        try:
            logo = Image.open(
                '/Users/tumashab/Documents/AUB MSBA/MSBA 382 - Samar/Individual Project/aub_logo.png')
            st.image(logo, width=200)
        except:
            st.write("Logo not found")

        st.markdown(
            "<h2 style='color: #03045E;'>Student Depression in India Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("---")

        # Filters
        st.markdown("<h3 style='color: #0077B6;'>Filters</h3>",
                    unsafe_allow_html=True)

        # Gender filter with checkboxes
        st.markdown("**Gender**")
        gender_options = df['Gender'].unique()
        selected_genders = []
        for gender in gender_options:
            if st.checkbox(gender, value=True, key=f"gender_{gender}"):
                selected_genders.append(gender)

        # Age range filter
        st.markdown("**Age Range**")
        age_min = int(df['Age'].min())
        age_max = int(df['Age'].max())
        age_range = st.slider(
            "Select age range",
            min_value=age_min,
            max_value=age_max,
            value=(age_min, age_max),
            key="age_slider"
        )

        # Depression filter
        st.markdown("**Depression Status**")
        depression_filter = st.radio(
            "Filter by depression status",
            options=["All", "With Depression", "Without Depression"],
            key="depression_radio"
        )

        # Cities filter
        st.markdown("**City**")
        city_list = ["All", "Agra", "Ahmedabad", "Bangalore", "Bhopal", "Chennai", "Delhi",
                     "Faridabad", "Ghaziabad", "Hyderabad", "Indore", "Jaipur", "Kalyan",
                     "Kanpur", "Kolkata", "Lucknow", "Ludhiana", "Meerut", "Mumbai",
                     "Nagpur", "Nashik", "Patna", "Pune", "Rajkot", "Srinagar", "Surat",
                     "Thane", "Vadodara", "Varanasi", "Vasai-Virar", "Visakhapatnam"]
        selected_city = st.selectbox(
            "Select a city", city_list, key="city_filter")

    # Apply filters
    filtered_df = df.copy()

    # Fix Khaziabad typo to Ghaziabad
    filtered_df['City'] = filtered_df['City'].replace('Khaziabad', 'Ghaziabad')

    if selected_genders:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_genders)]

    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (
        filtered_df['Age'] <= age_range[1])]

    if depression_filter == "With Depression":
        filtered_df = filtered_df[filtered_df['Depression'] == 1]
    elif depression_filter == "Without Depression":
        filtered_df = filtered_df[filtered_df['Depression'] == 0]

    if selected_city != "All":
        filtered_df = filtered_df[filtered_df['City'] == selected_city]

    # Main dashboard
    st.markdown("<h2 style='text-align: center; color: #03045E; margin-bottom: 15px; margin-top: 10px;'>Student Depression Analytics Dashboard</h2>", unsafe_allow_html=True)

    # Top row metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Calculate metrics
    total_students = len(filtered_df)
    depression_cases = len(filtered_df[filtered_df['Depression'] == 1])
    depression_rate = (depression_cases / total_students *
                       100) if total_students > 0 else 0  # Changed to percentage
    high_risk = len(filtered_df[(filtered_df['Depression'] == 1) & (
        filtered_df['Suicidal thoughts'] == 'Yes')])

    # Top city with depression
    city_depression = filtered_df[filtered_df['Depression'] == 1].groupby(
        'City').size().reset_index(name='count')
    top_city = city_depression.nlargest(
        1, 'count')['City'].values[0] if not city_depression.empty else "N/A"

    # Family history percentage
    depressed_with_history = len(filtered_df[(filtered_df['Depression'] == 1) & (
        filtered_df['Family History of Mental Illness'] == 'Yes')])
    family_history_pct = (depressed_with_history /
                          depression_cases * 100) if depression_cases > 0 else 0

    # Display metrics
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Total Students</div>
            <div class="metric-value">{total_students:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Depression Cases</div>
            <div class="metric-value">{depression_cases:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Depression Rate</div>
            <div class="metric-value">{depression_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">High Risk Students</div>
            <div class="metric-value">{high_risk:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Top City w/ Dep.</div>
            <div class="metric-value">{top_city}</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-label">Depressed w/ F. Hist.</div>
            <div class="metric-value">{family_history_pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Second row visualizations
    col1, col2, col3, col4 = st.columns(4)

    # Color palette for charts
    colors = ['#03045E', '#0077B6', '#00B4D8', '#90E0EF', '#CAF0F8']

    # 1. Gender pie chart
    with col1:
        gender_counts = filtered_df['Gender'].value_counts()
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="Gender Distribution",
            color_discrete_sequence=colors[:len(gender_counts)]
        )
        fig_gender.update_layout(
            height=300,
            showlegend=True,
            font=dict(size=12),
            margin=dict(t=40, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_gender, use_container_width=True)

        # Academic Pressure and Financial Stress grouped bar chart
        stress_data = filtered_df.groupby(
            'Depression')[['Academic Pressure', 'Financial Stress']].mean().reset_index()
        stress_data['Depression_Status'] = stress_data['Depression'].map(
            {0: 'No Depression', 1: 'Depression'})

        # Reshape data for grouped bar chart with stress types on x-axis
        stress_melted = stress_data.melt(
            id_vars=['Depression', 'Depression_Status'],
            value_vars=['Academic Pressure', 'Financial Stress'],
            var_name='Stress Type',
            value_name='Average Score'
        )

        fig_stress = px.bar(
            stress_melted,
            x='Stress Type',
            y='Average Score',
            color='Depression_Status',
            title="Academic & Financial Stress by Depression",
            barmode='group',
            # Dark blue for No Depression, Light blue for Depression
            color_discrete_sequence=[colors[0], colors[2]]
        )
        fig_stress.update_layout(
            height=300,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                title=None
            ),
            margin=dict(t=40, b=40, l=0, r=0),
            xaxis_title="",
            yaxis_title="Average Score (1-5)",
            yaxis=dict(range=[0, 5.5])
        )
        st.plotly_chart(fig_stress, use_container_width=True)

    # 2. Age distribution
    with col2:
        # Create age bins
        bins = [18, 25, 35, 45, 55, 60]
        labels = ['18-24', '25-34', '35-44', '45-54', '55-59']
        filtered_df['Age_Group'] = pd.cut(
            filtered_df['Age'], bins=bins, labels=labels, include_lowest=True)
        age_dist = filtered_df['Age_Group'].value_counts().sort_index()

        fig_age = px.bar(
            x=age_dist.index,
            y=age_dist.values,
            title="Age Distribution",
            labels={'x': 'Age Group', 'y': 'Count'},
            color_discrete_sequence=[colors[1]]
        )
        fig_age.update_layout(
            height=300,
            showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_age, use_container_width=True)

        # Degree Level stacked chart (under Age Distribution)
        degree_data = filtered_df.groupby(
            ['Degree_Level', 'Depression']).size().reset_index(name='Count')
        degree_data['Depression_Status'] = degree_data['Depression'].map(
            {0: 'No Depression', 1: 'Depression'})

        fig_degree = px.bar(
            degree_data,
            x='Degree_Level',
            y='Count',
            color='Depression_Status',
            title="Depression Distribution by Degree Level",
            color_discrete_sequence=[colors[0], colors[2]],
            barmode='stack'
        )

        fig_degree.update_layout(
            height=300,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.35,
                xanchor="center",
                x=0.5,
                title=None
            ),
            margin=dict(t=40, b=80, l=0, r=0),
            xaxis_title="",
            yaxis_title="Number of Students",
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_degree, use_container_width=True)

    # 3. Family history and depression
    with col3:
        # Create grouped data
        family_depression = filtered_df.groupby(
            ['Family History of Mental Illness', 'Depression']).size().reset_index(name='count')
        family_depression['Depression_Status'] = family_depression['Depression'].map(
            {0: 'No Depression', 1: 'Depression'})

        # Rename family history values for clarity
        family_depression['Family History of Mental Illness'] = family_depression['Family History of Mental Illness'].map({
            'Yes': 'With Family History',
            'No': 'No Family History'
        })

        fig_family = px.bar(
            family_depression,
            x='Family History of Mental Illness',
            y='count',
            color='Depression_Status',
            title="Family History & Depression",
            barmode='group',
            color_discrete_sequence=[colors[0], colors[2]]
        )
        fig_family.update_layout(
            height=300,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                title=None
            ),
            margin=dict(t=40, b=40, l=0, r=0),
            xaxis_title="",
            yaxis_title="Count"
        )
        st.plotly_chart(fig_family, use_container_width=True)

        # Sleep Hours line chart (under Family History)
        # First create a copy and rename sleep duration categories
        sleep_df = filtered_df.copy()
        sleep_df['Sleep Duration'] = sleep_df['Sleep Duration'].replace({
            '5-6 hours': '5-6 hrs',
            '7-8 hours': '7-8 hrs',
            'Less than 5 hours': '< 5 hrs',
            'More than 8 hours': '> 8 hrs',
            'Others': 'Others'
        })

        sleep_data = sleep_df.groupby(
            ['Sleep Duration', 'Depression']).size().reset_index(name='Count')
        sleep_data['Depression_Status'] = sleep_data['Depression'].map(
            {0: 'No Depression', 1: 'Depression'})

        fig_sleep = px.line(
            sleep_data,
            x='Sleep Duration',
            y='Count',
            color='Depression_Status',
            title="Sleep Hours Distribution by Depression",
            markers=True,
            color_discrete_sequence=[colors[0], colors[2]]
        )

        fig_sleep.update_layout(
            height=300,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.45,
                xanchor="center",
                x=0.5,
                title=None
            ),
            margin=dict(t=40, b=100, l=0, r=0),
            xaxis_title="",
            yaxis_title="Number of Students"
        )

        st.plotly_chart(fig_sleep, use_container_width=True)

    # 4. Top 5 cities lollipop chart
    with col4:
        city_depression_counts = filtered_df[filtered_df['Depression'] == 1].groupby(
            'City').size().reset_index(name='count')
        top_5_cities = city_depression_counts.nlargest(
            5, 'count').sort_values('count', ascending=True)

        fig_cities = go.Figure()
        fig_cities.add_trace(go.Scatter(
            x=top_5_cities['count'],
            y=top_5_cities['City'],
            mode='markers+lines',
            marker=dict(size=12, color=colors[1]),
            line=dict(color=colors[3], width=2),
            name=''
        ))

        # Add dots at the end
        fig_cities.add_trace(go.Scatter(
            x=top_5_cities['count'],
            y=top_5_cities['City'],
            mode='markers',
            marker=dict(size=15, color=colors[0]),
            name='',
            showlegend=False
        ))

        fig_cities.update_layout(
            title="Top 5 Cities - Depression Count",
            xaxis_title="Depression Cases",
            yaxis_title="",
            height=300,
            showlegend=False,
            margin=dict(t=40, b=0, l=0, r=0)
        )
        st.plotly_chart(fig_cities, use_container_width=True)

        # Dietary Habits grouped bar chart (under Top 5 Cities)
        diet_data = filtered_df.groupby(
            ['Dietary Habits', 'Depression']).size().reset_index(name='Count')
        diet_data['Depression_Status'] = diet_data['Depression'].map(
            {0: 'No Depression', 1: 'Depression'})

        fig_diet = px.bar(
            diet_data,
            x='Dietary Habits',
            y='Count',
            color='Depression_Status',
            title="Dietary Habits by Depression",
            barmode='group',
            color_discrete_sequence=[colors[0], colors[2]]
        )

        fig_diet.update_layout(
            height=300,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.4,
                xanchor="center",
                x=0.5,
                title=None
            ),
            margin=dict(t=40, b=90, l=0, r=0),
            xaxis_title="",
            yaxis_title="Count",
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_diet, use_container_width=True)
