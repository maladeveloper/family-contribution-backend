
import numpy as np 

test_dict = {
    'MAL001':{
        'income': 750
    }, 
    'SRI001':{
        'income':800
    },
    'ANU001':{
        'income':370
    },
    'MAI001':{
        'income': 290
    }
}



def apply_tax(user_dict,TOTAL_TAX_PER_WEEK):

    DEGREE_POLY = 1
    
    income_list = np.array([i['income'] for i in user_dict.values()])

    
    A = TOTAL_TAX_PER_WEEK / np.sum(income_list**(DEGREE_POLY + 1))

    for k,v  in user_dict.items():
        user_dict[k]['taxDue'] = round(A * v['income']**(DEGREE_POLY + 1))

        #Establish the tax percentage as 0 
        user_dict[k]['taxPerc'] = 0 

        #Ensure that the income is not zero
        if user_dict[k]['income'] != 0:

            #Use this taxDue to find effective percentage
            user_dict[k]['taxPerc'] = user_dict[k]['taxDue'] /user_dict[k]['income']


    return user_dict

