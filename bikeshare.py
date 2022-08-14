# load packages
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
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter the name of the city: ").lower()
    condition = True
    while condition:
        if city in CITY_DATA.keys():
            condition = False
        else:
            print("City must be one of: (chicago, new york city, washington)")
            city = input("Enter the name of the city: ").lower()
        
    # get user input for month (all, january, february, ... , june)
    MONTH_NAME = ["all", "january", "february", "march", "April", "may", "june"]
    month = input("Enter the name of the month: ").lower()
    while condition == False:
        if month in MONTH_NAME:
            condition = True
        else:
            print("Month must be one of: (all, january, february, ... , june)")
            month = input("Enter the name of the month: ").lower()
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_NAME = ["all", "monday","tuesday","wednesday", "thursday", "friday", "saturday", "sunday"]
    day = input("Enter the name for day of the week: ").lower()
    while condition:
        if day in DAY_NAME:
            condition = False
        else:
            print("Day must be one of: (all, monday, tuesday, ... , sunday)")
            day = input("Enter the name for day of the week: ").lower()
    
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
    df = pd.read_csv(CITY_DATA[city])
    df["month"] = pd.to_datetime(df["Start Time"]).dt.strftime("%B").str.lower()
    df["day"] = pd.to_datetime(df["Start Time"]).dt.strftime("%A").str.lower()
    if month != "all" and day == "all":
        df = df[df.month == month]
    elif month == "all" and day != "all":
        df = df[df.day == day]
    elif month != "all" and day != "all":
        df = df[((df.month == month) & (df.day == day))]
    
    df = df.iloc[:,:-2].reset_index(drop=True)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = pd.to_datetime(df["Start Time"]).dt.strftime("%B").value_counts().index[0]

    # display the most common day of week
    common_day = pd.to_datetime(df["Start Time"]).dt.strftime("%A").value_counts().index[0]

    # display the most common start hour
    common_start_hour = pd.to_datetime(df["Start Time"]).dt.strftime("%H").value_counts().index[0]
    
    print("Most common; ", \
          "- month: %s" % common_month, \
          "- day: %s" % common_day, \
          "- start hour: %s" % common_start_hour, sep = "\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df["Start Station"].value_counts().index[0]

    # display most commonly used end station
    common_end_station = df["End Station"].value_counts().index[0]

    # display most frequent combination of start station and end station trip
    common_start_end_station = ("From" + " " + df["Start Station"] + " " + "To" + " " + df["End Station"]).value_counts().index[0]
    
    print("Most commonly used; ", \
         "- start station: %s" % common_start_station, \
         "- end station: %s" % common_end_station, \
         "- start + end station: %s" % common_start_end_station, sep = "\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df["Trip Duration"].sum()

    # display mean travel time
    mean_duration = np.mean(df["Trip Duration"])
    
    print("- total travel time: %s" % total_duration, \
         "- mean travel time: %s" % mean_duration, sep = "\n")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
   
    print("*"*5," Counts of User Types ","*"*5, sep = "")
    print(user_types)
    print("*"*32)
    
    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df["Gender"].value_counts()
        print()
        print("*"*12," Gender ","*"*12, sep = "")
        print(gender)
        print("*"*32)
        print()
     # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest =int(df["Birth Year"].min())
        recent = int(df["Birth Year"].max())
        common = int(df["Birth Year"].value_counts().index[0])
        print("*"*7," Birth Year Stats ","*"*7, sep = "")
        print("- earliest year: %s" % earliest, \
             "- recent year: %s" % recent, \
             "- common year: %s" % common, sep = "\n")
        print("*"*32)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
