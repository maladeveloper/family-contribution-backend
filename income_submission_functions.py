from pprint import pprint


def get_income_summary(income_arr):

    inc_summ = {inc_inf["NAME"]:{ "amount":inc_inf["AMOUNT"], "dateAcquired":inc_inf["DATE"]} for inc_inf in income_arr}

    inc_summ["totalIncome"] = sum([int(inc_inf["AMOUNT"]) for inc_inf in income_arr])

    return inc_summ
