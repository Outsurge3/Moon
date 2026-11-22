# THE MOON CIRCLE - African Lunar, Seasonal & Cosmic Calendar
# Southern Hemisphere | South Africa | SAST
# Run: streamlit run moon_circle_app.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime

st.set_page_config(page_title="The Moon Circle", page_icon="🌙", layout="wide")

# ============ DATA - ASTRONOMICAL (SAST, South Africa) ============
# Sources: NASA Eclipse / Timeanddate astronomical calculations for SAST (UTC+2)
# 2026-2027 New Moons are astronomical anchors. Symbolic 28-day cycle is separate.

COSMIC_EVENTS_2026_2027 = [
    # (date, time SAST, event, visible_SA, type)
    ("2026-01-18", "21:52", "New Moon", "Not visible - new moon", "Moon"),
    ("2026-02-01", "06:09", "Full Moon", "Yes - rises evening", "Moon"),
    ("2026-02-17", "14:01", "New Moon", "Not visible", "Moon"),
    ("2026-03-03", "13:38", "Full Moon - Harvest Moon (SA Autumn)", "Yes", "Moon"),
    ("2026-03-20", "16:46", "March Equinox - Autumn Equinox (Southern Hemisphere)", "Day/night equal", "Solar"),
    ("2026-04-02", "20:12", "Full Moon", "Yes", "Moon"),
    ("2026-04-22", "04:00", "Lyrid Meteor Shower Peak", "Yes - pre-dawn, best after midnight", "Meteor"),
    ("2026-05-01", "07:23", "Full Moon", "Yes", "Moon"),
    ("2026-05-16", "05:39", "Eta Aquariid Meteor Shower Peak", "Yes - excellent in SA", "Meteor"),
    ("2026-06-21", "04:42", "June Solstice - Winter Solstice (Southern Hemisphere)", "Shortest day", "Solar"),
    ("2026-06-29", "16:56", "Full Moon", "Yes", "Moon"),
    ("2026-07-28", "23:00", "Delta Aquariid Meteor Shower Peak", "Yes", "Meteor"),
    ("2026-08-12", "22:00", "Perseid Meteor Shower Peak", "Partial - low in north", "Meteor"),
    ("2026-08-28", "06:19", "Total Lunar Eclipse", "YES - Visible in South Africa", "Eclipse"),
    ("2026-09-23", "03:54", "September Equinox - Spring Equinox (Southern Hemisphere)", "Day/night equal", "Solar"),
    ("2026-10-26", "05:12", "New Moon", "Not visible", "Moon"),
    ("2026-11-24", "08:43", "Full Moon", "Yes", "Moon"),
    ("2026-12-14", "20:00", "Geminid Meteor Shower Peak", "Yes - excellent in SA", "Meteor"),
    ("2026-12-21", "17:03", "December Solstice - Summer Solstice (Southern Hemisphere)", "Longest day", "Solar"),
    ("2026-12-24", "02:28", "Full Moon", "Yes - Christmas Eve", "Moon"),
    ("2027-02-06", "22:57", "Annular Solar Eclipse", "YES - Partial visible in SA, annular path in S. America/Atlantic", "Eclipse"),
    ("2027-02-20", "16:03", "Total Lunar Eclipse", "YES - Visible in SA at moonrise", "Eclipse"),
    ("2027-03-20", "22:25", "March Equinox - Autumn Equinox", "Day/night equal", "Solar"),
]

