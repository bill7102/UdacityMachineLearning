#!/usr/bin/env python
# coding: utf-8

# In[74]:


import time
import pandas as pd
import numpy as np
import click

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
 
    click.clear()
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_index = '0'
    while not city_index in ['1','2','3']:
        print('\nEnter city?')
        print('  1 - Chicago')
        print('  2 - New York City')
        print('  3 - Washington DC')
        city_index = input('Selection: ')
    
    city = list(CITY_DATA.keys())[int(city_index)-1]
    click.clear()
    print("You selected: ",city.capitalize())
    
    # get user input for month (all, january, february, ... , june)
    valid_month = False
    months = ['all','january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
    while(not valid_month):
        print ("\nEnter month:")
        i = 0
        for m in months:
            print("  {:2d} - {}".format(i,m.capitalize()))
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
            click.clear()
            print("Invalid Month...") 

    click.clear()
    print("You selected: ",months[month_input].capitalize())

    # get user input for day of week (all, monday, tuesday, ... sunday)

    valid_dow = False
    days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    while(not valid_dow):
        print ("\nEnter day of week:")
        i = 0
        for d in days:
            print("  ",i," - ",d.capitalize())
            i = i + 1
        try:
            dow_input = int(input("Selection: "))
            if (dow_input >= 0 and dow_input <= 7):
                valid_dow = True
        except:
            click.clear()
            print("Invalid Day of Week...") 
    
    day = days[dow_input]
    click.clear()
    print("\nProcessing data for: ")
    print("  City  :",city.capitalize())
    print("  Month :",months[month_input].capitalize()) 
    print("  Day   :",days[dow_input].capitalize()) 
    print('-'*40)
    input("Press any key to continue...")
    click.clear()
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
        df = df[(df['month'] == month)]
    if (day != 'all'):
        df = df[(df['day of week']  == day.capitalize())]
    return df


# In[83]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['all','january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']

    most_common_month = df['month'].value_counts().idxmax()
    print("Most common month is         ",months[most_common_month].capitalize())

    # display the most common day of week

    most_common_dow = df['day of week'].value_counts().idxmax()
    print("Most common day of week is   ",most_common_dow.capitalize())

    # display the most common start hour

    most_common_hour = df['hour'].value_counts().idxmax()
    print("Most common start hour is    ",most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press any key to continue...")
    click.clear()


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
    input("Press any key to continue...")
    click.clear()


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
    input("Press any key to continue...")
    click.clear()

# In[155]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()


    # Display counts of user types.   Group by user type
    print("\nCounts of user type\n")
    gb = df.groupby("User Type").agg(['count'])
    print(gb['Start Time'])

    print("")
    
    # Display counts of gender.  Group by gender
    try:
        print("\nCounts of gender\n")
        gb = df.groupby("Gender").agg(['count'])
        print(gb['Start Time'])
    except:
        print("Cannot display counts by gender.  Data not available for this city.")
    print("")
    
    # Display earliest, most recent, and most common year of birth.   Oldest, newest, group by birth date

    try:
        gb = df.groupby("Birth Year")
        earliest_birth_year = df["Birth Year"][df["Birth Year"].idxmin()]
        print("Earliest birth year    {:4d}".format(earliest_birth_year))
        recent_birth_year = df["Birth Year"][df["Birth Year"].idxmax()]
        print("Most recent birth year {:4d}".format(recent_birth_year))
        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
        print("Most common birth year {:4d}".format(most_common_birth_year))
    except:
        print("Birth Date data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press any key to continue...")
    click.clear()

# In[156]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if (df.shape[0] == 0):
            print("No data found for city, month, and day")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()