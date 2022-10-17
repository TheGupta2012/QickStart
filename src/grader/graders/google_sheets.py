from __future__ import print_function

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime


def append_values(values):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # pylint: disable=maybe-no-member
    credentials = service_account.Credentials.from_service_account_file(
        "token.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    current_dateTime = str(datetime.now())
    print(current_dateTime)
    values.append(current_dateTime)
    try:
        service = build("sheets", "v4", credentials=credentials)

        body = {"values": [values]}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId="1rGx-dn1ULt4rLldpUKK94yz4F9FInD-l3xw5BHD0YJI",
                range="raw data",
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == "__main__":
    # Pass:  value_input_option and  _values
    append_values(["A", "B", "c", "d", "e"])
