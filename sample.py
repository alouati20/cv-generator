from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load credentials from the downloaded JSON file
credentials = Credentials.from_service_account_file('credentials.json')

# Build the service object for interacting with the Google Docs API
service = build('docs', 'v1', credentials=credentials)

# Call the documents.list method to retrieve a list of documents
document_list = service.documents().list().execute()

document2 = service.documents().get(documentId="1pCNwqLtLLBptZ6qnOD4NWfu7whfREqdSO4ylxP5NU6M").execute()
print(f"The title of the document is: {document2.get('title')}")

# Extract titles from the document list
titles = [document['title'] for document in document_list.get('documents', [])]

# Print the titles
for title in titles:
    print(title)