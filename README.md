# analyticsapp

*All the below instructions are done on Ubuntu Machine. If you are using different OS then please search the alterantive for performing below instructions.*


##### Virtualenv Configuration

Install virtualenv by following instructions if already not exists in your machine: (Virtualenv)[https://virtualenv.pypa.io/en/stable/installation/]


*In terminal*

> virtualenv -p python3.4 appenv

> cd appevn/

> source bin/activate


##### Clone app from github

> git clone https://github.com/yshlodha/analyticsapp.git

> cd analyticsapp/

> pip install -r requirements.txt

##### Run Migrations

> python manage.py migrate


##### Run server

*For local Envirnonment:*

> python manage.py runserver 


##### Perform Operation

To perform operations on APIs you can use any rest client you like. I am define operation for POSTman rest client.

*create client api key by registering client*

On url type:

> localhost:8000/app/client/<client_name>/

> method = 'POST' request

body will contents:

> {'email': '<youremailaddress>'}

<client_name> will be whatever unique name you like 

This request will gives you a json response.

> {'api_key': '<some hash_value>'}

Please Keep this Hash Value of api key some where so you can use after words in other API calls.

After registering Client.

Post some data on API.

On Url:

>  localhost:8000/app/client/<client_name>/data/

> Method = 'POST' request

body will content data something like:

> {"page_name": "http://gmail.com", "timestamp": "2018-04-21 20:00:55.445560+00:00", "userinfo": {"username": "yshlodha", "name": "Yash Lodha", "email": "someone@example.com"}, "sessioninfo": {"sessionkey": "3453wfrnjwnefijnewiqasfadsgeeasfsafqwr3", "login_at": "2018-04-22 22:00:49.445560+00:00", "logout_at": "2018-04-22 22:05:29.445560+00:00"}, "location": {"country": "India", "city": "Mumbai"}, "api_key": "d122f0f205e37726448e362d49516bbe"}


- Don't forget to use the api_key hash_value you get on client register api call in the body in 'api_key' field.

empty json will be received on success.


TO view the Data for the given page with some analytics performed on them

API Url:

> localhost:8000/app/client/<client_name>/data/?api_key=<your api key>&page_name=<the page name you have submitted data for>

> method = 'GET' request

In this API request you will sends api_key and name of the page you want to see data against in the query_string of url.

the response of this API is similar to:

> {"client_name":"yash_2","views":{"monthly_views":[{"city":"Mumbai","country":"India","views":1},{"city":"New Delhi","country":"India","views":2}],"day_views":[{"city":"Mumbai","country":"India","views":1},{"city":"New Delhi","country":"India","views":1}]},"average_session_duration":38046.18395966666,"client_id":2,"page_name":"http://gmail.com","number_of_unique_user":{"last_week":3,"last_month":3,"last_day":2}}


Now Another call you can use to see the users which are still online on the give page. 

in Url:

> localhost:8000/app/client/<client_name>/onlineusers/?api_key=<your api key>&page_name=<the page name you have submitted data for>

> method = 'GET' request

same as the request api for client_data

This api will response:

> {"online_users":1}

This is the number of users who logout_at is not provide at the time of client data creation API call. If client does npt provide logout_at time in the sessioninfo that is consider as currently online and not logout from the page.
