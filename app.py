import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import pydeck as pdk
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import io

# ======================================================
# SAFE API KEY LOADING (CLOUD SAFE)
# ======================================================

if "HF_API_KEY" not in st.secrets:
    st.error("Hugging Face API key not found in Streamlit Secrets.")
    st.stop()

HF_API_KEY = st.secrets["HF_API_KEY"]

# ======================================================
# OPENAI CLIENT USING HF ROUTER
# ======================================================

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
)

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

st.title("AI Travel Planner Pro")
st.caption("Your intelligent student-friendly travel companion.")

# ======================================================
# SIDEBAR INPUTS
# ======================================================

st.sidebar.header("Trip Preferences")

destination = st.sidebar.text_input("Destination City")
duration = st.sidebar.slider("Days", 1, 7, 3)
budget = st.sidebar.number_input("Total Budget (INR)", min_value=1000, step=1000)
travel_style = st.sidebar.selectbox("Travel Style", ["Solo", "Friends", "Family"])
food_pref = st.sidebar.selectbox("Food Preference", ["Vegetarian", "Non-Vegetarian", "Local Cuisine"])
accommodation = st.sidebar.selectbox("Accommodation", ["Hostel", "Budget Hotel", "Airbnb"])

generate = st.sidebar.button("Generate Travel Plan")

# ======================================================
# WEATHER
# ======================================================

def get_weather(city):
    try:
        data = requests.get(f"https://wttr.in/{city}?format=j1").json()
        temp = data["current_condition"][0]["temp_C"]
        desc = data["current_condition"][0]["weatherDesc"][0]["value"]
        return temp, desc
    except:
        return None, None

# ======================================================
# MAP
# ======================================================

def get_coordinates(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        response = requests.get(url, headers={"User-Agent": "travel-app"}).json()
        if response:
            return float(response[0]["lat"]), float(response[0]["lon"])
    except:
        return None, None
    return None, None

# ======================================================
# AI GENERATION (WITH ERROR HANDLING)
# ======================================================

def generate_plan(prompt):
    try:
        completion = client.chat.completions.create(
            model="HuggingFaceH4/zephyr-7b-beta",  # <-- removed suffix
            messages=[
                {"role": "system", "content": "You are a professional travel planner."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"API Error: {str(e)}"

# ======================================================
# PDF EXPORT
# ======================================================

def generate_pdf(text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph(text.replace("\n", "<br/>"), styles["Normal"]))
    elements.append(Spacer(1, 12))
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ======================================================
# MAIN
# ======================================================

if generate and destination:

    prompt = f"""
    Create a detailed {duration}-day itinerary for {destination}.
    Budget: ₹{budget}
    Travel style: {travel_style}
    Food: {food_pref}
    Stay: {accommodation}
    Provide day-wise breakdown and total estimated cost.
    """

    with st.spinner("Generating travel plan..."):
        plan = generate_plan(prompt)

    if plan.startswith("API Error"):
        st.error(plan)
        st.stop()

    temp, desc = get_weather(destination)

    col1, col2, col3 = st.columns(3)
    col1.metric("Trip Duration", f"{duration} Days")
    col2.metric("Budget", f"₹{budget}")
    if temp:
        col3.metric("Weather", f"{temp}°C | {desc}")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📌 Itinerary", "🗺 Map View", "💰 Budget"])

    # ==================================================
    # ITINERARY
    # ==================================================

    with tab1:
        st.markdown(plan)
        st.download_button("Download TXT", plan, file_name="travel_plan.txt")
        pdf = generate_pdf(plan)
        st.download_button("Download PDF", pdf, file_name="travel_plan.pdf")

    # ==================================================
    # MAP
    # ==================================================

    with tab2:
        lat, lon = get_coordinates(destination)
        if lat and lon:
            map_df = pd.DataFrame({"lat": [lat], "lon": [lon]})
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=map_df,
                get_position='[lon, lat]',
                get_radius=500,
                get_fill_color=[255, 0, 0],
            )
            view_state = pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=11,
            )
            st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
        else:
            st.warning("Map not available.")

    # ==================================================
    # BUDGET
    # ==================================================

    with tab3:
        accom = budget * 0.35
        food = budget * 0.25
        transport = budget * 0.20
        activities = budget * 0.20

        labels = ["Accommodation", "Food", "Transport", "Activities"]
        sizes = [accom, food, transport, activities]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%")
        ax.axis("equal")
        st.pyplot(fig)

else:
    st.info("Enter trip details and generate your travel plan.")

st.markdown("---")
st.caption("Deployed on Streamlit Cloud | Powered by Hugging Face Router")
