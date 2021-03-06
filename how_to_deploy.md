Nginx configuration and Django deploy
==========================================

Update and upgrade Ubuntu server
------------------------------------------
```
sudo apt update
sudo apt upgrade
```

Install python, nginx and curl
------------------------------------------

```
sudo apt install python3-pip python3-dev libpq-dev nginx curl
```

Install python 3.9
-----------------------------------------

```
sudo apt install python3.9
```

Install pipenv
-----------------------------------------

```
sudo apt install pipenv
```


Install docker and postgres client
-----------------------------------------

```
sudo apt install docker.io
sudo apt install docker-compose
sudo apt install postgresql-client-12
```

Configure git
-----------------------------------------
* Fork the project add the ssh public key to your github account.

```
git config --global user.name "Your Name"
git config --global user.email "your@email.com.br"
cd ~/.ssh
ssh-keygen -t ed25519 -C "your@email.com.br"
```

Clone the project
-----------------------------------------

```
git clone git@github.com:pedromadureira000/work-at-codevance.git
```

Create the .venv
-----------------------------------------

You must create the .venv inside the project. You can set PIPENV_VENV_IN_PROJECT to do it

```
export PIPENV_VENV_IN_PROJECT="enabled"
pipenv sync --python /usr/bin/python3.9
```

Notes on deploying on Raspberry-PI: 
-----------------------------------------

* Use psycopg2 instead of psycopg2-binary

Run Postgres and Redis container
-----------------------------------------

You must run this in the same folder where the 'docker-compose.yml' file is.

```
sudo docker-compose up -d
```

Connect to default database and create the database that you will use
-----------------------------------------

```
psql postgres://phsw:senhasegura@localhost:5432/postgres
create database codevance_challenge;
```

Edit .env file
-----------------------------------------

You have to do it for both backend and frontend. 
Use the env_sample as example.

Do migrations
-----------------------------------------

```
python manage.py migrate
```

Run initial command to create users and supplier companies
-----------------------------------------

```
python manage.py initial
```

Create systemd socket for Gunicorn
-----------------------------------------

* Create the file with:

```
sudo vim /etc/systemd/system/gunicorn.socket
```

* Then copy this to that file

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Create systemd service for Gunicorn
-----------------------------------------

* Create the file with:

```
sudo vim /etc/systemd/system/gunicorn.service
```

* Then copy this to that file and edit the user field and working directory path

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=<your ubuntu server user>
Group=www-data
WorkingDirectory=/home/<Your home directory>/work-at-codevance/backend
ExecStart=/home/<Your home directory>/work-at-codevance/backend/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock settings.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable the Gunicorn socket
-----------------------------------------

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

Check the Gunicorn socket???s logs 
-----------------------------------------

```
sudo journalctl -u gunicorn.socket
```

Test socket activation
-----------------------------------------

It will be dead. The gunicorn.service will not be active yet since the socket has not yet received any connections

```
sudo systemctl status gunicorn  
```

Test the socket activation
-----------------------------------------

It must return a html response

```
curl --unix-socket /run/gunicorn.sock localhost 
```

If you don't receive a html, check the logs. Check your /etc/systemd/system/gunicorn.service file for problems. If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process:
-----------------------------------------

