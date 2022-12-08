from utils import check_mobile, check_email, format_name, gen_member_id, logger
import pandas as pd
from datetime import datetime
pd.options.mode.chained_assignment = None  # Default="warn"


def main():
    logger.info("Loading data")
    data = pd.read_csv("./data/mock_data/mock_data.csv") ## UPDATE PATH HERE
    data_valid_names = data[~data["name"].isnull()]
    data_invalid_name = data[data["name"].isnull()]

    # Save data with empty names, processing stops here this dataset, continuing with valid names
    logger.info("Saving invalid names data")
    data_invalid_name.to_csv("./data/invalid_data/invalid_names.csv", ## UPDATE PATH HERE
        header=True,
        index=False,
    ) 

    # Convert date of birth from string to datetime
    logger.info("Generating DoB date time")
    data_valid_names["tmp_dob_datetime"] = data_valid_names["dob"].apply(lambda x: datetime.strptime(x, "%d/%b/%Y"))

    # Calculate age of user
    logger.info("Generating age")
    data_valid_names["age"] = (datetime(2022,1,1) - data_valid_names["tmp_dob_datetime"]).dt.days / 365

    # Determine if over 18 years old
    logger.info("Determing if user is above 18 years old")
    data_valid_names["above_18"] = data_valid_names["age"].apply(lambda x: x > 18)

    # Format date of birth to YYYYMMDD
    logger.info("Formatting DoB to YYYYMMDD")
    data_valid_names["tmp_dob"] = data_valid_names["dob"].apply(lambda x: datetime.strftime(datetime.strptime(x, "%d/%b/%Y"), "%Y%m%d"))

    # Check and format mobile numbers
    logger.info("Validating mobile numbers")
    data_valid_names["tmp_mobile"] = data_valid_names.apply(check_mobile,
                                                                 axis=1)

    # Check email addresses
    logger.info("Validating email addresses")
    data_valid_names["tmp_email"] = data_valid_names.apply(check_email,
                                                               axis=1)

    # Drop unnecessary columns
    logger.info("Dropping unnecessary columns")
    data_valid_names = data_valid_names.drop(["tmp_dob_datetime",
                                          "dob",
                                          "mobile",
                                         "email"],
                                         axis=1)

    # Rename column to dob
    logger.info("Renaming columns")
    data_valid_names = data_valid_names.rename(
        columns={
            "tmp_dob":"dob",
            "tmp_mobile":"mobile",
            "tmp_email":"email"
        }
    )

    # Filter for only valid data mobile is a digits, over 18 years old and valid email
    logger.info("Extracting valid data")
    valid_data = data_valid_names.loc[(~data_valid_names["mobile"].isnull()) & \
                                 (data_valid_names["above_18"] == True) & \
                                 (~data_valid_names["email"].isnull())]

    # Filter for invalid data
    logger.info("Extracting invalid data")
    invalid_data = data_valid_names.loc[(data_valid_names["mobile"].isnull()) | \
                                 (~data_valid_names["above_18"] == True) | \
                                 (data_valid_names["email"].isnull())]
    
    # Save invalid applicants data
    logger.info("Saving invalid data")
    invalid_data.to_csv("./data/invalid_data/invalid_data.csv", ## UPDATE PATH HERE
        header=True,
        index=False,
    )

    # Format name to extract first and last name
    logger.info("Extracting first and last names")
    valid_data["first_name"] = valid_data["name"].apply(lambda x: format_name(x)[0])
    valid_data["last_name"] = valid_data["name"].apply(lambda x: format_name(x)[1])

    # Generate membership ID
    logger.info("Generating membership ID")
    valid_data["member_id"] = valid_data.apply(gen_member_id,
                                           axis=1)

    # Saving final data                                           
    logger.info("Saving final data")
    valid_data = valid_data[["member_id", "name", "first_name", "last_name", "above_18", "age", "dob", "mobile", "email"]]
    valid_data.to_csv("./data/cleaned_data/final_data.csv", ## UPDATE PATH HERE
        header=True,
        index=False,
    )

    # Number of applications
    logger.info(f"Number of successful applications: {valid_data.count()[0]}")
    logger.info(f"Number of failed applications: {invalid_data.count()[0]}")

if __name__ == "__main__":
    main()
    logger.info("Data extraction, formatting and saving completed")
