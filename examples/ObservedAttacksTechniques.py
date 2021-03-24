# for more up to date documentation go to https://automation.trendmicro.com/xdr/home
# Tested with XDR V2.0 API, Trend Micro XDR Product Manager Team
# Programmer:  D. Girard, Trend Micro XDR Product Manager Team, March 23rd 2021
import argparse  # for the script arguments
# import pandas as pd   # mainly for CSV flatening and export. TBD
import json      #
import tmconfig  # tmconfig.py with your api keys / token
import TMVisionOne  #Trend Micro Vision One/XDR API wrapper class
import time # for timing our script execution
from datetime import datetime, timedelta  # to calculate date and time range of the search


def optionparse():
    """Argument Parser."""
    opts = argparse.ArgumentParser(description='Trend Micro Vision One Observed Attack Techniques Script',
                                   formatter_class=argparse.RawTextHelpFormatter)
    opts.add_argument('-d', '--days', help='Past days of logs')
    opts.add_argument('-H', '--hours', help='Past hours of logs')
    opts.add_argument('-m', '--minutes', help='Past minutes of logs')
    opts.add_argument('-r', '--riskLevel', help="Array like this:['undefined', 'info', 'low', 'medium', 'high', 'critical']", default="['high', 'critical']")
    opts.add_argument('-e', '--endpointName', help='Specify an EndPoint as a filter', default="")
    #opts.add_argument('-t', '--output_type', default='json', help='output to json or csv')
    opts.add_argument('-f', '--filename', help='file name for the output')
    opts.add_argument('-s', '--size', help='page size, max 200', default=200)
    parsed_args = opts.parse_args()
    return parsed_args

# used to validate our exported data file
def validate_json(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as f:
            json_obj = json.load(f)
            f.close()
        print(f"{filepath} is a valid JSON file")
    except ValueError as e:
        print(f"{filepath} Not a valid JSON file.  {e}")

    finally:
        f.close()


def main(args):
    try:
        begin = time.time()
        input = args.riskLevel
        riskLevels = list(map(str, input.strip('[]\\').split(',')))
        x = TMVisionOne.XDR(tmconfig.zone, tmconfig.xdr_token, "Trend Micro Vision One Search Script Sample")
        if args.days:
            my_date = datetime.now() - timedelta(days=int(args.days))
        elif args.hours:
            my_date = datetime.now() - timedelta(hours=int(args.hours))
        elif args.minutes:
            my_date = datetime.now() - timedelta(minutes=int(args.minutes))

        istart = x.convert_DateToEpoc(str(my_date.replace(microsecond=0)))
        iEnd = x.convert_DateToEpoc(str(datetime.today().replace(microsecond=0)))
        #riskLevels = ["medium", "high", "critical"]
        ret = x.getOAT(istart,iEnd,args.size, riskLevels,args.endpointName)
        #ret = x.search(istart, iEnd, args.datalake, args.query)
        js =json.loads(ret)
        #print(json.dumps(js, indent=4))
        #p0 = pd.read_json(json.dumps(js['data']['logs']))
        print("*********STARTING*******************")
        total_cnt = js['data']['totalCount']
        print("Script parameters : " + str(args))
        print(f"Period from      : {my_date} to {datetime.now()}")
        print(f"Found            : {total_cnt}  hits")
        if total_cnt > 0:
            if "nextBatchToken" in js['data']:
                next_token = js['data']['nextBatchToken']
            result = list()
            if args.filename:
                filename = args.filename
            else:
                filename = "oat_results_" + datetime.now().strftime("%Y-%m-%dT%H-%M") + ".json"
            print(f"Records saved to : {filename}")
            js1 = js['data']['detections']
            result.append(js1)
            page_cnt = round(int(total_cnt)/args.size)
            pages = str(page_cnt)
            for i in range(page_cnt):
                p = i + 1
                print(f"Page {p} of {pages}")
                offset = (p*args.size)
                if offset > total_cnt:
                    break

                #ret = x.search(istart, iEnd, args.datalake, args.query, offset)
                ret = x.getOAT(istart, iEnd, args.size, riskLevels,args.endpointName, nextBatchToken=next_token)
                next_token = js['data']['nextBatchToken']
                js2 = json.loads(ret)
                js3=js2['data']['detections']
                result.append(js3)
            with open(filename, 'w', encoding="utf-8") as f1:
                json.dump(result, f1,indent=4)
                f1.close()
            validate_json(filename)
        end = time.time()

        print(f"Total runtime of the program is {round(end - begin, 2)} seconds")
        print("*********Program ended without problems**********")


    except Exception as err:
        print(f"main : {err}")
        exit(-1)


if __name__ == '__main__':
    # tested arguments in my lab :  -d 7 -q "hostName:globalnetworkissues.com OR objectIps:(204.188.205.176 OR 5.252.177.25)
    #validate_son("query_results_2021-03-22T22-09.json")
    args = optionparse()
    print('Welcome to Trend Micro Vision One Observed Attack Techniques script')
    print("Example :ObservedAttacksTechniques.py  -H 4 -r '[undefined, info, low, medium, high, critical]'")
    main(args)


