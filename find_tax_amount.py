
import numpy as np 

##Vars
TAX_DUE, TAX_PERC = 'taxDue', 'taxPerc'
##

test_dict = {
    'MAL001':750, 
    'SRI001':800,
    'ANU001':370,
    'MAI001':290
}



def apply_tax(user_dict,TOTAL_TAX_PER_WEEK):

    DEGREE_POLY = 1
    
    income_list = np.array([i for i in user_dict.values()])

    
    A = TOTAL_TAX_PER_WEEK / np.sum(income_list**(DEGREE_POLY + 1))

    tax_dict = { name:dict() for name in user_dict.keys()}

    for k,v  in user_dict.items():
        tax_dict[k][TAX_DUE] = round(A * v**(DEGREE_POLY + 1))

        #Establish the tax percentage as 0 
        tax_dict[k][TAX_PERC] = 0 

        #Ensure that the income is not zero
        if user_dict[k] != 0:

            #Use this taxDue to find effective percentage
            tax_dict[k][TAX_PERC] = tax_dict[k][TAX_DUE] /user_dict[k]

    return tax_dict


