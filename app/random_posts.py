import asyncio
from get_linkedin_profile import get_linkedin_profile
from get_post import get_post
from comment_on_post import comment_on_post
from request_connect_linkedin import request_connect_linkedin
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv
from search_linkedin import search_linkedin
import requests

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
    print(message_text)
    return message_text


def main(key):
    occupations = [
        "Software Engineer",
        # "Data Scientist",
        # "Project Manager",
        # "Digital Marketing Specialist",
        # "Graphic Designer",
        # "Human Resources Manager",
        # "Financial Analyst",
        # "Product Manager",
        # "Business Development Manager",
        # "Content Creator",
        # "UX/UI Designer",
        # "Cybersecurity Analyst",
        # "Supply Chain Manager",
        # "Sales Executive",
        # "Video Editor",
        # "Real Estate Agent",
        # "Pharmaceutical Sales",
        # "Renewable Energy Consultant",
        # "Machine Learning Engineer",
        # "Corporate Lawyer",
        # "Healthcare Administrator",
        # "Public Relations Specialist",
        # "Educational Consultant",
        # "Civil Engineer",
        # "Event Planner",
        # "Chef",
        # "Fitness Trainer",
        # "Fashion Designer",
        # "Environmental Scientist",
        # "Biotechnologist",
        # "Construction Project Manager",
        # "Aviation Pilot",
        # "Veterinary Surgeon",
        # "Marine Biologist",
        # "Art Director",
        # "Freelance Writer",
        # "Social Media Manager",
        # "Actuary",
        # "Industrial Designer",
        # "Archaeologist",
    ]

    posts = []

    for occupation in occupations:
        search_results = asyncio.run(
            search_linkedin(
                {"searchTerm": occupation, "amount": 1, "key": key},
                headless=False,
            )
        )
        for profile in search_results:
            try:
                profile_info = asyncio.run(
                    get_linkedin_profile(
                        {"linkedin_url": profile, "key": key},
                        headless=False,
                    )
                )

                recent_post = profile_info["recent_posts"][0]

                # post_info = asyncio.run(
                #     get_post(
                #         {"post_url": recent_post, "key": key},
                #         headless=False,
                #     )
                # )
                # posts.append(post_info)
                requests.post(
                    "https://hooks.zapier.com/hooks/catch/18369368/3j74gm9/",
                    {"name": profile_info["name"], "profile": profile, "post": recent_post},
                )
            except:
                pass
    return posts


key = "AQEDAR5mR60C386-AAABjs-h9BAAAAGO8654EFYAnlJkWITqvqUD3WfQNNBMZRzOQLGwMBt7s6N5va13mQ71C2WEWkghD2IdYSy1WHG3OOkC5SIPscZcn9icKjGHyT0uPw-twG031xOKucazzmOpce6G"
print(main(key))