# 13 x 28-day symbolic cycle = 364 days. Anchor to first New Moon after Dec Solstice 2025
# This is SYMBOLIC for planning, NOT astronomical lunar month (29.53 days)
MOON_CYCLE = [
    {"n": 1, "name": "Moon 1: First Planting", "dates": "18 Jan - 14 Feb 2026", "season": "Late Summer", "theme": "Beginnings, clearing, setting intention"},
    {"n": 2, "name": "Moon 2: Ripening", "dates": "15 Feb - 14 Mar 2026", "season": "Late Summer to Autumn", "theme": "Growth, tending, patience"},
    {"n": 3, "name": "Moon 3: Turning", "dates": "15 Mar - 11 Apr 2026", "season": "Autumn", "theme": "Equinox, balance, harvest assessment"},
    {"n": 4, "name": "Moon 4: Gathering", "dates": "12 Apr - 9 May 2026", "season": "Autumn", "theme": "Harvest, gratitude, storing"},
    {"n": 5, "name": "Moon 5: Letting Go", "dates": "10 May - 6 Jun 2026", "season": "Autumn to Winter", "theme": "Release, composting, rest"},
    {"n": 6, "name": "Moon 6: Stillness", "dates": "7 Jun - 4 Jul 2026", "season": "Winter", "theme": "Solstice, introspection, restoration"},
    {"n": 7, "name": "Moon 7: Deep Roots", "dates": "5 Jul - 1 Aug 2026", "season": "Winter", "theme": "Wisdom, family, foundations"},
    {"n": 8, "name": "Moon 8: First Bud", "dates": "2 Aug - 29 Aug 2026", "season": "Winter to Spring", "theme": "Preparation, quiet hope"},
    {"n": 9, "name": "Moon 9: Blossoming", "dates": "30 Aug - 26 Sep 2026", "season": "Spring", "theme": "Equinox, renewal, planting"},
    {"n": 10, "name": "Moon 10: Rain Calling", "dates": "27 Sep - 24 Oct 2026", "season": "Spring", "theme": "Nourishment, growth, intention"},
    {"n": 11, "name": "Moon 11: Abundance", "dates": "25 Oct - 21 Nov 2026", "season": "Spring to Summer", "theme": "Vitality, generosity, expression"},
    {"n": 12, "name": "Moon 12: Full Sun", "dates": "22 Nov - 19 Dec 2026", "season": "Summer", "theme": "Solstice, celebration, joy"},
    {"n": 13, "name": "Moon 13: Completion", "dates": "20 Dec - 16 Jan 2027", "season": "Summer", "theme": "Integration, rest, closing the year"},
]

# ============ RITUAL LIBRARY ============
# Each ritual has 5 / 15 / 30 min versions. All are CONTEMPORARY wellness rituals unless marked DOCUMENTED.

def ritual_card(title, purpose, prep, materials, steps_5, steps_15, steps_30, reflection, affirmation, origin="Contemporary - Developed for The Moon Circle"):
    st.markdown(f"### {title}")
    st.caption(f"Origin: {origin}")
    st.write(f"**Purpose:** {purpose}")
    st.write(f"**Preparation:** {prep}")
    st.write(f"**Materials:** {materials}")
    tab1, tab2, tab3 = st.tabs(["⏱️ 5 min - Minimum", "⏱️ 15 min - Standard", "⏱️ 30 min - Extended"])
    with tab1:
        for s in steps_5: st.write(f"- {s}")
    with tab2:
        for s in steps_15: st.write(f"- {s}")
    with tab3:
        for s in steps_30: st.write(f"- {s}")
    st.write(f"**Reflection:** {reflection}")
    st.write(f"**Closing:** *{affirmation}*")
    st.divider()

SEASONS = {
    "Spring (Sep-Nov) - Rebirth, Planting, Renewal": {
        "opening": "Plant one seed (real or symbolic) and name one intention you will water daily.",
        "weekly": ["Week 1: Clear one space in home", "Week 2: Plant / start one new habit", "Week 3: Walk in nature, notice new growth", "Week 4: Share seedlings / kindness"],
        "daily": "2 min morning: Face sun, breathe, name 1 intention. Evening: What grew today?",
        "physical": "30-min walk, gardening, stretching in morning sun.",
        "nature": "Visit a garden, park, or water. Notice buds, birds returning.",
        "closing": "Harvest list: Write 10 things that grew this season. Burn / bury list with gratitude."
    },
    "Summer (Dec-Feb) - Vitality, Abundance, Joy": {
        "opening": "Share food / water with someone. Set a generosity intention.",
        "weekly": ["Week 1: Joy audit - what gives energy?", "Week 2: Cook for family", "Week 3: Swim / outdoor play", "Week 4: Give away what you no longer need"],
        "daily": "Morning: Drink water mindfully. Evening: 3 joys of the day.",
        "physical": "Swimming, dancing, early morning walk before heat.",
        "nature": "Sit under tree at midday, watch shade and light.",
        "closing": "Celebration meal, gratitude for abundance, rest before autumn."
    },
    "Autumn (Mar-May) - Harvest, Gratitude, Release": {
        "opening": "Lay out harvest - food, work, lessons. Thank each one.",
        "weekly": ["Week 1: Assess finances / work", "Week 2: Preserve / save / store", "Week 3: Let go of one habit / item", "Week 4: Thank elders / mentors"],
        "daily": "Morning: What am I harvesting? Evening: What can I release?",
        "physical": "Slower walks, strength work, warm foods.",
        "nature": "Collect fallen leaves, compost, notice trees letting go.",
        "closing": "Release ceremony: Write what to release, safely burn / tear and compost."
    },
    "Winter (Jun-Aug) - Stillness, Restoration, Wisdom": {
        "opening": "Light a candle. Commit to rest and listening this season.",
        "weekly": ["Week 1: Digital sunset - no phone after 20:00", "Week 2: Story night - share family stories", "Week 3: Deep clean one room", "Week 4: Plan for spring"],
        "daily": "Morning: Slow tea, journal 3 lines. Evening: Silence 5 min.",
        "physical": "Gentle yoga, warm baths, early sleep.",
        "nature": "Star-gazing, notice bare branches, cold air breathing.",
        "closing": "Solstice reflection: What wisdom did winter teach me?"
    },
}

