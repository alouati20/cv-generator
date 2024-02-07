# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START docs_quickstart]
import os.path
import openai
from openai import OpenAI

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

# The ID of a sample document.
DOCUMENT_ID = "1oGKXThtAE_olF7r3QsvkcXRd-Tc8EVGl0Gt1WWM0TRs"


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
        service = build("docs", "v1", credentials=creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        rawDoc = open("raw.txt", "w")
        rawDoc.write(str(document))
        rawDoc.close()
        f = open("demofile2.txt", "w")
        #f.write(str(document))
        text_styles = extract_text_styles(document)
        f.write(str(text_styles))
        f.close()




        # Set your OpenAI GPT-3 API key
        #openai.api_key = "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"

        # Define the raw text
        raw_text = text_styles

        # Concatenate the raw text into a single string
        input_text = ' '.join(raw_text)

        # Define the JSON schema
        json_schema = {
            "$ref": "#/definitions/CV",
            "definitions": {
                "CV": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "minLength": 1
                        },
                        "user": {
                            "type": "string"
                        },
                        "type": {
                            "anyOf": [
                                {
                                    "type": "string",
                                    "const": "original"
                                },
                                {
                                    "type": "string",
                                    "const": "duplicated"
                                },
                                {
                                    "type": "string"
                                }
                            ]
                        },
                        "languagesAdditionalText": {
                            "type": "string"
                        },
                        "header": {
                            "type": "object",
                            "properties": {
                                "civility": {
                                    "type": "string"
                                },
                                "firstName": {
                                    "type": "string",
                                    "minLength": 1
                                },
                                "lastName": {
                                    "type": "string",
                                    "minLength": 1
                                },
                                "title": {
                                    "type": "string",
                                    "minLength": 1
                                },
                                "expertise": {
                                    "type": "string"
                                },
                                "tags": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "maxItems": 2
                                },
                                "projectNumber": {
                                    "type": "string"
                                },
                                "experiencesYears": {
                                    "type": "string"
                                },
                                "description": {
                                    "type": "string",
                                    "maxLength": 350
                                },
                                "legalEntity": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "civility",
                                "firstName",
                                "lastName",
                                "title",
                                "expertise",
                                "tags",
                                "projectNumber",
                                "experiencesYears",
                                "description",
                                "legalEntity"
                            ],
                            "additionalProperties": False
                        },
                        "languages": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "label": {
                                        "type": "string"
                                    },
                                    "name": {
                                        "type": "string"
                                    },
                                    "level": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "name",
                                    "level"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "technos": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "anyOf": [
                                            {
                                                "type": "string"
                                            },
                                            {
                                                "type": "string",
                                                "const": "other"
                                            }
                                        ]
                                    },
                                    "skills": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        }
                                    },
                                    "label": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "type",
                                    "skills"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "conferences": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "participation": {
                                        "type": "string"
                                    },
                                    "name": {
                                        "type": "string"
                                    },
                                    "description": {
                                        "type": "string"
                                    },
                                    "link": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "participation",
                                    "name",
                                    "description",
                                    "link"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "trainings": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "date": {
                                        "type": "string"
                                    },
                                    "name": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "date",
                                    "name"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "degrees": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "date": {
                                        "type": "string"
                                    },
                                    "title": {
                                        "type": "string"
                                    },
                                    "school": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "date",
                                    "title"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "experiences": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "company": {
                                        "type": "string"
                                    },
                                    "startDate": {
                                        "type": [
                                            "number",
                                            "string"
                                        ]
                                    },
                                    "endDate": {
                                        "type": [
                                            "number",
                                            "string"
                                        ]
                                    },
                                    "jobPosition": {
                                        "type": "string"
                                    },
                                    "missionSummary": {
                                        "type": "string"
                                    },
                                    "achievements": {},
                                    "teamSize": {
                                        "type": [
                                            "number",
                                            "string"
                                        ]
                                    },
                                    "teamProfiles": {},
                                    "technologies": {},
                                    "toolsAndMethodolgies": {}
                                },
                                "required": [
                                    "company",
                                    "startDate",
                                    "endDate",
                                    "jobPosition",
                                    "missionSummary",
                                    "teamSize"
                                ],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": [
                        "title",
                        "user",
                        "type",
                        "languagesAdditionalText",
                        "createdDate",
                        "updatedDate",
                        "createdBy",
                        "updatedBy",
                        "header",
                        "languages",
                        "communities",
                        "technos",
                        "conferences",
                        "trainings",
                        "degrees",
                        "experiences"
                    ],
                    "additionalProperties": False
                }
            },
            "$schema": "http://json-schema.org/draft-07/schema#"
        }

        # Convert the JSON schema to a string
        json_schema_str = json.dumps(json_schema, indent=2, ensure_ascii=False)

        # Create a prompt for GPT-3 to generate JSON structure
        prompt = f"Transform the following raw text into a JSON structure following the given schema:\n\n{input_text}\n\nSchema:\n\n{json_schema_str}\nJSON OUTPUT:"


        client = OpenAI(api_key='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')
        #OpenAI.api_key = os.getenv('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')

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with unstructured data, and your task is to parse it into JSON format respecting a certain structure." + prompt
                },
                {
                    "role": "user",
                    "content": "This is the Resume in RAW Data, I want to to be in JSON structure. DO NOT REPEAT experiences, try to think how to split them" + str(text_styles)
                }
            ],
            temperature=0.4,
            top_p=1
        )

        # Extract the generated JSON structure from GPT-3 response
        #generated_json = completion["choices"][0]["text"].strip()

        genai = open("genai.txt", "w")
        genai.write(str(response.choices[0].message.content))
        genai.close()

        print(f"The title of the document is: {document}")
    except HttpError as err:
        print(err)



import json

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


#----------------------------------------------------------






if __name__ == "__main__":
    main()
# [END docs_quickstart]
