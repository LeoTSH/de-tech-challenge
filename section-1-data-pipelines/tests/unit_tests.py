import pytest
import pandas as pd
from src.utils import check_mobile, check_email, format_name, gen_member_id

def test_check_mobile_pass():
    data = pd.DataFrame(
            {
                "mobile":["+65 9503 6865"]
        }
    )
    data["res"] = data.apply(
        check_mobile,
        axis=1
    )
    assert data["res"].values == "95036865"


def test_check_email_pass():
    data = pd.DataFrame(
            {
                "email":["hhavick2k@goo.ne.jp"]
        }
    )
    data["res"] = data.apply(
        check_email,
        axis=1
    )
    assert data["res"].values == "hhavick2k@goo.ne.jp"


def test_format_name_pass():
    data = pd.DataFrame(
            {
                "name":["Aaryan Sathasivam s/o P. Nilanga"]
        }
    )
    data["res"] = data["name"].apply(
            lambda x: format_name(x)
    )
    assert data["res"].values[0] == ("aaryan_sathasivam", "p_nilanga")


def test_gen_member_id_pass():
    data = pd.DataFrame(
            {
                "last_name":["p_nilanga"],
                "dob":["19860611"]
        }
    )
    data["res"] = data.apply(
        gen_member_id,
        axis=1
    )
    assert data["res"].values == "p_nilanga_bc6f7"
