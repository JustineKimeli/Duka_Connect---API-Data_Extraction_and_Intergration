# ==================================================
# Day 1 - API Data Extraction and Transformation
# ==================================================

# importing necessary libraries
import csv
import json
from pathlib import Path

import pandas as pd
import requests
import sys 

# 
API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_PATH = Path("output") / "customers_clean.csv"

# defining fetch users from api
def fetch_users(url: str = API_URL, timeout: float = 10.0) -> list[dict]:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list) or not all(
            isinstance(user, dict) for user in data
        ):
            raise ValueError("API response must be a list of user objects")

        return data

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(f"Request timed out: {url}") from exc

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(f"Connection failed: {url}") from exc

    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(f"HTTP error: {exc}") from exc

    except requests.exceptions.JSONDecodeError as exc:
        raise ValueError("API response contains invalid JSON") from exc


def describe_structure(payload) -> None:
    # Prints the payload and one records are made
    print(f"Top-level type: {type(payload).__name__}")

    if isinstance(payload, dict):
        print("Record type: dict")
        for key, value in payload.items():
            print(f"  {key}: {type(value).__name__}")

    elif isinstance(payload, list):
        if not payload:
            print("The payload is an empty list.")
            return

        record = payload[0]
        print(f"Record type: {type(record).__name__}")

        if isinstance(record, dict):
            for key, value in record.items():
                print(f"  {key}: {type(value).__name__}")
        else:
            print("The first record is not a dictionary.")

    else:
        print("Payload is neither a list nor a dictionary.")


def extract_core_fields(users: list[dict]) -> list[dict]:
    """Return one small dict per user with id, name, email, city and company name."""
    # Extract required fields 
    core_fields = []

    for user in users:
        core_fields.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("address", {}).get("city"),
            "company": user.get("company", {}).get("name")
        })
    return core_fields



def build_structures(users: list[dict]) -> tuple[list, list[tuple], dict]:
    # List comprehension and one dict comprehension.
    # List_comprehension
    names = [user.get("name") for user in users]

    
    id_email = [
        (user.get("id"), user.get("email"))
        for user in users
    ]

    # Dict comprehension
    id_to_city = {
        user.get("id"): user.get("address", {}).get("city")
        for user in users
    }

    return names, id_email, id_to_city

# Recursuve function to flatten dictionaries
def flatten_user(user: dict, parent_key: str = "", sep: str = "_") -> dict:    
    # Empty dictionary
    flattened = {}

    # looping through each value and key in items
    for key, value in user.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key

        if isinstance(value, dict):
            flattened.update(flatten_user(value, new_key, sep))
        else:
            flattened[new_key] = value

    return flattened

# Loading records to DataFrame
def to_dataframe(flat_users: list[dict]) -> pd.DataFrame:
    """Build a DataFrame with the columns in the expected-output order."""
    # Conversison to dataframe
    df = pd.DataFrame(flat_users)

    df = df.rename(columns={"id": "customer_id", "company_catchPhrase": "company_catchphrase"})

    # convert to valid data type


    df["address_geo_lat"] = pd.to_numeric(df["address_geo_lat"],
        errors="coerce")

    df["address_geo_lng"] = pd.to_numeric(df["address_geo_lng"],
            errors="coerce")

    
    expected_columns = [
        "customer_id",
        "name",
        "username",
        "email",
        "address_street",
        "address_suite",
        "address_city",
        "address_zipcode",
        "address_geo_lat",
        "address_geo_lng",
        "phone",
        "website",
        "company_name",
        "company_catchphrase",
        "company_bs",
    ]

    df = df[expected_columns]

    print("DataFrame: \n")
    print(df.shape)

    print("DataTypes:")
    print(df.dtypes)


    df = df.reindex(columns=expected_columns)

    return df


# Exporting to CSV
def export_csv(df: pd.DataFrame, path: Path = OUTPUT_PATH) -> Path:
    """Exporting to csv."""
    # create output folder
    path.parent.mkdir(parents=True, exist_ok=True)
    # save df as csv file
    df.to_csv(path, index=False)
    # file path
    return path


def main():


    try:
        users = fetch_users()

        print("=== STRUCTURE ANALYSIS ===\n")
        describe_structure(users)

        print("=== CORE FIELDS ===")
        core_fields = extract_core_fields(users)


        for field in core_fields[:2]:
            print(field)

        names, id_email, city = build_structures(users)


        print(f"Names Count: {len(names)}")
        print(f"Email count: {len(id_email)}")
        print(f"City  count: {len(city)}")


        flat_users = [
            flatten_user(user)
            for user in users
        ]


        df = to_dataframe(flat_users)

        output_file =export_csv(df)

        print("=== SUMMARY ===")
        print(f"Users Processed: {len(users)}")
        print(f"CSV exported to: {output_file}")
    
    
    except RuntimeError as exc:
        print(f"Error: {exc}", file= sys.stderr)
        sys.exit(1)



if __name__ == "__main__":
    main()