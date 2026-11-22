"""
THE MOON CIRCLE
A South-African seasonal reflection and astronomy companion.

Run locally:
    python -m pip install -r requirements.txt
    python -m streamlit run app.py

The 13 × 28-day calendar is a contemporary planning framework, not an
astronomical or historically documented African calendar. Moon phase is an
approximation calculated from a known reference new moon.
"""

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import streamlit as st

# ---------------------------------------------------------------------
# Page setup and constants
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="The Moon Circle",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

SA_TZ = ZoneInfo("Africa/Johannesburg")
UTC = timezone.utc

APP_START = date(2026, 1, 18)
SYMBOLIC_CYCLE_DAYS = 28
SYMBOLIC_YEAR_DAYS = 13 * SYMBOLIC_CYCLE_DAYS

# Reference new moon: 2000-01-06 18:14 UTC.
# This produces an approximate phase, not a precision ephemeris.
REFERENCE_NEW_MOON = datetime(2000, 1, 6, 18, 14, tzinfo=UTC)
SYNODIC_MONTH = 29.530588853

SEASONS = {
    "Summer": {
        "months": "December – February",
        "theme": "Vitality, abundance and joy",
        "description": "A season often associated with warmth, longer days and outdoor life in much of South Africa.",
        "opening": "Choose one thing you would like to enjoy or share this season.",
        "weekly": [
            "Notice one activity that gives you energy.",
            "Prepare or share a meal with someone.",
            "Spend time outdoors during a comfortable part of the day.",
            "Pass on an item or skill that may help someone else.",
        ],
        "daily": "Name one good moment from the day.",
        "nature": "Notice changes in daylight, heat, rain and plant growth.",
        "closing": "Write down what you enjoyed and what you want to carry forward.",
    },
    "Autumn": {
        "months": "March – May",
        "theme": "Harvest, gratitude and adjustment",
        "description": "A time to notice what has matured, what has changed and what needs attention.",
        "opening": "Think of one effort that has produced a result, however small.",
        "weekly": [
            "Review one goal and the progress you have made.",
            "Organise something you want to keep or preserve.",
            "Pass on, recycle or donate an item you no longer need.",
            "Thank someone who has helped you.",
        ],
        "daily": "Ask: what did I learn today?",
        "nature": "Notice changing leaves, temperatures and seasonal weather.",
        "closing": "Record three things you learned or completed this season.",
    },
    "Winter": {
        "months": "June – August",
        "theme": "Rest, reflection and foundations",
        "description": "A useful season for slower routines, learning and preparing for future projects.",
        "opening": "Choose one area of life where a little more rest or structure would help.",
        "weekly": [
            "Make one small improvement to your space.",
            "Ask a family member about a memory or lesson.",
            "Spend time on a skill you want to develop.",
            "Make a simple plan for the next season.",
        ],
        "daily": "Take a quiet moment and write one sentence about your day.",
        "nature": "Notice the night sky, cooler air and changes in daylight.",
        "closing": "Write down one lesson you want to remember.",
    },
    "Spring": {
        "months": "September – November",
        "theme": "Renewal, planting and new beginnings",
        "description": "A season often associated with new growth and warmer days in much of South Africa.",
        "opening": "Choose one small intention and one practical action that supports it.",
        "weekly": [
            "Clear or organise one small area.",
            "Begin a manageable habit or project.",
            "Notice new growth in a garden or local green space.",
            "Share encouragement, knowledge or a useful resource.",
        ],
        "daily": "Ask: what small thing can I help grow today?",
        "nature": "Notice buds, insects, birds, rainfall and changing temperatures.",
        "closing": "List what began, improved or became clearer this season.",
    },
}

SEASON_ORDER = ["Summer", "Autumn", "Winter", "Spring"]

