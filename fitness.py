import streamlit as st
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="FitFuel - Gym Diet Planner",
    page_icon="💪",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.meal {
    padding: 18px;
    border-radius: 12px;
    background-color: #ffffff;
    border-left: 5px solid #ff4b4b;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown('<div class="title">💪 FitFuel</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Personalized Gym Diet Planner</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("👤 Your Profile")

name = st.sidebar.text_input(
    "Name",
    placeholder="Enter your name"
)

age = st.sidebar.number_input(
    "Age",
    min_value=15,
    max_value=80,
    value=25
)

gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)

height = st.sidebar.number_input(
    "Height (cm)",
    min_value=100.0,
    max_value=230.0,
    value=175.0
)

weight = st.sidebar.number_input(
    "Weight (kg)",
    min_value=30.0,
    max_value=200.0,
    value=60.0
)

goal = st.sidebar.selectbox(
    "Fitness Goal",
    [
        "Gain Muscle / Weight",
        "Maintain Weight",
        "Lose Fat"
    ]
)

activity = st.sidebar.selectbox(
    "Activity Level",
    [
        "Lightly Active",
        "Moderately Active",
        "Very Active"
    ]
)

diet = st.sidebar.selectbox(
    "Diet Preference",
    [
        "Vegetarian",
        "Non-Vegetarian"
    ]
)

generate = st.sidebar.button(
    "🔥 Generate My Diet Plan",
    use_container_width=True
)


# ---------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------

def calculate_bmi(weight, height):

    height_m = height / 100

    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal Weight"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def calculate_bmr(weight, height, age, gender):

    if gender == "Male":

        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )

    else:

        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

    return bmr


def calculate_calories(bmr, activity, goal):

    activity_factor = {
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }

    calories = bmr * activity_factor[activity]

    if goal == "Gain Muscle / Weight":
        calories += 300

    elif goal == "Lose Fat":
        calories -= 400

    return int(calories)


def calculate_protein(weight, goal):

    if goal == "Gain Muscle / Weight":

        return int(weight * 1.8)

    elif goal == "Lose Fat":

        return int(weight * 2.0)

    else:

        return int(weight * 1.6)


# ---------------------------------------------------
# DIET PLAN
# ---------------------------------------------------

def vegetarian_plan():

    return {

        "🌅 Breakfast": [
            "3 Paneer Stuffed Paratha",
            "200 ml Milk",
            "1 Banana"
        ],

        "🥤 Mid-Morning Shake": [
            "300 ml Milk",
            "1 Banana",
            "1 Full Spoon Peanut Butter",
            "20 g Oats"
        ],

        "🍱 Lunch": [
            "2-3 Roti",
            "1 Bowl Dal",
            "1 Bowl Rice",
            "100 g Paneer",
            "Salad"
        ],

        "⚡ Pre-Workout": [
            "1 Banana",
            "2 Brown Bread",
            "Peanut Butter"
        ],

        "🏋️ Post-Workout": [
            "300 ml Milk",
            "1 Banana",
            "20 g Oats"
        ],

        "🌙 Dinner": [
            "2-3 Roti",
            "Paneer / Tofu",
            "1 Bowl Dal",
            "Vegetable Sabzi",
            "Salad"
        ],

        "🥛 Before Bed": [
            "200 ml Milk"
        ]
    }


def nonveg_plan():

    return {

        "🌅 Breakfast": [
            "3 Egg Omelette",
            "2 Brown Bread",
            "1 Banana",
            "200 ml Milk"
        ],

        "🥤 Mid-Morning Shake": [
            "300 ml Milk",
            "1 Banana",
            "1 Full Spoon Peanut Butter",
            "20 g Oats"
        ],

        "🍱 Lunch": [
            "2-3 Roti",
            "1 Bowl Rice",
            "150 g Chicken",
            "Vegetable Sabzi",
            "Salad"
        ],

        "⚡ Pre-Workout": [
            "1 Banana",
            "2 Brown Bread",
            "Peanut Butter"
        ],

        "🏋️ Post-Workout": [
            "300 ml Milk",
            "1 Banana",
            "20 g Oats"
        ],

        "🌙 Dinner": [
            "2-3 Roti",
            "150 g Chicken",
            "1 Bowl Dal",
            "Vegetable Sabzi",
            "Salad"
        ],

        "🥛 Before Bed": [
            "200 ml Milk"
        ]
    }


