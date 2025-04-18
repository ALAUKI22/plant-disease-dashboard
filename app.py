import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from PIL import Image
from io import BytesIO
import base64

# Set page config to use wider layout
st.set_page_config(layout="wide")

# Helper function to convert image to base64
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Load Data
@st.cache_data
def load_data():
    # Use relative path or hosted CSV file
    try:
        return pd.read_csv("plant_disease_dashboard.csv")
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'plant_disease_dashboard.csv' is in the correct directory.")
        return pd.DataFrame()

df = load_data()

# Custom CSS styles
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #4CAF50;
        height: 100%;
    }
    .metric-title {
        font-size: 16px;
        color: #666666;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 28px;
        color: #2c3e50;
        font-weight: 700;
        margin: 5px 0;
    }
    .metric-subtext {
        font-size: 14px;
        color: #7f8c8d;
    }
    .risk-high {
        color: #e74c3c;
        background-color: #fde8e8;
        padding: 3px 10px;
        border-radius: 15px;
        font-weight: 600;
        font-size: 18px;
    }
    .risk-medium {
        color: #f39c12;
        background-color: #fef5e7;
        padding: 3px 10px;
        border-radius: 15px;
        font-weight: 600;
        font-size: 18px;
    }
    .risk-low {
        color: #27ae60;
        background-color: #e8f8f0;
        padding: 3px 10px;
        border-radius: 15px;
        font-weight: 600;
        font-size: 18px;
    }
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 15px;
        margin-bottom: 30px;
    }
    @media (max-width: 1200px) {
        .metric-grid {
            grid-template-columns: repeat(3, 1fr);
        }
    }
    @media (max-width: 800px) {
        .metric-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    .horizontal-scroller {
        display: flex;
        overflow-x: auto;
        gap: 15px;
        padding: 15px 0;
        width: 100%;
    }
    .horizontal-scroller img {
        height: 220px;
        width: auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        object-fit: cover;
        flex: 0 0 auto;
    }
    .horizontal-scroller::-webkit-scrollbar {
        height: 6px;
    }
    .horizontal-scroller::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    .horizontal-scroller::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Dashboard"])

# Page 1: HOME
if page == "🏠 Home":
    st.title("🌱 Plant Disease Detection Dashboard")
    st.markdown("Welcome to your intelligent assistant for plant health monitoring.")

    st.markdown(
        """
        <div style="text-align:center; padding:10px;">
            <img src="https://www.ischool.berkeley.edu/sites/default/files/styles/fullscreen/public/sproject_teaser_image/reversed.jpg?itok=7ZCOj-Gt" width="600">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style='border: 2px solid #4CAF50; background-color: #ECFFDC; padding: 15px; border-radius: 10px; font-size: 16px;'>
        <strong>🌿 Why Plant Disease Detection?</strong><br><br>
        Detecting plant diseases is crucial for several reasons:<br><br>
        <ul>
            <li><strong>Agricultural Productivity:</strong> Early identification of diseases can prevent widespread outbreaks.</li>
            <li><strong>Economic Impact:</strong> Minimizing crop losses helps farmers' economic stability.</li>
            <li><strong>Food Security:</strong> Protecting crops maintains stable food supply.</li>
            <li><strong>Environmental Protection:</strong> Reduces need for chemical treatments.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sample images (use relative paths or hosted images)
    sample_images = [
        "sample_images/Cercospora_leaf_spot_fixed.jpg",
        "sample_images/healthy.jpg",
        "sample_images/Late_blight.jpg",
        "sample_images/Leaf_scorch.jpg",
        "sample_images/Northern_Leaf_Blight.jpg",
        "sample_images/Powdery_mildew.jpg"
    ]

    gallery_html = '<div class="horizontal-scroller">'
    
    for img_path in sample_images:
        try:
            if os.path.exists(img_path):
                img = Image.open(img_path)
                width = int(img.width * 220 / img.height)
                img = img.resize((width, 220))
                gallery_html += f'<img src="data:image/jpeg;base64,{image_to_base64(img)}">'
            else:
                # Fallback to placeholder if image not found
                gallery_html += f'<img src="https://via.placeholder.com/300x220?text=Image+Not+Found" alt="Placeholder">'
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
    
    gallery_html += '</div>'
    st.markdown(gallery_html, unsafe_allow_html=True)

# Page 2: DASHBOARD
elif page == "📊 Dashboard":
    st.title("🌿 Plant Disease Analytics")
    
    # Expanded Filters
    with st.sidebar.expander("🔍 Filters", expanded=True):
        selected_crop = st.multiselect(
            "Select Crop(s)", 
            df['crop_name'].unique(), 
            default=df['crop_name'].unique()
        )
        selected_status = st.multiselect(
            "Health Status", 
            df['status'].unique(), 
            default=['Healthy', 'Diseased']
        )
        selected_region = st.multiselect(
            "Select Region(s)", 
            df['region'].unique(), 
            default=df['region'].unique()
        )
    
    # Apply filters
    filtered_df = df[
        (df['crop_name'].isin(selected_crop)) &
        (df['status'].isin(selected_status)) &
        (df['region'].isin(selected_region))
    ]
    
    st.subheader("📈 Key Metrics")

    # Calculate metrics
    total_cases = len(filtered_df)
    diseased_cases = len(filtered_df[filtered_df['status'] == 'Diseased'])
    disease_ratio = (diseased_cases / total_cases) * 100 if total_cases > 0 else 0
    most_affected_crop = filtered_df[filtered_df['status'] == 'Diseased']['crop_name'].mode()[0] if not filtered_df.empty else "N/A"
    most_common_disease = filtered_df[filtered_df['status'] == 'Diseased']['disease_name'].mode()[0] if not filtered_df.empty else "N/A"

    # Determine risk level
    if disease_ratio > 50:
        risk_level = "High"
        risk_class = "risk-high"
    elif disease_ratio > 20:
        risk_level = "Medium"
        risk_class = "risk-medium"
    else:
        risk_level = "Low"
        risk_class = "risk-low"

    # Create the metrics grid
    st.markdown(f"""
    <div class='metric-grid'>
        <div class='metric-card'>
            <div class='metric-title'>Total Cases Analyzed</div>
            <div class='metric-value'>{total_cases:,}</div>
            <div class='metric-subtext'>Historical records</div>
        </div>
        <div class='metric-card'>
            <div class='metric-title'>Disease Prevalence</div>
            <div class='metric-value'>{disease_ratio:.1f}%</div>
            <div class='metric-subtext'>Affected plants</div>
        </div>
        <div class='metric-card'>
            <div class='metric-title'>Most Affected Crop</div>
            <div class='metric-value'>{most_affected_crop}</div>
            <div class='metric-subtext'>Highest infection rate</div>
        </div>
        <div class='metric-card'>
            <div class='metric-title'>Most Common Disease</div>
            <div class='metric-value'>{most_common_disease.split('___')[-1].replace('_', ' ') if most_common_disease != "N/A" else "N/A"}</div>
            <div class='metric-subtext'>Frequent detection</div>
        </div>
        <div class='metric-card'>
            <div class='metric-title'>Overall Risk Level</div>
            <div class='metric-value'><span class='{risk_class}'>{risk_level} Risk</span></div>
            <div class='metric-subtext'>Monitoring recommendation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚨 Top Disease Alerts")
        if not filtered_df.empty:
            top_diseases = filtered_df[filtered_df['status'] == 'Diseased']['disease_name'].value_counts().nlargest(5)
            
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            
            # Color code by severity
            colors = []
            for val in top_diseases.values:
                if val > 50: colors.append('#dc3545')  # Red for high
                elif val > 20: colors.append('#fd7e14')  # Orange for medium
                else: colors.append('#ffc107')  # Yellow for low
            
            top_diseases.plot(kind='barh', ax=ax1, color=colors)
            plt.xlabel("Case Count")
            plt.title("Most Frequently Detected Diseases")
            plt.gca().invert_yaxis()
            
            # Add value labels
            for i, v in enumerate(top_diseases):
                ax1.text(v + 0.5, i, str(v), color='black', ha='left', va='center')
            
            st.pyplot(fig1)
        else:
            st.warning("No disease cases found for selected filters")
    
    with col2:
        st.subheader("🌍 Regional Hotspots")
        if not filtered_df.empty:
            region_risk = filtered_df[filtered_df['status'] == 'Diseased']['region'].value_counts()
            
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            
            # Color code by severity
            colors = []
            for val in region_risk.values:
                if val > 50: colors.append('#dc3545')
                elif val > 20: colors.append('#fd7e14')
                else: colors.append('#ffc107')
            
            region_risk.plot(kind='bar', ax=ax2, color=colors)
            plt.ylabel("Disease Cases")
            plt.title("Regions with Highest Disease Occurrence")
            plt.xticks(rotation=45)
            
            # Add value labels
            for i, v in enumerate(region_risk):
                ax2.text(i, v + 0.5, str(v), ha='center')
            
            st.pyplot(fig2)
        else:
            st.warning("No regional data available")
    
    st.markdown("---")
    
    # Additional Visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🌱 Crop Health Status")
        if not filtered_df.empty:
            crop_health = filtered_df.groupby(['crop_name', 'status']).size().unstack().fillna(0)
            
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            crop_health.plot(kind='bar', stacked=True, ax=ax3, color=['#4CAF50', '#F44336'])
            
            plt.xticks(rotation=45, ha='right')
            plt.xlabel('Crop')
            plt.ylabel('Count')
            plt.legend(title='Health Status', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            
            st.pyplot(fig3)
        else:
            st.warning("No data available for selected filters")
    
    with col4:
        st.subheader("🔄 Health Status Ratio")
        if not filtered_df.empty:
            status_counts = filtered_df['status'].value_counts()
            
            fig4, ax4 = plt.subplots(figsize=(8, 6))
            ax4.pie(status_counts, labels=status_counts.index, 
                   autopct='%1.1f%%', startangle=90, 
                   colors=['#4CAF50', '#F44336'],
                   explode=(0.1, 0), shadow=True)
            ax4.axis('equal')
            ax4.set_title('Health Status Distribution')
            
            st.pyplot(fig4)
        else:
            st.warning("No data available for selected filters")
    
    # Data Table
    with st.expander("📋 View Filtered Data", expanded=False):
        if not filtered_df.empty:
            st.dataframe(
                filtered_df.sort_values('status', ascending=False),
                height=300,
                use_container_width=True
            )
        else:
            st.warning("No data available for selected filters")