# ============ APP UI ============

st.title("🌙 The Moon Circle")
st.subheader("African Lunar, Seasonal & Cosmic Calendar  •  Southern Hemisphere  •  South Africa (SAST)")
st.info("⚖️ **Cultural Integrity:** This app distinguishes 4 things: 1) **Scientific astronomy**, 2) **Documented traditional knowledge** (with attribution), 3) **Contemporary interpretations**, 4) **New rituals created for this app**. It is NOT an authority on all African traditions. Please seek guidance from knowledgeable practitioners in your community.")

menu = st.sidebar.radio("Navigate", ["🏠 Today", "🌑 13-Moon Calendar", "🌀 Seasonal Wheel", "🌿 Seasonal Programmes", "✨ Cosmic Events", "📚 Ritual Library", "🏛️ Cultural Traditions"])

# TODAY
if menu == "🏠 Today":
    today = date.today()
    st.header(f"Today: {today.strftime('%A, %d %B %Y')} - South Africa")
    st.write("**Season now (Southern Hemisphere):** Spring (Sep-Nov) - Rebirth, planting, renewal")
    st.write("**Moon:** Check tonight - Moon phase follows astronomical cycle. Full Moon 24 Dec 2026 will be visible across SA.")
    st.write("**Today's Practice (5 min):** Stand outside. Notice light, wind, temperature. Name 1 thing you are planting this week.")
    st.success("Working-person tip: Do Minimum version on busy days. Consistency > perfection.")
    if st.button("Get Today's Ritual"):
        st.write("**Morning (5 min):** Water + breath + 1 intention. **Evening (5 min):** 3 gratitudes, 1 release.")

# 13-MOON
elif menu == "🌑 13-Moon Calendar":
    st.header("The 13-Moon Calendar")
    st.warning("**Symbolic vs Astronomical:** A symbolic cycle is 13 x 28 days = 364 days, used for planning. A real lunar month is ~29.53 days from New Moon to New Moon, so it drifts. We show BOTH. Use symbolic for rhythm, astronomical for sky-watching.")
    for m in MOON_CYCLE:
        with st.expander(f"{m['name']} • {m['dates']} • {m['season']}"):
            st.write(f"**Theme:** {m['theme']}")
            st.write("**Explore:** What is growing? What needs tending? What needs releasing?")
            st.write("**Practice:** New Moon - set intention. Full Moon - review & gratitude. Last Quarter - release.")
    st.write("**Lunar-Solar Relationship:** The Sun gives seasons (solstice/equinox). The Moon gives monthly rhythm. Together they create the year.")

