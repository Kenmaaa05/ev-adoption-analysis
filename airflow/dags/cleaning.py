import os
import pandas as pd
import numpy as np

def clean_ev_data(
    raw_filename="Electric_Vehicle_Population_Data.csv",
    cleaned_filename="cleaned_ev.csv",
    utility_filename="utility_providers.csv"
):
    raw_path = os.path.join("/opt/airflow/data", raw_filename)
    cleaned_path = os.path.join("/opt/airflow/outputs", cleaned_filename)
    utility_path = os.path.join("/opt/airflow/outputs", utility_filename)

    ev = pd.read_csv(raw_path)

    # 1. Column Formatting & String Standardization

    ev.columns = ev.columns.str.strip().str.lower().str.replace(' ', '_', regex=False)

    ev['model'] = ev['model'].str.upper().str.strip()
    ev['make'] = ev['make'].str.upper().str.strip()
    ev['county'] = ev['county'].str.title().str.strip()
    ev['city'] = ev['city'].str.title().str.strip()
    ev['electric_vehicle_type'] = ev['electric_vehicle_type'].str.strip()
    ev['clean_alternative_fuel_vehicle_(cafv)_eligibility'] = ev['clean_alternative_fuel_vehicle_(cafv)_eligibility'].str.strip()

    # 2. Replacing Fake Zeros with Real NaNs and Imputing Missing Electric Ranges

    ev['electric_range'] = ev['electric_range'].replace(0, pd.NA)
    missing_before = ev['electric_range'].isna().sum()

    range_map = (
        ev.groupby(['make', 'model'])['electric_range']
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
        .to_dict()
    )
    def impute_range(row):
        if pd.isna(row['electric_range']):
            return range_map.get((row['make'], row['model']), np.nan)
        return row['electric_range']

    ev['electric_range'] = ev.apply(impute_range, axis=1)

    # 3. Creating Range Categories

    def categorize_range(r):
        if pd.isna(r): return 'Unknown'
        elif r < 100: return 'Low'
        elif r < 200: return 'Medium'
        elif r < 300: return 'High'
        else: return 'Very High'

    ev['range_category'] = ev['electric_range'].apply(categorize_range)

    # 4. Extracting Coordinates from vehicle_location

    ev[['longitude', 'latitude']] = ev['vehicle_location'].str.extract(r'POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)')
    ev['latitude'] = pd.to_numeric(ev['latitude'], errors='coerce')
    ev['longitude'] = pd.to_numeric(ev['longitude'], errors='coerce')
    ev.drop(columns=['vehicle_location'], inplace=True)

    # 5. Drop Garbage Rows + Unneeded Columns

    ev = ev[ev['state'] == 'WA']
    ev = ev.dropna(subset=['county', 'city', 'postal_code', 'latitude', 'longitude', 'electric_utility'])
    ev.drop(columns=['vin_(1-10)', '2020_census_tract', 'postal_code', 'base_msrp'], inplace=True)

    # 6. Exploding Multi-Utility Entries

    utility_df = ev[['dol_vehicle_id', 'electric_utility']].copy()
    utility_df['electric_utility'] = utility_df['electric_utility'].str.split(r'\|\|?')
    utility_df['electric_utility'] = utility_df['electric_utility'].apply(
        lambda lst: [x.strip() for x in lst if x and x.strip()] if isinstance(lst, list) else []
    )

    utility_df = utility_df.explode('electric_utility')
    utility_df['electric_utility'] = utility_df['electric_utility'].str.strip()

    utility_df.drop_duplicates(inplace=True)
    ev.drop(columns=['electric_utility'], inplace=True)

    # 7. CAFV Eligibility Simplified

    cafv_map = {
        'Clean Alternative Fuel Vehicle Eligible': 'Eligible',
        'Eligibility unknown as battery range has not been researched': 'Unknown',
        'Not eligible due to low battery range': 'Not_Eligible'
    }
    ev['clean_alternative_fuel_vehicle_(cafv)_eligibility'] = ev['clean_alternative_fuel_vehicle_(cafv)_eligibility'].map(cafv_map)

    # 8. Classifying Counties as Urban or Rural

    washington_counties = {
        "Adams": "rural",
        "Asotin": "rural",
        "Cowlitz": "rural",
        "Columbia": "rural",
        "Chelan": "rural",
        "Franklin": "rural",
        "Ferry": "rural",
        "Clallam": "rural",
        "Island": "rural",       
        "Garfield": "rural",
        "Douglas": "rural",
        "Mason": "rural",
        "Jefferson": "rural",
        "Grant": "rural",
        "San Juan": "rural",     
        "Klickitat": "rural",
        "Grays Harbor": "rural",
        "Skagit": "rural",
        "Lincoln": "rural",
        "Kittitas": "rural",
        "Yakima": "rural",
        "Okanogan": "rural",
        "Lewis": "rural",
        "Pend Oreille": "rural",
        "Pacific": "rural",
        "Skamania": "rural",
        "Walla Walla": "rural",
        "Stevens": "rural",
        "Whitman": "rural",
        "Wahkiakum": "rural",
        "Benton": "urban",
        "Clark": "urban",
        "King": "urban",
        "Kitsap": "urban",
        "Pierce": "urban",
        "Snohomish": "urban",
        "Spokane": "urban",
        "Thurston": "urban",
        "Whatcom": "urban"
    }

    ev['if_urban'] = ev['county'].map(washington_counties)
    ev["if_urban"] = ev["if_urban"].fillna("Urban")

    ev.to_csv(cleaned_path, index=False)
    utility_df.to_csv(utility_path, index=False)