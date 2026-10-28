## Duka Connect - API Data Extraction and Extraction

# Overview
This project builds a simple data pipeline for Duka Connect, a Nairobi-based B2B distributor. It retrieves customer records from a REST API, processes nested JSON data, converts the records into a structured table, and saves the results as a CSV file for business analytics.

[API_URLhttps://jsonplaceholder.typicode.com/users
]




# Approach

- Fetch customer records using Python's requests library
- Validate HTTP responses and parse JSON data
- Inspect nested dictionaries and Python data types
- Extract important customer fields, including names, emails, cities, and company names
- Build lists, tuples, and dictionaries using loops and comprehensions
- Recursively flatten nested JSON objects into single-level records
- Organize transformed records using Pandas
- Standardize column names and convert geographic coordinates to numeric values
- Export a clean CSV file without an extra index column
- Handle connection errors, timeouts, unsuccessful HTTP responses, and invalid JSON


# Project Structure
```
api-extraction/
|--- extract_customers.py
|---| output/
|   |--- customers_clean.csv
|--- requirements.txt
|--- README.md

```

# Output

The pipeline generates the following file:

output/customers_clean.csv

The expected output contains 15 columns and 10 sample user records when the API returns its standard dataset.

# Assumptions and Data Handling

- Missing customer fields are represented as None during extraction.
- Missing address or company information is handled safely without raising a KeyError.
- Missing values in the exported CSV appear as empty fields.
- Geographic coordinates are converted to numeric values where possible.
- The API is expected to return a JSON list containing user dictionaries.
- The request timeout defaults to 10 seconds.
- The output directory is created automatically if it does not exist.
- Each successful run replaces the previous CSV instead of appending duplicate records

# How to run
**Install the required libaries**
pip install requests pandas

**Run the script**
python extraction.py

# Error Handling

The script handles error to manage common API request failures, including:
- **Invalid URLs:** Detects connection errors when the API cannot be reached.
- **Request timeouts:** Handles requests that take longer than the allowed time.
- **HTTP errors:** Reports unsuccessful responses, (Non-200 HTTP responses)
- **Invalid JSON:** Identifies responses that cannot be decoded as valid JSON.


# Conclusion
This project demonstrates a practical workflow, from extracting records from an external API to transforming nested JSON into a clean, analytics-ready CSV dataset. It applies Python data structures, comprehensions, recursive functions, Pandas transformations, file handling, and exception management to prepare  data for downstream purposes.
