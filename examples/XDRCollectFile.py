# This is a script tp show how to collect a file through XDR Automation API's
# for more up to date documentation go to https://automation.trendmicro.com/xdr/home
# Tested with XDR V2.0 API D. Girard, Trend Micro XDR Product Manager Team, February 14th 2021
import argparse
import tmconfig # This is where you have your API Token and your hosting zone (US by default)
import TMVisionOne


def main():
    try:
        """Argument Parser."""
        par = argparse.ArgumentParser(description='Trend Micro Vision One File Collector',
                                       formatter_class=argparse.RawTextHelpFormatter)
        par.add_argument('-e', '--endpointName', help='EndpointName', required=False)
        par.add_argument('-f', '--fileFullPatch', help='File with full path', required=False)
        par.add_argument('-d', '--description', help='Description', default='', required=False)
        par.add_argument('-i', '--interval', help='Interval (min) to verify if the file is ready to download',
                                type=int, default=5, required=False)
        par.add_argument('-r', '--retrieve', help='retrieve a file via task number', required=False)
        args = par.parse_args()

        # use zone (ex: 'us') and xdr_token (API Key) from tmconfig or hardcode it here
        # par.prog is equivalent to sys.argv[0] and it is the script name. We pass it as a parameter to identify
        # who call the API's. It is a good practice to identify your app through User-Agent.
        # You can also pass any string
        #tmconfig.zone
        x = TMVisionOne.XDR(tmconfig.zone, tmconfig.xdr_token, "Trend Micro Vision One CollectFile.py sample")
        print(x.listResponseTask())
        if args.retrieve is not None:
            x.retrieve(args.retrieve, args.interval)
        else:
            print(x.collectFile(args.endpointName, args.fileFullPatch, args.description, args.interval))

        print("Program ended without problems")

    except Exception as err:
        print("main : " + str(err))
        exit(-1)


if __name__ == '__main__':
    print('=================================================')
    print('Welcome to Trend Micro Vision One File Collector')
    print('=================================================')
    print('To send the collect command, use these parameters and keep track of the task number')
    print("""XDRCollectFile.py -e CA-DAVEG-L -f "c:\data\screenshots-XDR-SASE-001.jpg" -d "collect test file" """)
    print('\nTo retrieve a file, wait for the file to be ready and use task number like this')
    print("XDRCollectFile.py -r 00000099 -i 10")
    print('The retrieve process will retry every 10 minutes for 60 minutes \n')
    print('Note: make sure tmconfig.py is next to this script and that you configured the zone and xdr_token variables')
    print('=================================================')
    main()
