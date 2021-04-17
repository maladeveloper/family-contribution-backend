from pprint import pprint

##Vars
f_end_name, f_end_amount, f_end_date = "NAME", "AMOUNT", "DATE"
amount, date = "amount", "dateAcquired"
total_inc = "totalIncome"

##Pending users Vars 
all_paid, users_paid_not_paid = "allPaid", "users"

##All paid users Vars
income, tax_due = "income", "taxDue"

def get_total_inc(summarised_inc):

    return {name:info[total_inc] for name, info in summarised_inc.items()}

def get_income_summary(income_arr):

    inc_summ = {inc_inf[f_end_name]:{ amount:inc_inf[f_end_amount], date:inc_inf[f_end_date]} for inc_inf in income_arr}

    inc_summ[total_inc] = sum([int(inc_inf[f_end_amount]) for inc_inf in income_arr])

    return inc_summ

def reverse_income_summary(summarised_inc):

    del summarised_inc[total_inc]

    un_summarised_inc = []

    pprint(summarised_inc)

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
Returns the not paid users in a format that is friendly to the frontend.
'''
def format_users_tax( paid_status, not_paid_users=None, users_income=None, users_tax=None ):

    if not paid_status:

        return { all_paid:paid_status, users_paid_not_paid:not_paid_users}
    
    ##Otherwise all users have paid and now zip user income and tax due together.
    users_dict = {user_name:{ income:users_income[user_name], tax_due:users_tax[user_name] } for user_name in users_income.keys()}

    return {all_paid:paid_status, users_paid_not_paid:users_dict}