# WHEEL
elif menu == "🌀 Seasonal Wheel":
    st.header("The African Seasonal Wheel")
    st.write("Click / view - Outer ring = 13 Moons, Middle = Seasons, Inner = Solar events. Tap a section below to explore.")
    # Draw wheel
    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_aspect('equal'); ax.axis('off')
    # Seasons - 4 quadrants (Southern Hemisphere: Dec at top)
    seasons = [("Summer\nDec-Feb", "#FFD54F"), ("Autumn\nMar-May", "#FF8A65"), ("Winter\nJun-Aug", "#81D4FA"), ("Spring\nSep-Nov", "#A5D6A7")]
    # Draw 13 moons as outer ring
    angles = np.linspace(90, 90-360, 14)
    for i in range(13):
        a1, a2 = np.deg2rad(angles[i]), np.deg2rad(angles[i+1])
        ax.add_patch(plt.matplotlib.patches.Wedge((0,0), 1.0, np.rad2deg(a2), np.rad2deg(a1), width=0.22, facecolor=plt.cm.viridis(i/13), edgecolor='white'))
        mid = np.deg2rad((angles[i]+angles[i+1])/2)
        ax.text(0.89*np.cos(mid), 0.89*np.sin(mid), f"{i+1}", ha='center', va='center', fontsize=9, color='white', weight='bold')
    # Seasons inner
    for i, (label, col) in enumerate(seasons):
        # Summer at top (90 deg) going clockwise
        start = 90 - i*90
        ax.add_patch(plt.matplotlib.patches.Wedge((0,0), 0.75, start-90, start, width=0.35, facecolor=col, edgecolor='white', alpha=0.9))
        mid = np.deg2rad(start-45)
        ax.text(0.57*np.cos(mid), 0.57*np.sin(mid), label, ha='center', va='center', fontsize=8, weight='bold')
    ax.text(0,0,"THE\nMOON\nCIRCLE", ha='center', va='center', fontsize=14, weight='bold')
    ax.text(0,-1.25,"Outer: 13 Moons • Middle: 4 Seasons • Centre: You", ha='center', fontsize=9)
    st.pyplot(fig)
    sel = st.selectbox("Explore a Moon:", [m['name'] for m in MOON_CYCLE])
    m = [x for x in MOON_CYCLE if x['name']==sel][0]
    st.success(f"**{m['name']}** - {m['dates']} | {m['season']} | {m['theme']}")

# SEASONAL PROGRAMMES
elif menu == "🌿 Seasonal Programmes":
    st.header("Seasonal Ritual Engine - 4 Programmes")
    choice = st.selectbox("Choose Season:", list(SEASONS.keys()))
    s = SEASONS[choice]
    st.subheader(f"Opening Ceremony: {choice}")
    st.write(s['opening'])
    st.write(f"**Weekly Activities:**")
    for w in s['weekly']: st.write(f"- {w}")
    st.write(f"**Daily Mindfulness:** {s['daily']}")
    st.write(f"**Physical:** {s['physical']}")
    st.write(f"**Nature Connection:** {s['nature']}")
    st.write(f"**Evening Reflection:** What did I learn today? What am I grateful for?")
    st.write(f"**Closing Ceremony:** {s['closing']}")
    st.info("Working-person: Opening & Closing = 30 min on a weekend. Daily = 5 min. Weekly = 15 min.")

# COSMIC EVENTS
elif menu == "✨ Cosmic Events":
    st.header("Cosmic Event Engine - SAST")
    st.write("All times in **South African Standard Time (UTC+2)**. Visibility from South Africa shown.")
    filter_type = st.selectbox("Filter:", ["All", "Moon", "Solar", "Eclipse", "Meteor"])
    for d, t, ev, vis, typ in COSMIC_EVENTS_2026_2027:
        if filter_type != "All" and filter_type != typ: continue
        with st.expander(f"{d} {t} SAST - {ev}"):
            st.write(f"**Visible from SA:** {vis}")
            st.write(f"**Reflective Ritual (15 min):** 1) Step outside / look at sky photo (5 min), 2) Journal: What is this event teaching me about cycles? (5 min), 3) Set one small action for the next moon (5 min)")
            st.write(f"**Closing:** *I move with the rhythm of sky and earth.*")

