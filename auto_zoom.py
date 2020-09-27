import pickle
import os.path
import googleapiclient.discovery as gapi
import google_auth_oauthlib.flow as gflow 
import google.auth.transport.requests as grequest

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1F0qfPUQzd63skDYFv9l1LHKrpIPYx6m2LFKHBqZPp-M'


class ScrapeDocs:
    def __init__(self):
        self.creds = None
        self.time_link_data = {}

    def auth(self):
        """
        Code for auth
        """
    
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:

            # this if statement is used if the credentials EXIST, but aren't valid
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(grequest.Request())

            # this is used if credentials DONT exist
            else:
                flow = gflow.InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES
                )

                # (probably a thing that gets get request params)
                self.creds = flow.run_local_server(port=0)
    
            # now that the credentials are fixed they are re-saved into the token.pickle file
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

    def read_table_data(self):
        """
        Code for reading doc
        """
        # send credentials into api(credentials contain ids like project id and client id)
        service = gapi.build('docs', 'v1', credentials=self.creds)
    
        # make request to doc with api and DOCUMENT_ID
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        all_table_rows = document['body']['content'][3]['table']['tableRows'][1: 7]

        for row in all_table_rows:
            # get cells of current row
            cells = row['tableCells']

            # get the first cell(time cell which contains period and time)
            time_cell = cells[0]

            # get the cells content
            cell_content = time_cell['content']

            # get the text of the part of the cell that we want
            meeting_time = cell_content[1]['paragraph']['elements'][0]['textRun']['content']

            meeting_time = meeting_time.strip()
            meeting_time = meeting_time.replace(' AM', '')
            meeting_time = meeting_time.replace(' ', '')

            dash_index = meeting_time.index('-')

            # get the last cell(zoom link for my class) and create links_array
            links_array = []
            link_cell = cells[5]

            # get the links in that cell
            links = link_cell['content']

            # go through all the links and form links_array
            for link in links:
                # get url
                url = link['paragraph']['elements'][0]['textRun']['textStyle']['link']['url']

                # strip url
                url.strip()
                url = url.replace(' ', '')

                # append url to links_array
                links_array.append(url)

            # fill up self.time_link_data
            new_meeting_time = meeting_time[0: dash_index]
            self.time_link_data[new_meeting_time + ":00"] = links_array