RITUALS = [
    {
        "title": "Morning Intention",
        "category": "Morning",
        "purpose": "Begin the day with a clear, realistic priority.",
        "materials": "Optional notebook and water.",
        "five": ["Pause for three calm breaths.", "Choose one priority for today.", "Name the first small action."],
        "fifteen": ["Take a quiet moment.", "Write one priority and why it matters.", "Break it into a first step.", "Stretch or move gently if comfortable."],
        "thirty": ["Review yesterday without judging yourself.", "Write one priority.", "Plan the first two steps.", "Spend a few minutes outside or near a window.", "Finish by choosing when to begin."],
        "reflection": "What would make today feel meaningful?",
        "closing": "I can begin with one manageable step.",
    },
    {
        "title": "Evening Reflection",
        "category": "Evening",
        "purpose": "Create a gentle transition from the day to rest.",
        "materials": "Optional notebook; no special equipment needed.",
        "five": ["Take three slow breaths.", "Name one thing that went well.", "Choose one thought to leave for tomorrow."],
        "fifteen": ["Put away one distraction.", "Write three things you noticed today.", "Identify anything that needs attention tomorrow."],
        "thirty": ["Make a warm drink if you like.", "Write about one challenge and one success.", "Prepare one thing that will make tomorrow easier.", "Spend a few quiet minutes reading or listening to calm sounds."],
        "reflection": "What can wait until tomorrow?",
        "closing": "Rest is part of a balanced life.",
    },
    {
        "title": "New Moon: Begin Again",
        "category": "New Moon",
        "purpose": "Use the new-moon idea as a prompt for setting an intention.",
        "materials": "Paper or a notes app.",
        "five": ["Choose one intention.", "Write one practical action.", "Decide when to take that action."],
        "fifteen": ["Review what has changed recently.", "Write up to three intentions.", "Choose the most important one.", "Make its first step specific."],
        "thirty": ["Reflect on the past few weeks.", "Write what you want to begin, continue and change.", "Choose one small commitment.", "Put a reminder somewhere useful."],
        "reflection": "What am I ready to begin?",
        "closing": "A clear intention becomes useful through action.",
    },
    {
        "title": "Full Moon: Review and Appreciate",
        "category": "Full Moon",
        "purpose": "Reflect on progress and recognise what deserves appreciation.",
        "materials": "Optional notebook.",
        "five": ["Name one thing you appreciate.", "Name one thing you learned.", "Choose one next step."],
        "fifteen": ["Review a goal.", "Write down progress, including small steps.", "Thank someone who supported you."],
        "thirty": ["Look back over the last few weeks.", "Record achievements and lessons.", "Notice what needs adjusting.", "Choose one next step for the coming days."],
        "reflection": "What has changed since I last checked in?",
        "closing": "Progress can be gradual and still matter.",
    },
    {
        "title": "Gratitude Pause",
        "category": "Gratitude",
        "purpose": "Pay attention to people, moments and resources you value.",
        "materials": "None.",
        "five": ["Name three things you appreciate.", "Choose one person you could thank."],
        "fifteen": ["Write five specific things you appreciate.", "Send a genuine thank-you message if appropriate.", "Notice how those moments came about."],
        "thirty": ["Write about people who have supported you.", "Recall a small moment that made you happy.", "Choose one practical way to show appreciation."],
        "reflection": "What might I overlook when life gets busy?",
        "closing": "I can notice and appreciate the good around me.",
    },
    {
        "title": "Let Go and Make Space",
        "category": "Release",
        "purpose": "Identify one manageable thing you no longer need to carry forward.",
        "materials": "Optional paper and a recycling bin.",
        "five": ["Name one task, worry or habit you want to address.", "Write one small action you can take."],
        "fifteen": ["Write down what is taking up attention.", "Separate what you can influence from what you cannot.", "Choose one practical next step."],
        "thirty": ["Tidy one small area or organise one list.", "Write what you want to change.", "Recycle or put away the paper if you used it.", "Choose a realistic next action."],
        "reflection": "What can I simplify?",
        "closing": "I can make space through small, practical choices.",
    },
]

# ---------------------------------------------------------------------
# Date and astronomy helpers
# ---------------------------------------------------------------------