# RITUAL LIBRARY
elif menu == "📚 Ritual Library":
    st.header("Ritual Library - Searchable")
    search = st.text_input("Search ritual (e.g. morning, new moon, gratitude):", "").lower()
    cat = st.selectbox("Category:", ["All", "Morning", "Evening", "New Moon", "Full Moon", "Seasonal", "Gratitude", "Nature", "Silence", "Release"])

    # Rituals
    rituals = []
    if cat in ["All", "Morning"] and ("morning" in search or search==""):
        ritual_card("🌅 Morning Intention Ritual", "Start day with clarity", "Water, quiet corner", "Water, journal if you have it",
            ["Drink water slowly", "3 deep breaths", "Name 1 intention"],
            ["Drink water", "5 min breath", "Write 3 intentions", "Stretch 5 min"],
            ["Drink water", "10 min journal", "10 min walk outside", "5 min gratitude", "5 min planning"],
            "What do I want to grow today?", "I begin with intention and kindness.")
    if cat in ["All", "Evening"] and ("evening" in search or search==""):
        ritual_card("🌙 Evening Release Ritual", "End day, let go of stress", "Dim lights, phone off", "Candle (optional)",
            ["3 breaths", "Name 1 thing to release", "Breathe out"],
            ["Journal 3 gratitudes", "Body scan 5 min", "Release list 5 min"],
            ["Warm bath / tea", "Journal 10 min", "10 min silence", "Forgiveness reflection"],
            "What can I put down tonight?", "I rest. Tomorrow is new.")
    if cat in ["All", "New Moon"] and ("new" in search or search==""):
        ritual_card("🌑 New Moon Ceremony", "Set intention for new cycle", "Quiet, dark sky if possible", "Paper, pen",
            ["Breathe", "Write 1 intention", "Place paper where you see it"],
            ["Clean space", "Write 3 intentions", "Visualise 5 min", "Commit to 1 action"],
            ["Clean + candle", "Review last moon 10 min", "Write intentions 10 min", "Meditation 10 min"],
            "What is ready to begin?", "I plant with trust.")
    if cat in ["All", "Full Moon"] and ("full" in search or search==""):
        ritual_card("🌕 Full Moon Reflection", "Review, gratitude, celebrate", "Outside or window", "None",
            ["Look at moon", "Name 1 gratitude", "Breathe"],
            ["Walk 5 min", "Journal wins 5 min", "Gratitude 5 min"],
            ["Moon walk 10 min", "Journal 10 min", "Share gratitude with family 10 min"],
            "What has come to fullness?", "I am grateful for what is.")
    if cat in ["All", "Gratitude"] and ("gratitude" in search or search==""):
        ritual_card("🙏 Gratitude Practice", "Cultivate appreciation", "Quiet", "Journal",
            ["Name 3 things you're grateful for"],
            ["Write 5 gratitudes", "Thank one person by message"],
            ["Write 10 gratitudes", "Cook / share food", "Call elder to thank"],
            "Who helped me this week?", "I have enough. I am enough.")
    if cat in ["All", "Release"] and ("release" in search or search==""):
        ritual_card("🍂 Release & Renewal", "Let go safely", "Safe space", "Paper, bin / compost",
            ["Write 1 thing to release", "Tear paper"],
            ["Write 3 releases", "Breathe, tear, compost"],
            ["Walk 10 min", "Write + burn safely / tear", "Plan new habit"],
            "What no longer serves me?", "I release with love. I make space.")
    if not rituals and search:
        st.write("Try: morning, evening, new moon, full moon, gratitude, release")

# CULTURAL TRADITIONS
elif menu == "🏛️ Cultural Traditions":
    st.header("Cultural Traditions - Documented Knowledge Only")
    st.warning("We do NOT invent month names or ceremonies. Names vary by region, clan, and language. Below are documented examples - presented separately.")
    st.subheader("Zulu (isiZulu) - KwaZulu-Natal")
    st.write("Documented Zulu lunar calendar is tied to agricultural and ecological markers. Examples documented by historians/linguists include months linked to planting, first fruits, and rains. Names and order differ between sources. Always confirm with local elders / izangoma in your area.")
    st.write("Example documented names in some sources: uMasingana, uNhlolanja, uNdasa, uMbasa, uNhlaba, uNhlangulana, uNtulikazi, uNcwaba, uMandulo, uMfumfu, uLwezi, uZibandlela. *Variation is normal - not error.*")
    st.subheader("Xhosa (isiXhosa) - Eastern Cape")
    st.write("Documented Xhosa months are also lunar-ecological, e.g. EyoMqungu (June - dry grass), EyoMsintsi, EyeKhala, etc. Different districts use different names. Presented separately from Zulu system.")
    st.subheader("Sotho-Tswana (Sesotho / Setswana)")
    st.write("Sotho calendars track seasons: Selemo (spring), Lehlabula (summer), Letshitla / Hoetla (autumn), Mariha (winter). Month names vary between Basotho, Batswana, Bapedi. Do not merge into one system.")
    st.subheader("Khoi & San")
    st.write("Khoi and San peoples have rich astronomical knowledge - stars used for navigation, seasonal hunting, rain prediction, and storytelling. Much knowledge is oral and held by specific communities. We do not list sacred stories here without community permission. Seek guidance from Khoi/San cultural custodians.")
    st.subheader("How We Handle This in the App")
    st.write("1. **Documented** = cited from published ethnography / community sources\n2. **Contemporary** = modern interpretation, labelled as such\n3. **New** = created for this app for personal development\n4. **Scientific** = NASA / astronomical data")
    st.success("If you are a cultural practitioner and see an error, please contact us to correct it. This is a living calendar.")

st.sidebar.markdown("in ---")
st.sidebar.write("🌙 The Moon Circle v1.0")
st.sidebar.write("Made for South Africa • SAST")
st.sidebar.write("Working-person friendly: 5 / 15 / 30 min versions")