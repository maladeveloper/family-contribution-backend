from pprint import pprint

##Vars
f_end_name, f_end_amount, f_end_date = "NAME", "AMOUNT", "DATE"
amount, date = "amount", "dateAcquired"
total_inc = "totalIncome"



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

        