def south_african_today() -> date:
    return datetime.now(SA_TZ).date()


def season_for_day(day: date) -> str:
    month = day.month
    if month in (12, 1, 2):
        return "Summer"
    if month in (3, 4, 5):
        return "Autumn"
    if month in (6, 7, 8):
        return "Winter"
    return "Spring"


def moon_age_days(day: date) -> float:
    local_midday = datetime(day.year, day.month, day.day, 12, tzinfo=SA_TZ)
    age = (local_midday.astimezone(UTC) - REFERENCE_NEW_MOON).total_seconds() / 86400
    return age % SYNODIC_MONTH


def moon_phase(day: date):
    age = moon_age_days(day)
    fraction = age / SYNODIC_MONTH
    illumination = (1 - __import__("math").cos(2 * __import__("math").pi * fraction)) / 2

    if age < 1.85 or age >= SYNODIC_MONTH - 1.85:
        name, emoji = "New Moon", "🌑"
    elif age < 5.53:
        name, emoji = "Waxing Crescent", "🌒"
    elif age < 9.22:
        name, emoji = "First Quarter", "🌓"
    elif age < 12.91:
        name, emoji = "Waxing Gibbous", "🌔"
    elif age < 16.61:
        name, emoji = "Full Moon", "🌕"
    elif age < 20.30:
        name, emoji = "Waning Gibbous", "🌖"
    elif age < 23.99:
        name, emoji = "Last Quarter", "🌗"
    else:
        name, emoji = "Waning Crescent", "🌘"

    return name, emoji, round(illumination * 100), round(age, 1)


