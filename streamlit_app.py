import datetime
from datetime import date

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="PTO Calculator",
    page_icon="🗓️",
    layout="wide",
)

SHIFT_OPTIONS = {
    "Standard (8-hour day)": 8,
    "12-hour shift": 12,
}

PERIOD_OPTIONS = {
    "Biweekly (14 days)": 14,
    "Weekly (7 days)": 7,
    "Monthly (30 days)": 30,
}


def get_end_of_year_date(today: date, year_end_choice: str, custom_date: date | None) -> date:
    if year_end_choice == "Custom date" and custom_date is not None:
        return custom_date if custom_date > today else custom_date.replace(year=today.year + 1)

    end_of_year = date(today.year, 12, 31)
    return end_of_year if today <= end_of_year else date(today.year + 1, 12, 31)


def convert_balance_to_hours(balance: float, balance_unit: str, hours_per_day: int) -> float:
    if balance_unit == "Days":
        return balance * hours_per_day
    return balance


def convert_hours_to_days(hours: float, hours_per_day: int) -> float:
    return round(hours / hours_per_day, 2)


def periods_remaining(today: date, end_date: date, period_days: int) -> int:
    days_left = max(0, (end_date - today).days)
    return days_left // period_days


def build_projection_dataframe(start_hours: float, accrual_hours: float, periods: int) -> pd.DataFrame:
    projected_hours = [round(start_hours + accrual_hours * i, 2) for i in range(periods + 1)]
    return pd.DataFrame(
        {
            "Pay period #": list(range(periods + 1)),
            "Projected PTO hours": projected_hours,
        }
    )


def main() -> None:
    st.title("PTO Calculator")
    st.write(
        "Estimate your remaining paid time off in both hours and days. "
        "Use the sidebar to enter your balance, accrual rate, and planned PTO usage."
    )

    with st.sidebar:
        st.header("Inputs")
        st.write("Choose how you track your PTO and when your year ends.")

        balance_unit = st.radio("Balance tracked in", ["Hours", "Days"], index=0)
        current_balance = st.number_input(
            f"Current PTO balance ({balance_unit})",
            min_value=0.0,
            value=40.0,
            step=1.0,
            format="%.2f",
        )

        shift_label = st.radio("Shift schedule", list(SHIFT_OPTIONS.keys()), index=0)
        hours_per_day = SHIFT_OPTIONS[shift_label]

        accrual_rate = st.number_input(
            "Accrual per pay period (hours)",
            min_value=0.0,
            value=8.0,
            step=0.5,
            format="%.2f",
        )

        pay_period = st.selectbox("Pay period frequency", list(PERIOD_OPTIONS.keys()), index=0)
        pay_period_days = PERIOD_OPTIONS[pay_period]

        year_end_choice = st.selectbox("PTO year-end", ["Calendar year", "Custom date"])
        custom_end_date = None
        if year_end_choice == "Custom date":
            custom_end_date = st.date_input(
                "Select PTO year-end date",
                date(date.today().year, 12, 31),
            )

        plan_pto = st.checkbox("I plan to use PTO before year-end")
        planned_use_unit = "Hours"
        planned_use_value = 0.0
        if plan_pto:
            planned_use_unit = st.radio("Planned PTO unit", ["Hours", "Days"], index=0)
            planned_use_value = st.number_input(
                f"Projected PTO use ({planned_use_unit})",
                min_value=0.0,
                value=0.0,
                step=1.0,
                format="%.2f",
            )

        st.divider()
        st.write("Need help?")
        with st.expander("How this calculator works"):
            st.write(
                "The app converts your current PTO balance into hours, applies future accruals "
                "through the selected year-end, and then converts the result back into days. "
                "If you plan to use PTO before year-end, it will also estimate your balance after that usage."
            )

    today = date.today()
    end_of_year = get_end_of_year_date(today, year_end_choice, custom_end_date)
    remaining_periods = periods_remaining(today, end_of_year, pay_period_days)
    current_hours = convert_balance_to_hours(current_balance, balance_unit, hours_per_day)
    projected_hours = round(current_hours + accrual_rate * remaining_periods, 2)
    projected_days = convert_hours_to_days(projected_hours, hours_per_day)
    planned_use_hours = convert_balance_to_hours(planned_use_value, planned_use_unit, hours_per_day) if plan_pto else 0.0
    after_use_hours = round(max(0.0, projected_hours - planned_use_hours), 2)
    after_use_days = convert_hours_to_days(after_use_hours, hours_per_day)

    summary_col1, summary_col2, summary_col3 = st.columns(3)
    summary_col1.metric("Current balance", f"{current_balance:.2f} {balance_unit}")
    summary_col2.metric("Projected remaining", f"{projected_hours:.2f} hrs", f"{projected_days:.2f} days")
    summary_col3.metric("Remaining periods", remaining_periods)

    st.info(
        f"Year-end date: {end_of_year} ({(end_of_year - today).days} days from today). "
        f"Using {hours_per_day}-hour days."
    )

    if plan_pto:
        pto_col1, pto_col2 = st.columns(2)
        pto_col1.metric("Planned PTO use", f"{planned_use_value:.2f} {planned_use_unit}")
        pto_col2.metric("Balance after use", f"{after_use_hours:.2f} hrs", f"{after_use_days:.2f} days")
        if planned_use_hours > projected_hours:
            st.error(
                "Your planned PTO use is greater than the projected remaining balance. "
                "Adjust your planned PTO or accrual rate to avoid a negative balance."
            )

    tabs = st.tabs(["Results", "Projection"])
    with tabs[0]:
        st.subheader("Projected PTO summary")
        st.write(
            "This summary estimates how much PTO you will have remaining at your selected year-end, "
            "including projected accruals from each future pay period."
        )
        st.markdown(
            f"- **Current PTO balance:** {current_balance:.2f} {balance_unit}  
             - **Accrual rate:** {accrual_rate:.2f} hours per pay period  
             - **Pay period length:** {pay_period}"
        )
        if plan_pto:
            st.markdown(f"- **Planned PTO use:** {planned_use_value:.2f} {planned_use_unit}")

    with tabs[1]:
        st.subheader("Future accrual projection")
        if remaining_periods > 0:
            projection_df = build_projection_dataframe(current_hours, accrual_rate, remaining_periods)
            projection_df["Projected PTO days"] = projection_df["Projected PTO hours"].apply(
                lambda value: round(value / hours_per_day, 2)
            )
            st.line_chart(projection_df.set_index("Pay period #")[["Projected PTO hours"]])
            st.dataframe(projection_df, use_container_width=True)
        else:
            st.warning("No future pay periods remain before the selected year-end.")


if __name__ == "__main__":
    main()
