##Defined
from VARIABLES import TOTAL_TAX_PER_WEEK, WEEKS_PER_PAYMENT

##Tax Calculation Vars
DEGREE_POLY = 1
TOTAL_TAX =  TOTAL_TAX_PER_WEEK * WEEKS_PER_PAYMENT

##Income Submission and Payment Table Vars
f_end_name = "NAME" #Shared Var
f_end_amount, f_end_date = "AMOUNT", "DATE" #Income Submission Vars
f_end_income, f_end_tax, f_end_tax_perc = "INCOME", "TAX_DUE", "TAX_PERC" #Payment table Vars

##Income database Vars
amount, date = "amount", "dateAcquired"
total_inc = "totalIncome"

##Pending users Vars 
all_paid, users_paid_not_paid = "allPaid", "users"

##All paid users Vars
income, tax_due = "income", "taxDue"


def get_income_summary(income_arr):

    inc_summ = {inc_inf[f_end_name]:{ amount:inc_inf[f_end_amount], date:inc_inf[f_end_date]} for inc_inf in income_arr}

    inc_summ[total_inc] = sum([int(inc_inf[f_end_amount]) for inc_inf in income_arr])

    return inc_summ

def reverse_income_summary(summarised_inc):

    del summarised_inc[total_inc]

    un_summarised_inc = []

    for name, inf in summarised_inc.items():

        tmp_dict = dict()

        tmp_dict[f_end_name], tmp_dict[f_end_amount], tmp_dict[f_end_date] = name, inf[amount], inf[date]

        un_summarised_inc.append(tmp_dict)
    
    return un_summarised_inc


'''
Used to get the total income per user.
Input: All information about income submitted per data e.g {MAL001:{totalIncome:120, Tutoring:120}, ...}
Output: Summarised information about user's total income {MAL001:120...}
'''
def get_inc_per_user(paid_users_data):

    return {user_name: info[total_inc] for user_name, info in paid_users_data.items()}
        

'''
Applies tax on the user's income and returns the tax value.
Input:Income per user e.g { MAL001':750, 'SRI001':800, 'ANU001':370, 'MAI001':290}
Output: Tax per user e.g {'MAL001': 296, 'SRI001': 337, 'ANU001': 72, 'MAI001': 44}
'''
def apply_tax(user_dict):

    income_list = [i for i in user_dict.values()]

    try:
        
        div_amount = TOTAL_TAX / sum([income**(DEGREE_POLY + 1) for income in income_list])
    
    except ZeroDivisionError: #Triggered if all income is 0.

        return {user_name:0 for user_name in user_dict.keys()}

    tax_dict = dict()

    for user_name, user_income  in user_dict.items():

        tax_dict[user_name] = round(div_amount * user_income ** (DEGREE_POLY + 1))

    return tax_dict

def calculate_tax_perc(tax, income):

    tax_perc = 0 if (tax == 0) or (income==0) else round(100*(tax/income))

    return tax_perc
    

'''
Returns the not paid users in a format that is friendly to the frontend.
'''
def format_users_tax( paid_status, not_paid_users=None, all_users=None, users_income=None, users_tax=None ):

    if not paid_status:

        return { all_paid:paid_status, users_paid_not_paid:not_paid_users}
    
    ##Otherwise all users have paid and now zip user income and tax due together.
    user_info_arr = []

    for user_id in users_income.keys():

        temp_info_dict = { 
            f_end_name:     all_users[user_id],
            f_end_income:   users_income[user_id],
            f_end_tax:      users_tax[user_id], 
            f_end_tax_perc: calculate_tax_perc(users_tax[user_id], users_income[user_id])
        }

        user_info_arr.append(temp_info_dict)

    return {all_paid:paid_status, users_paid_not_paid:user_info_arr}