def symbolic_moon_for_day(day: date):
    offset = (day - APP_START).days
    cycle_index = (offset // SYMBOLIC_CYCLE_DAYS) % 13
    cycle_number = (offset // SYMBOLIC_CYCLE_DAYS) + 1
    start = APP_START + timedelta(days=(offset // SYMBOLIC_CYCLE_DAYS) * SYMBOLIC_CYCLE_DAYS)
    end = start + timedelta(days=SYMBOLIC_CYCLE_DAYS - 1)
    names = [
        ("First Planting", "Beginnings, clearing and setting intention"),
        ("Ripening", "Growth, tending and patience"),
        ("Turning", "Balance and reviewing progress"),
        ("Gathering", "Harvest, gratitude and storing"),
        ("Letting Go", "Release, composting and rest"),
        ("Stillness", "Restoration and reflection"),
        ("Deep Roots", "Wisdom, family and foundations"),
        ("First Bud", "Preparation and quiet hope"),
        ("Blossoming", "Renewal and planting"),
        ("Rain Calling", "Nourishment, growth and intention"),
        ("Abundance", "Vitality, generosity and expression"),
        ("Full Sun", "Celebration, joy and energy"),
        ("Completion", "Integration, rest and closing a cycle"),
    ]
    name, theme = names[cycle_index]
    return {
        "number": cycle_number,
        "name": name,
        "theme": theme,
        "start": start,
        "end": end,
        "within_cycle": (day - start).days + 1,
    }


def format_date(day: date) -> str:
    return day.strftime("%A, %d %B %Y")


def render_ritual(ritual):
    st.subheader(ritual["title"])
    st.caption(f"Category: {ritual['category']} · Contemporary practice created for this app")
    st.write(ritual["purpose"])
    st.caption(f"Materials: {ritual['materials']}")
    t1, t2, t3 = st.tabs(["5 minutes", "15 minutes", "30 minutes"])
    with t1:
        for step in ritual["five"]:
            st.write(f"- {step}")
    with t2:
        for step in ritual["fifteen"]:
            st.write(f"- {step}")
    with t3:
        for step in ritual["thirty"]:
            st.write(f"- {step}")
    st.write(f"**Reflection:** {ritual['reflection']}")
    st.write(f"*{ritual['closing']}*")
    st.divider()


# ---------------------------------------------------------------------
# Sidebar and shared header
# ---------------------------------------------------------------------

today = south_african_today()

st.sidebar.title("🌙 The Moon Circle")
st.sidebar.caption("A seasonal reflection companion")
page = st.sidebar.radio(
    "Explore",
    [
        "Today",
        "13-Moon Calendar",
        "Seasonal Wheel",
        "Seasonal Programmes",
        "Cosmic & Moon Guide",
        "Ritual Library",
        "Cultural Notes",
        "Journal",
    ],
)
st.sidebar.divider()
st.sidebar.caption("South Africa · SAST (UTC+2)")
st.sidebar.caption("Version 2.0 · Educational and reflective")

st.title("🌙 The Moon Circle")
st.markdown(
    "A South African seasonal reflection and sky-awareness companion. "
    "Use the symbolic calendar for planning and the astronomy guide for "
    "approximate sky information."
)

with st.expander("A note about culture, science and this calendar"):
    st.markdown(
        """
        - **Astronomy:** Moon phase is estimated mathematically and is not a
          substitute for a professional ephemeris or local sky forecast.
        - **Symbolic calendar:** The 13 periods of 28 days are a contemporary
          planning framework created for this app. They are not presented as
          an ancient, universal or specifically Zulu calendar.
        - **Seasonal programme:** The four seasons use the Southern Hemisphere
          month pattern as a broad guide. Local weather and ecology vary.
        - **Rituals:** The activities in this app are contemporary reflection
          exercises, not ceremonies claimed to belong to a particular culture.
        - **Cultural knowledge:** Traditions differ between communities and
          knowledge holders. The app avoids assigning sacred practices or
          unverified month names to whole peoples.
        """
    )

# ---------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------

if page == "Today":
    season = season_for_day(today)
    phase, phase_icon, illumination, age = moon_phase(today)
    symbolic = symbolic_moon_for_day(today)

    st.header(f"Today · {format_date(today)}")
    st.caption("Date and time zone: South Africa Standard Time")

    a, b, c = st.columns(3)
    a.metric("Season", season, SEASONS[season]["months"])
    b.metric("Approximate Moon Phase", f"{phase_icon} {phase}")
    c.metric("Estimated illumination", f"{illumination}%")

    st.subheader(f"Your symbolic period: Moon {symbolic['number']} – {symbolic['name']}")
    st.write(f"**Theme:** {symbolic['theme']}")
    st.write(
        f"**Dates:** {symbolic['start'].strftime('%d %b %Y')} – "
        f"{symbolic['end'].strftime('%d %b %Y')} "
        f"({symbolic['within_cycle']} of 28 days)"
    )

    st.subheader("A small practice for today")
    st.write(SEASONS[season]["daily"])
    st.info("Keep it manageable. A short reflection is enough; you do not need to complete every activity.")

    with st.expander("What does the Moon estimate mean?"):
        st.write(
            f"The calculated lunar age is about {age} days into an average "
            f"{SYNODIC_MONTH:.2f}-day cycle. Actual visible appearance depends "
            "on location, weather, horizon and observation time."
        )

elif page == "13-Moon Calendar":
    st.header("The 13-Moon Calendar")
    st.warning(
        "This is a symbolic planning calendar: 13 × 28 days = 364 days. "
        "It does not match the astronomical lunar cycle, which averages "
        "about 29.53 days. Its dates are calculated from 18 January 2026."
    )

    chosen_date = st.date_input("Explore a date", value=today)
    item = symbolic_moon_for_day(chosen_date)
    st.subheader(f"Moon {item['number']} · {item['name']}")
    st.write(f"**Period:** {item['start'].strftime('%d %B %Y')} – {item['end'].strftime('%d %B %Y')}")
    st.write(f"**Day in period:** {item['within_cycle']} / 28")
    st.write(f"**Theme:** {item['theme']}")
    st.write("**Reflection:** What is growing, what needs attention, and what can be simplified?")

    st.divider()
    st.subheader("All 13 periods")
    for i in range(13):
        start = APP_START + timedelta(days=i * SYMBOLIC_CYCLE_DAYS)
        end = start + timedelta(days=27)
        names = [
            "First Planting", "Ripening", "Turning", "Gathering",
            "Letting Go", "Stillness", "Deep Roots", "First Bud",
            "Blossoming", "Rain Calling", "Abundance", "Full Sun",
            "Completion",
        ]
        with st.expander(f"Moon {i + 1}: {names[i]} · {start:%d %b %Y} – {end:%d %b %Y}"):
            st.write("This is one 28-day section of the app's symbolic planning year.")
            st.write("Use the theme as a prompt, not as a rule or prediction.")

elif page == "Seasonal Wheel":
    st.header("Southern Hemisphere Seasonal Wheel")
    st.caption("A simple seasonal overview — not a claim about one shared African traditional calendar.")

    wheel_cols = st.columns(4)
    season_emojis = {"Summer": "☀️", "Autumn": "🍂", "Winter": "❄️", "Spring": "🌱"}
    for col, season_name in zip(wheel_cols, SEASON_ORDER):
        data = SEASONS[season_name]
        with col:
            st.markdown(f"### {season_emojis[season_name]} {season_name}")
            st.write(data["months"])
            st.caption(data["theme"])

    st.divider()
    selected = st.selectbox("Explore a season", SEASON_ORDER, index=SEASON_ORDER.index(season_for_day(today)))
    data = SEASONS[selected]
    st.subheader(f"{selected}: {data['theme']}")
    st.write(data["description"])
    st.write(f"**Opening reflection:** {data['opening']}")
    st.write("**Ideas for the weeks:**")
    for activity in data["weekly"]:
        st.write(f"- {activity}")
    st.write(f"**Daily prompt:** {data['daily']}")
    st.write(f"**Nature observation:** {data['nature']}")
    st.write(f"**Closing reflection:** {data['closing']}")

elif page == "Seasonal Programmes":
    st.header("Seasonal Programmes")
    selected = st.selectbox("Choose a season", SEASON_ORDER, index=SEASON_ORDER.index(season_for_day(today)))
    data = SEASONS[selected]
    st.subheader(f"{selected} · {data['months']}")
    st.write(data["description"])
    st.markdown(f"**Start here:** {data['opening']}")
    st.markdown("**Weekly activities**")
    for activity in data["weekly"]:
        st.write(f"- {activity}")
    st.markdown(f"**Daily mindfulness prompt:** {data['daily']}")
    st.markdown(f"**Nature connection:** {data['nature']}")
    st.markdown(f"**End-of-season reflection:** {data['closing']}")
    st.info("Choose only the activities that are useful and practical for your circumstances.")

elif page == "Cosmic & Moon Guide":
    st.header("Cosmic & Moon Guide")
    st.write(
        "The phase estimate below is calculated from an average lunar cycle. "
        "It does not calculate moonrise, moonset, eclipses or local visibility."
    )
    chosen_date = st.date_input("Check the estimated Moon phase", value=today, key="phase_date")
    phase, icon, illumination, age = moon_phase(chosen_date)
    x, y, z = st.columns(3)
    x.metric("Estimated phase", f"{icon} {phase}")
    y.metric("Illumination", f"{illumination}%")
    z.metric("Lunar age", f"{age} days")
    st.caption("Approximation only. Small differences from published astronomical calendars are expected.")

    st.subheader("The eight commonly used phase names")
    phases = [
        ("🌑", "New Moon", "The Moon is near the Sun in the sky and is difficult to see."),
        ("🌒", "Waxing Crescent", "The illuminated portion appears to grow."),
        ("🌓", "First Quarter", "About half of the visible disk is illuminated."),
        ("🌔", "Waxing Gibbous", "More than half is illuminated and growing."),
        ("🌕", "Full Moon", "The visible disk is close to fully illuminated."),
        ("🌖", "Waning Gibbous", "The illuminated portion appears to shrink."),
        ("🌗", "Last Quarter", "About half of the visible disk is illuminated again."),
        ("🌘", "Waning Crescent", "A thinner crescent remains before the next new moon."),
    ]
    for emoji, name, description in phases:
        st.write(f"**{emoji} {name}:** {description}")

    st.subheader("Seasonal sky observation")
    st.write(
        "If you choose to observe the sky, do so from a safe, familiar place. "
        "Never look directly at the Sun, including during an eclipse. Use "
        "certified solar viewing equipment for solar events."
    )
    st.caption(
        "This version does not publish a dated eclipse or meteor-shower timetable. "
        "Check a current astronomy source before planning an observation."
    )

elif page == "Ritual Library":
    st.header("Ritual Library")
    st.write("These are contemporary reflection exercises written for The Moon Circle.")
    query = st.text_input("Search by title, category or keyword", placeholder="Try: gratitude, evening, moon")
    categories = ["All"] + sorted({r["category"] for r in RITUALS})
    category = st.selectbox("Filter by category", categories)

    filtered = []
    for ritual in RITUALS:
        searchable = " ".join([
            ritual["title"], ritual["category"], ritual["purpose"],
            ritual["reflection"], ritual["closing"],
        ]).casefold()
        matches_query = not query.strip() or query.casefold().strip() in searchable
        matches_category = category == "All" or ritual["category"] == category
        if matches_query and matches_category:
            filtered.append(ritual)

    if filtered:
        for ritual in filtered:
            render_ritual(ritual)
    else:
        st.info("No matching practices. Try a broader word or choose All categories.")

elif page == "Cultural Notes":
    st.header("Cultural Notes")
    st.warning(
        "This page is intentionally cautious. It does not claim to document "
        "specific ceremonies, sacred knowledge or a single pan-African calendar."
    )
    st.subheader("Why the wording matters")
    st.write(
        "African communities have diverse languages, histories, ecological "
        "knowledge and ways of marking time. Practices may differ between "
        "regions, families and knowledge holders. A seasonal pattern used in "
        "one place should not automatically be attributed to another."
    )
    st.subheader("How this app labels information")
    st.markdown(
        """
        - **Scientific estimate:** a calculation or astronomical fact, with
          its limits stated.
        - **Seasonal guide:** a broad Southern Hemisphere month pattern.
        - **Contemporary practice:** a reflection exercise newly written for
          this app.
        - **Community knowledge:** should be included only with reliable
          sources, accurate language, clear attribution and appropriate
          permission where required.
        """
    )
    st.subheader("Before adding a cultural tradition")
    st.write(
        "Record the exact community and language, the source or knowledge "
        "holder, the location and context, and any known variation. Do not "
        "present a general internet summary as the voice of an entire people."
    )
    st.caption("This page is a framework for responsible research, not a substitute for community guidance.")

elif page == "Journal":
    st.header("Reflection Journal")
    st.write(
        "Write a private note for this session. In this starter version, "
        "entries are kept only in the current app session and may disappear "
        "when the app restarts or the session ends. Do not enter sensitive "
        "personal information."
    )
    journal_date = st.date_input("Entry date", value=today, key="journal_date")
    journal_text = st.text_area("Your reflection", height=180, placeholder="What did you notice, learn or appreciate?")
    if st.button("Save this session's entry", type="primary"):
        if journal_text.strip():
            st.session_state.setdefault("journal_entries", [])
            st.session_state["journal_entries"].insert(
                0, {"date": journal_date.isoformat(), "text": journal_text.strip()}
            )
            st.success("Entry added to this app session.")
        else:
            st.warning("Write a note before saving.")

    entries = st.session_state.get("journal_entries", [])
    if entries:
        st.subheader("Entries in this session")
        for entry in entries:
            with st.expander(entry["date"]):
                st.write(entry["text"])
    else:
        st.caption("No entries saved in this session yet.")

# Footer
st.divider()
st.caption(
    "The Moon Circle · South Africa · Symbolic planning and approximate phase estimates. "
    "Not an authoritative cultural, astronomical or medical resource."
)
