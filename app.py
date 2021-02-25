import requests, smtplib, ssl, confuse, time
from email.mime.text import MIMEText
from urllib.parse import quote

config = confuse.Configuration('dropshout', __name__)

def main():
    twitch = TwitchAPI()
    for game in config['games'].get():
        if twitch.is_there_a_drop(game['id']):
            print("Drops for {}!".format(game['name']))
            send_mails(game)
        time.sleep(1)  # This is so we don't spam the server and get blocked.

def send_mails(game):
    game_url = 'https://www.twitch.tv/directory/game/' + quote(game['name'])
    print(game_url)
    msg = MIMEText(u'Hello!<br>\
                     This is an automated notification to tell you that you can get Twitch drops from {} streams today!<br>\
                     <a href="' + game_url + '">Check it out!</a>'.format(game['name']), 'html')
    print(msg)
    msg['Subject'] = "{} Twitch Drops today!".format(game['name'])
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config['mail']['smtp']['server_hostname'].get(),
                          config['mail']['smtp']['port'].get(),
                          context=context) as server:
        server.login(config['mail']['smtp']['login']['username'].get(),
                     config['mail']['smtp']['login']['password'].get())
        for reciever in game['subscribers']:
            server.sendmail(config['mail']['smtp']['login']['username'].get(),
                            reciever,
                            msg.as_string())

class TwitchAPI():
    def __init__(self):
        data = {'client_id': config['api_credentials']['client_id'].get(),
                'client_secret': config['api_credentials']['client_secret'].get(),
                'grant_type': 'client_credentials',
                'scope': ''}
        r = requests.post('https://id.twitch.tv/oauth2/token', data=data).json()
        self.token = r['access_token']

    def is_there_a_drop(self, game_id):
        response = requests.get('https://api.twitch.tv/helix/streams?game_id=' + game_id,
                                headers={'Client-ID': config['api_credentials']['client_id'].get(),
                                         'Authorization': 'Bearer ' + self.token})
        for data in response.json()['data']:
            if 'c2542d6d-cd10-4532-919b-3d19f30a768b' in data['tag_ids']:
                # This is the UUID tag for "Drops Enabled"
                return True
        return False

if __name__ == "__main__":
    main()