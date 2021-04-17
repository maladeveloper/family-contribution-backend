##Defined
from VARIABLES import TOTAL_TAX_PER_WEEK, WEEKS_PER_PAYMENT

##Vars
DEGREE_POLY = 1
TOTAL_TAX =  TOTAL_TAX_PER_WEEK * WEEKS_PER_PAYMENT

##Income Submission Vars
f_end_name, f_end_amount, f_end_date = "NAME", "AMOUNT", "DATE"
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

    div_amount = TOTAL_TAX / sum([income**(DEGREE_POLY + 1) for income in income_list])

    tax_dict = dict()

    for user_name, user_income  in user_dict.items():

        tax_dict[user_name] = round(div_amount * user_income ** (DEGREE_POLY + 1))

    return tax_dict


'''
Returns the not paid users in a format that is friendly to the frontend.
'''
def format_users_tax( paid_status, not_paid_users=None, users_income=None, users_tax=None ):

    if not paid_status:

        return { all_paid:paid_status, users_paid_not_paid:not_paid_users}
    
    ##Otherwise all users have paid and now zip user income and tax due together.
    users_dict = {user_name:{ income:users_income[user_name], tax_due:users_tax[user_name] } for user_name in users_income.keys()}

    return {all_paid:paid_status, users_paid_not_paid:users_dict}
