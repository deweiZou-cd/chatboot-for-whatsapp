# Deploy service

1. clone this code `git clone git@github.com:kipley-ai/Kipley-integration-with-messaging-apps.git`
2. put the SSL CA file to the folder `mv xxx.pem ./`. This is for connecting with MySQL database
3. install all the requirements `pip3 install -r requirements.txt`
4. change the configs in `configs.py`.
5. run fly launch command `fly launch` (Optional)
6. modify `Procfile` and `fly.toml` files if you ran `fly launch` command (Optional)
7. We are now ready to deploy our app to Fly.io. At the command line, run: `fly deploy`


# Configuration Parameters in configs.py

---
| parameter | detail                                          |
|-----|-------------------------------------------------|
| DB_HOST | host of database server                         |
| DB_PORT | port of database server                         |
| DB_USERNAME | username to login to database server            |
| DB_PASSWD | password to login to database server            |
| DB_WORKING_DATABASE | database name on the database server            |
| TWILIO_ACCOUNT_SID | twilio account SID, use it to connect to twilio |
|TWILIO_AUTH_TOKEN | token to login to twilio account                |
|TWILIO_NUMBER | phone number (Whatsapp number) on twilio        |
| KB_PLATFORM_URL | base URL of kn platform                         |
| KB_APP_DETAIL_PATH | path to app detail API    |
|CONVERSATION_PLUGIN_MAP | maaping of app plugin, key is plugin_name of app, value is a tuple, whose first element is API or WEBSOCKET, and second element is where to find the API/websocket address|
|KB_MY_APP_PATH | path to my app API |

