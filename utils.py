from typing import Dict


def pretty_money(x: float) -> str:
    return f"₹{x:,.2f}" if x is not None else "-"


def summary_from_crew(result: Dict) -> str:
    s = []
    ea = result.get('expense_analysis', {})
    s.append(f"Total expenses: {ea.get('total_expenses')}")
    s.append(f"Estimated monthly savings: {ea.get('savings')}")
    return "\n".join(s)