# ---------------------------------------------------
# MAIN APP
# ---------------------------------------------------

if generate:

    if name.strip() == "":
        name = "Athlete"

    bmi = calculate_bmi(weight, height)

    category = bmi_category(bmi)

    bmr = calculate_bmr(
        weight,
        height,
        age,
        gender
    )

    calories = calculate_calories(
        bmr,
        activity,
        goal
    )

    protein = calculate_protein(
        weight,
        goal
    )

    # -----------------------------------------------
    # WELCOME
    # -----------------------------------------------

    st.success(
        f"🔥 Welcome {name}! Your personalized plan is ready."
    )

    # -----------------------------------------------
    # METRICS
    # -----------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "BMI",
            bmi
        )

    with col2:

        st.metric(
            "BMI Category",
            category
        )

    with col3:

        st.metric(
            "Daily Calories",
            f"{calories} kcal"
        )

    with col4:

        st.metric(
            "Protein Target",
            f"{protein} g"
        )

    st.divider()

    # -----------------------------------------------
    # PROFILE
    # -----------------------------------------------

    st.subheader("📊 Your Fitness Profile")

    profile = pd.DataFrame({

        "Parameter": [
            "Name",
            "Age",
            "Gender",
            "Height",
            "Weight",
            "Goal",
            "Activity Level",
            "Diet"
        ],

        "Value": [
            name,
            f"{age} years",
            gender,
            f"{height} cm",
            f"{weight} kg",
            goal,
            activity,
            diet
        ]

    })

    st.dataframe(
        profile,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------------------------
    # DIET PLAN
    # -----------------------------------------------

    st.subheader("🍽️ Your Daily Diet Plan")

    if diet == "Vegetarian":

        plan = vegetarian_plan()

    else:

        plan = nonveg_plan()

    for meal, foods in plan.items():

        st.markdown(
            f'<div class="meal"><h3>{meal}</h3>',
            unsafe_allow_html=True
        )

        for food in foods:

            st.write(f"• {food}")

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------
    # TARGETS
    # -----------------------------------------------

    st.divider()

    st.subheader("🎯 Daily Targets")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info(
            f"🔥 Calories\n\n**{calories} kcal/day**"
        )

    with c2:

        st.info(
            f"🥩 Protein\n\n**{protein} g/day**"
        )

    with c3:

        st.info(
            f"💧 Water\n\n**2.5–3.5 L/day**"
        )

    # -----------------------------------------------
    # BMI MESSAGE
    # -----------------------------------------------

    st.divider()

    if bmi < 18.5:

        st.warning(
            "Your BMI is in the underweight range. "
            "A calorie surplus and resistance training "
            "can support healthy weight gain."
        )

    elif bmi < 25:

        st.success(
            "Your BMI is in the normal range. "
            "Focus on progressive strength training "
            "and consistent nutrition."
        )

    elif bmi < 30:

        st.warning(
            "Your BMI is in the overweight range. "
            "A controlled calorie deficit with strength "
            "training may help reduce body fat."
        )

    else:

        st.warning(
            "Your BMI is in the obese range. "
            "Consider consulting a qualified healthcare "
            "professional before making major dietary changes."
        )

    # -----------------------------------------------
    # DISCLAIMER
    # -----------------------------------------------

    st.caption(
        "⚠️ This app provides general fitness and nutrition "
        "guidance and is not a substitute for advice from "
        "a registered dietitian or healthcare professional."
    )

else:

    st.info(
        "👈 Enter your details in the sidebar and click "
        "**Generate My Diet Plan** to begin."
    )
