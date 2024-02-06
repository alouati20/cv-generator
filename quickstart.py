from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
import json
from extractors.extract_certifications import extract_certifications
from extractors.extract_title import extract_title
from extractors.extract_formation import extract_formation
from extractors.extract_skills import extract_skills
from extractors.extract_frameworks import extract_frameworks
from extractors.extract_ide import extract_ide
from extractors.extract_tools import extract_tools



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

DOCUMENT_ID = "1EZe9hw2Sw0k1x42O1V1lnh3qBVMRLyecMa423-agG8g"


def main():
  """Shows basic usage of the Docs API.
  Prints the title of a sample document.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=8080)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    filename = 'demofile2.txt'

    service = build("docs", "v1", credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    f = open(filename, "w")
    #f.write(str(document))
    text_styles = extract_text_styles(document)
    format_content(str(text_styles))
    f.write(str(text_styles))
    f.close()
    
  except HttpError as err:
    print(err)




def extract_text_styles(json_content):
    text_styles = []

    def recursive_extract(element):
        if isinstance(element, dict):
            if "textRun" in element:
                text_run = element["textRun"]
                if "content" in text_run and text_run["content"] not in ["\n", " ", "\\x0b"]:
                    text_styles.append(text_run["content"].replace("\\x0b", ""))
            for key, value in element.items():
                recursive_extract(value)
        elif isinstance(element, list):
            for item in element:
                recursive_extract(item)

    recursive_extract(json_content)
    return text_styles

def format_content(text):
    # Clean the text
  cleaned_text = str(text).replace('\\x0b', '').replace('\\n', '').replace('\\t', '')

  # Organize the data into a dictionary
  data = {
      "title": extract_title(cleaned_text.split("'")),
      "certifications": extract_certifications(cleaned_text),
      "formation": extract_formation(cleaned_text),
      "skills": extract_skills(cleaned_text),
      "frameworks": extract_frameworks(cleaned_text),
      "ide": extract_ide(cleaned_text),
      "tools": extract_tools(cleaned_text),
      "autres": cleaned_text.split("Autres")[1].split("LANGUES")[0].strip(', '),
      "langues": cleaned_text.split("LANGUES")[1].split("ExpériencesProfessionnelles")[0].strip(', '),
      "experiences_professionnelles": cleaned_text.split("ExpériencesProfessionnelles")[1].split("Ayoub A.")[0].strip(', '),
  }

  print(cleaned_text.split("'")[1])

  # Write data to a JSON file
  with open('cv_data.json', 'w') as json_file:
      json.dump(data, json_file, ensure_ascii=False, indent=4)



if __name__ == "__main__":
  main()
# [END docs_quickstart]
