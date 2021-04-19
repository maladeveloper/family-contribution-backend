##Built-in
import datetime
from collections import OrderedDict
import pprint

##Defined
from VARIABLES import DATE_FORMAT, DATE_SEPERATOR, DB_DATE_SEP, STR_DATE_SEP, ROLLING_PERIOD, WEEKS_PER_PAYMENT


#e.g '01/03/2021-07/03/2021' -> (datetime(01/03/2021),datetime(07/03/2021)
def convert_to_datetime(date_pair):

    return (datetime.datetime.strptime(date_pair.split(DATE_SEPERATOR)[0], DATE_FORMAT), datetime.datetime.strptime(date_pair.split(DATE_SEPERATOR)[1],DATE_FORMAT))


#e.g (datetime(01/03/2021),datetime(07/03/2021) -> '01/03/2021-07/03/2021'
def convert_to_stringtime(date_pair):

    return datetime.datetime.strftime(date_pair[0], DATE_FORMAT) + DATE_SEPERATOR + datetime.datetime.strftime(date_pair[1], DATE_FORMAT)


#e.g "01/03/2021-07/03/2021" -> "01_03_2021-07_03_2021"
def convert_to_db_date(string_date):

    return string_date.replace(STR_DATE_SEP, DB_DATE_SEP)


#e.g "01_03_2021-07_03_2021" -> "01/03/2021-07/03/2021"
def convert_to_str_date(db_date):

    return db_date.replace(DB_DATE_SEP, STR_DATE_SEP)



def sort_dates(dates_arr, desc=False):

    return sorted(dates_arr,key=lambda date: convert_to_datetime(date)[1], reverse=desc) 


def get_average_dates(cur_date, all_dates):

    previous_num_dates = ROLLING_PERIOD - 1

    average_dates = [cur_date] #The array to return with the dates

    previous_dates = [date for date in all_dates if convert_to_datetime(date)[1] < convert_to_datetime(convert_to_str_date(cur_date))[0]] #Only keep the dates previous to current date. 
    
    prev_dates_desc = sort_dates(previous_dates) #Sort the dates in decending order.

    ##Put the past number of dates in the average dates list (if less than number per period return with what is in average array)
    for _ in range(previous_num_dates):

        try:

            average_dates.append(prev_dates_desc.pop())
        
        except: #Means there is no more previous dates

            return average_dates
        
    return average_dates

    

        

        


    

