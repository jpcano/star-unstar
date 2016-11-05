#!/usr/bin/python
#
# Stars/Unstars all the repos for an organization.
#

import sys
import urllib2
import json
import os.path

if not os.path.exists('API_KEY'):
    print 'An API key is needed.'
    print 'Please, go to https://github.com/settings/tokens/new'
    print 'and request a new API token with default permissions.'
    print 'Then copy the API key you are given and put it in a file'
    print 'named API_KEY in this directory.'
    print
    print 'Happy starring/unstarring!'
    sys.exit(1)

if len(sys.argv) != 3 or (sys.argv[1] != 'star' and sys.argv[1] != 'unstar'):
    print 'Usage: %s <star|unstar> <ORGANIATION_NAME>' % sys.argv[0]
    sys.exit(1)

API_KEY = open('API_KEY', 'r').read().strip()

def request(url, method='GET'):
    req = urllib2.Request('https://api.github.com%s' % url, headers={"Authorization" : "token " + API_KEY}, data='')
    req.get_method = lambda: method
    contents = urllib2.urlopen(req).read()
    if len(contents.strip()) == 0:
        contents = '{}'
    return json.loads(contents)

org = sys.argv[2]
repos = request('/orgs/%s/repos?per_page=200' % org)

for repo in repos:
    repo_id = '%s/%s' % (repo['owner']['login'], repo['name'])
    if sys.argv[1] == 'star':
         print 'Starring %s' % repo_id
         request('/user/starred/%s' % repo_id, method='PUT')
    elif sys.argv[1] == 'unstar':
        print 'Unstarring %s' % repo_id
        request('/user/starred/%s' % repo_id, method='DELETE')
