# django-original-template
Django project with Docker (using docker-compose), nginx and uwsgi used
for a number of apps

This creates three containers:
	- web_server: web server with Django application installed
	- nginx_server: nginx proxy server
	- db_server: MySql Database


---
# Create Docker Machine
---
Create new docker-machine. The docker image needs to have more storage so use '--virtualbox-disk-size'. If you find out that the container needs more memory, use '--virtualbox-memory' (ex. --virtualbox-memory 12144). Be careful when assigning memory as this is set aside for the virtualbox and will no longer be available to the system when the container is brought up. You can run out of system memory if this number is set too high :

```bash
docker-machine create --driver virtualbox  template-app

```

---
Starting Docker:
---
These two commands may be necessary to get Docker running on your machine if you get the error message: "ERROR: Couldn't connect to Docker daemon - you might need to run `docker-machine start education-data`".

```bash
	docker-machine start template-app
	eval "$(docker-machine env template-app)"
```


---  
How to Run.  
---  
```

		Example Commands:

		Start up using development parameters and import data
		```bash
		./deploy.sh -e development -m template-app -i import

		```

		Start up using development parameters and import data
		```bash
		./deploy.sh -e development -i import  

		```

		Start up using staging parameters but delete containers and images first
		```bash
		./deploy.sh -e staging -d destroy  

		```

		Start up using production parameters but delete containers and images first and restart docker-machine
		```bash
		./deploy.sh -e production -d destroy -r restart  

		```

		Start up default machine using production parameters but delete containers and images first and restart docker-machine
		```bash
		./deploy.sh -e production -m default -d destroy -r restart  
		```


	---
	# Checks
	---
		Using the 'checks' flag runs a series of tests for version/dependencies, coding issues, license types, and Django security issues

		These checks verify the following:
			- version/dependencies: check for new versions of requirements
			- coding issues: basic python coding checks
			- license types: print out all the license types used in dependencies
			- Django security: basic security settings check

		These checks should be run in development. The required packages for the checks are not installed in staging and production. If you find that there is a lot of output with the checks (i.e. a lot of issues), you may want to add >> deploy.log to the end of the run command. This will pipe the output to the text file named deploy.log in the root directory. Note that the file can be named anything you want, but *.log files are gitignored and not written to github.

---
# Changes to database
---
		If you have imported new data into the database or made edits via the admin screen, you can dump the database
		to a backup file in the WebApp/scripts directory using the following command:
		```bash
			./backup.sh
		```
		Once the command runs, change to the WebApp/scripts directory:

		you will find a new file named

		'[env file specified name]_backup.sql'.

		Delete the original script and rename this to '[env file specified name].sql'.


---
# CI/CD
---

		CI/CD is handled via Codeship and the file /bin/codeship.sh is run via the deployment service. The crux of this script is the last two lines that rsyncs the files via SSH to the server. There are also corresponding environment variables that are set on the Codeship project. And finally, there are Codeship SSH keys that are added to the server. Unless some bigger architectural change is made, there should be no reason to edit the /bin/codeship.sh file or the Codeship settings. The deployment branches are:
			- staging: deploys to the staging server
			- production: deploys to the production server

---
# Servers
---

[app specificc info goes here]

---
# Debugging
---
	Logfiles to help with debugging can be found at:
			- ./nginx/log/nginx/access.log: access log from proxy nginx server. This shows all of the requests to the calculator and the status codes.
			- ./nginx/log/nginx/error.log: error log from proxy nginx server. This will display any Nginx errors.
			-./WebApp/logs/error.log: this displays any Django errors.
			-./WebApp/logs/warning.log: this displays any Django warnings.

			SSH into the web_server to view the Uwsgi error log:
			```BASH
				docker exec -it web_server bash
				nano /var/log/uwsgi/uwsgi.log
			```

			To write to the Django logfiles, do the following;
			```
			# put the following at the top of the script.
			import logging

			# Create logger to log to file
			logger = logging.getLogger(__name__)

			# put the following where you want the logging to print.
			logger.warning("my message here" + any_python_var)

			```
---
# Making changes to files and rebuilding containers
---
		---
		Database dumps
		---

		Using docker commands:
		```Bash
		docker exec -i -t db_server mysql -uroot -proot mysqldump [env file specified name] > scripts/[env file specified name]_backup.sql
		```
		Using bash script:
		```Bash
		./backup.sh
		```

		Stopping and removing all containers and images:
		```Bash
		docker stop $(docker ps -a -q) &&
		docker rm $(docker ps -a -q) &&
		docker rmi $(docker images -f dangling=true -q)
		```

		----
		SASS Changes
		----
		We are using SASS on this project so the CSS (stylesheets) are compiled. Do not add styles to the CSS files. All style changes need to be done in the files under template-app/static/template-app/css/sass. To make changes in the SASS files in development, you must re-compile the CSS. In development, you can use 'compass watch' to automatically compile the CSS when changes to the SASS file occur. To start this process, do the following;
		1) Navigate to .../template-app/WebApp/template-app/static/template-app in your terminal.
		2) then type in 'compass watch' and press enter. You should see a message that compass watch is now 'watching' the file. On each change/save, a message will display saying which style sheets have been recompiled if changes are identified.
