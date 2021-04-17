from VARIABLES import TOTAL_TAX_PER_WEEK, WEEKS_PER_PAYMENT
##Vars
DEGREE_POLY = 1
TOTAL_TAX =  TOTAL_TAX_PER_WEEK * WEEKS_PER_PAYMENT
##

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


