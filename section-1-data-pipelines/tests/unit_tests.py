import pytest
import pandas as pd
from src.utils import check_mobile, check_email, format_name, gen_member_id

def test_check_mobile_pass():
    data = pd.DataFrame(
            {
                "mobile_no":["40601711"]
        }
    )
    data["res"] = data.apply(
        check_mobile,
        axis=1
    )
    assert data["res"].values == "40601711"


def test_check_email_pass():
    data = pd.DataFrame(
            {
                "email":["William_Dixon@woodward-fuller.biz"]
        }
    )
    data["res"] = data.apply(
        check_email,
        axis=1
    )
    assert data["res"].values == "William_Dixon@woodward-fuller.biz"


def test_format_name_pass():
    data = pd.DataFrame(
            {
                "name":["Kristen Horn"]
        }
    )
    data["res"] = data["name"].apply(
            lambda x: format_name(x)
    )
    assert data["res"].values[0] == ("Kristen", "Horn")


def test_gen_member_id_pass():
    data = pd.DataFrame(
            {
                "last_name":["Dixon"],
                "date_of_birth":["19860110"]
        }
    )
    data["res"] = data.apply(
        gen_member_id,
        axis=1
    )
    assert data["res"].values == "Dixon_3864b"
