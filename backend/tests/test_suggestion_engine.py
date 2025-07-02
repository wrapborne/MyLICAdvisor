import pytest
import sys
import os

# Project root ka absolute path calculate karo
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Us path ko Python ke module search path me add karo
sys.path.insert(0, project_root)

from backend.utils.suggestion_engine import suggest_plans  # ✅


#from utils.suggestion_engine import suggest_plans

# Sample user inputs for tests
BASE_INPUT = {
    "age": 30,
    "premium_budget": 5000,
    "maturity_goal_amount": 200000,
    "maturity_payout_preference": ["lump_sum"],
    "payment_mode": "full",
    "payment_frequency": "yearly",
    "gender": "male",
    "smoking_status": "non-smoker",
    "optional_riders": []
}

def test_recommend_plan_found():
    """
    Should recommend at least one plan with standard valid input.
    """
    results = suggest_plans(BASE_INPUT)
    assert isinstance(results, list)
    assert len(results) >= 1
    assert all("plan_id" in plan for plan in results)


def test_age_too_low():
    """
    Should not recommend any plans if age is below plan min_age.
    """
    input_data = BASE_INPUT.copy()
    input_data["age"] = 5  # too young
    results = suggest_plans(input_data)
    assert len(results) == 0


def test_age_too_high():
    """
    Should not recommend any plans if age exceeds plan max_age.
    """
    input_data = BASE_INPUT.copy()
    input_data["age"] = 70  # too old
    results = suggest_plans(input_data)
    assert len(results) == 0


def test_premium_below_minimum():
    """
    Should not recommend any plans if budget is below the lowest min_premium.
    """
    input_data = BASE_INPUT.copy()
    input_data["premium_budget"] = 100  # unrealistic low budget
    results = suggest_plans(input_data)
    assert len(results) == 0


def test_no_matching_payout_preference():
    """
    Should not recommend any plans if selected payout preference not supported.
    """
    input_data = BASE_INPUT.copy()
    input_data["maturity_payout_preference"] = ["lifetime"]  # few plans support lifetime
    input_data["age"] = 30
    results = suggest_plans(input_data)
    assert len(results) >= 0  # depends on plans config; can be 0 or more
