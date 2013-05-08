#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import urllib
import re
import oauth2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        ip_address = self.request.remote_addr
        addr = self.getAddressInfo(ip_address)
        glass = {
          "address" : addr,
          "html": "<article>\n  <section>\n    <div class=\"layout-figure\">\n      <div class=\"align-center\">\n        <p class=\"text-x-large\">YOU</p>\n        <img src=\"http://pinkgirlq8.com/wp-content/uploads/taco-bell.png\" width=\"50\" height=\"60\">\n        <p class=\"text-x-large\">TB</p>\n      </div>\n      <div>\n        <div class=\"text-normal\">\n          <p>720 Story Road</p>\n          <p>San Jose, CA</p>\n          <p class=\"green\">Open</p>\n        </div>\n      </div>\n    </div>\n  </section>\n</article>\n",
          "notification": {
            "level": "DEFAULT"
          }
        }        
        self.yelp_search
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(glass))
    
    """ Fetches IP Address Information.
        
        Retrieves location information latitude, longitude, city, zip code
        and requires a string input of an IP address.
    
        Args:
            ip_address: String IP Address. For example:
            
            "107.212.24.150"
        
        Returns:
            A JSON dump of address information with the following keys:
            city, lat, long, zip. For example:
            
            { 
              \"lat\": \"37.33939\", 
              \"city\": \"SAN JOSE\", 
              \"zip\": \"95101\", 
              \"long\": \"-121.89496\"
            }
    
        """
    def getAddressInfo(self, ip_address):
      # ip_address = '107.212.24.150'
      url = 'http://ipinfodb.com/ip_locator.php?ip=' + ip_address
      url_file = urllib.urlopen(url)
      contents = url_file.read()
      
      address_info = {}
      address_info['city']   = re.search('<li>City : (.*)</li>', contents)
      address_info['lat']    = re.search('<li>Latitude : (.*)</li>', contents)
      address_info['long']   = re.search('<li>Longitude : (.*)</li>', contents)
      address_info['zip']    = re.search('<li>Zip or postal code : (.*)</li>', contents)
      
      for item in address_info:
        address_info[item] = address_info[item].group(1)
      return json.dumps(address_info)
    
    
        
    def yelp_search(self):
      consumer_key = '4zRvW-MqSSovi-GTT52r4Q'
      consumer_secret = 'FW4qaexJchzvcCxyKF_dqSwp20o'
      token = 'kjOUF5dhJXRy8CcLdcBbZzwBa5MfaFSt'
      token_secret = 'lI5vkmFN7ttioutaGiQehO9PGZY'
      
      consumer = oauth2.Consumer(consumer_key, consumer_secret)
      url = 'http://api.yelp.com/v2/search?term=bars&location=sf'

      print 'URL: %s' % (url,)

      oauth_request = oauth2.Request('GET', url, {})
      oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                            'oauth_timestamp': oauth2.generate_timestamp(),
                            'oauth_token': token,
                            'oauth_consumer_key': consumer_key})

      token = oauth2.Token(token, token_secret)
      oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
      signed_url = oauth_request.to_url()
      print 'Signed URL: %s' % (signed_url,)
      

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
