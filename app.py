import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import pydeck as pdk
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import A4
import io

# CONFIG

HF_API_KEY = "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"

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
)

# PAGE CONFIG + MODERN STYLE

st.set_page_config(page_title="AI Travel Planner Pro", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}
.main-title {
    font-size: 40px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AI Travel Planner Pro</div>', unsafe_allow_html=True)
st.markdown("Your intelligent student-friendly travel companion.")


# SIDEBAR

st.sidebar.header("Trip Preferences")

destination = st.sidebar.text_input("Destination City")
duration = st.sidebar.slider("Days", 1, 7, 3)
budget = st.sidebar.number_input("Total Budget (INR)", min_value=1000, step=1000)
travel_style = st.sidebar.selectbox("Travel Style", ["Solo", "Friends", "Family"])
food_pref = st.sidebar.selectbox("Food Preference", ["Vegetarian", "Non-Vegetarian", "Local Cuisine"])
accommodation = st.sidebar.selectbox("Accommodation", ["Hostel", "Budget Hotel", "Airbnb"])

generate = st.sidebar.button("Generate Travel Plan")
regenerate = st.sidebar.button("Regenerate")


# WEATHER FUNCTION

def get_weather(city):
    try:
        geo = requests.get(f"https://wttr.in/{city}?format=j1").json()
        temp = geo["current_condition"][0]["temp_C"]
        desc = geo["current_condition"][0]["weatherDesc"][0]["value"]
        return temp, desc
    except:
        return None, None


# GEOCODING

def get_coordinates(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        response = requests.get(url, headers={"User-Agent": "travel-app"}).json()
        if response:
            return float(response[0]["lat"]), float(response[0]["lon"])
    except:
        return None, None
    return None, None


# AI GENERATION

def generate_plan(prompt):
    completion = client.chat.completions.create(
        model="HuggingFaceH4/zephyr-7b-beta:featherless-ai",
        messages=[
            {"role": "system", "content": "You are a professional travel planner."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=900,
        temperature=0.7,
    )
    return completion.choices[0].message.content

# PDF EXPORT

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


# MAIN LOGIC

if (generate or regenerate) and destination:

    prompt = f"""
    Create a detailed {duration}-day itinerary for {destination}.
    Budget: ₹{budget}
    Travel style: {travel_style}
    Food: {food_pref}
    Stay: {accommodation}
    Provide day-wise plan and total estimated cost.
    """

    with st.spinner("Generating intelligent itinerary..."):
        plan = generate_plan(prompt)

    temp, desc = get_weather(destination)

    col1, col2, col3 = st.columns(3)
    col1.metric("Trip Duration", f"{duration} Days")
    col2.metric("Budget", f"₹{budget}")
    if temp:
        col3.metric("Current Weather", f"{temp}°C | {desc}")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📌 Itinerary", "🗺 Map View", "💰 Budget Analysis", "💡 Travel Tips"]
    )


    # ITINERARY TAB

    with tab1:
        st.markdown(plan)

        st.download_button("Download as TXT", plan, file_name="travel_plan.txt")

        pdf = generate_pdf(plan)
        st.download_button(
            "Download as PDF",
            pdf,
            file_name="travel_plan.pdf",
            mime="application/pdf",
        )


    # MAP VIEW TAB

    with tab2:

        lat, lon = get_coordinates(destination)

        if lat and lon:
            map_df = pd.DataFrame({
                "lat": [lat],
                "lon": [lon]
            })

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
                zoom=12,
                pitch=50,
            )

            st.pydeck_chart(pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": destination}
            ))

        else:
            st.warning("Unable to load map.")


    # BUDGET ANALYSIS TAB

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

        st.success(f"Estimated Spend: ₹{sum(sizes):.0f}")
        st.info(f"Remaining Budget: ₹{budget - sum(sizes):.0f}")


    # TRAVEL TIPS TAB

    with tab4:
        tips_prompt = f"Give 5 smart budget travel tips for students visiting {destination}"
        tips = generate_plan(tips_prompt)
        st.markdown(tips)

else:
    st.info("Enter trip details and generate your travel plan.")

st.markdown("---")
st.caption("AI Travel Planner Pro Your Personal Traval Planner")