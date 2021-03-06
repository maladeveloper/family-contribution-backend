##Built-in
import datetime

##Defined
from VARIABLES import WEEKS_PER_PAYMENT as WEEKS
from date_functions import convert_to_datetime, convert_to_stringtime
#

def order_dates(dates, descend=False):

    datetime_dates = [convert_to_datetime(cur_date) for cur_date in dates]

    sorted_dates = sorted(datetime_dates, key=lambda dates:dates[1])

    if descend:
        sorted_dates.reverse()

    #convert back to strs 
    return [convert_to_stringtime(date) for date in sorted_dates]
    
def find_latest_date(all_dates):
        
    datetime_dates = [convert_to_datetime(cur_date) for cur_date in all_dates]

    #Get latest date based on second date in each tuple 
    latest_dates = max(datetime_dates, key=lambda dates:dates[1])
    
    return latest_dates

def get_current_dates(all_dates):

    latest_dates = find_latest_date(all_dates) #returns latest dates as tuples with datetime

    #Break with false if current date is before start of latest date (dont need to add any new date)
    if datetime.datetime.now() < (latest_dates[1] + datetime.timedelta(days = 1)) :
        
        return False

    else: #Otherwise keep adding the weeks until it encapsulates current date

        latest_date = latest_dates[1]

        latest_dates_arr = [latest_date + datetime.timedelta(days = 1), latest_date + datetime.timedelta(weeks = WEEKS) ]

        while (datetime.datetime.now()> latest_dates_arr[1]):

            latest_dates_arr = [latest_dates_arr[1] + datetime.timedelta(days = 1), latest_dates_arr[1] + datetime.timedelta(weeks = WEEKS) ]

        return latest_dates_arr 

def set_active_dates(dates_dict):

    latest_string_date = convert_to_stringtime(find_latest_date(dates_dict))
    
    new_dates_dict = {date:False for date in dates_dict.keys() if date != latest_string_date}

    new_dates_dict[latest_string_date] = dates_dict[latest_string_date]

    return new_dates_dict


def get_refreshed_dates(all_dates_dict):

    all_dates = all_dates_dict.keys()

    add_curr_dates = get_current_dates(all_dates) #returned an array of datetimes having the newest dates OR False

    if(add_curr_dates):

        #Stringify the dates and then push them to the database
        add_curr_dates = convert_to_stringtime(add_curr_dates)

        all_dates_dict[add_curr_dates] = True

    return set_active_dates(all_dates_dict)


