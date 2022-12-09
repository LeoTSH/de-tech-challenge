import pathlib
import pandas as pd
from datetime import datetime
from utils import logging, check_mobile, check_email, format_name, gen_member_id, format_dob, calculate_age
pd.options.mode.chained_assignment = None  # Default="warn"

def main():
    logging.info("Loading data")

    data_path = pathlib.Path("./data/mock_data") ## UPDATE PATH HERE
    dfs = []

    for filename in data_path.iterdir():
        df = pd.read_csv(filename, index_col=None, header=0)
        dfs.append(df)

    data = pd.concat(dfs, axis=0, ignore_index=True)

    # Separate date into valid and invalid names data
    data_valid_names = data[~data["name"].isnull()]
    data_invalid_name = data[data["name"].isnull()]

    # Save data with empty names, processing stops here this dataset, continuing with valid names
    logging.info("Saving invalid names data")
    data_invalid_name.to_csv("./data/invalid_data/invalid_names.csv", ## UPDATE PATH HERE
        header=True,
        index=False,
    ) 

    # Convert date of birth from string to datetime
    logging.info("Generating formatted date of birth")
    data_valid_names["format_dob"] = data_valid_names["date_of_birth"].apply(lambda x: format_dob(x))

    # Calculate age of user
    logging.info("Generating age")
    data_valid_names["age"] =  data_valid_names["format_dob"].apply(lambda x: calculate_age(x))

    # Determine if over 18 years old
    logging.info("Determing if user is above 18 years old")
    data_valid_names["above_18"] = data_valid_names["age"].apply(lambda x: x > 18)

    # Check and format mobile numbers
    logging.info("Validating mobile numbers")
    data_valid_names["tmp_mobile"] = data_valid_names.apply(check_mobile,
                                                                 axis=1)

    # Check email addresses
    logging.info("Validating email addresses")
    data_valid_names["tmp_email"] = data_valid_names.apply(check_email,
                                                               axis=1)

    # Drop unnecessary columns
    logging.info("Dropping unnecessary columns")
    data_valid_names = data_valid_names.drop(["tmp_email",
                                          "date_of_birth",
                                          "mobile_no"],
                                         axis=1)

    # Rename columns
    logging.info("Renaming columns")
    data_valid_names = data_valid_names.rename(
    columns={
        "format_dob":"date_of_birth",
        "tmp_mobile":"mobile"
        }
    )

    # Filter for only valid data mobile is a digits, over 18 years old and valid email
    logging.info("Extracting valid data")
    valid_data = data_valid_names.loc[(~data_valid_names["mobile"].isnull()) & \
                                 (data_valid_names["above_18"] == True) & \
                                 (~data_valid_names["email"].isnull())]

    # Filter for invalid data
    logging.info("Extracting invalid data")
    invalid_data = data_valid_names.loc[(data_valid_names["mobile"].isnull()) | \
                                 (~data_valid_names["above_18"] == True) | \
                                 (data_valid_names["email"].isnull())]
    
    # Format name to extract first and last name
    logging.info("Extracting first and last names")
    valid_data["first_name"] = valid_data["name"].apply(lambda x: format_name(x)[0])
    valid_data["last_name"] = valid_data["name"].apply(lambda x: format_name(x)[1])

    # Save invalid applicants data
    logging.info("Saving invalid data")
    invalid_data.to_csv("./data/invalid_data/invalid_data.csv", ## UPDATE PATH HERE
        header=True,
        index=False,
    )

    # Generate membership ID
    logging.info("Generating membership ID")
    valid_data["member_id"] = valid_data.apply(gen_member_id,
                                           axis=1)

    # Saving final data                                           
    logging.info("Saving final data")
    valid_data = valid_data[["member_id", "name", "first_name", "last_name", "above_18", "age", "date_of_birth", "mobile", "email"]]
    valid_data.to_csv("./data/cleaned_data/final_data.csv", ## UPDATE PATH HERE
        header=True,
        index=False,
    )

    # Number of applications
    logging.info(f"Number of successful applications: {valid_data.count()[0]}")
    logging.info(f"Number of failed applications: {invalid_data.count()[0]}")
    logging.info(f"Number of applications with invalid names: {data_invalid_name.count()[0]}")

if __name__ == "__main__":
    main()
    logging.info("Data extraction, formatting and saving completed")
