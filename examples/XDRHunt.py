# for more up to date documentation go to https://automation.trendmicro.com/xdr/home
# Tested with XDR V2.0 API, Trend Micro XDR Product Manager Team, November 2020
import argparse
import requests
import json
import tmconfig  # tmconfig.py with your api keys / token
from datetime import datetime, timedelta
import time

url_base = tmconfig.region['us'] # use the right region
token = tmconfig.xdr_token # get your account API token

header = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}

dl = {'edr': 'endpointActivityData', 'msg': 'messageActivityData',
          'det': 'detections', 'net': 'networkActivityData'}

def convert_epochTodate(epoc):
    #Used to convert Suspicious Objects date-time in Epoc format to Human understandable dates
    #time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(1493286710))
    #Thu, 27 Apr 2017 05:51:50 +0000
    human_date = time.strftime("%b %d %Y %H:%M:%S", time.localtime(epoc))
    return human_date

def convert_DateToEpoc(human):
    #Used to convert normal date-te into Epoc format
    #int(time.mktime(time.strptime('2000-01-01 12:34:00', '%Y-%m-%d %H:%M:%S'))) - time.timezone
    epoch = int(time.mktime(time.strptime(human, '%Y-%m-%d %H:%M:%S'))) - time.timezone
    return epoch


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


# wrapper for XDR post requests
def callpostapi(url_path, query_params, body):
    try:
        r = requests.post(url_base + url_path, params=query_params, headers=header, data=body)
        if r.status_code != 200:
            raise Exception(str(r.status_code) + "  " + r.text)

        if 'application/json' in r.headers.get('Content-Type', ''):
            return json.dumps(r.json(), indent=4)
        else:
            return r.text

    except Exception as err:
        print("callpostapi : " + str(err))
        exit(-1)


# Get a workbench detail
def search(ifrom, ito, source, query):
    try:
        url_path = '/v2.0/xdr/search/data'
        query_params = {}
        body = {
            "from": ifrom,
            "to": ito,
            "source": source,
            "query": query
            }
        b = json.dumps(body)
        return callpostapi(url_path, query_params, b)

    except Exception as err:
        print("search : " + source + '   ' + query + " " + str(err))
        exit(-1)


def return_iso_dates(daystosubstract):
    try:
        days_to_substract = daystosubstract
        my_date = datetime.now() - timedelta(days=days_to_substract)
        my_date = my_date.strftime("%Y-%m-%d %H:%M:%S")
        istart = convert_DateToEpoc(my_date)
        my_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        iEnd = convert_DateToEpoc(my_end)
        return istart, iEnd

    except Exception as err:
        print("return_iso_dates : " + str(daystosubstract) + '   ' + str(err))
        exit(-1)



def optionparse():
    """Argument Parser."""
    opts = argparse.ArgumentParser(description='XDR Hunting Script',
                                   formatter_class=argparse.RawTextHelpFormatter)
    opts.add_argument('-d', '--days', help='Days of logs', default=1)
    opts.add_argument('-l', '--datalake', help='Data Lake to query: edr, msg, net, det', default='edr')
    opts.add_argument('-q', '--query', help='XDR search query')
    parsed_args = opts.parse_args()
    return parsed_args


def main(args):

    if args.query:
        my_date = datetime.now() - timedelta(days=int(args.days))
        istart = convert_DateToEpoc(str(my_date.replace(microsecond=0)))
        iEnd = convert_DateToEpoc(str(datetime.today().replace(microsecond=0)))
        ret = search(istart, iEnd, dl[args.datalake], args.query)
        print(ret)
    else:
        print("No query supplied, example -q 'hostName:globalnetworkissues.com OR objectIps:(204.188.205.176 OR 5.252.177.25)'")



if __name__ == '__main__':
    # tested arguments in my lab :  -d 7 -q "hostName:globalnetworkissues.com OR objectIps:(204.188.205.176 OR 5.252.177.25)"
    args = optionparse()
    print('Welcome to Trend Micro XDR Hunting script')
    main(args)


