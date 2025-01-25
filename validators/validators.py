from utils import handle_exceptions
import json, aiohttp, asyncio, re
from aiohttp import ClientTimeout, ClientResponseError
from collections import Counter
from stores.model.schemas import Validator_Schema

class Validator():

    def __init__(self):
        self.validator_list = json.load(open('assets/validators.json', 'r'))
        self.timeout_secs = 3  # Timeout in seconds
        self.timeout = ClientTimeout(total=self.timeout_secs)
        self.ipv4_pattern = r'(?:[01]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\.(?:[01]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\.(?:[01]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\.(?:[01]?[0-9]{1,2}|2[0-4][0-9]|25[0-5])'

        self.validators = {}
    

    @handle_exceptions
    async def get_public_ip(self, responses):
        '''
        Utility Function to calculate the most likely public-ip 
        based on numberof occurrences
        '''

        gathered_ips = []

        for res in responses:
            if res['response']:
                ips = re.findall(self.ipv4_pattern, res['response'] if res['response'] is str else str(res['response']))

            # Push found IPs to list, every IP gets counted once per response
            gathered_ips.extend(list(set(ips)))

        count = Counter(gathered_ips)

        return count.most_common()[0][0]


    @handle_exceptions
    def _check_response(self, validator: Validator_Schema):
        '''
        Utility-Function to check if a verifier works

        The function will save the response type and the 
        regex-pattern/json-structure for further usage

        The response types most probably contain the following
        content type: text/plain, application/json, text/html
        '''

        val = {
            'url': validator.url,
            'type': 'json' if 'application/json' in validator.content_type else 'text',
            'json_key': None,
            'usable': True
        }

        if validator.content_type == 'application/json':
            for key in validator.response:
                # print(key, validator.response[key])
                if self.public_ip in validator.response[key]:
                    val['json_key'] = key
        
        # Trying to 
        elif validator.content_type == 'text/plain':
            if self.public_ip != validator.response.strip():
                val['usable'] = False
            
        # Any other format can't be judged
        else:
            if self.public_ip != validator.response.strip():
                val['usable'] = False
    
        return val

    @handle_exceptions
    async def fetch_validator_data(self, validator):
        '''
        Helper function to fetch data for each validator
        '''
        
        async with aiohttp.ClientSession() as session:
            async with session.get(validator, timeout=self.timeout) as response:
                content_type = response.headers.get('Content-Type', '').split(';')[0].strip().lower()

                response = await response.json() if content_type == 'application/json' else await response.text()

                return {
                    'url': validator,
                    'response': response,
                    'content_type': content_type,
                }
    

    @handle_exceptions
    async def sort_validators(self):
        '''
        Function to check validators and store response methods
        '''

        tasks = [self.fetch_validator_data(validator) for validator in self.validator_list['ip_validators']]
                
        responses = await asyncio.gather(*tasks)
        responses = [res for res in responses if res]

        self.public_ip = await self.get_public_ip(responses)
        validators = [self._check_response(Validator_Schema(**res)) for res in responses]

        return (self.public_ip, validators)


    @handle_exceptions
    async def check_validators():
        '''
        Function to check availablity of Validators

        Check availability, latency
        '''

        