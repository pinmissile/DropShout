import requests, smtplib, ssl, confuse, time
from email.mime.text import MIMEText
from urllib.parse import quote

config = confuse.Configuration('dropshout', __name__)

def main():
    twitch = TwitchAPI()
    for game in config['games'].get():
        game_data = twitch.is_there_a_drop(game['id'])
        if game_data:
            print("Drops for {}!".format(game['name']))
            send_mails(game, game_data)
        time.sleep(1)  # This is so we don't spam the server and get blocked.

def send_mails(game_config, game_data):
    # Build intro message
    msg_string = 'Hello!<br><br>\
        This is an automated notification of an ongoing Twitch Drops promotion for ' + game_data[0]['game_name'] + ' today!<br><br>\
            Here are some stream links:<br><br>'
    # Build stream links
    for stream in [x for x in game_data if 'c2542d6d-cd10-4532-919b-3d19f30a768b' in x['tag_ids']]:
        msg_string += '<a href="https://www.twitch.tv/' + stream['user_login'] + '">' + stream['title'] +'</a><br>',
    # Build mail
    msg = MIMEText(msg_string, 'html')
    msg['Subject'] = "{} Twitch Drops today!".format(game_data[0]['game_name'])
    context = ssl.create_default_context()
    # Connect to the server and send the mail.
    with smtplib.SMTP_SSL(config['mail']['smtp']['server_hostname'].get(),
                          config['mail']['smtp']['port'].get(),
                          context=context) as server:
        server.login(config['mail']['smtp']['login']['username'].get(),
                     config['mail']['smtp']['login']['password'].get())
        for reciever in game_config['subscribers']:
            # Send out one mail individually, as to not share mail addresses with everyone who is subscribed.
            msg['To'] = reciever
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
                # We return the entire object so we can link streams without doing another API get
                return response.json()['data']
        return False

if __name__ == "__main__":
    main()