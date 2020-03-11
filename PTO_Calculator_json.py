from   datetime import date
import datetime
from   datetime import datetime
import time
import pandas as pd
import numpy as np
import json

with open('test.json') as test_json:
    test_json = json.load(test_json)


def hours_current_balance(nurse_or_not):
    

    if test_json['nurse_or_not'] == 'yes':
        nurse_hours_num = accruing_pto_hours()
        #nurse_hours_pto = input('Are you going to use PTO?')
        
        if test_json['use_pto'] == 'yes':
            #num_of_hours = input('How many hours?')
            num_of_hours = test_json['num_pto_hours']
            num_of_hours_num = float(num_of_hours)
            hours_remaining = nurse_hours_num - num_of_hours_num
            days_remaining = float(hours_remaining / 12)
            days_remaining = float(round(days_remaining, 2))
            print('You have ' , hours_remaining , 'hours', ', that is ' , days_remaining ,' days')

        if test_json['use_pto'] == 'no':
            no_pto_days = round(float(nurse_hours_num) / 12,2)
            print('You have ' , nurse_hours_num , 'hours' ', that is' , no_pto_days , ' days')

    if nurse_or_not == 'no':
        hours_balance_num = accruing_pto_hours()
        norm_shift_pto = input('Are you going to use PTO?')

        if norm_shift_pto == 'yes':
            num_of_hours = input('How many hours of PTO?')
            pto_hours = float(num_of_hours)
            hours_remaining = hours_balance_num - pto_hours
            days_remaining = hours_remaining / 8
            days_remaining = float(round(days_remaining,2))
            print('You have ' , hours_remaining , 'hours' , ', that is ', days_remaining, ' days')

        if norm_shift_pto == 'no':
            no_pto_days = round(float(hours_balance) / 8,2)
            print('You have ' , hours_balance , 'hours' , ', that is ', no_pto_days, ' days')

    return nurse_hours_num;

def hours_total_pto(nurse_or_not):
    if nurse_or_not == 'yes':
        hours_balance = input('How many hours do you have?')
        hours_balance_num = float(hours_balance)
        norm_shift_pto = input('Are you going to use PTO?')

        if norm_shift_pto == 'yes':
            num_of_hours = input('How many hours of PTO?')
            pto_hours = float(num_of_hours)
            hours_remaining = hours_balance_num - pto_hours
            days_remaining = hours_remaining / 12
            days_remaining = float(round(days_remaining,2))
            print('You have ' , hours_remaining , 'hours' , ', that is ', days_remaining, ' days')

        if norm_shift_pto == 'no':
            no_pto_days = round(float(hours_balance) / 12,2)
            print('You have ' , hours_balance , 'hours' , ', that is ', no_pto_days, ' days')

    if nurse_or_not == 'no':
        hours_balance = input('How many hours do you have?')
        hours_balance_num = float(hours_balance)
        norm_shift_pto = input('Are you going to use PTO?')

        if norm_shift_pto == 'yes':
            num_of_hours = input('How many hours of PTO?')
            pto_hours = float(num_of_hours)
            hours_remaining = hours_balance_num - pto_hours
            days_remaining = hours_remaining / 8
            days_remaining = float(round(days_remaining,2))
            print('You have ' , hours_remaining , 'hours' , ', that is ', days_remaining, ' days')

        if norm_shift_pto == 'no':
            no_pto_days = round(float(hours_balance) / 8,2)
            print('You have ' , hours_balance , 'hours' , ', that is ', no_pto_days, ' days')
        

def days_current_balance(nurse_or_not):
    if nurse_or_not == 'yes':
        nurse_days_num = accruing_pto_days()
        nurse_days_pto = input('Are you going to use PTO?')
        
        if nurse_days_pto == 'yes':
            num_of_days = input('How many days?')
            num_of_days_num = float(num_of_days)
            days_remaining = nurse_days_num - num_of_days_num
            days_remaining = float(days_remaining)
            hours_remaining = float(days_remaining * 12)
            hours_remaining = float(round(hours_remaining, 2))
            print('You have ' , days_remaining , 'days', ', that is ' , hours_remaining ,' hours')

        if nurse_days_pto == 'no':
            no_pto_hours = 0
            no_pto_hours = float(nurse_days) * 12
            print('You have ' , nurse_days_num, ',that is' , no_pto_hours ,' hours')

    if nurse_or_not == 'no':
        days_balance_num = accruing_pto_days()
        norm_shift_pto = input('Are you going to use any PTO?')

        if norm_shift_pto == 'yes':
            num_of_days = input('How many days?')
            pto_days = float(num_of_days)
            days_remaining = days_balance_num - pto_days
            hours_remaining = days_remaining * 8
            hours_remaining = float(round(hours_remaining,2))
            print('You have ' , days_remaining , 'days' , ', that is ', hours_remaining, ' hours')

        if norm_shift_pto == 'no':
            no_pto_hours = float(days_balance) * 8
            print('You have ' , days_balance , 'days' , ', that is ', no_pto_hours, ' hours')
       

