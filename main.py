import json
import urllib.request
import pandas
import os

# Some environment variables
from flatten_json import flatten




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
        return json.dump(api_call, file, indent=4)


def save_to_csv_not_flattened(filename, api_call):
    from flatten_json import flatten
    save_to_json('tmp', flatten(api_call))
    with open('tmp.json') as f:
        data = json.load(f)
    df = pandas.Series(data).to_frame()
    # save_to_csv_flattened(filename,api_call)
    # os.remove('tmp.json')
    return df.to_csv(filename + '.csv', index=True)


def save_to_csv_flattened(filename, api_call):
    save_to_json('tmp', api_call)
    df = (pandas.DataFrame(api_call))
    return df.to_csv(filename + '.csv', index=True)


def save_to_csv(filename, api_call):
    try:
        save_to_csv_not_flattened(filename, api_call)
        print('Not flattened - CSV created successfully')
        return
    except Exception as e:
        print('JSON not flattened, trying to flatten...')
        #print(e)
    try:
        save_to_csv_flattened(filename, api_call)
        print('Flattened - CSV created successfully')
        return
    except Exception as e:
        print('Error flattening JSON!')
        #print(e)

#a = generic_api_call('/api/v1/entity/services', False)
a = generic_api_call('/api/v1/problem/feed', False)

save_to_csv('example',a)

# save_to_csv_not_flattened('a', a)
#
# # from flatten_json import flatten
# # save_to_json('tmp', flatten(a))
# # print(a)
# # df = (pandas.DataFrame(api_call))
# # os.remove('tmp.json')
# # df.to_csv(filename + '.csv', index=True)

# a = generic_api_call('/api/v1/problem/feed?relativeTime=30mins', True)
# from flatten_json import flatten
# ab = save_to_json('tmp', flatten(a))
# with open('tmp.json') as f:
#   data = json.load(f)
# df = pandas.Series(data).to_frame()
# print(df)
# df.to_csv (r'a.csv', index=True)
