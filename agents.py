from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from llm import call_gemini
from prompts import EXPENSE_ANALYZER_PROMPT, INVESTMENT_ADVISOR_PROMPT, GOAL_PLANNER_PROMPT


class ExpenseInput(BaseModel):
    income: float
    expenses: Dict[str, float]


class ExpenseAnalyzer:
    """Analyzes user expenses and suggests cuts. Uses a rule-based engine and optional LLM for richer suggestions."""

    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm

    def analyze(self, data: ExpenseInput) -> Dict[str, Any]:
        income = data.income
        expenses = data.expenses
        total_exp = sum(expenses.values())
        savings = max(0.0, income - total_exp)
        ratios = {k: v / income for k, v in expenses.items() if income > 0}

        high = [k for k, r in ratios.items() if r > 0.15]

        tips = []
        for k in high:
            tips.append(f"Consider reducing {k} — it consumes {ratios[k]*100:.1f}% of your income.")

        # ✅ always initialized, not inside loop
        suggestions = [
            "Review and cancel unused subscriptions.",
            "Cook more at home and reduce dining out frequency.",
            "Switch to a cheaper phone/internet plan if possible.",
        ]

        if self.use_llm:
            prompt = EXPENSE_ANALYZER_PROMPT + "\n\nUser Data:\n" + str(
                {"income": income, "expenses": expenses}
            )
            llm_out = call_gemini(prompt)
            if llm_out:
                return {
                    "total_expenses": total_exp,
                    "savings": savings,
                    "high_expenses": high,
                    "llm": llm_out,
                }

        return {
            "total_expenses": total_exp,
            "savings": savings,
            "high_expenses": high,
            "tips": tips + suggestions,
        }


class SavingsPlanner:
    """Suggest emergency fund and short-term safe instruments."""

    def __init__(self):
        pass

    def plan(self, income: float, expenses: float) -> Dict[str, Any]:
    # Simple rule: emergency fund = 3-6 months of expenses
        monthly_needed = expenses
        recommended = monthly_needed * 6
        monthly_saving_goal = max(0.0, (recommended - 0) / 12) # to build in a year by default
        return {
        'emergency_fund_target': recommended,
        'monthly_saving_goal': monthly_saving_goal,
        'short_term_options': ['liquid mutual funds', 'high-yield savings', 'short-term FD']
        }


class InvestmentAdvisor:
    """Recommends allocations based on risk appetite."""

    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm

    def recommend(self, age: int, risk: str, monthly_savings: float, horizon: str) -> Dict[str, Any]:
        risk = risk.lower()
        if risk == 'low':
            allocation = {'stocks': 0.2, 'mutual_funds': 0.3, 'gold': 0.1, 'bonds': 0.3, 'cash': 0.1}
        elif risk == 'medium':
            allocation = {'stocks': 0.4, 'mutual_funds': 0.3, 'gold': 0.1, 'bonds': 0.15, 'cash': 0.05}
        else: # high
            allocation = {'stocks': 0.6, 'mutual_funds': 0.25, 'gold': 0.05, 'bonds': 0.05, 'cash': 0.05}

        instruments = {
        'stocks': ['large-cap index', 'dividend stock sample'],
        'mutual_funds': ['index fund SIP', 'diversified equity fund'],
        'gold': ['digital gold', 'sovereign gold bonds'],
        'bonds': ['govt bonds', 'corporate bond funds'],
        'cash': ['savings', 'liquid funds']
        }

        if self.use_llm:
            prompt = INVESTMENT_ADVISOR_PROMPT + "\n\nUser data:\n" + str({'age': age, 'risk': risk, 'monthly_savings': monthly_savings, 'horizon': horizon})
            llm_out = call_gemini(prompt)
            if llm_out:
                return {'allocation': allocation, 'llm': llm_out}

        return {'allocation': allocation, 'monthly_savings': monthly_savings, 'instruments': instruments}


class GoalPlanner:
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm

    def plan_goals(self, goals: List[Dict[str, Any]], monthly_surplus: float) -> Dict[str, Any]:
    # goals: [{'name': 'Car', 'amount': 500000, 'years': 3}, ...]
    # naive prioritized plan: sort by years ascending
        sorted_goals = sorted(goals, key=lambda g: g['years'])
        plan = []
        for g in sorted_goals:
            months = g['years'] * 12
            monthly = g['amount'] / months if months > 0 else g['amount']
            plan.append({'name': g['name'], 'monthly_required': monthly, 'timeline_months': months})

        if self.use_llm:
            prompt = GOAL_PLANNER_PROMPT + "\n\nGoals:\n" + str(goals) + "\nMonthly surplus:" + str(monthly_surplus)
            llm_out = call_gemini(prompt)
            if llm_out:
                return {'plan': plan, 'llm': llm_out}

        return {'plan': plan, 'monthly_surplus': monthly_surplus}


# Simple Crew orchestrator
class CrewFinanceCoach:
    def __init__(self, use_llm=False):
        self.exp_analyzer = ExpenseAnalyzer(use_llm=use_llm)
        self.savings = SavingsPlanner()
        self.invest = InvestmentAdvisor(use_llm=use_llm)
        self.goals = GoalPlanner(use_llm=use_llm)

    def run_all(self, income: float, expenses: Dict[str, float], age: int = 30, risk: str = 'medium', goals: Optional[List[Dict]] = None):
        exp_input = ExpenseInput(income=income, expenses=expenses)
        e = self.exp_analyzer.analyze(exp_input)
        total_exp = e.get('total_expenses', sum(expenses.values()))
        savings_plan = self.savings.plan(income, total_exp)
        surplus = max(0.0, income - total_exp)
        invest_rec = self.invest.recommend(age, risk, surplus, 'long')
        goals = goals or []
        goals_plan = self.goals.plan_goals(goals, surplus)

        return {
            'expense_analysis': e,
            'savings_plan': savings_plan,
            'investment_recommendation': invest_rec,
            'goals_plan': goals_plan,
        }