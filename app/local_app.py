import asyncio
from add_sales_nav_list import add_sales_nav_list
from add_sales_nav_note import add_sales_nav_note
from comment_on_post import comment_on_post
from get_dm import get_dm
from get_inmail import get_inmail
from get_linkedin_profile import get_linkedin_profile
from get_recent_connections import get_recent_connections
from get_sales_nav_url import get_sales_nav_url
from request_connect_linkedin import request_connect_linkedin
from request_connect_sales_nav import request_connect_sales_nav
from search_linkedin import search_linkedin
from search_sales_nav import search_sales_nav
from send_dm import send_dm
from send_inmail import send_inmail
from get_own_profile import get_own_profile
from login import login
from security_code import security_code
import argparse
import json

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser()

    # Add parameters
    parser.add_argument("-function", type=str)
    parser.add_argument("-params", type=str)
    parser.add_argument("-proxy", type=str)

    # Parse the arguments
    function_name = parser.parse_args().function
    params = parser.parse_args().params
    proxy = parser.parse_args().proxy

    params = json.loads(params)
    proxy = json.loads(proxy)

    functions = {
        "add_sales_nav_list": add_sales_nav_list,
        "add_sales_nav_note": add_sales_nav_note,
        "comment_on_post": comment_on_post,
        "get_dm": get_dm,
        "get_inmail": get_inmail,
        "get_linkedin_profile": get_linkedin_profile,
        "get_recent_connections": get_recent_connections,
        "get_sales_nav_url": get_sales_nav_url,
        "request_connect_linkedin": request_connect_linkedin,
        "request_connect_sales_nav": request_connect_sales_nav,
        "search_linkedin": search_linkedin,
        "search_sales_nav": search_sales_nav,
        "send_dm": send_dm,
        "send_inmail": send_inmail,
        "get_own_profile": get_own_profile,
        "login": login,
        "security_code": security_code,
    }
    function = functions[function_name]
    if not function:
        raise Exception(f"Function with name {function_name} does not exist")
    print(json.dumps(asyncio.run(function(params, headless=False))))


main()
