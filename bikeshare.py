import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Please provide the city of your choice. (Chicago, New York City, Washington): ").strip().lower()
        if city in cities:
            break
        print("Invalid city entry - Please choose from Chicago, New York City, or Washington.")

    #get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Please provide the month selection of your choice. (January, February, March, April, May, June, or 'All'): ").strip().lower()
        if month in months:
            break
        print("Invalid selection. Please select 'all' or a month from January to June.")

    #get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
       day = input("Please select a day of the week or 'all': ").strip().lower()
       if day in days:
            break
       print("Invalid selection. Please choose 'all' or a day of the week.")

    print('-'*40)
    return city, month, day


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

    #load in CSV data
    df = pd.read_csv(CITY_DATA[city])

    #convert start time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #extract isolated time values
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['start_hour'] = df['Start Time'].dt.hour
    
    #filter by month and day
    if month != 'all':
        df = df[df['month'] == month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day]
        
    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    if month == 'all':
        mc_month = df['month'].mode()[0].title()
        print(f"Most common month: {mc_month}")
    else:
        print(f"\nMonth filtered to {month.title()}, so your entry will exclusively return {month.title()} for most common month. If you would like the most common month in the data, choose 'All' as your selection.\n")
    #display the most common day of week
    if day == 'all':
        mc_day = df['day_of_week'].mode()[0].title()
        print(f"Most common day of the week: {mc_day}")
    else:
        print(f"\nDay filtered to {day.title()}, so your entry will exclusively return {day.title()} for most common day. If you would like the most common day in the data, choose 'All' as your selection.\n")
        
    #display the most common start hour
    mc_sh = df['start_hour'].mode()[0]
    print(f"Most common start hour: {mc_sh}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    s_station = df['Start Station'].mode()[0]
    print(f"Most common start station: {s_station}")

    #display most commonly used end station
    e_station = df['End Station'].mode()[0]
    print(f"Most common end station: {e_station}")
    

    #display most frequent combination of start station and end station trip
    combo_tuple = list(zip(df['Start Station'], df['End Station']))
    combo_series = pd.Series(combo_tuple)
    mc_combo = combo_series.mode()[0]
    print(f"Most frequent trip: {mc_combo[0]} to {mc_combo[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time in multiple time units
    ttts = df['Trip Duration'].sum()
    tttm = ttts/60
    ttth = ttts/3600
    tttd = ttts/86400
    
    print(f"Total travel time:\n {ttts:,} seconds\n {tttm:,} minutes\n {ttth:,} hours\n {tttd:,} days")
    
    #display mean travel time in multiple time units
    avg_tts = df['Trip Duration'].mean()
    avg_ttm = avg_tts/60
    avg_tth = avg_tts/3600
    avg_ttd = avg_tts/86400
    
    print(f"\nAverage travel time:\n {avg_tts:,} seconds\n {avg_ttm:,} minutes\n {avg_tth:,} hours\n {avg_ttd:,} days")

    #display median travel time in multiple time units
    med_tts = df['Trip Duration'].median()
    med_ttm = med_tts/60
    med_tth = med_tts/3600
    med_ttd = med_tts/86400
    
    print(f"\nMedian travel time:\n {med_tts:,} seconds\n {med_ttm:,} minutes\n {med_tth:,} hours\n {med_ttd:,} days")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #calculate total amount of trips in queried data
    total_trips = len(df)
    print(f"Total trips for selected data: {total_trips:,}\n")
    
    #Display counts of user types
    ut = df['User Type'].value_counts()
    print("User Types:")
    print(ut.to_string())

    #Display counts of gender
    if 'Gender' in df.columns:
        gc = df['Gender'].value_counts()
        print("\nGender:")
        print(gc.to_string())
    else:
        print("\nGender data not available for this city")

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        print("\nBirth Year:")
        print(f"Earliest        {earliest}")
        print(f"Most recent     {recent}")
        print(f"Most common     {common}")   
    else:
        print("\nBirth year data not available for Washington, please select Chicago or New York City to view birth year data.")
               
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#provide user with their selections
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print(f"\nYou have selected:\n"
              f" City  : {city.title()}\n"
              f" Month : {month.title()}\n"
              f" Day   : {day.title()}\n")
        print('-'*40)
        
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #raw data view option
        row_start = 0
        show_data = input("Would you like to see 5 rows of raw data? Enter yes or type anything else to signal no: ").strip().lower()
        while show_data == 'yes' and row_start < len(df):
            print(df.iloc[row_start : row_start + 5])
            row_start += 5
            if row_start >= len(df):
                print("End of data.")
                break
            show_data = input("Would you like to see 5 more rows of raw data? Enter yes or type anything else to signal no: ").strip().lower()
        
        #restart option
        restart = input('\nWould you like to restart? Enter yes or type anything else to signal no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()