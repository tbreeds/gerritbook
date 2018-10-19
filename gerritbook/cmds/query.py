# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import argparse
import json
import logging
import requests

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern')
    parser.add_argument('--all', dest='all', default=False,
                        action='store_true')
    args = parser.parse_args()

    params = dict(q=args.pattern,
                  o=['DETAILS'])
    if args.all:
        params['o'].append('ALL_EMAILS')

    req = requests.get('https://review.openstack.org/accounts/',
                       headers={'Accept': 'application/json'},
                       params=params,
                       )

    if req.status_code == 200:
        print('')
        results = json.loads(req.text[4:])
        logging.debug(results)
        for account in results:
            emails = [account['email']]
            if 'secondary_emails' in account:
                emails += account['secondary_emails']
            for email in emails:
                print('%(email)s\t%(name)s\t%(description)s' %
                      dict(name=account['name'],
                           email=email,
                           description=account.get('username', '')
                           )
                      )
    else:
        print(req)
    return 0