```
sudo journalctl -u gunicorn  #(check logs)
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

Configure Nginx to Proxy Pass to Gunicorn
-----------------------------------------

* Create the file

```
sudo vim /etc/nginx/sites-available/work-at-codevance
```

* Paste the nginx configuration code, and edit the sever name with your server IP.

```
server {
        listen 80;
        # Above is the server IP
        server_name <your server ip>;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /api {
                include proxy_params;
                proxy_pass http://unix:/run/gunicorn.sock;
        }

        location / {
                include proxy_params;
                proxy_pass http://localhost:3000;
        }
}
```

Enable the file by linking it to the sites-enabled directory:
-----------------------------------------

```
sudo ln -s /etc/nginx/sites-available/work-at-codevance /etc/nginx/sites-enabled
```

Test for syntax errors
-----------------------------------------

```
sudo nginx -t
```

Restart nginx
-----------------------------------------

```
sudo systemctl restart nginx
```

Firewall configurations
-----------------------------------------

```
sudo ufw allow 'Nginx Full'
```


Run celery
-----------------------------------------

```
cd ~/work-at-codevance/backend
pipenv shell
celery -A settings worker -l INFO &
```

Run celery beat
-----------------------------------------

```
celery -A settings beat -l INFO &
```

Nuxt deploy
=========================================

Install node from NodeSource PPA
-----------------------------------------

The PPA will be added to your configuration and your local package cache will be updated automatically. After running the setup script from Nodesource, you can install the Node.js package

```
cd ~
curl -sL https://deb.nodesource.com/setup_14.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs
```

Install the build-essential package
-----------------------------------------

In order for some npm packages to work (those that require compiling code from source, for example), you will need to install the build-essential package:

```
sudo apt install build-essential
```

Installing PM2
-----------------------------------------

PM2 is a process manager for Node.js applications. It makes possible to daemonize applications so that they will run in the background as a service.
The -g option tells npm to install the module globally, so that it???s available system-wide.

```
sudo npm install pm2@latest -g
```

Install project dependencies
-----------------------------------------

```
npm install
```

Make the Build 
-----------------------------------------

```
npm run build
```

Start the app with PM2
-----------------------------------------

```
pm2 start npm --name "project name" -- start
```
* This also adds your application to PM2???s process list. 
* Applications that are running under PM2 will be restarted automatically if the application crashes or is killed, but we can take an additional step to get the application to launch on system startup using the startup subcommand. This subcommand generates and configures a startup script to launch PM2 and its managed processes on server boots:

```
pm2 startup systemd
```
* Save the PM2 process list and corresponding environments
```
pm2 save
```
* You have now created a systemd unit that runs pm2 for your user on boot.

Start the service with systemctl
-----------------------------------------

```
sudo systemctl start pm2-sammy  #(replace sammy with your username)
```

Reboot
-----------------------------------------
If at this point you encounter an error, you may need to reboot, which you can achieve with 'sudo reboot'.

```
systemctl status pm2-sammy.service #(replace sammy with your username)
```

Solving common errors
----------------------------------------
*  Nginx Is Showing the Default Page Instead of the Django Application
  - If Nginx displays the default page instead of proxying to your application, it usually means that you need to adjust the server_name within the /etc/nginx/sites-available/myproject file to point to your server???s IP address or domain name.
* 404 Not Found
  - Check if your .env file is configured correctly. You may have set ALLOWED_HOSTS wrong for example.
* Nginx Is Displaying a 502 Bad Gateway Error Instead of the Django Application
  - A 502 error indicates that Nginx is unable to successfully proxy the request. A wide range of configuration problems express themselves with a 502 error, so more information is required to troubleshoot properly.
  - The primary place to look for more information is in Nginx???s error logs. Generally, this will tell you what conditions caused problems during the proxying event. Follow the Nginx error logs by typing:
  ```
  sudo tail -F /var/log/nginx/error.log
  ```

The primary place to look for more information is in Nginx???s error logs. Generally, this will tell you what conditions caused problems during the proxying event. Follow the Nginx error logs by typing:
* `npm install` ends with "Killed" (https://stackoverflow.com/questions/38127667/npm-install-ends-with-killed)

PLUS
-----------------------------------------

* Some PM2 commands
```
pm2 stop app_name_or_id
pm2 restart app_name_or_id
pm2 list
pm2 info app_name
pm2 monit (status, CPU, and memory usage)
pm2 logs order-system --lines 1000
```

* It may be useful to testing Django
```
sudo ufw allow 8000
sudo ufw delete allow 8000
```
