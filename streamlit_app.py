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
    "Standard (8-hour day)": {"hours_per_day": 8, "hours_per_week": 40},
    "12-hour shift": {"hours_per_day": 12, "hours_per_week": 36},
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
    return balance * hours_per_day if balance_unit == "Days" else balance


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
    st.write("Plan your PTO with clear daily, hourly, and weekly projections.")

    st.markdown("---")

    with st.container():
        st.subheader("Enter your PTO details")
        input_col1, input_col2 = st.columns([2, 1])

        with input_col1:
            balance_unit = st.radio("Balance tracked in", ["Hours", "Days"], index=0)
            current_balance = st.number_input(
                f"Current PTO balance ({balance_unit})",
                min_value=0.0,
                value=40.0,
                step=1.0,
                format="%.2f",
            )

            shift_label = st.selectbox("Shift schedule", list(SHIFT_OPTIONS.keys()), index=0)
            shift_rules = SHIFT_OPTIONS[shift_label]
            hours_per_day = shift_rules["hours_per_day"]
            hours_per_week = shift_rules["hours_per_week"]

            accrual_rate = st.number_input(
                "Accrual per pay period (hours)",
                min_value=0.0,
                value=8.0,
                step=0.5,
                format="%.2f",
            )

            pay_period = st.selectbox("Pay period frequency", list(PERIOD_OPTIONS.keys()), index=0)
            pay_period_days = PERIOD_OPTIONS[pay_period]

            year_end_choice = st.selectbox("PTO year-end", ["Calendar year", "Custom date"], index=0)
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

        with input_col2:
            st.markdown("#### Quick notes")
            st.write(
                "- **8-hour shift** means a standard 40-hour PTO week.\n"
                "- **12-hour shift** means a 36-hour PTO week.\n"
                "- Remaining weeks are calculated from projected hours divided by weekly hours."
            )
            st.write("### Year-end settings")
            st.write(
                "Choose a PTO cutoff date for your employer year. If you select a custom date, "
                "it will use the next matching date after today."
            )

    st.markdown("---")

    today = date.today()
    end_of_year = get_end_of_year_date(today, year_end_choice, custom_end_date)
    remaining_periods = periods_remaining(today, end_of_year, pay_period_days)
    current_hours = convert_balance_to_hours(current_balance, balance_unit, hours_per_day)
    projected_hours = round(current_hours + accrual_rate * remaining_periods, 2)
    projected_days = convert_hours_to_days(projected_hours, hours_per_day)
    current_weeks = round(current_hours / hours_per_week, 2)
    projected_weeks = round(projected_hours / hours_per_week, 2)
    planned_use_hours = convert_balance_to_hours(planned_use_value, planned_use_unit, hours_per_day) if plan_pto else 0.0
    used_weeks = round(planned_use_hours / hours_per_week, 2) if plan_pto else 0.0
    after_use_hours = round(max(0.0, projected_hours - planned_use_hours), 2)
    after_use_days = convert_hours_to_days(after_use_hours, hours_per_day)
    after_use_weeks = round(after_use_hours / hours_per_week, 2)

    st.subheader("PTO results")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Current balance", f"{current_hours:.2f} hrs", f"{current_weeks:.2f} weeks")
    metric_col2.metric("Projected remaining", f"{projected_hours:.2f} hrs", f"{projected_days:.2f} days")
    metric_col3.metric("Projected weeks", f"{projected_weeks:.2f} weeks", f"{hours_per_week} hrs/week")
    metric_col4.metric("Remaining periods", remaining_periods)

    st.markdown("---")

    if plan_pto:
        use_col1, use_col2, use_col3 = st.columns(3)
        use_col1.metric("Planned PTO use", f"{planned_use_hours:.2f} hrs", f"{used_weeks:.2f} weeks")
        use_col2.metric("Balance after use", f"{after_use_hours:.2f} hrs", f"{after_use_days:.2f} days")
        use_col3.metric("Weeks left after use", f"{after_use_weeks:.2f} weeks")
        if planned_use_hours > projected_hours:
            st.error(
                "Your planned PTO use exceeds projected remaining hours. "
                "Reduce planned PTO or increase accrual rate."
            )

    tabs = st.tabs(["Summary", "Projection", "Details"])
    with tabs[0]:
        st.subheader("Current PTO summary")
        st.write(
        f"**Shift type:** {shift_label}  \n"
        f"**Weekly PTO conversion:** {hours_per_week} hours = 1 week  \n"
        f"**Year-end:** {end_of_year} ({(end_of_year - today).days} days from today)"
    )
        st.write(
            f"- Start balance: {current_balance:.2f} {balance_unit} (equivalent to {current_hours:.2f} hours)\n"
            f"- Future accrual: {accrual_rate:.2f} hours x {remaining_periods} periods = {accrual_rate * remaining_periods:.2f} hours\n"
            f"- Projected remaining hours: {projected_hours:.2f} hrs"
        )
        if plan_pto:
            st.write(
                f"- Planned use: {planned_use_value:.2f} {planned_use_unit} ({planned_use_hours:.2f} hrs)\n"
                f"- Balance after planned use: {after_use_hours:.2f} hrs ({after_use_days:.2f} days, {after_use_weeks:.2f} weeks)"
            )

    with tabs[1]:
        st.subheader("Future accrual projection")
        if remaining_periods > 0:
            projection_df = build_projection_dataframe(current_hours, accrual_rate, remaining_periods)
            projection_df["Projected PTO days"] = projection_df["Projected PTO hours"].apply(
                lambda value: round(value / hours_per_day, 2)
            )
            projection_df["Projected PTO weeks"] = projection_df["Projected PTO hours"].apply(
                lambda value: round(value / hours_per_week, 2)
            )
            st.line_chart(projection_df.set_index("Pay period #")["Projected PTO hours"])
            st.dataframe(projection_df, use_container_width=True)
        else:
            st.warning("No pay periods remain before the selected year-end.")

    with tabs[2]:
        st.subheader("Calculation details")
        st.write(
            "This calculator converts your current balance into hours, "
            "adds projected accruals to year-end, then converts totals back into days and weeks."
        )
        st.markdown(
            f"- Balance unit: **{balance_unit}**  \n"
            f"- Hours per day: **{hours_per_day}**  \n"
            f"- Hours per week: **{hours_per_week}**  \n"
            f"- Selected pay period: **{pay_period}**  \n"
            f"- Year-end date: **{end_of_year}**"
        )


if __name__ == "__main__":
    main()
