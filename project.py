#!/usr/bin/env python
# coding: utf-8

# In[74]:


import time
import pandas as pd
import numpy as np

# In[75]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[76]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_index = '0'
    while not city_index in ['1','2','3']:
        print('What city?')
        print('  1 - Chicago')
        print('  2 - New York City')
        print('  3 - Washington DC')
        city_index = input('Selection: ')
    
    city = list(CITY_DATA.keys())[int(city_index)-1]

    print("You selected: ",city.capitalize())
    
    # get user input for month (all, january, february, ... , june)
    valid_month = False
    months = ['all','january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
    while(not valid_month):
        print ("Enter month:")
        i = 0
        for m in months:
            print("  ",i," - ",m.capitalize())
            i = i + 1
        try:
            month_input = int(input("Selection: "))
            if (month_input >= 0 and month_input <= 12):
                valid_month = True
                if (month_input == 0):
                    month = 'all'
                else:
                    month = month_input
        except:
            print("Invalid Month...") 
    print("You selected: ",months[month_input-1].capitalize())

    # get user input for day of week (all, monday, tuesday, ... sunday)

    valid_dow = False
    days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    while(not valid_dow):
        i = 0
        for d in days:
            print("  ",i+1," - ",d.capitalize())
            i = i + 1
        try:
            dow_input = int(input("Selection: "))
            if (month_input >= 0 and month_input <= 7):
                valid_dow = True
        except:
            print("Invalid Day of Week...") 
    print("You selected: ",days[dow_input].capitalize())
    day = days[dow_input]

    print(city,month,day)
    print('-'*40)
    return city, month, day


# In[77]:

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['month'] = pd.Series(df['Start Time']).dt.month
    df['day of week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    if (month != 'all'):
        df = df[(df['month']        == month)           ]
    if (day != 'all'):
        df = df[(df['day of week']  == day.capitalize())]

    return df


# In[83]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
    most_common_month = df['month'].value_counts().idxmax()
    print("Most common month is         ",months[most_common_month-1].capitalize())

    # display the most common day of week
    
    most_common_dow = df['day of week'].value_counts().idxmax()
    print("Most common day of week is   ",most_common_dow.capitalize())

    # display the most common start hour

    most_common_hour = df['hour'].value_counts().idxmax()
    print("Most common start hour is is ",most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[88]:

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("Most common start station is         ",most_common_start_station)

    # display most commonly used end station
    
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("Most common end station is           ",most_common_end_station)

    # display most frequent combination of start station and end station trip
    df['start end'] = df['Start Station'] + " to " + df['End Station']
    most_common_start_end_station = df['start end'].value_counts().idxmax()
    print("Most common start and end station is ",most_common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[93]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()
    print("Average trip duration is ",total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Average trip duration is ",mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[155]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.   Group by user type
    gb = df.groupby("User Type").agg(['count'])
    print(gb['Start Time'])
    print("")
    
    # Display counts of gender.  Group by gender
    try:
        gb = df.groupby("Gender").agg(['count'])
        print(gb['Start Time'])
    except:
        print("Counts by gender not availalbe for this city...")
    print("")
    
    # Display earliest, most recent, and most common year of birth.   Oldest, newest, group by birth date
    try:
        gb = df.groupby("Birth Year")
        earliest_birth_year = df["Birth Year"][df["Birth Year"].idxmin()]
        print("Earliest birth year    ",earliest_birth_year)
        recent_birth_year = df["Birth Year"][df["Birth Year"].idxmax()]
        print("Most recent birth year ",recent_birth_year)
        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
        print("Most common birth year ",most_common_birth_year)
    except:
        print("Earliest, most recent, and most common year of birth not available for this city... ")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[156]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #df = load_data('chicago',2,'monday')
        #print(df.head)
        #print(df['month'].head)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()


# In[146]:



    #df = pd.read_csv('chicago.csv')
    #df['Start Time']= pd.to_datetime(df['Start Time'])
    #df['month'] = pd.Series(df['Start Time']).dt.month
    #df['day of week'] = pd.Series(df['Start Time']).dt.weekday_name
    #print(df.head)
    #df = df[(df['day_of_week']  == day.capitalize())]
    #df = df[(df['month']        == 1)]
    #df = df[(df['day of week']  == 'Monday' )]
    #print(df.head)
    #gb = df.groupby("Birth Year")
    #print(gb[gb["Birth Year"] == gb["Birth Year"].min()])
    #earliest_birth_year = 
    #print("Earliest birth year ",earliest_birth_year)
    #recent_birth_year = gb[["Birth Year"]][gb["Birth Year"] == gb["Birth Year"].max()]
    #print("Most recent birth year ",recent_birth_year)
    #most_common_birth_year = df['Birth Year'].value_counts().idxmax()
    #print("Most common birth year           ",most_common_birth_year)
    #print(df[["Birth Year"]][df["Birth Year"] == df["Birth Year"].max()]) 
    #df['Start Time']= pd.to_datetime(df['Start Time'])
    #df['month'] = pd.Series(df['Start Time']).dt.month
    #df['day_of_week'] = pd.Series(df['Start Time'].dt.weekday_name
    #df = df[(df['month'] == month) & (df['day_of_week']  == day.capitalize())]
    #df['Start Time']= pd.to_datetime(df['Start Time'])
    #df['Start Time'] = pd.to_datetime(df["Start Time"])
    #df['Start Time'] = pd.to_datetime(df{''.timeStamp)
    #print(df['Start Time'])
    #print(pd.Series(tds).dt.days)
    # WHy is this column a series?
    #df['month'] = pd.Series(df['Start Time']).dt.month
    #print(df.columns.values)
    #print(df.dtypes)
    #print(df[df.columns[2]])
    #df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')


# In[ ]:




