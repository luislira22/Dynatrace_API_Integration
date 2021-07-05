import csv
import json
import urllib.request

# Some environment variables
PROD_TENANT = ""
PROD_TENANT_API_TOKEN = ""


# Api call works in the format PROD_TENANT + {Endpoint} + {Authorization}

# Function that builds the API URL call
#
# - endpoint: The API endpoint /api/v1/problem/feed , for example
# - query_params_bool: Simple check to use ? or & in the API token parameter
def url_builder(endpoint, query_params_bool):
    if not query_params_bool:
        return PROD_TENANT + endpoint + '?Api-Token=' + PROD_TENANT_API_TOKEN
    else:
        return PROD_TENANT + endpoint + '&Api-Token=' + PROD_TENANT_API_TOKEN


# Function that builds the API URL call
#
# - endpoint: The API endpoint /api/v1/problem/feed , for example
# - query_params_bool: Simple check to use ? or & in the API token parameter
#
# Usage example:
# generic_api_call('/api/v1/problem/feed', False)
# generic_api_call('/api/v1/problem/feed?relativeTime=30mins', True)
def generic_api_call(endpoint, query_params_bool):
    with urllib.request.urlopen(url_builder(endpoint, query_params_bool)) as response:
        html = response.read()
        return json.loads(html.decode('utf-8'))


# Function that writes a JSON with the output from API call
#
# - filename: The name of the file to be written, please don't add the .json filetype as it is already included
# - api_call: The API call to be written to JSON
#
# Usage example:
# api = generic_api_call('/api/v1/problem/feed', False) - Create the api call
# save_to_json('Example', api) - Write the result into JSON
def save_to_json(filename, api_call):
    with open(filename + '.json', 'w') as file:
        json.dump(api_call, file, indent=4)
