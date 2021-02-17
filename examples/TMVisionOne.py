"""
This is a script to wrap some (not all) of Trend Micro XDR/Vision One API.
WARNING : This is unsupported code. This is for demo and prototyping only
for more up to date documentation go to https://automation.trendmicro.com/xdr/home
Tested with XDR V2.0 API D. Girard, Trend Micro XDR Product Manager Team, February 14th 2021
"""

import requests
import shutil
import json
import time

class XDR:
    """
    please update regions dictionary as we add new regions
    """
    regions = {'us': 'https://api.xdr.trendmicro.com', 'eu': 'https://api.eu.xdr.trendmicro.com',
              'jp': 'https://api.xdr.trendmicro.co.jp', 'sg': 'https://api.sg.xdr.trendmicro.com',
              'au': 'https://api.au.xdr.trendmicro.com', 'in': 'https://api.in.xdr.trendmicro.com'}

    def __init__(self, region_code, xdr_token):
        try:
            self.url_base = self.regions[region_code]
            self.token = xdr_token
            self.header = {'Authorization': 'Bearer ' + xdr_token, 'Content-Type': 'application/json;charset=utf-8'}
        except Exception as err:
            print("XDR Class initialization eror: " + str(err))
            exit(-1)

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
            print("callapi : " + str(err))
            exit(-1)

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
            print("callpostapi : " + str(err))
            exit(-1)

    def download_file(self, url, filename):
        try:
            with requests.get(url, stream=True) as r:
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

        except Exception as err:
            print("download_file : " + str(err))
            print("URL was : " + url)

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
            print("getComputerId : " + str(err))
            exit(-1)

    def getSingleEndPointInfos(self, computerId):
        try:
            url_path = '/v2.0/xdr/eiqs/query/endpointInfo'
            query_params = {}
            data = {"computerId": computerId}
            body = json.dumps(data)
            print(body)
            return self.callpostapi(url_path, query_params, body)

        except Exception as err:
            print("getSingleEndPointInfos : " + str(err))
            exit(-1)

    def getDownloadInfo(self, actionId):
        try:
            url_path = '/v2.0/xdr/response/downloadInfo'
            query_params = {'actionId': actionId}
            print(query_params)
            return self.callapi(url_path, query_params)
        except Exception as err:
            print("getDownloadInfo : " + str(err))
            exit(-1)

    def getResponseTaskDetails(self, actionId):
        try:
            url_path = '/v2.0/xdr/response/getTask'
            query_params = {'actionId': actionId}
            print(query_params)
            return self.callapi(url_path, query_params)
        except Exception as err:
            print("getResponseTaskDetails : " + str(err))
            exit(-1)

    def listResponseTask(self):
        try:
            url_path = '/v2.0/xdr/response/listTasks'
            query_params = {}
            return self.callapi(url_path, query_params)
        except Exception as err:
            print("listResponseTask : " + str(err))
            exit(-1)

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
            print("retrieve : " + str(err))
            exit(-1)

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
            print("collectFile : " + str(err))
            exit(-1)
