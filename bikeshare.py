# Links for reference:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.month_name.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.min.html
# https://dfrieds.com/data-analysis/value-counts-python-pandas.html
# https://github.com/Aritra96/bikeshare-project/blob/master/bikeshare.py was having difficulty with bringing up the birth year for the cities that had those columns and found this great example of using try and except. I used it in my own way and it fixed the problem.
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.head.html (to add in the option to view next five rows of data)

import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may',
              'june', 'july', 'august', 'september', 'october', 'november', 'december']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some us bikeshare data!')

    city_name = ''

    while city_name.lower() not in CITY_DATA:
        city_name = input(
            "\nWhat is the name of the city you would like to analyze\n")
        if city_name.lower() in CITY_DATA:
            # A correct city was chosen and analyzed
            city = CITY_DATA[city_name.lower()]
        else:
            # An incorrect city was picked
            print("no data on this city, please choose a correct one. \n")

    month_name = ''

    while month_name.lower() not in MONTH_DATA:
        month_name = input("\nWhat month would you like to analyze? \n")
        if month_name.lower() in MONTH_DATA:
            # A correct month was chosen to be analyzed
            month = month_name.lower()
        else:
            # An incorrect month was picked
            print("Not a month, please choose a correct month. \n")

    day_name = ''

    while day_name.lower() not in DAY_DATA:
        day_name = input("\nWhat is the name of the day to analyze?\n")
        if day_name.lower() in DAY_DATA:
            # A correct day was picked
            day = day_name.lower()
        else:
            # An incorrect day was picked
            print("Sorry you did not pick a correct day, please choose another. \n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all: to apply no day filter
    Returns:
        df - Pandas DataFram containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and say of week from Start Time to create mew columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter via month if necessary
    if month != 'all':
        # use the month index to get the right list
        month = MONTH_DATA.index(month)

    # filter by day of week if necessary
    if day != 'all':
        # filter by day of week to create new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print("The most common month from your selection of data is: " +
          MONTH_DATA[common_month].title())

    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the week from your selection of data is: " + common_day_of_week)

    popular_hour = df['hour'].mode()[0]
    print("The most common start hour from your selection of data is: " + str(popular_hour))

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips. """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print("The most popular start startion from your selection of data is: " +
          common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print("The most popular end station from your selection of data is: " +
          common_end_station)

    common_combination = (df['Start Station'] + "||" +
                          df['End Station']).mode()[0]
    print("The most common combo of start station and end station trip is : " +
          str(common_combination.split("||")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_trip_time = df['Trip Duration'].sum()
    print("The total travel time from your selection of data is: " +
          str(total_trip_time))

    mean_trip_time = df['Trip Duration'].mean()
    print("The mean travel time from your selection of data is: " + str(mean_trip_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df['User Type'].value_counts()
    print("The count of user types from your selection of data is: \n" + str(user_type))

    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("The count of user gender from your selection of data is: \n" + str(gender))
    else:
        print("This city contains no information on gender.")
    try:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The earliest birth year from your selected data is: {}\n'.format(
            earliest_birth_year))
        print('The most recent birth year from your selected data is: {}\n'.format(
            most_recent_birth_year))
        print('The Moost popular birth year from your selected data is: {}\n'.format(
            most_common_birth_year))
    except:
        print("There is no information on birth year in this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """ Gives the user the option to display raw data on request.
    Args:
        (DataFrame) df - Pandas Dataframe with city data filtered by month and day.
    """
    print(df.head())
    start_loc = 0
    while True:
        view_raw_data = input(
            '\nWould you like to see the following five rows of data? Yes or no and hit enter.\n')
        if view_raw_data.lower() != 'yes':
            return
        start_loc = start_loc + 5
        print(df.iloc[start_loc:start_loc+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        user_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            view_raw_data = input(
                '\nWould you like to see the following five rows of data? Yes or no and hit enter.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
