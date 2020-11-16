'''
Config file for some of Trend Micro XDR Scripts
XDR Product Manager Team, November 2020
Do not share your api keys in public github
'''

# Get your token from your XDR Administrator, in XDR Console under Account Management.
# You can also use the key for Splunk integration in XDr under Alert Notifications, it will work for most
xdr_token = ''

'''
Region            FQDN
United States     api.xdr.trendmicro.com
European Union    api.eu.xdr.trendmicro.com
Japan             api.xdr.trendmicro.co.jp
Singapore         api.sg.xdr.trendmicro.com
and more regions to come, Australia, Canada...
please update region dictionary
'''
region = {'us': 'https://api.xdr.trendmicro.com', 'eu': 'https://api.eu.xdr.trendmicro.com',
          'jp': 'https://api.xdr.trendmicro.co.jp', 'sg': 'https://api.sg.xdr.trendmicro.com'}

#Addition configuration
vt_api_key = '' # register to virustotal.com for a key
bazaar_api_key = ''  #this is free, just register to bazaar.abuse.ch