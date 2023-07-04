import pandas as pd
from emissions.models import Emission
from emissions.utils.generics import read_csv_file, miles_to_kilometers
from emissions.utils.enums import ActivityType, Unit
from pathlib import Path


def load_activity_data(activity_data_file: Path) -> pd.DataFrame:
    """
    Load activity data and update date format
    """
    activity_data = read_csv_file(activity_data_file)
    activity_data['Date'] = pd.to_datetime(activity_data['Date'], format='%d/%m/%Y').dt.date
    return activity_data


def load_emission_factors(emission_factors_file: Path) -> dict:
    """
    Return emission factor data in dictionary where keys are tuples of activity and identifiers and values
    are tuples of co2e, unit, scope and category.
    """
    emission_factors_data = read_csv_file(emission_factors_file)
    emission_factors = {
        (
            ActivityType[row['Activity'].replace(" ", "_").upper()],
            row['Lookup identifiers'].upper()
        ): (
            float(row['CO2e']),
            Unit[row['Unit'].replace(" ", "_").upper()],
            row['Scope'],
            row['Category']
        )
        for _, row in emission_factors_data.iterrows()
    }
    return emission_factors


def lookup_emission_factor(row, emission_factors):
    """
    Retrieve emission factor based on the activity type and lookup identifier from the dictionary
    of emission factors. If emission factor not found, a default value of 0.0 is returned.
    """
    activity = ActivityType[row['Activity'].replace(" ", "_").upper()]
    if activity == ActivityType.ELECTRICITY:
        lookup_identifier = row['Country']
    elif activity == ActivityType.AIR_TRAVEL:
        lookup_identifier = row['Flight range'] + ', ' + row['Passenger class']
    elif activity == ActivityType.PURCHASED_GOODS_AND_SERVICES:
        lookup_identifier = row['Supplier category']
    return emission_factors.get((activity, lookup_identifier.upper()), 0.0)


def save_emission(co2e, scope, category, activity, unit):
    """
    Save Emission object to the database.
    """
    Emission.objects.create(
        co2e=co2e,
        scope=scope,
        activity=activity,
        unit=unit,
        category=category if category else None
    )


def calculate_emissions(activity_data, emission_factors):
    """
    Iterate over the activity data and use emission factors to calculate emissions.
    Once calculation is completed emissions are stored in the database.
    """

    for _, row in activity_data.iterrows():
        activity = ActivityType[row['Activity'].replace(" ", "_").upper()]
        emission_factor, emission_factor_unit, scope, category = lookup_emission_factor(row, emission_factors)

        if activity == ActivityType.ELECTRICITY:
            value = row['Electricity Usage']
            unit = Unit[row['Units'].replace(" ", "_").upper()]
        elif activity == ActivityType.AIR_TRAVEL:
            value = row['Distance travelled']
            unit = Unit[row['Distance units'].replace(" ", "_").upper()]
            if unit == Unit.MILES and emission_factor_unit == Unit.KILOMETRES:
                value = miles_to_kilometers(value)
                unit = emission_factor_unit
        elif activity == ActivityType.PURCHASED_GOODS_AND_SERVICES:
            value = row['Spend']
            unit = Unit[row['Spend units'].replace(" ", "_").upper()]

        if unit != emission_factor_unit:
            raise ValueError('Inconsistent Units')

        co2e = value * emission_factor
        save_emission(co2e, scope, category, activity, unit)