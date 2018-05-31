#! /usr/bin/env python

''' Copyright 2015 Akamai Technologies, Inc. All Rights Reserved.
 
 Licensed under the Apache License, Version 2.0 (the 'License');
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at 

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an 'AS IS' BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

Sample client for network-lists
In order to 'create' a new list, you'll want to 
remove the # at the beginning of the '_create_network_list' call
and update the IP addresses to be appropriate for your needs.
'''



import requests, logging, json, sys
from http_calls import EdgeGridHttpCaller
from akamai.edgegrid import EdgeGridAuth
from config import EdgeGridConfig
import urllib

if sys.version_info[0] >= 3:
    # python3
    from urllib import parse
else:
    # python2.7
    import urlparse as parse

def _init():
    global session, config, debug, verbose, httpCaller

    # Establish an HTTP session
    session = requests.Session()

    # Load the .edgerc credentials file
    section_name = 'networklists'
    config = EdgeGridConfig({}, section_name)

    # Set up verbose output and debugging
    if hasattr(config, 'debug') and config.debug:
        debug = True
    else:
        debug = False

    if hasattr(config, 'verbose') and config.verbose:
        verbose = True
    else:
        verbose = False

    # Set the EdgeGrid credentials
    session.auth = EdgeGridAuth(
        client_token=config.client_token,
        client_secret=config.client_secret,
        access_token=config.access_token
    )

    # If include any special headers (used for debugging)
    if hasattr(config, 'headers'):
        session.headers.update(config.headers)

    # Set up the base URL
    baseurl = '{}://{}/'.format('https', config.host)
    httpCaller = EdgeGridHttpCaller(session, debug, verbose, baseurl)

def _get_network_lists():
	print('Requesting the list of network lists')

	events_result = httpCaller.getResult('/network-list/v1/network_lists')
	return events_result

def _create_network_list(name,ips):
	print('Creating a network list {} for ip addresses {}'.format(name, json.dumps(ips)))
	headers = {'Content-Type': 'application/json'}
	path = '/network-list/v1/network_lists'
	data_obj = {
		'name' : name,
		'type' : 'IP',
		'list' : ips
	}
	
	httpCaller.postResult(urljoin(baseurl, path), json.dumps(data_obj))

def main():
    _init()
    
    Id = {}
    lists = _get_network_lists()['network_lists']
    
    def _mapper(x):
        print('{}, {}'.format(str(x['numEntries']), x['name']))
        
    map(_mapper, lists)
    #_create_network_list('test',['1.2.3.4'])

if __name__ == '__main__':
    main()

