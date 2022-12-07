import re
import logging
import pandas as pd
from datetime import datetime
from hashlib import sha256

# Logging config
log_date = datetime.strftime(datetime.now(), "%Y%m%d")
logger = logging.getLogger('__name__')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger.setLevel(logging.DEBUG)


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
    
    try:
        mobile = data['mobile']
        logger.info(f"Processing number: {mobile}")
        result = None 
        alphabet_pattern = re.compile(r"[A-Za-z]+")

        # If number contains alphabets, return "False"
        if re.findall(alphabet_pattern, mobile):
            return result
    
        pattern = re.compile(r"\+|\-|\s")
        mobile = re.sub(pattern=pattern, repl="", string=mobile)
        mobile = mobile if not mobile.startswith("65") else mobile[2:]
        result = mobile if len(mobile) == 8 else "False"
    except Exception as e:
        logger.error("Execption occurred", exc_info=True)
    finally:
        logger.info(f"Mobile result: {result}")
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
    
    email = data['email']
    logger.info(f"Processing email: {email}")
    result = None
    pattern = re.compile("([A-Za-z0-9]+[.\-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
        
    try:
        result = re.fullmatch(pattern, email).group()
    except Exception as e:
        logger.error("Execption occurred", exc_info=True)
    finally:
        logger.info(f"Email result: {result}")
        return result


def format_name(name: str) -> str:
    """
    Splits provided name into first and last names.
    Checks for patronymic terms and splits/joins based on those terms for Indian and Malay names.
    
    For Chinese names, the first word is considered the last name and the rest, first name hence, the results will need to be reversed.    
    
    Args:
        name (str): Name provided by the user
        
    Returns:
        result (tuple): First and last name, lowercase
        
    Raises:
        ValueError: If provided value is not str type

    """

    result = ()
    indian_patronymic = re.compile(r"s\/o|d\/o")
    malay_patronymic = re.compile(r"Binte|Bin")
    sub_pattern = re.compile(r"\.\ |\s")
                                    
    try:
        logger.info(f"Processing name: {name}")
        
        if re.findall(indian_patronymic, name):
            tmp = re.split(indian_patronymic, name)
            result = (re.sub(sub_pattern, "_", tmp[0].strip()).lower(), \
                      re.sub(sub_pattern, "_", tmp[1].strip()).lower())
        elif re.findall(malay_patronymic, name):
            tmp = re.split(malay_patronymic, name)
            result = (re.sub(sub_pattern, "_", tmp[0].strip()).lower(), \
                      re.sub(sub_pattern, "_", (re.findall(malay_patronymic, name)[0].strip()+" "+tmp[1].strip())).lower())
        else:
            result = (" ".join(name.split()[1:]).lower(), name.split()[0].lower())
    except Exception as e:
        logger.error("Execption occurred", exc_info=True)
    finally:
        logging.info(f"Name result: {result}")
        return result


def gen_member_id(data: pd.Series) -> pd.Series:
    """
    Generates the membership ID for the user
    
    Args:
        lastname (str): last name of the user
        dob (str): DoB name of the user
        
    Returns:
        result (str): Membership ID
        
    Raises:
        ValueError: If provided values are not of str type

    """

    last_name = data['last_name']
    dob = data['dob']
    logger.info(f"Processing lastname: {last_name} and DoB: {dob}")
    result = None
        
    try:
        # Truncate hash to first 5 characters
        dob_hash = sha256(dob.encode("utf-8")).hexdigest()
        result = f"{last_name}_{dob_hash[:5]}".strip()
    except Exception as e:
        logger.error("Execption occurred", exc_info=True)
    finally:
        logger.info(f"Membership ID result: {result}")
        return result
