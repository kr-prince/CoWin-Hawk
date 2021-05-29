"""
module containing the utility functions for common use
"""

import json
import http.client
from datetime import datetime
from fake_useragent import UserAgent

# we need to create a default browser agent in case fake-agent fails
fallback_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
uagent = UserAgent(cache=False, use_cache_server=False, fallback=fallback_agent)

def get_headers():
    return {'Content-Type': 'application/json', 'Cache-Control': 'no-cache', 'User-Agent': uagent.random }

def custom_request(host, url, method='GET', urlParams=None, payload=None):
    """ This custom request functions abstracts a fake header creation and fetching the required data
        with error handling. It returs <data>,<'OK'> OR <None>,<Response Status> in case of error.
    """
    data, status, body = None, None, None
    headers = get_headers()
    
    if payload is not None:
        body = json.dumps(payload, indent=4)

    if urlParams is not None:
    	url = url.format(**urlParams)
    
    try:
        conn = http.client.HTTPSConnection(host)
        conn.request(method, url=url, headers=headers, body=body)
        resp = conn.getresponse()
        assert (resp.status == 200)
        data = json.loads(resp.read(), encoding='utf-8')
    except Exception as ex:
        data = None
    finally:
        status = resp.reason
    
    return data, status


def read_jsonFile(filePath):
	"""  Reads any json file and returns the result
	"""
	data = None
	with open(filePath, 'r') as file:
		data = json.loads(file.read())
	return data



