import pandas as pd
import streamlit as st
import os
import datetime

os.getcwd()

st.write("PTO App")

def main():    
    days_or_hours = st.selectbox("Do you have your PTO in days or hours?",
                                ("Hours", "Days"))

    pto_box = st.number_input("How many " + days_or_hours.lower() + " do you have?", key='pto_input_box')

    twelve_hour_shift_option = st.selectbox('Do you work 12 hour shifts?', ['No', 'Yes'])


    accrual_rate = st.number_input("How many hours do you accrue per check?", key='pto_accrual_rate')
    current_date = datetime.datetime.now()
    end_of_year = datetime.datetime(current_date.year, 12, 31)
    remaining_biweekly_periods = (end_of_year - current_date).days // 14

    if days_or_hours == 'Days' and twelve_hour_shift_option == 'No':
        remaining_pto_days = round(((accrual_rate * remaining_biweekly_periods) / 8) + (pto_box) ,2)
        remaining_pto_hours = round((accrual_rate * remaining_biweekly_periods) + (pto_box * 8) ,2)
        remaining_pto_string = st.write("You have " + str(remaining_pto_hours) + ' hours and ' + str(remaining_pto_days) + " days remaining for the year.")

    if days_or_hours == 'Days' and twelve_hour_shift_option == 'Yes':
        remaining_pto_days = round(((accrual_rate * remaining_biweekly_periods) / 12) + (pto_box) ,2)
        remaining_pto_hours = round((accrual_rate * remaining_biweekly_periods) + (pto_box * 12) ,2)
        remaining_pto_string = st.write("You have " + str(remaining_pto_hours) + ' hours and ' + str(remaining_pto_days) + " days remaining for the year.")

    if days_or_hours == 'Hours' and twelve_hour_shift_option == 'No':
        remaining_pto_days = round(((accrual_rate * remaining_biweekly_periods) / 8) + (pto_box / 8) ,2)
        remaining_pto_hours = round((accrual_rate * remaining_biweekly_periods) + (pto_box),2)
        remaining_pto_string = st.write("You have " + str(remaining_pto_hours) + ' hours and ' + str(remaining_pto_days) + " days remaining for the year.")

    if days_or_hours == 'Hours' and twelve_hour_shift_option == 'Yes':
        remaining_pto_days = round(((accrual_rate * remaining_biweekly_periods) / 12) + (pto_box / 12) ,2)
        remaining_pto_hours = round((accrual_rate * remaining_biweekly_periods) + (pto_box) ,2)
        remaining_pto_string = st.write("You have " + str(remaining_pto_hours) + ' hours and ' + str(remaining_pto_days) + " days remaining for the year.")


    with st.expander("Will you use PTO?"):
        days_to_use = st.number_input('How many days will you use?', key='pto_usage')

        if twelve_hour_shift_option == 'No':
            days_remaining = round(remaining_pto_days - days_to_use, 2)
            hours_remaining = round((remaining_pto_hours) - (days_to_use * 8) ,2 )

            st.write("You have " + str(hours_remaining) + " hours and " + str(days_remaining) + " days remaining after PTO")

        else:        
        # if days_or_hours == 'Days' and twelve_hour_shift_option == 'Yes':
            days_remaining = round(remaining_pto_days - days_to_use, 2)
            hours_remaining = round((remaining_pto_hours) - (days_to_use * 12) ,2 )
            
            st.write("You have " + str(hours_remaining) + " hours and " + str(days_remaining) + " days remaining after PTO")

        

if __name__ == '__main__':
    main()