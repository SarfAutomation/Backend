import asyncio
from add_sales_nav_list import add_sales_nav_list
from add_sales_nav_note import add_sales_nav_note
from comment_on_post import comment_on_post
from get_dm import get_dm
from get_inmail import get_inmail
from get_linkedin_profile import get_linkedin_profile
from get_linkedin_url import get_linkedin_url
from get_notifications import get_notifications
from get_recent_connections import get_recent_connections
from get_sales_nav_url import get_sales_nav_url
from request_connect_linkedin import request_connect_linkedin
from request_connect_sales_nav import request_connect_sales_nav
from search_linkedin import search_linkedin
from search_sales_nav import search_sales_nav
from send_dm import send_dm
from send_inmail import send_inmail
from get_own_profile import get_own_profile
from get_post import get_post
from login import login
from security_code import security_code
import json
import os
import shutil

def handler(event, context):
    functions = {
        "add_sales_nav_list": add_sales_nav_list,
        "add_sales_nav_note": add_sales_nav_note,
        "comment_on_post": comment_on_post,
        "get_dm": get_dm,
        "get_inmail": get_inmail,
        "get_linkedin_profile": get_linkedin_profile,
        "get_linkedin_url": get_linkedin_url,
        "get_notifications": get_notifications,
        "get_recent_connections": get_recent_connections,
        "get_sales_nav_url": get_sales_nav_url,
        "request_connect_linkedin": request_connect_linkedin,
        "request_connect_sales_nav": request_connect_sales_nav,
        "search_linkedin": search_linkedin,
        "search_sales_nav": search_sales_nav,
        "send_dm": send_dm,
        "send_inmail": send_inmail,
        "get_own_profile": get_own_profile,
        "get_post": get_post,
        "login": login,
        "security_code": security_code,
    }
    data = event["body"]
    if isinstance(data, str):
        data = json.loads(data)

    print("============================")
    print(data)
    function_name = data["function_name"]
    params = data["params"]
    proxy = None if "proxy" not in data else data["proxy"]
    function = functions[function_name]
    if not function:
        raise Exception(f"Function with name {function_name} does not exist")
    result = asyncio.run(function(params, proxy=proxy))
    # Clean up /tmp directory
    for filename in os.listdir('/tmp'):
        file_path = os.path.join('/tmp', filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result),
    }
