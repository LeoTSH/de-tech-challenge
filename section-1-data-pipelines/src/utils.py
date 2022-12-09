import re
import logging
import dateutil
import pandas as pd
from hashlib import sha256
from datetime import datetime

# logger config
# log_date = datetime.strftime(datetime.now(), "%Y%m%d")
# logger = logging.getLogger('process_data')
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# logger.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s - %(message)s'
)

def check_mobile(data: pd.Series) -> pd.Series:
    """
    Checks if a provided mobile number is valid.
    Determines if alphabets are present in the number, replaces "+", "-" and whitespaces.
    Removes 65 if the number starts with it.
    
    Args:
        mobile (str): Mobile number provided by the user
        
    Returns:
        Formatted mobile number or None if the number is invalid
        
    Raises:
        ValueError: If provided value is not str type
    """
    result = None 
    
    try:
        mobile = data['mobile_no']
        logging.info(f"Processing number: {mobile}")
        
        alphabet_pattern = re.compile(r"[A-Za-z]+")

        # If number contains alphabets, return None
        if re.findall(alphabet_pattern, mobile):
            return result
    
        pattern = re.compile(r"\+|\-|\s")
        mobile = re.sub(pattern=pattern, repl="", string=mobile)
        result = mobile if len(mobile) == 8 else result
    except Exception as e:
        logging.error("Execption occurred", exc_info=True)
    finally:
        logging.info(f"Mobile result: {result}")
        return result


def check_email(data: pd.Series) -> pd.Series:
    """
    Checks and validates provided email address.
    Before "@", match at least 1 or more characters/numbers before ".", "-", or "_" (Can be zero matches) 
    and at least 1 or more character/numbers 

    After "@", match at least 1 or more characters/numbers including "-"
    Uses capture group to determine domain information, matches ".", at least 2 or more characters 2 times.
    
    Args:
        email (str): Email address provided by the user
        
    Returns:
        result (str): Email address is valid, else None
        
    Raises:
        ValueError: If provided value is not str type

    """
    
    result = None
    email = data['email']
    logging.info(f"Processing email: {email}")
    pattern = re.compile("([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        
    try:
        result = re.fullmatch(pattern, email).group()
    except Exception as e:
        logging.error("Execption occurred", exc_info=True)
    finally:
        logging.info(f"Email result: {result}")
        return result


def format_name(name: str) -> str:
    """
    Splits provided name into first and last names.
    Removes affixes from the customer names
        
    Args:
        name (str): Name provided by the user
        
    Returns:
        result (tuple): First and last name, lowercase
        
    Raises:
        ValueError: If provided value is not str type

    """

    result = ()
    name_affixes = re.compile(r"[mM]r\.\s|[mM]rs\.\s|[mM]s\.\s|[dD]r\.\s|\s[jJ]r\.|\sMD|\sDDS|\sPhD|\sDVM")
                                    
    try:
        logging.info(f"Processing name: {name}")
        remove_affixes = re.sub(name_affixes, "", name)
        split_names = remove_affixes.split(" ")
        result = (split_names[0].strip(), split_names[1].strip())
    except Exception as e:
        logging.error("Execption occurred", exc_info=True)
    finally:
        logging.info(f"Name result: {result}")
        return result


def gen_member_id(data: pd.Series) -> pd.Series:
    """
    Generates the membership ID for the customer
    
    Args:
        lastname (str): last name of the customer
        dob (str): DoB name of the customer
        
    Returns:
        result (str): Membership ID
        
    Raises:
        ValueError: If provided values are not of str type

    """

    last_name = data['last_name']
    dob = data['date_of_birth']
    logging.info(f"Processing lastname: {last_name} and DoB: {dob}")
    result = None
        
    try:
        # Truncate hash to first 5 characters
        dob_hash = sha256(dob.encode("utf-8")).hexdigest()
        result = f"{last_name}_{dob_hash[:5]}".strip()
    except Exception as e:
        logging.error("Execption occurred", exc_info=True)
    finally:
        logging.info(f"Membership ID result: {result}")
        return result


def format_dob(dob: str) -> str:
    """
    Formats the customer's date of birth to YYYYMMDD format.
    
    Args:
        dob (str): Date of birth name of the user
        
    Returns:
        result (str): Formatted date of birth
        
    Raises:
        ValueError: If provided values are not of str type

    """
    
    logging.info(f"Processing DoB: {dob}")
    result = None
    
    try:
        result = datetime.strftime(dateutil.parser.parse(dob), "%Y%m%d")
    except Exception as e:
        logging.error("Execption occurred", exc_info=True)
    finally:
        logging.info(f"Date of birth result: {result}")
        return result

def calculate_age(format_dob: str) -> str:
    """
    Calculates the age of the customer based on date of birth.
    
    Args:
        format_dob (str): Date of birth name of the customer
        
    Returns:
        result (str): Age of the customer rounded to 2 decimal points
        
    Raises:
        ValueError: If provided values are not of str type

    """
    
    logging.info(f"Processing formatted DoB: {format_dob}")
    result = None
    
    try:
        age_datetime = datetime.strptime(format_dob, "%Y%m%d")
        result = round(((datetime(2022,1,1) - age_datetime).days / 365), 2)
    except Exception as e:
        logging.error("Execption occurred", exc_info=True)
    finally:
        logging.info(f"Age result: {result}")
        return result
