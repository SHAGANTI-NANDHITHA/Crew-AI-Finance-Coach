import streamlit as st
from crew import CrewFinanceCoach
from utils import pretty_money

# Page config
st.set_page_config(
    page_title="CrewAI Finance Coach",
    page_icon="💰",
    layout="wide",
)

# Sidebar
st.sidebar.title("💼 CrewAI — Finance Coach")
st.sidebar.markdown("Navigate through sections:")
page = st.sidebar.radio("", ["🏠 Home", "📝 Input Form", "📊 Results"])

st.title("💰 CrewAI — Finance Coach")
st.caption("A multi-agent finance coach for **expense analysis, savings plan, investment recommendation, and goal planning**.")

# Input form page
if page == "📝 Input Form":
    with st.form("input_form"):
        st.subheader("📥 Enter Your Details")

        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly income (₹)", min_value=0.0, value=50000.0, step=1000.0)
            age = st.number_input("Your age", min_value=18, max_value=100, value=28)
            risk = st.selectbox("Risk appetite", ["Low", "Medium", "High"])
        with col2:
            st.markdown("**Major Monthly Expenses**")
            rent = st.number_input("🏠 Rent / EMI", value=15000.0)
            food = st.number_input("🍲 Food / Groceries", value=6000.0)
            transport = st.number_input("🚗 Transport", value=2000.0)
            subscriptions = st.number_input("📺 Subscriptions", value=800.0)
            shopping = st.number_input("🛍️ Shopping / Lifestyle", value=3000.0)
            others = st.number_input("💡 Other expenses", value=2000.0)

        st.markdown("### 🎯 Goals (Optional)")
        goal1_name = st.text_input("Goal 1 name", "Car")
        goal1_amount = st.number_input("Goal 1 amount (₹)", value=500000.0)
        goal1_years = st.number_input("Goal 1 timeline (years)", min_value=0, value=3)

        submitted = st.form_submit_button("🚀 Get Advice")

    if submitted:
        expenses = {
            "rent": rent,
            "food": food,
            "transport": transport,
            "subscriptions": subscriptions,
            "shopping": shopping,
            "others": others,
        }

        coach = CrewFinanceCoach(use_llm=False)  # change to True if LLM is configured
        result = coach.run_all(
            income,
            expenses,
            age=int(age),
            risk=risk.lower(),
            goals=[{"name": goal1_name, "amount": goal1_amount, "years": goal1_years}],
        )

        st.session_state["result"] = result
        st.success("✅ Analysis complete! Go to the **📊 Results** tab to view insights.")

# Results page
elif page == "📊 Results":
    if "result" not in st.session_state:
        st.warning("⚠️ Please first submit your details in the **📝 Input Form** tab.")
    else:
        result = st.session_state["result"]

        # Expense Analysis
        st.header("💸 Expense Analysis")
        ea = result["expense_analysis"]

        c1, c2 = st.columns(2)
        c1.metric("Total Expenses", pretty_money(ea.get("total_expenses")))
        c2.metric("Estimated Savings", pretty_money(ea.get("savings")))

        with st.expander("🔎 High Expense Categories"):
            st.write(ea.get("high_expenses"))
        with st.expander("💡 Tips"):
            st.write(ea.get("tips"))

        st.divider()

        # Savings Plan
        st.header("💡 Savings Plan")
        sp = result["savings_plan"]

        st.metric("Emergency Fund Target", pretty_money(sp.get("emergency_fund_target")))
        st.metric("Monthly Saving Goal", pretty_money(sp.get("monthly_saving_goal")))

        st.divider()

        # Investment Recommendation
        st.header("📈 Investment Recommendation")
        inv = result["investment_recommendation"]

        with st.expander("📊 Allocation"):
            st.write(inv.get("allocation"))
        with st.expander("💹 Suggested Instruments"):
            st.write(inv.get("instruments"))

        st.divider()

        # Goals Plan
        st.header("🎯 Goals Plan")
        gp = result["goals_plan"]
        st.write(gp.get("plan"))

# Home page
elif page == "🏠 Home":
    st.info(
        """
        👋 Welcome to **CrewAI Finance Coach**!  
        Use the sidebar to enter your income, expenses, and goals.  
        Get **personalized advice** on saving, investing, and achieving your goals.
        """
    )
