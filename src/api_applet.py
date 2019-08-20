import time, uuid , json
import urllib.request
import hmac, hashlib
from base64 import b64encode


class Invalid_Key_Filename ( Exception ):
    pass

class yahoo_api ( object ):
    def __init__ ( self , key_file_name ): # key_file_name is your consumer_secret key
        try:
            with open(key_file_name,'r') as kfn:
                self.consumer_secret = kfn.read().strip('\n')
        except IOError:
            raise Invalid_Key_Filename("Please Enter Correct Private Key Filename")
        self.url = 'https://weather-ydn-yql.media.yahoo.com/forecastrss'
        self.method = 'GET'
        self.app_id = '3kxpga70'
        self.consumer_key = 'dj0yJmk9T3E5VVFpeU1qbXluJmQ9WVdrOU0ydDRjR2RoTnpBbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PThm'
        self.concat = '&'

        
    def process(self):
        #Prepare signature string (merge all params and SORT them
        merged_params = self.query.copy()
        merged_params.update(self.oauth)
        sorted_params = [k + '=' + urllib.parse.quote(merged_params[k], safe='') for k in sorted(merged_params.keys())]
        signature_base_str =  self.method + self.concat + urllib.parse.quote(self.url, safe='') + self.concat + urllib.parse.quote(self.concat.join(sorted_params), safe='')
        #Generate signature
        composite_key = urllib.parse.quote(self.consumer_secret, safe='') + self.concat
        oauth_signature = b64encode(hmac.new( bytes(composite_key , 'latin-1') , bytes(signature_base_str,'latin-1'), hashlib.sha1).digest())
        oauth_signature = oauth_signature.decode('utf-8')
        #Prepare Authorization header
        self.oauth['oauth_signature'] = oauth_signature
        auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(k,v) for k,v in self.oauth.items()])
        #Send request
        self.url = self.url + '?' + urllib.parse.urlencode(self.query)
        opener = urllib.request.build_opener()
        opener.addheaders = [('Authorization', auth_header),
                             ('X-Yahoo-App-Id', self.app_id),
                             ('Pragma', 'no-cache'),
                             ('User-Agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(self.url)
        data = response.read().decode('utf-8')
        del response
        del opener
        target = json.loads(data)
        return(target)

    def query_(self , location , unit = 'c'):
        self.query = {'location': location, 'format': 'json' , 'u' : unit}
        self.url = 'https://weather-ydn-yql.media.yahoo.com/forecastrss'
        self.oauth = {
        'oauth_consumer_key': self.consumer_key,
        'oauth_nonce': uuid.uuid4().hex,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_version': '1.0'
        }
        return(self.process())
