# for more up to date documentation go to https://automation.trendmicro.com/xdr/home
# Tested with XDR V2.0 API, Trend Micro XDR Product Manager Team, November 2nd 2020
import requests
import json
import tmconfig  # tmconfig.py with your api keys / tokens

url_base = tmconfig.region['us'] # use the right region
token = tmconfig.xdr_token # get your account API token

header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}

# wrapper for XDR get requests
def callgetapi(url_path, query_params):
    try:
        r = requests.get(url_base + url_path, params=query_params, headers=header)
        # print(r.status_code)
        if r.status_code != 200:
            raise Exception(str(r.status_code) + "  " + r.text)

        if 'application/json' in r.headers.get('Content-Type', ''):
            return json.dumps(r.json(), indent=4)
        else:
            return r.text

    except Exception as err:
        print("callgetapi : " + str(err))
        exit(-1)


# Get a workbench detail
def getWorkbench(id):
    try:
        url_path = '/v2.0/xdr/workbench/workbenches/{workbenchId}'
        url_path = url_path.format(**{'workbenchId': id})
        query_params = {}
        return callgetapi(url_path, query_params)

    except Exception as err:
        print("getWorkbench : " + id + " " + str(err))
        exit(-1)


# Get a list of workbenches ids for a time range
def listWorkbenchIds(strstart, strend,intoffset, intlimit):
    # lstWorkbenches = listWorkbenchIds('2020-08-29T13:52:30.000Z', '2020-10-14T13:52:40.000Z', offset, limit)
    try:
        ids = []
        url_path = '/v2.0/siem/events'
        query_params = {'source': 'all', 'startDateTime': strstart,
                        'endDateTime': strend,
                        'sortBy': '-createdTime',
                        'offset': intoffset,
                        'limit': intlimit }
        json2 = json.loads(callgetapi(url_path, query_params))
        if "totalCount" in json2['data']:
            #print("Key exist in JSON data")
            totalcount = json2['data']['totalCount']
            count_all = int(totalcount)
            countpages = int(float(count_all + (intlimit - 1)) / float(intlimit))
            x = 0
            for page in range(1,countpages + 1):
                for sub in json2['data']['workbenchRecords']:
                    # print(getWorkbench(sub['workbenchId']))
                    ids.append(sub['workbenchId'])
                    #print(str(x))
                    x = x + 1
                query_params = {'source': 'all', 'startDateTime': strstart,
                                'endDateTime': strend,
                                'sortBy': '-createdTime',
                                'offset': x,
                                'limit': intlimit}
                json2 = json.loads(callgetapi(url_path, query_params))
            return ids

    except Exception as err:
        print("listWorkbenchIds from " + strstart + " to " + strend + '  ' + str(err))
        exit(-1)

# Get a list of workbenches for a time range
def listWorkbenches(strstart, strend,intoffset, intlimit):
    #lstWorkbenches = listWorkbenches('2020-08-29T13:52:30.000Z', '2020-10-14T13:52:40.000Z', offset, limit)
    try:
        wb = []
        url_path = '/v2.0/siem/events'
        # todo add filters on investigationStatus
        # arraynull
        # If All status is selected, leave it as null; otherwise, put an array of integer(s); [0]: New;
        # [1]: In Progress; [2]: Resolved: True Positive; [3]: Resolved: False Positive
        query_params = {'source': 'all', 'startDateTime': strstart,
                        'endDateTime': strend,
                        'sortBy': '-createdTime',
                        'offset': intoffset,
                        'limit': intlimit }
        json2 = json.loads(callgetapi(url_path, query_params))
        if "totalCount" in json2['data']:
            #print("Key exist in JSON data")
            totalcount = json2['data']['totalCount']
            count_all = int(totalcount)
            countpages = int(float(count_all + (intlimit - 1)) / float(intlimit))
            x = 0
            for page in range(1,countpages + 1):
                wb.append(json2)
                x = x + intoffset
                query_params = {'source': 'all', 'startDateTime': strstart,
                                'endDateTime': strend,
                                'sortBy': '-createdTime',
                                'offset': x,
                                'limit': intlimit}
                json2 = json.loads(callgetapi(url_path, query_params))
            return wb

    except Exception as err:
        print("listWorkbenches from " + strstart + " to " + strend + '  ' + str(err))
        exit(-1)

# Test #1
print("List Workbench ID's ")
offset = 0
limit = 50
lstWorkbenches = listWorkbenchIds('2020-08-29T13:52:30.000Z', '2020-10-14T13:52:40.000Z', offset, limit)
print(str(len(lstWorkbenches)))
print(lstWorkbenches)

# Test #2
print("List Workbenches by going through WB Id list")
for wb in lstWorkbenches:
    print(getWorkbench(wb))

# test #3
print("Test Call Workbenches List")
lstWorkbenches = listWorkbenches('2020-08-29T13:52:30.000Z', '2020-10-14T13:52:40.000Z', offset, 25)
print(str(len(lstWorkbenches)))
print(lstWorkbenches)
for wb in lstWorkbenches:
    print(json.dumps(wb, indent=4))