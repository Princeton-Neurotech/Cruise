"""
Recursively extracts the text from a Google Doc.
"""
from __future__ import print_function

import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import client,file,tools
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os 

SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
# 'https://docs.google.com/document/d/'
DOCUMENT_ID = '18rDVSBn23-Es6pF_iEsSiNWIrGumdPARHlbpmjsQtN4/edit'

def get_credentials():
    """Gets valid user credentials from storage.co
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth 2.0 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.jsoxwn', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    else:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
            print(text)
    return text

def main():
    print(0)
    """Uses the Docs API to print out the text of a document."""
    print(1)
    credentials = get_credentials()
    print(2)
    http = credentials.authorize(Http())
    print(3)
    docs_service = discovery.build('docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    print(4)
    doc = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    print(5)
    doc_content = doc.get('body').get('content')
    print(6)
    text = read_strucutural_elements(doc_content)
    print(text)
    with open("extracted.txt", "w") as text_file:
        text_file.write(text)

if __name__ == '__main__':
    print(33)
    main()
    print(42)