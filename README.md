# DropShout
An app that notifies you by mail if any configured game has an ongoing Twitch Drops promotion. It uses the Twitch.tv API, and you're gonna have to set that up in order to get the app rolling.

Since Twitch's API doesn't allow you to directly retrieve ongoing Drops campaigns, we do this the roundabout way. 
The script checks the top 20 streamers of a preconfigured game, and checks if they have the "Drops Enabled" tag on their stream. From that, we can infer that there's an ongoing drops campaign.

Best applied via a daily cron job. I ran this with Python 3.8.1.

Custom config via Confuse needs to be added by yourself. Name the file config.yaml and place it in the directory below, depending on your system:

```
macOS: ~/.config/dropshout and ~/Library/Application Support/dropshout
Other Unix: ~/.config/dropshout and /etc/dropshout
Windows: %APPDATA%\dropshout where the APPDATA environment variable falls back to %HOME%\AppData\Roaming if undefined
```

Config format:

```
mail:
  smtp:
    server_hostname: '<YOUR MAIL SERVER>'
    port: <YOUR MAIL SERVER PORT (Likely 465)>
    login:
      username: '<YOUR USERNAME>'
      password: '<YOUR PASSWORD>'

games: [{'name': '<GAME NAME>',
         'id': '<GAME ID>',
         'subscribers': ['<MAIL #1>', '<MAIL #2>']},
         {'name': '<GAME NAME>',
         'id': '<GAME ID>,
         'subscribers': ['<MAIL #1>']}] # And etc.

api_credentials:
  client_id: <'YOUR CLIENT ID'>
  client_secret: <'YOUR CLIENT SECRET'>
```

*How do I get the game ID?*

[Register an app](https://dev.twitch.tv/docs/authentication#registration) at Twitch.tv, and make an REST API [get for games](https://dev.twitch.tv/docs/api/reference#get-games), using the game name.
