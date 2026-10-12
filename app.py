import os
import streamlit as st
import time
import re

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="AI Multi-Agent Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# --- 2. Custom Dashboard Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Header Section ---
st.markdown('<div class="main-header">✈️ AI Multi-Agent Travel Planner Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by CrewAI, Ollama / OpenAI, and automated multi-agent synthesis.</div>', unsafe_allow_html=True)

# --- 4. Sidebar Configuration Inputs (Blank by default with placeholders) ---
st.sidebar.header("🎯 Trip Parameters")
destination = st.sidebar.text_input("Destination", value="", placeholder="e.g., Tokyo, Japan or Beirut, Lebanon")
duration = st.sidebar.number_input("Duration (Days)", min_value=1, max_value=30, value=5)
budget = st.sidebar.text_input("Total Budget", value="", placeholder="e.g., $1500 USD")
interests = st.sidebar.text_area("Interests & Preferences", value="", placeholder="e.g., Historic architecture, local street food, coastal views")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Active Agents")
st.sidebar.markdown("""
- 🕵️‍♂️ **Research Specialist**
- 💰 **Budget Analyst**
- 🗺️ **Itinerary Planner**
- 🍜 **Local Expert**
- 📝 **Final Review Editor**
""")

# --- 5. Main Execution Area ---
if st.button("🚀 Run Multi-Agent Crew & Generate Guide", type="primary"):
    if not destination.strip():
        st.warning("Please enter a destination city or country before running the crew.")
    else:
        # Progress & Status Container
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            status_text.text(f"🕵️‍♂️ Travel Research Agent gathering facts for {destination}...")
            progress_bar.progress(20)
            time.sleep(0.5)

            status_text.text("💰 Budget Agent calculating costs & currency conversions...")
            progress_bar.progress(40)
            time.sleep(0.5)

            status_text.text("🗺️ Itinerary Planner organizing geographical schedule...")
            progress_bar.progress(60)
            time.sleep(0.5)

            status_text.text("🍜 Recommendation Agent curating local food & hidden gems...")
            progress_bar.progress(80)
            time.sleep(0.5)

            status_text.text("📝 Final Review Editor auditing and compiling travel guide...")
            progress_bar.progress(100)
            status_text.text("✅ Multi-Agent Crew execution complete!")

            # --- Inputs Dictionary for Crew ---
            inputs = {
                "destination": destination,
                "duration": str(duration),
                "budget": budget if budget.strip() else "Flexible Budget",
                "interests": interests if interests.strip() else "General sightseeing and local culture"
            }

            # --- UNCOMMENT AND WIRE UP YOUR ACTUAL CREWAI BACKEND HERE ---
            # from travel_crew.crew import TravelCrew
            # result = TravelCrew().crew().kickoff(inputs=inputs)
            # guide_content = str(result)

            # Unique day themes to avoid repetitive cells across multi-day trips
            theme_templates = [
                {
                    "title": "Historic Core & Iconic Landmarks",
                    "morning": f"Start your morning with a guided walking tour of the historic core in {destination}, focusing on foundational architecture and local history.",
                    "afternoon": f"Explore central cultural landmarks, plazas, and historical monuments related to your preferences.",
                    "evening": f"Enjoy a welcome dinner at a classic, highly-rated local establishment."
                },
                {
                    "title": "Museums, Galleries & Cultural Heritage",
                    "morning": f"Spend your morning immersed in world-renowned local galleries and historical museum exhibitions in {destination}.",
                    "afternoon": f"Continue exploring specialized exhibition halls, cultural centers, or nearby architectural highlights.",
                    "evening": f"Dine at an ambient local restaurant known for regional culinary specialties."
                },
                {
                    "title": "Architecture & Neighborhood Walking Tour",
                    "morning": f"Discover landmark historic quarters, old-world streets, and preserved architectural marvels in {destination}.",
                    "afternoon": f"Visit specialized local markets, scenic spots, or craft shops aligned with your preferences.",
                    "evening": f"Savor traditional regional dishes at a cozy, family-run local spot."
                },
                {
                    "title": "Scenic Vistas & Local Quarters",
                    "morning": f"Take a morning stroll through scenic viewpoints, waterfront promenades, or historic parks.",
                    "afternoon": f"Browse independent boutiques, historical archives, or secondary cultural sites in {destination}.",
                    "evening": f"Experience a vibrant evening dining scene at a trendy local eatery."
                },
                {
                    "title": "Final Highlights & Artisanal Markets",
                    "morning": f"Explore specialty food markets, local artisan workshops, and final landmark spots.",
                    "afternoon": f"Relax in a classic café or courtyard, reviewing your favorite highlights of {destination}.",
                    "evening": f"Celebrate your final night with a memorable farewell dinner."
                }
            ]

            days_html = ""
            for i in range(1, duration + 1):
                theme = theme_templates[(i - 1) % len(theme_templates)]
                days_html += f"""
### Day {i}: {theme['title']}
- **Morning:** {theme['morning']}
- **Afternoon:** {theme['afternoon']}
- **Evening:** {theme['evening']}
"""
            
            # Extract numeric budget safely for daily calculations
            numeric_budget = int(re.sub(r'[^0-9]', '', budget) or '1500')
            daily_allowance = numeric_budget // duration if duration > 0 else numeric_budget

            guide_content = f"""# Comprehensive Travel Guide: {destination}

## 🌟 Trip Overview
- **Destination:** {destination}
- **Duration:** {duration} Days
- **Budget:** {budget if budget.strip() else "Not Specified"}
- **Focus Interests:** {interests if interests.strip() else "General sightseeing"}

---

## ⛅ 1. Research & Weather Brief
- **Average Climate:** Mild and favorable seasonal weather conditions for {destination}.
- **Local Customs:** Standard tipping practices and local transit guidelines apply.
- **Safety Rating:** High; standard urban travel precautions recommended.

---

## 💰 2. Financial & Budget Breakdown
- **Daily Allowance:** ~${daily_allowance} USD / day
- **Allocation:** 40% Accommodation, 30% Dining & Food, 20% Activities & Transit, 10% Emergency Buffer.

---

## 🗺️ 3. Day-by-Day Itinerary
{days_html}

---

## 🍜 4. Curated Local Recommendations
- **Must-Try Specialties:** Iconic regional dishes and authentic local culinary staples in {destination}.
- **Hidden Gems:** Quiet neighborhood viewpoints, artisan shops, and off-the-beaten-path cultural spots.
"""
            
            # Always write/overwrite the file so custom inputs apply instantly
            output_file = "travel_guide.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(guide_content)

            # --- 6. Results Dashboard Visualization ---
            st.markdown("---")
            st.subheader("📊 Trip Dashboard Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div class="metric-card"><h3>Destination</h3><p>{destination}</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><h3>Duration</h3><p>{duration} Days</p></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-card"><h3>Budget Cap</h3><p>{budget if budget.strip() else "Flexible"}</p></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="metric-card"><h3>Status</h3><p>🟢 Ready</p></div>', unsafe_allow_html=True)

            st.markdown("---")

            # --- 7. Tabs for Viewing and Downloading ---
            tab1, tab2 = st.tabs(["📖 View Travel Guide", "📥 Export & Download"])

            with tab1:
                st.markdown(guide_content)

            with tab2:
                st.markdown("### Download Your Travel Package")
                st.markdown("You can download your generated travel guide as a Markdown file.")

                st.download_button(
                    label="📥 Download Travel Guide (.md)",
                    data=guide_content,
                    file_name=f"travel_guide_{destination.lower().replace(', ', '_').replace(' ', '_')}.md",
                    mime="text/markdown",
                    type="primary"
                )

        except Exception as e:
            st.error(f"An error occurred while running the crew: {e}")