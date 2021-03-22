"""
This is a script to wrap some (not all) of Trend Micro XDR/Vision One API.
WARNING : This is unsupported code. This is for demo and prototyping only
for more up to date documentation go to https://automation.trendmicro.com/xdr/home
Tested with XDR V2.0 API
David Girard, Trend Micro XDR Product Manager Team, February 14th 2021
"""

import requests
import shutil
import json
from datetime import datetime, timedelta
import time

class XDR:
    """
    please update regions dictionary as we add new regions
    """
    regions = {'us': 'https://api.xdr.trendmicro.com', 'eu': 'https://api.eu.xdr.trendmicro.com',
              'jp': 'https://api.xdr.trendmicro.co.jp', 'sg': 'https://api.sg.xdr.trendmicro.com',
              'au': 'https://api.au.xdr.trendmicro.com', 'in': 'https://api.in.xdr.trendmicro.com'}

    dlake = {'edr': 'endpointActivityData', 'msg': 'messageActivityData',
          'det': 'detections', 'net': 'networkActivityData'}

    products = {'apexonesaas': 'sao', 'cloudappsecurity': 'sca',
          'xdrsensor': 'xes', 'c1s': 'networkActivityData'}

    def __init__(self, region_code, xdr_token, appname='Custom app using XDR API'):
        # change your appname in the calling script
        try:
            self.url_base = self.regions[region_code]
            self.token = xdr_token
            self.header = {'Authorization': 'Bearer ' + xdr_token, 'Content-Type': 'application/json;charset=utf-8',
                           'User-Agent': appname}
        except Exception as err:
            msg = "XDR Class initialization error: " + str(err) + " region " + region_code
            print(msg)
            raise msg

    #Private wrapper for get requests
    def callapi(self, url_path, query_params):
        try:
            base = self.url_base
            r = requests.get(base + url_path, params=query_params, headers=self.header)
            print(r.status_code)
            if r.status_code != 200:
                raise Exception(str(r.status_code) + "  " + r.text)
            if 'application/json' in r.headers.get('Content-Type', ''):
                return json.dumps(r.json(), indent=4)
            else:
                return r.text

        except Exception as err:
            msg = "callapi : " + str(err) + " url: " + url_path + " params: " + json.dumps(query_params)
            print(msg)
            raise msg


    # wrapper for XDR post requests
    def callpostapi(self, url_path, query_params, body):
        try:
            base=self.url_base
            r = requests.post(base + url_path, params=query_params, headers=self.header, data=body)
            if r.status_code != 200:
                raise Exception(str(r.status_code) + "  " + r.text)
            if 'application/json' in r.headers.get('Content-Type', ''):
                return json.dumps(r.json(), indent=4)
            else:
                return r.text
        except Exception as err:
            msg = "callpostapi : " + str(err) + " url: " + url_path + " params: " + json.dumps(query_params) +\
                  " body: " + json.dumps(body)
            print(msg)
            raise msg

    #Private wrapper for put requests
    def callputapi(self, url_path, query_params, body):
        try:
            base = self.url_base
            r = requests.put(base + url_path, params=query_params, headers=self.header, data=body)
            print(r.status_code)
            if r.status_code != 200:
                raise Exception(str(r.status_code) + "  " + r.text)
            if 'application/json' in r.headers.get('Content-Type', ''):
                return json.dumps(r.json(), indent=4)
            else:
                return r.text

        except Exception as err:
            msg = "callputapi : " + str(err) + " url: " + url_path + " params: " + json.dumps(query_params) +\
                  " body: " + json.dumps(body)
            print(msg)
            raise msg


    #Private wrapper for get requests
    def calldeleteapi(self, url_path):
        try:
            base = self.url_base
            r = requests.delete(base + url_path, headers=self.header)
            print(r.status_code)
            if r.status_code != 200:
                raise Exception(str(r.status_code) + "  " + r.text)
            if 'application/json' in r.headers.get('Content-Type', ''):
                return json.dumps(r.json(), indent=4)
            else:
                return r.text

        except Exception as err:
            msg = "calldeleteapi : " + str(err) + " url: " + url_path
            print(msg)
            raise msg


    def convert_epochTodate(epoc):
        # Used to convert Suspicious Objects date-time in Epoc format to Human understandable dates
        # time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(1493286710))
        # Thu, 27 Apr 2017 05:51:50 +0000
        human_date = time.strftime("%b %d %Y %H:%M:%S", time.localtime(epoc))
        return human_date

    def convert_DateToEpoc(human):
        # Used to convert normal date-te into Epoc format
        # int(time.mktime(time.strptime('2000-01-01 12:34:00', '%Y-%m-%d %H:%M:%S'))) - time.timezone
        epoch = int(time.mktime(time.strptime(human, '%Y-%m-%d %H:%M:%S'))) - time.timezone
        return epoch


    def download_file(self, url, filename):
        try:
            with requests.get(url, stream=True) as r:
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

        except Exception as err:
            msg = "download_file : " + str(err) + " url: " + url + " filename "+ filename
            print(msg)
            raise msg


    def getComputerId(self, computerName):
        try:
            url_path = '/v2.0/xdr/eiqs/query/agentInfo'
            query_params = {}
            data = {
                "criteria":{
                    "field": "hostname",
                    "value": computerName
                }
            }
            body = json.dumps(data)
            print(body)
            result = self.callpostapi(url_path, query_params, body)
            return result
        except Exception as err:
            msg = "getComputerId : " + str(err) + " ComputerName: " + computerName
            print(msg)
            raise msg


    def getSingleEndPointInfos(self, computerId):
        try:
            url_path = '/v2.0/xdr/eiqs/query/endpointInfo'
            query_params = {}
            data = {"computerId": computerId}
            body = json.dumps(data)
            print(body)
            return self.callpostapi(url_path, query_params, body)

        except Exception as err:
            msg = "getSingleEndPointInfos : " + str(err) + " ComputerI: " + computerId
            print(msg)
            raise msg

    def getDownloadInfo(self, actionId):
        try:
            url_path = '/v2.0/xdr/response/downloadInfo'
            query_params = {'actionId': actionId}
            print(query_params)
            return self.callapi(url_path, query_params)
        except Exception as err:
            msg = "getDownloadInfo : " + str(err) + " actionId: " + actionId
            print(msg)
            raise msg

    def getResponseTaskDetails(self, actionId):
        try:
            url_path = '/v2.0/xdr/response/getTask'
            query_params = {'actionId': actionId}
            print(query_params)
            return self.callapi(url_path, query_params)
        except Exception as err:
            msg = "getResponseTaskDetails : " + str(err) + " actionId: " + actionId
            print(msg)
            raise msg

    def listResponseTask(self):
        try:
            url_path = '/v2.0/xdr/response/listTasks'
            query_params = {}
            return self.callapi(url_path, query_params)
        except Exception as err:
            msg = "listResponseTask : " + str(err)
            print(msg)
            raise msg

    def retrieve(self, task, interval):
        try:
            start = time.time()
            PERIOD_OF_TIME = 3600  # 60 minutes
            print("Start rerieving task: " + task + " " + str(start))
            while True:
                print(str(time.time()))
                res = self.getResponseTaskDetails(task)
                print(res)
                js = json.loads(res)
                #if "totalCount" in js['data']:
                status = js['data']['taskStatus']
                if status == 'success':
                    # download file and break
                    dl = self.getDownloadInfo(task)
                    print(dl)
                    js2 = json.loads(dl)
                    url = js2['data']['url']
                    filename = js2['data']['filename']
                    password = js2['data']['password']
                    self.download_file(url, filename)
                    with open(filename + '.txt', 'w') as f:
                        f.write(password)
                        f.close
                    print("Task completed with success. Look for file " + filename + " and password is in txt")
                    break
                elif status == 'failed':
                    msg = js['data']['error']['message']
                    print(task + " " + status + "\n" + msg)

                    with open(task + '.txt', 'w') as f:
                        f.write(task + " " + status + "\n" + msg)
                        f.close
                    break
                else:
                    print(status)
                if time.time() > start + PERIOD_OF_TIME:
                    print("60 minutes timeout for task " + task)
                    break
                time.sleep(interval * 60)# wait for x minutes

        except Exception as err:
            msg = "retreive : " + str(err) + " task: " + task + " interval: " + str(interval)
            print(msg)
            raise msg

    def collectFile(self, computerName, filepath, description="", interval=5):
        try:
            result = self.getComputerId(computerName)
            js = json.loads(result)
            errorcode = js['errorCode']
            if errorcode == 0:
                computerId = js['result']['computerId']
                result = self.getSingleEndPointInfos(computerId)
                js2 = json.loads(result)
                productCode = js2['result']['productCode']
            else:
                raise Exception("No computer Id for " & computerName)

            url_path = '/v2.0/xdr/response/collectFile'
            query_params = {}
            data = {
                    "description": description,
                    "productId": productCode,
                    "computerId": computerId,
                    "filePath": filepath
                    }
            body = json.dumps(data)
            print(body)
            result = self.callpostapi(url_path, query_params, body)
            print(result)

            return result

        except Exception as err:
            msg = "collectFile : " + str(err) + " computerName: " + computerName + " filePath: " + filepath
            print(msg)
            raise msg


    def createHook(self, urlhook, evtype="workbench"):
        try:
            url_path = '/v2.0/xdr/portal/notifications/webhooks'
            query_params = {}
            data = {
                "url": urlhook,
                "eventType": evtype,
                "headerData": {},
                "isVerifyingCertificate": False,
                "isGeneratingClientCert": False
            }
            body = json.dumps(data)
            print(body)
            result = self.callpostapi(url_path, query_params, body)
            print(result)

        except Exception as err:
            msg = "createHook : " + str(err) + " urlhook: " + urlhook + " evtype: " + evtype
            print(msg)
            raise msg


    def queryHooks(self):
        try:
            url_path = '/v2.0/xdr/portal/notifications/webhooks'
            query_params = {}
            result = self.callapi(url_path, query_params)

            print(result)

        except Exception as err:
            msg = "queryHook : " + str(err)
            print(msg)
            raise msg

    def updateHook(self, id, data={}):
        try:
            url_path = '/v2.0/xdr/portal/notifications/webhooks/{webhook_id}'
            url_path = url_path.format(**{'webhook_id': id})

            query_params = {}
            data = {
                "headerData": data,
                "isVerifyingCertificate": False,
                "isGeneratingClientCert": False
            }
            body = json.dumps(data)
            print(body)
            result = self.callputapi(url_path, query_params, body)
            print(result)

        except Exception as err:
            msg = "updateHook : " + str(err) + " id: " + str(id)
            print(msg)
            raise msg


    def deleteHook(self, id):
        try:
            url_path = '/v2.0/xdr/portal/notifications/webhooks/{webhook_id}'
            url_path = url_path.format(**{'webhook_id': id})
            result = self.calldeleteapi(url_path)
            print(result)

        except Exception as err:
            msg = "deleteHook : " + str(err) + " id: " + str(id)
            print(msg)
            raise msg


    def triggerHook(self, evType="workbench", evdata={}):
        try:
            url_path = '/v2.0/xdr/portal/notifications/webhooks/triggerRequest'
            query_params = {}
            data = {
                "eventType": evType,
                "eventData": evdata
            }
            body = json.dumps(data)
            print(body)
            result = self.callpostapi(url_path, query_params, body)
            print(result)

        except Exception as err:
            msg = "triggerHook : " + str(err) + " evType: " + evType
            print(msg)
            raise msg


    # Search data lakes
    def search(self, ifrom, ito, source, query, offset=0):
        try:
            url_path = '/v2.0/xdr/search/data'
            query_params = {}
            body = {
                "offset": offset,
                "from": ifrom,
                "to": ito,
                "source": source,
                "query": query
                }
            b = json.dumps(body)
            return self.callpostapi(url_path, query_params, b)

        except Exception as err:
            print("search : " + source + '   ' + query + " " + str(err))
            msg = "search : " + str(err) + " query: " + query  + " query: " + query
            print(msg)
            raise msg


    def return_iso_dates(self, daystosubstract):
        try:
            days_to_substract = daystosubstract
            my_date = datetime.now() - timedelta(days=days_to_substract)
            my_date = my_date.strftime("%Y-%m-%d %H:%M:%S")
            istart = self.convert_DateToEpoc(my_date)
            my_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            iEnd = self.convert_DateToEpoc(my_end)
            return istart, iEnd

        except Exception as err:
            print("return_iso_dates : " + str(daystosubstract) + '   ' + str(err))
            exit(-1)

"""
    def getOAT(self, start, end, size=200, risk):
        try:


        except Exception as err:
            print("collectFile : " + str(err))
            exit(-1)
"""