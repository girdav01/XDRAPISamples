# This is a generic test script for XDR Automation API's
# for more up to date documentation go to https://automation.trendmicro.com/xdr/home
# Tested with XDR V2.0 API D. Girard, Trend Micro XDR Product Manager Team, November 2nd 2020
import requests
import json
import tmconfig  #tmconfig.py with your api keys

url_base = tmconfig.region['us'] #use the right region

# Get your token from your XDR Administrator, in XDR Console under Account Management.
# You can also use the key for Splunk integration in XDr under Alert Notifications, it will work for most
token = tmconfig.xdr_token
header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}

def callapi(url_path, query_params):
    r = requests.get(url_base + url_path, params=query_params, headers=header)
    print(r.status_code)
    if 'application/json' in r.headers.get('Content-Type', ''):
        return json.dumps(r.json(), indent=4)
    else:
        return r.text

def listroles():
    url_path = '/v2.0/xdr/portal/accounts/roles'
    query_params = {}
    return callapi(url_path, query_params)

def models():
    url_path = '/v2.0/xdr/models'
    query_params = {}
    return callapi(url_path, query_params)


def listintel():
    url_path = '/v2.0/xdr/threatintel/reports'
    # Query parameters status string Enum: "all" "expire" "active"
    query_params = {'status': 'all'}
    return callapi(url_path, query_params)

def listWorkbench(strstart, strend,intoffset, intlimit):
    url_path = '/v2.0/siem/events'
    query_params = {'source': 'all', 'startDateTime': strstart,
                    'endDateTime': strend,
                    'sortBy': '-createdTime',
                    'offset': intoffset,
                    'limit': intlimit }
    return callapi(url_path, query_params)


def getWorkbench(id):
    url_path = '/v2.0/xdr/workbench/workbenches/{workbenchId}'
    url_path = url_path.format(**{'workbenchId': id})
    query_params = {}
    return callapi(url_path, query_params)

def deleteaccount(email):
    url_path = '/v2.0/xdr/portal/accounts/{email}'
    url_path = url_path.format(**{'email': email})
    query_params = {}
    #headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}
    r = requests.delete(url_base + url_path, params=query_params, headers=header)
    print(r.status_code)
    if 'application/json' in r.headers.get('Content-Type', ''):
        print(json.dumps(r.json(), indent=4))
    else:
        print(r.text)

def createaccount(email, name):
    # note that we don't test other roles than Analyst and we hardcoded type 0 = local
    #  and we hardcoded autorization 3 (UI + API)
    url_path = '/v2.0/xdr/portal/accounts/{email}'
    url_path = url_path.format(**{'email': email})
    query_params = {}
    body = \
    {
        'type': 0,
        'name': name,
        'enabled': True,
        'description': 'Test account',
        'token': token,
        'authorization': 3,
        'role': 'Analyst'
    }

    body=json.dumps(body)
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}
    r = requests.post(url_base + url_path, params=query_params, headers=header, data=body)
    print(r.status_code)
    if 'application/json' in r.headers.get('Content-Type', ''):
        print(json.dumps(r.json(), indent=4))
    else:
        print(r.text)


print("XDR API demo script")
print("===================")
print("List Roles")
print(listroles())
print("END List Roles")
print("===================")
print("Test Delete and Create Account")
email = 'email@email.com'
name = 'test analyst'
#print(deleteaccount(email))
#print(createaccount(email, name))
print("===================")
print("List detection models")
print(models())
print("END List detection models")

print("===================")
print("List Intelligence Reports")
print(listintel())
print("END List Intelligence Reports")
print("===================")

print("List Workbench")
offset = 0
limit = 50
lstWorkbenches = listWorkbench('2020-08-29T13:52:30.000Z', '2020-10-14T13:52:40.000Z', offset, limit)

print(lstWorkbenches)

json2 = json.loads(lstWorkbenches)
if "totalCount" in json2['data']:
    print("Key exist in JSON data")
    totalcount = json2['data']['totalCount']
    print(totalcount)
    count_all = int(totalcount)
    countpages = int(float(count_all + (limit - 1)) / float(limit))
    #if int(totalcount)> limit :
    #workbencheIds = json2['data']['workbenchRecords'][0]['workbenchId']
    #print(workbencheIds)
    x=0
    for sub in json2['data']['workbenchRecords']:
        print(getWorkbench(sub['workbenchId']))
        print(str(x))
        x=x+1


print("END List Workbench")
print("===================")
#print("Get Workbench Id : WB-10797-20201006-0000")
#print(getWorkbench('WB-10797-20201006-0000'))
#print("===================")

