import os.path
import openai
import json
from openai import OpenAI
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

# The ID of a sample document.
# DOCUMENT_ID = "1oGKXThtAE_olF7r3QsvkcXRd-Tc8EVGl0Gt1WWM0TRs" #Achraf
DOCUMENT_ID = "18kduFE9o1lhzwx-8tyNVX5HuS-d4KvNGWRAbkzm7nvE"  # Ayoub


# DOCUMENT_ID = "1z29wC7G_6CjQQt-yN_2U_Jc4sFK-LIUOlJphRfLVxT0"  # Hassen
# DOCUMENT_ID = "1wYeLu0wuBTTpkVYXkvOSY7jqVj9Hn7tfoqgeoHtMpz4" #Boubaker


# DOCUMENT_ID = "1wYeLu0wuBTTpkVYXkvOSY7jqVj9Hn7tfoqgeoHtMpz4" #Boubaker

def authenticate_google_docs():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        creds = refresh_credentials(creds)
    return build("docs", "v1", credentials=creds)


def refresh_credentials(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=8080)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    return creds


def main():
    try:
        service = authenticate_google_docs()
        document = get_document_content(service)
        save_raw_text(document)
        text_content = extract_text_content(document)
        save_text_content(text_content)
        raw_text = ' '.join(text_content)

        openai.api_key = "sk-xxxx"

        json_schema = generate_json_schema()
        json_schema_str = json.dumps(json_schema, indent=2, ensure_ascii=False)

        prompt = f"Transform the following raw text into a JSON structure following the given schema:\n\n{raw_text}\n\nSchema:\n\n{json_schema_str}\nJSON OUTPUT:"

        client = OpenAI(api_key='sk-xxxx')

        response = generate_gpt3_response(client, prompt, text_content)

        save_generated_json(response)

    except HttpError as err:
        print(err)


def get_document_content(service):
    return service.documents().get(documentId=DOCUMENT_ID).execute()


def save_raw_text(document):
    with open("raw.txt", "w") as raw_doc:
        raw_doc.write(json.dumps(document))


def save_text_content(text_content):
    with open("demofile2.txt", "w") as f:
        f.write(json.dumps(text_content))


def generate_json_schema():
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
    return json_schema


def generate_gpt3_response(client, prompt, text_content):
    return client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system",
             "content": "You will be provided with unstructured data, and your task is to parse it into JSON format respecting a certain structure." + prompt},
            {"role": "user",
             "content": "This is the Resume in RAW Data, I want it to be in JSON structure. DO NOT REPEAT experiences, try to think how to split them" + str(
                 text_content)}
        ],
        temperature=0.4,
        top_p=1
    )


def save_generated_json(response):
    with open("genai.txt", "w") as genai:
        genai.write(str(response.choices[0].message.content))


def extract_text_content(json_content):
    text_content = []

    def recursive_extract(element):
        if isinstance(element, dict):
            if "textRun" in element:
                text_run = element["textRun"]
                if "content" in text_run and text_run["content"] not in ["\n", " ", "\\x0b"]:
                    text_content.append(text_run["content"].replace("\\x0b", ""))
            for key, value in element.items():
                recursive_extract(value)
        elif isinstance(element, list):
            for item in element:
                recursive_extract(item)

    recursive_extract(json_content)
    return text_content


if __name__ == "__main__":
    main()
