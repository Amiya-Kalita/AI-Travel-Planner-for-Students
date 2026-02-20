# 🌍 AI Travel Planner Pro

### Intelligent Budget-Aware Travel Planning for Students

AI Travel Planner Pro is a full-stack Generative AI web application that creates personalized, budget-friendly travel itineraries for students.

Built with **Streamlit** and powered by the **Hugging Face Router API**, the app combines large language models, real-time weather data, interactive maps, and budget analytics into a modern travel planning experience.


## 🚀 Problem Statement

Students face several challenges when planning trips:

* Limited budgets
* Generic travel suggestions
* No cost transparency
* Time-consuming manual planning
* Lack of personalized recommendations

AI Travel Planner Pro solves this by generating structured, realistic, and budget-aware travel plans tailored to user preferences.


## ✨ Features

### 🧠 AI-Powered Itinerary Generator

* Day-wise structured travel plan
* Morning / Afternoon / Evening breakdown
* Budget-based recommendations
* Food & accommodation customization
* Travel style personalization (Solo / Friends / Family)


### 💰 Smart Budget Analysis

* Automatic cost allocation:

  * Accommodation
  * Food
  * Transport
  * Activities
* Budget utilization chart
* Remaining balance estimation


### 🗺 Interactive Map View

* Live geolocation via OpenStreetMap
* Interactive PyDeck map visualization
* Destination-based mapping


### 🌦 Live Weather Preview

* Real-time temperature
* Current weather conditions


### 📄 Export Options

* Download itinerary as TXT
* Download itinerary as PDF


### 💡 AI Travel Tips

* Smart cost-saving suggestions
* Context-aware travel advice


### 🎨 Modern UI / UX

* Clean dashboard layout
* Google Fonts integration
* Tab-based navigation
* Responsive design
* User-friendly interaction flow


## 🛠 Tech Stack

| Layer      | Technology                   |
| ---------- | ---------------------------- |
| Frontend   | Streamlit                    |
| AI Model   | HuggingFaceH4/zephyr-7b-beta |
| LLM Access | Hugging Face Router API      |
| Mapping    | PyDeck + OpenStreetMap       |
| Weather    | wttr.in API                  |
| Charts     | Matplotlib                   |
| PDF Export | ReportLab                    |
| Backend    | Python                       |


## 🧠 System Architecture

User Input
↓
Prompt Engineering
↓
Hugging Face Router API
↓
AI Itinerary Generation
↓
Budget Analysis + Weather + Map
↓
Multi-Tab Dashboard Output


## 📦 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-travel-planner-pro.git
cd ai-travel-planner-pro
```


### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```


### 3️⃣ Add Hugging Face API Key

Open `app.py` and update:

```python
HF_API_KEY = "YOUR_HF_TOKEN"
```

You can create a token here:
[https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)



### 4️⃣ Run the App

```bash
streamlit run app.py
```



## 📂 Project Structure

```
ai-travel-planner-pro/
│
├── app.py
├── requirements.txt
└── README.md
```


## 📊 What This Project Demonstrates

* Large Language Model integration
* Prompt engineering
* API orchestration
* Multi-API integration (Weather + Maps + AI)
* Data visualization
* PDF generation
* Full-stack AI application design
* Modern UI development with Streamlit


## 🎯 Use Cases

* Student travel planning
* Budget travel optimization
* AI portfolio showcase
* Hackathon submission
* Startup prototype
* GenAI demonstration project


## 🔐 Security Note

Do not expose your Hugging Face API key in public repositories.
For deployment, use secure environment variables or Streamlit secrets.


## 📈 Future Improvements

* Multi-city itinerary planning
* Flight & train cost estimation
* Google Places integration
* User authentication & saved trips
* Expense tracker during trip
* Dark/Light mode toggle
* Conversational travel chatbot
* SaaS-ready architecture


## 👨‍💻 Author

Built as a practical Generative AI application demonstrating real-world LLM integration and user-centric product design.
