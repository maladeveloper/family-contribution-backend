##Built-in
import datetime
##Defined
from VARIABLES import WEEKS_PER_PAYMENT as WEEKS
from VARIABLES import DATE_FORMAT, DATE_SEPERATOR

def find_latest_date(all_dates):
        
    #e.g '01/03/2021-07/03/2021' -> (datetime(01/03/2021),datetime(07/03/2021))
    datetime_dates = [(datetime.datetime.strptime(cur_date.split(DATE_SEPERATOR)[0], DATE_FORMAT), datetime.datetime.strptime(cur_date.split("-")[1],DATE_FORMAT)) for cur_date in all_dates]

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


def get_refreshed_dates(all_dates_dict):

    all_dates = all_dates_dict.keys()

    add_curr_dates = get_current_dates(all_dates) #returned an array of datetimes having the newest dates OR False

    if(add_curr_dates):

        #Stringify the dates and then push them to the database
        add_curr_dates = datetime.datetime.strftime(add_curr_dates[0], DATE_FORMAT) + DATE_SEPERATOR + datetime.datetime.strftime(add_curr_dates[1], DATE_FORMAT)

        all_dates_dict[add_curr_dates] = True

    return all_dates_dict


