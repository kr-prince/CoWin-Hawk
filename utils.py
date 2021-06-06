"""
module containing the utility functions for common use
"""

import json
import sys
import time
import http.client
from datetime import datetime
from fake_useragent import UserAgent
from dbUtils import setMonitoringQuerys, getQuerysByStatus, setNotifiedQuerys

# we need to create a default browser agent in case fake-agent fails
fallback_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
uagent = UserAgent(fallback=fallback_agent, cache=False, use_cache_server=False)


def custom_request(host, url, method='GET', urlParams=None, payload=None, headers=None):
    """ This custom request functions abstracts a fake header creation and fetching the required data
        with error handling. It returs <data>,<'OK'> OR <None>,<Response Status> in case of error.
    """
    data, status, body = None, None, None
    
    # if a custom header is sent we only add the fake-agent else we create a generic header
    if headers is None:
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'User-Agent': uagent.random
        }
    else:
        headers['User-Agent'] = uagent.random
    
    if payload is not None:
        body = json.dumps(payload, indent=4)

    if urlParams is not None:
    	url = url.format(**urlParams)
    
    print("host, url, urlParams", host, url, urlParams)
    sys.stdout.flush()
    
    try:
        conn = http.client.HTTPSConnection(host)
        conn.request(method, url=url, headers=headers, body=body)
        resp = conn.getresponse()
        assert (resp.status == 200)
        data = json.loads(resp.read(), encoding='utf-8')
    except Exception as ex:
        print(ex)
        sys.stdout.flush()
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


# Template of SMS to be sent
text_template="""{date}
{min_age}+,D1:{dose1},D2:{dose2},{vaccine}
{center_name}
{center_address}
{district_name}
"""


def send_sms(message, phone, fast2sms_key):
    headers = {
        "authorization":fast2sms_key,
        "Content-Type":"application/json"
    }
    
    body = { "route" : "v3", "sender_id" : "TXTIND", "message" : message.strip(), "language" : "english",
                "flash" : 0, "numbers" : phone.strip(),
           }
    
    data, status = custom_request('www.fast2sms.com', '/dev/bulkV2', 'POST', payload=body, headers=headers)
    if data is not None:
        return data['message'][0]
    else:
        return status


def start_hawk(cowin_config):
    print("coming this side of the code ....")
    sys.stdout.flush()
    start_hour = 0
    while True:
        # Get todays date and start time
        from_date = datetime.strftime(datetime.today(), '%d-%m-%Y')
        start_time = datetime.now()

        # First convert all the newly 'Accepted' to 'Monitoring'
        setMonitoringQuerys()

        # Get all the queries having status 'Monitoring'
        for query in getQuerysByStatus('Monitoring'):
            phone, pindistId, distName = query[2], query[3], None
            data = None
            if query[4]=='NA' and len(pindistId)>=6:
                # Query is by Pincode
                distName = query[3]
                data, status = custom_request(cowin_config['cowin_host'],
                        cowin_config['url_calendarByPin'].format(pincode=pindistId, date=from_date))
            else:
                # Query is by District Id
                distName = query[4]
                data, status = custom_request(cowin_config['cowin_host'],
                        cowin_config['url_calendarByDist'].format(district_id=pindistId, date=from_date))

            if data is not None:
                for center in data['centers']:
                    for session in center['sessions']:
                        if session['available_capacity'] > 0:
                            # we found a slot.! Lets inform user
                            sms_body = text_template.format(date=session.get('date',''), 
                                        min_age=session.get('min_age_limit','NA'),
                                        dose1=session.get('available_capacity_dose1','NA'),
                                        dose2=session.get('available_capacity_dose2','NA'),
                                        vaccine=session.get('vaccine','NA'), center_name=center.get('name', 'NA'), 
                                        center_address=center.get('address', 'NA'),
                                        district_name=center.get('district_name', 'NA'))

                            sms_status = send_sms(sms_body, phone, cowin_config['fast2sms_key'])
                            setNotifiedQuerys(query[0], sms_body+'  - SMS: '+sms_status)
                            print("({0},{1}) Notified. SMS Status : {2}".format(phone, distName, sms_status))
            else:
                print("({0},{1})   Error: {2}".format(phone, distName, status))

        seconds = (datetime.now() - start_time).seconds
        # We pause for 5 seconds before re-searching, or less if we are taking more time to process a batch
        time.sleep(max(0, 5-seconds))
        start_hour += (datetime.now() - start_time).seconds
        if start_hour >= 1800:
            # We print the monitor live after around 30 mins
            print("CoWin-Hawk monitor live..")
            start_hour -= start_hour
        