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
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(glass))
    
    def getAddressInfo(self, ip_address):
      ip_address = '107.212.24.150'
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
  
  
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
