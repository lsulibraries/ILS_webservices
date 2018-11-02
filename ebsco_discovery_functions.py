import os
import json
import requests


class DiscoveryClient:
    def __init__(self):
        self.AuthToken = None
        self.AuthTimeout = None
        self.SessionToken = None
        self.Info = None

    def authenticate_user(self, UserId, Password):
        if not self.AuthToken and not self.AuthTimeout:
            url = 'https://eds-api.ebscohost.com/authservice/rest/uidauth'
            data = {'UserId': UserId,
                    'Password': Password,
                    'InterfaceId': 'WSapi', }
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json'}
            json_data = json.dumps(data)
            response = requests.post(url=url,
                                     data=json_data,
                                     headers=headers)
            response.raise_for_status()
            response_dict = json.loads(response.text)
            self.AuthToken = response_dict.get('AuthToken', None)
            self.AuthTimeout = response_dict.get('AuthTimeout', None)

    def create_session(self, Profile, Guest='n', Org=None):
        if not self.SessionToken:
            url = 'http://eds-api.ebscohost.com/edsapi/rest/createsession'
            data = {'Profile': Profile,
                    'Guest': Guest,
                    'Org': Org}
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'x-authenticationToken': self.AuthToken}
            json_data = json.dumps(data)
            response = requests.post(url=url,
                                     data=json_data,
                                     headers=headers)
            response.raise_for_status()

            req_results_dictionary = json.loads(response.text)
            self.SessionToken = req_results_dictionary.get('SessionToken', None)

    def end_session(self):
        url = 'http://eds-api.ebscohost.com//edsapi/rest/endsession'
        data = {'SessionToken': self.SessionToken}
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'x-authenticationToken': self.AuthToken}
        json_data = json.dumps(data)
        response = requests.post(url=url,
                                 data=json_data,
                                 headers=headers)
        response.raise_for_status()

    def show_info(self):
        if not self.Info:
            url = 'http://eds-api.ebscohost.com/edsapi/rest/info'
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json',
                       'x-authenticationToken': self.AuthToken,
                       'x-sessionToken': self.SessionToken}
            response = requests.get(url=url,
                                    headers=headers)
            self.Info = response.text

    def raw_search(self, query_string):
        '''Returns search results using an ampersand-separated URL parameter string.'''
        url = 'http://eds-api.ebscohost.com/edsapi/rest/Search?{}'.format(query_string)
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'x-authenticationToken': self.AuthToken,
                   'x-sessionToken': self.SessionToken}
        response = requests.get(url=url,
                                headers=headers)
        return response.text

    def basic_search(self, query):
        url = 'http://eds-api.ebscohost.com/edsapi/rest/search'
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'x-authenticationToken': self.AuthToken,
                   'x-sessionToken': self.SessionToken}
        search_text = {"SearchCriteria": {"Queries": [{
                                          "BooleanOperator": "And",
                                          "FieldCode": "IB",
                                          "Term": "{}".format(query)}, ],
                                          "SearchMode": "all",
                                          "IncludeFacets": "n",
                                          "Sort": "relevance",
                                          },
                       "RetrievalCriteria": {"View": "brief",
                                             "ResultsPerPage": 100,
                                             "PageNumber": 1,
                                             "Highlight": "n",
                                             },
                       "Actions": None
                       }
        search_json = json.dumps(search_text)
        response = requests.post(url=url,
                                 data=search_json,
                                 headers=headers)
        response.raise_for_status()
        return response.text

    def retrieve_record(self, accession_number, db_code, terms_to_highlight=None, preferred_format='ebook-epub'):
        '''Returns metadata (including abstract and full-text if applicable) for a single record.'''
        url = 'http://eds-api.ebscohost.com/edsapi/rest/retrieve'
        retrieve_dict = {'EbookPreferredFormat': preferred_format,
                         'HighlightTerms': terms_to_highlight,
                         'An': accession_number,
                         'DbId': db_code}
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'x-authenticationToken': self.AuthToken,
                   'x-sessionToken': self.SessionToken}
        retrieve_json = json.dumps(retrieve_dict)
        response = requests.get(url=url,
                                data=retrieve_json,
                                headers=headers)
        response.raise_for_status()
        return response.text


def read_credentials():
    with open('passwords.txt', 'r') as f:
        parsed_json = json.load(f)
        credentials = parsed_json['Discovery']
    return credentials["UserId"], credentials["Password"], credentials["Profile"]


def pretty_print(json_string):
    dictionary = json.loads(json_string, encoding='utf=8')
    return json.dumps(dictionary, ensure_ascii=True, indent=2)


def main(isbn):
    UserId, Password, Profile = read_credentials()
    client = DiscoveryClient()
    client.authenticate_user(UserId, Password)
    client.create_session(Profile)
    # client.show_info()
    a_search = client.basic_search(isbn)
    # a_result = json.loads(a_search)
    client.end_session()
    # print(pretty_print(a_search))
    return a_search


if __name__ == '__main__':
    a_search = main('0803741693')

    os.makedirs('output', exist_ok=True)
    with open(os.path.join('output', 'Discovery_search_for_a_novel_by_ISBN.txt'), 'w') as f:
        f.write(a_search)
