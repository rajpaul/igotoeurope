# sample-django-angular
Sample django angular js for demo

The project does the prcurement registration. First of all it prompt user to buy a plan for his/her procurement and register themself using that plan.The user registered get subscription mail in a certain interval.

1. Company registration
2. Company Certification Registration 
3. Multi step sign up etc.



Installation :
===============
Once you clone the repo, please go to the root directory . 
===============================================================

We used postgresql for this project . Please install postgresql if doesn't exist. 
1. Create a local_settings.py in the pr3 directory where main settings.py placed .
2. Create database whatever you want to name it and place the name of the database in local_settings.py configuration file .

3. Create your own virtualenv using the command $ virtualenv <YOUR VIRTUALENV NAME
4. Activate your virtualenv using $ source <YOUR VIRTUALENV NAME>/bin/activate
5. Install all requirement packagaes using $ pip install -r requirements.txt

It will install all the dependencies needed to run the application. If you see any error on the fly , please check the dependencies installed to install requirements dependencies. 

At the very last you need to migrate schema and create tables in your database. 
To do so please run the following command: 

$ python manage.py migrate

Once you done with successfull migration with the migrate command, you are done ! Now please run the server with django defaulf app server using the following command :

$ python manage.py runserver

Nice !! You are now able to see the application in your desired browser by the following address 

http://127.0.0.1:8000


Cheers!!


