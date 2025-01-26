import streamlit as st
import pandas as pd
import pickle

# Load the model
model_path = "C:/Users/Dell User/OneDrive/Desktop/Beacon/Beacon/Beacon-Flood-Prediction/models/model.pkl"  
with open(model_path, "rb") as file:
    model = pickle.load(file)

# Dataset preview
first_five_rows = pd.DataFrame({
    "MonsoonIntensity": [3, 8, 3, 4, 3],
    "TopographyDrainage": [8, 4, 10, 4, 7],
    "RiverManagement": [6, 5, 4, 2, 5],
    "Deforestation": [6, 7, 1, 7, 2],
    "Urbanization": [4, 7, 7, 3, 5],
    "ClimateChange": [4, 9, 5, 4, 8],
    "DamsQuality": [6, 1, 4, 1, 5],
    "Siltation": [2, 5, 7, 4, 2],
    "AgriculturalPractices": [3, 5, 4, 6, 7],
    "Encroachments": [2, 4, 9, 4, 5],
    "IneffectiveDisasterPreparedness": [4, 7, 8, 5, 6],
    "DrainageSystems": [10, 9, 7, 4, 7],
    "CoastalVulnerability": [7, 2, 4, 2, 6],
    "Landslides": [4, 6, 4, 6, 5],
    "Watersheds": [2, 2, 8, 6, 3],
    "DeterioratingInfrastructure": [3, 1, 6, 8, 3],
    "PopulationScore": [4, 1, 1, 8, 4],
    "WetlandLoss": [3, 9, 8, 6, 4],
    "InadequatePlanning": [2, 1, 3, 6, 3],
    "PoliticalFactors": [6, 3, 6, 10, 4],
    "FloodProbability": [0.45, 0.475, 0.515, 0.52, 0.475]
})

# Streamlit app configuration
st.set_page_config(
    page_title="Flood Probability Prediction",
    page_icon="⛈",
    layout="wide",
    initial_sidebar_state="expanded",
)

def show_home_page():
    st.title("🌧️ Flood Probability Prediction")
    st.markdown(
        """
        <style>
        .stTitle {
            color: #1f77b4;
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.write("""
        Welcome to the Flood Probability Prediction Section! Enter relevant environmental and socio-economic data to predict flood probability in a specific region.
    """)

    st.header("Enter the required inputs below:")

    # Input fields
    features = [
        "MonsoonIntensity", "TopographyDrainage", "RiverManagement", "Deforestation", "Urbanization",
        "ClimateChange", "DamsQuality", "Siltation", "AgriculturalPractices", "Encroachments",
        "IneffectiveDisasterPreparedness", "DrainageSystems", "CoastalVulnerability", "Landslides",
        "Watersheds", "DeterioratingInfrastructure", "PopulationScore", "WetlandLoss",
        "InadequatePlanning", "PoliticalFactors"
    ]

    inputs = []
    for feature in features:
        value = st.number_input(f"{feature}", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
        inputs.append(value)

    if st.button("Predict Flood Probability"):
        prediction = model.predict([inputs])[0]
        st.success(f"Predicted Flood Probability: {prediction:.2f}")

def show_about_page():
    st.title("About Flood Probability Prediction")

    st.subheader("Description")
    st.write("""
        Flood prediction helps in identifying, monitoring, and mitigating the risks associated with floods. This app uses a machine learning model to predict the probability of floods based on environmental and socio-economic factors.
    """)

    st.subheader("How It Works")
    st.write("""
        1. **Input Data:** Users provide values for 20 environmental and socio-economic factors.
        2. **Model Processing:** The input data is processed through a trained machine learning model.
        3. **Prediction Output:** The app predicts the flood probability based on the input data.
    """)

    st.subheader("Dataset Information")
    st.write("""
        The dataset used in this analysis comprises 21 features that influence flood occurrence. It contains 50,000 rows with no missing values. Below are the first five rows of the dataset:
    """)

    st.dataframe(first_five_rows)

    st.write("""
        **Features Description:**
        - 🌧️ **MonsoonIntensity:** Higher rainfall increases flood probability.
        - 🏖️ **TopographyDrainage:** Efficient drainage lowers flood risk.
        - 🌊 **RiverManagement:** Effective river management reduces floods.
        - 🌳 **Deforestation:** Increases runoff and flood risks.
        - 🏙️ **Urbanization:** Impermeable surfaces raise flood likelihood.
        - 🌍 **ClimateChange:** Extreme weather patterns elevate flood risks.
        - 🏋️ **DamsQuality:** Maintenance and status of dams.
        - 🎓 **Siltation:** Sediment accumulation reduces drainage capacity.
        - 🌿 **AgriculturalPractices:** Unsustainable practices increase flood risk.
        - 🏡 **Encroachments:** Construction in flood-prone areas obstructs water flow.
        - 🚨 **IneffectiveDisasterPreparedness:** Lack of emergency plans increases flood impact.
        - ♻️ **DrainageSystems:** Well-maintained systems reduce flood risk.
        - 🌊 **CoastalVulnerability:** Low-lying coastal areas are prone to floods.
        - 🌫 **Landslides:** Unstable soils and slopes can trigger floods.
        - 🏞️ **Watersheds:** Regions with poor watershed management face higher risks.
        - 🔨 **DeterioratingInfrastructure:** Damaged structures increase flood vulnerability.
        - 👤 **PopulationScore:** Densely populated areas suffer greater flood impact.
        - 🌰 **WetlandLoss:** Wetlands act as natural sponges to absorb water.
        - 🏛️ **InadequatePlanning:** Poor urban planning heightens flood risk.
        - 🏢 **PoliticalFactors:** Governance affects flood management efficacy.
    """)

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Home", "About"])

if page == "Home":
    show_home_page()
elif page == "About":
    show_about_page()
