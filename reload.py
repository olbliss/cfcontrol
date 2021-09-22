import requests
import os
os.system('clear')

username = 'olbliss'
token = '49007830e90c255969d9e8d3bcdcb9365b52c0c3'
domain_name = 'olbliss.pythonanywhere.com'

'''/api/v0/user/{username}/webapps/'''                      
'''/api/v0/user/{username}/webapps/{domain_name}/reload/'''

requests.post('https://www.pythonanywhere.com/api/v0/user/olbliss/webapps/{domain_name}/reload/'
        .format(domain_name=domain_name),
        headers={'Authorization': 'Token {token}'.format(token=token)})
