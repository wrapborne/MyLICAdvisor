import json
from typing import List, Dict, Any

# Load plans config on module import
with open("backend/configs/plans_config.json", "r") as f:
    PLANS_CONFIG = json.load(f)


def suggest_plans(user_input: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Suggests LIC plans based on user input and plan config.
    :param user_input: dict of validated user input data
    :return: list of matching plans with plan details
    """
    recommended_plans = []

    for plan in PLANS_CONFIG:
        # Eligibility: age
        user_age = user_input["age"]
        if not (plan["min_age"] <= user_age <= plan["max_age"]):
            continue

        # Eligibility: term - we skip here since user term not included yet, but add later as needed

        # Payout preference compatibility
        if not any(pref in plan["available_payout_options"]
                   for pref in user_input["maturity_payout_preference"]):
            continue

        # Payment mode compatibility
        if user_input["payment_mode"] not in plan["available_payment_modes"]:
            continue

        # Payment frequency compatibility
        if user_input["payment_frequency"] not in plan["available_payment_frequencies"]:
            continue

        # Dynamic premium budget check
        premium_budget = user_input["premium_budget"]
        if premium_budget < plan["min_premium"]:
            continue

        # Dynamic maturity goal check
        maturity_goal = user_input["maturity_goal_amount"]
        if maturity_goal < plan["min_maturity_goal"]:
            continue

        # If children_age given, later we'll add plan context logic here
        # For now, we include all eligible plans regardless of children_age

        # Passed all checks — add plan to recommendations
        recommended_plans.append(plan)

    return recommended_plans
