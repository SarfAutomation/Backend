import asyncio
from get_linkedin_profile import get_linkedin_profile
from get_post import get_post
from comment_on_post import comment_on_post
from request_connect_linkedin import request_connect_linkedin
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def chat(prompt):
    model = OpenAI()
    model.timeout = 30
    response = model.chat.completions.create(
        model="gpt-4-turbo",
        messages=(
            [
                {"role": "user", "content": prompt},
            ]
        ),
        max_tokens=1024,
    )
    message = response.choices[0].message
    message_text = message.content
    return message_text


def main():
    profile_info = asyncio.run(
        get_linkedin_profile(
            {
                "linkedin_url": "https://www.linkedin.com/in/jasonciment/",
                "key": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
            },
            headless=False,
        )
    )

    recent_post = profile_info["recent_posts"][0]

    post_info = asyncio.run(
        get_post(
            {
                "post_url": recent_post,
                "key": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
            },
            headless=False,
        )
    )

    print(post_info)

    # use post info to generate message
    message = chat(
        f"Generate a comment for this linkedin post with content {post_info}, only contain the comment and nothing else, avoid any placeholders."
    )
    asyncio.run(
        comment_on_post(
            {
                "post_url": recent_post,
                "comment": message,
                "key": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
            },
            headless=False,
        )
    )

    sleep(10)

    # use post info to generate message
    message = chat(
        f"""Generate me a Linkedin connect message, no more than 3 sentences and 300 charactors. It needs to end with some sort of "happy to connect".
 My goal is to get the person intrigued. And to show that I've done more than 10 minutes of research on him. Basically show I put time into crafting the message.  So it's not just about how well my message describes who he is, or what he does. Must mention something that can't be captured from quickly scanning their profile information. Avoid using strong words like "love, admire, inspiring", they dont seem real. Make it human-like. And keep it conversational, don't write sophisticatedly. 
Avoid any placeholders
Here's the profile JSON: {profile_info}"""
    )
    asyncio.run(
        request_connect_linkedin(
            {
                "linkedin_url": "https://www.linkedin.com/in/jasonciment/",
                "content": message,
                "key": "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G",
            },
            headless=False,
        )
    )


main()