def days_total_pto(nurse_or_not):
    if nurse_or_not == 'yes':
        nurse_days = input('How many days do you have?')
        nurse_days_num = float(nurse_days)
        
        nurse_days_pto = input('Are you going to use PTO?')
        
        if nurse_days_pto == 'yes':
            num_of_days = input('How many days?')
            num_of_days_num = float(num_of_days)
            days_remaining = nurse_days_num - num_of_days_num
            days_remaining = float(days_remaining)
            hours_remaining = float(days_remaining * 12)
            hours_remaining = float(round(hours_remaining, 2))
            print('You have ' , days_remaining , 'days', ', that is ' , hours_remaining ,' hours')

        if nurse_days_pto == 'no':
            no_pto_hours = 0
            no_pto_hours = float(nurse_days) * 12
            print('You have ' , nurse_days_num, ',that is' , no_pto_hours ,' hours')

    if nurse_or_not == 'no':
        days_balance = input('How many days do you have?')
        days_balance_num = float(days_balance)
        norm_shift_pto = input('Are you going to use any PTO?')

        if norm_shift_pto == 'yes':
            num_of_days = input('How many days?')
            pto_days = float(num_of_days)
            days_remaining = days_balance_num - pto_days
            hours_remaining = days_remaining * 8
            hours_remaining = float(round(hours_remaining,2))
            print('You have ' , days_remaining , 'days' , ', that is ', hours_remaining, ' hours')

        if norm_shift_pto == 'no':
            no_pto_hours = float(days_balance) * 8
            print('You have ' , days_balance , 'days' , ', that is ', no_pto_hours, ' hours')
        
def accruing_pto_hours():
    current_balance = test_json['current_balance']
##    current_balance = input('How many hours do you currently have?')
    current_balance = float(current_balance)   

##    hours_per_check = input('How many hours do you accrue per check?')
    hours_per_check = test_json['accrual_rate']
    hours_per_check = float(hours_per_check)
    
    end_of_year = date(2020, 12, 31)
    current_date = date.today()
    date_diff = (end_of_year - current_date)
    date_diff = date_diff.days
    weeks_left = float(round(date_diff / 7))
    checks_left = (weeks_left / 2)
    remaining_pto_accrual = (checks_left * hours_per_check)
    total_remaining_pto = remaining_pto_accrual + current_balance
    total_remaining_pto = round(total_remaining_pto,2)
##    print('Remaining pto hours for the year ' , total_remaining_pto)

    return total_remaining_pto

def accruing_pto_days():
    current_balance = input('How many days do you currently have?')
    current_balance = float(current_balance)
    current_balance_to_hours = (current_balance * 8)

    hours_per_check = input('How many hours do you accrue per check?')
    hours_per_check = float(hours_per_check)
    
    end_of_year = date(2020, 12, 31)
    current_date = date.today()
    date_diff = (end_of_year - current_date)
    date_diff = date_diff.days
    weeks_left = float(round(date_diff / 7))
    checks_left = (weeks_left / 2)
    remaining_pto_accrual = (checks_left * hours_per_check)
    remaining_pto_to_days = (remaining_pto_accrual / 8)
    total_remaining_pto = remaining_pto_to_days + current_balance
    total_remaining_pto = round(total_remaining_pto,2)
    print('Remaining pto days for the year ' , total_remaining_pto)
    
    return total_remaining_pto;

    
##MAIN METHOD##
def main():


    
   # hours_or_days_list = ['hours', 'days']
   # hours_or_days_list = [element.lower() for element in hours_or_days_list]
   # hours_or_days = input('Do you have your PTO in hours or days?')

##    while hours_or_days not in hours_or_days_list:
##        print('---Enter hours or days---')
##        hours_or_days = input('Do you have your PTO in hours or days?')    
    hours_or_days = test_json['hours_or_days']
    
##    know_total_or_balance_list = ['Total PTO', 'Current Balance']
##    know_total_or_balance_list = [element.lower() for element in know_total_or_balance_list]
##    know_total_or_balance = input('Do you know your total PTO for the year, or just current balance?')
##
    know_total_or_balance = test_json['current_or_total']
    
##    while know_total_or_balance not in know_total_or_balance_list:
##        print('---Enter Total PTO or Current Balance---')
##        know_total_or_balance = input('Do you know your total PTO for the year, or just current balance?')

    if know_total_or_balance == 'total pto': #total pto
        if hours_or_days == hours_or_days_list[0]: #hours
            nurse_or_not = input('Do you work 12 hour shifts?')
            hours_total_pto(nurse_or_not)
        
        if hours_or_days == hours_or_days_list[1]: #days
            nurse_or_not = input('Do you work 12 hour shifts?')
            days_total_pto(nurse_or_not)
            
                
    if know_total_or_balance == 'current balance': #current balance
        if hours_or_days == 'hours':  #hours
##            nurse_or_not = test_json['nurse_or_not']
##            print(nurse_or_not)
            hours_current_balance(test_json['nurse_or_not'])
                
        if hours_or_days == 'days': #days
            nurse_or_not = test_json['nurse_or_not']
            days_current_balance(nurse_or_not)
                
##    print()
##    input('Press X to Exit or Hit Enter for Another Simulation')
##    print()
##    print()
##    print('Another PTO Simulation Will Begin Now..')
##    print()
    
    return ;

#Calling main method
##while True

main()
    
        
                              






       
                
                
        
