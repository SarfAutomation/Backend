from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
import json

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def authorize_service_account():
    credentials = json.loads(os.getenv("GOOGLE_CLOUD_CREDENTIALS"))
    service_account_auth = Credentials.from_service_account_info(
        credentials, scopes=SCOPES
    )
    return service_account_auth


def give_permission(sheet_id, email):
    service = build("drive", "v3", credentials=authorize_service_account())
    service.permissions().create(
        fileId=sheet_id,
        body={
            "type": "user",
            "role": "writer",
            "emailAddress": email,
        },
        fields="id",
    ).execute()


async def create_and_share_sheet(sheet_name, email, question):
    auth = authorize_service_account()
    service = build("sheets", "v4", credentials=auth)

    sheet = (
        service.spreadsheets()
        .create(body={"properties": {"title": sheet_name}})
        .execute()
    )

    sheet_id = sheet["spreadsheetId"]
    print(
        f'Created Sheet "{sheet_name}" with ID: {sheet_id}, and the url is https://docs.google.com/spreadsheets/d/{sheet_id}'
    )

    give_permission(sheet_id, email)
    give_permission(sheet_id, "hugozhan0802@gmail.com")
    give_permission(sheet_id, "dyllanliuuu@gmail.com")

    print(f'Sheet "{sheet_name}" shared with {email} as an editor.')

    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range="A1",
        valueInputOption="RAW",
        body={"values": [[question]]},
    ).execute()

    print(f'Question "{question}" added to Sheet "{sheet_name}".')

    return sheet_id


def sheet_exists(spreadsheet_id, sheet_title):
    service = build("sheets", "v4", credentials=authorize_service_account())
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get("sheets", "")

    for sheet in sheets:
        if sheet["properties"]["title"] == sheet_title:
            return True
    return False


def create_new_sheet_if_not_exists(spreadsheet_id, sheet_title):
    service = build("sheets", "v4", credentials=authorize_service_account())

    if not sheet_exists(spreadsheet_id, sheet_title):
        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": sheet_title,
                        }
                    }
                }
            ]
        }

        response = (
            service.spreadsheets()
            .batchUpdate(
                spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body
            )
            .execute()
        )

        print(f"Created new sheet with title: {sheet_title}")
    else:
        print(f"Sheet '{sheet_title}' already exists.")


def add_to_google_sheet(row_data, sheet_id):
    service = build("sheets", "v4", credentials=authorize_service_account())
    sheet_number = 1

    while True:
        create_new_sheet_if_not_exists(sheet_id, f"Sheet{sheet_number}")
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=sheet_id,
                range=f"Sheet{sheet_number}!A1",
                valueInputOption="USER_ENTERED",
                body={
                    "values": [
                        ["=COUNTA(FILTER(B:B, LEN(TRIM(B:B))>=0))"],
                    ]
                },
            )
            .execute()
        )
        response = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=f"Sheet{sheet_number}!A1")
            .execute()
        )

        print(response.get("values", []))

        row_number = int(response.get("values", [])[0][0]) + 3
        if row_number <= 1000:
            break
        sheet_number += 1

    update_range = f"Sheet{sheet_number}!A{row_number}"
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=update_range,
        valueInputOption="RAW",
        body={"values": [row_data]},
    ).execute()

    print(f"Row added to Sheet ID {sheet_id} at row {row_number}")


def update_google_sheet(row_data, sheet_id):
    service = build("sheets", "v4", credentials=authorize_service_account())
    sheet_number = 1
    found = False

    while True:
        sheet_name = f"Sheet{sheet_number}"
        create_new_sheet_if_not_exists(sheet_id, sheet_name)

        # Fetch all identifiers in column A of the current sheet to find the matching row
        response = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=f"{sheet_name}!A:A")
            .execute()
        )

        values = response.get("values", [])
        row_number = None

        # Search for the identifier
        for i, value in enumerate(values, start=1):
            if value and value[0] == row_data[0]:
                row_number = i
                found = True
                break

        if found:
            break
        elif len(values) >= 1000:
            sheet_number += 1
        else:
            print("Identifier not found in any existing rows.")
            return

    # Update the found row with new data
    update_range = f"{sheet_name}!A{row_number}:F{row_number}"
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=update_range,
        valueInputOption="USER_ENTERED",
        body={"values": [row_data]},
    ).execute()

    print(f"Row {row_number} in {sheet_name} updated with ID {sheet_id}")


def get_google_sheet_rows(sheet_id, sheet_number):
    service = build("sheets", "v4", credentials=authorize_service_account())
    sheet_name = f"Sheet{sheet_number}"
    create_new_sheet_if_not_exists(sheet_id, sheet_name)

    # Fetch all identifiers in column A of the current sheet to find the matching row
    response = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=f"{sheet_name}!A:D")
        .execute()
    )

    values = response.get("values", [])
    return values[2:]


# sheet_id = "1l0KwmsVWmLoIEzXhQHjX6n0aOYqpY60uHmibqMHLvZc"
# add_to_google_sheet(["Data", "More Data"], sheet_id)
