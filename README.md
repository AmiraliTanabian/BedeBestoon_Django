## What is "BedeBestoon"? 
The Bedeh Beston project is a website (and in the future, we plan to develop a mobile app as well) that helps you manage and track your expenses and income.

## How use it ? 
<b>First way</b> : Go to <a href="https://atanabain.pythonanywhere.com/">link</a><br>
<b>Second way:</b> : Use on your system:
<ul>
  <li>Clone repository</li>
  
```
  git clone https://github.com/AmiraliTanabian/BedeBestoon_Django.git && cd edeBestoon_Django
```
<li>Installing dependencies</li>

```
pip install -r requirements.txt
```

<li>Complete the recaptcha config</li>
<p>Go to this <a href="https://www.google.com/recaptcha/admin/create">link</a> and create recaptcha with localhost:8000 domain and replace <b>site key</b> on 
  
  ```RECAPTCHA_PUBLIC_KEY``` on settings.py and <b>secret_key</b> on 
  ```RECAPTCHA_PRIVATE_KEY``` on settings.py to use recaptcha
</p>

<li>Set gmail password</li>
<p>For send mail we need your gmail password and address <br> Go to settings.py and replace your email address on <b>EMAIL_HOST</b> and email password on <b>EMAIL_HOST_PASSWORD</b>
Please note that this password is not your regular password, and you must set it up according to this guide:</p>


<p>
  <b>Enable Two-Step Verification:</b>

  Go to your Google Account Security Page.
    Find the "2-Step Verification" option and enable it if it's not already turned on.

  <b>Generate an App Password:</b>

  On the same security page, locate the "App Passwords" section.
    Select "Mail" as the app and "Other (Custom Name)" as the device. You can enter "Django" or any other relevant name.
    Click "Generate" to receive a unique 16-character password. Copy this password, as it won’t be shown again

Configure Django Settings:
Open your Django project’s settings file (settings.py) and add the following email configuration:

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-app-password"

Replace "your-email@gmail.com" with your actual Gmail address and "your-app-password" with the generated App Password.
</p>

<li>Create db</li>

```
python3 manage.py migrate
```

<li>Create super user to use admin panel</li>

```
python3 manage.py createsuperuser
```

<li>Run on localhost:</li>

```
python3 manage.py runserver
```

Go to localhost:8000
</ul>

## api 
<ul>
  <li>api/submit/spend</li>
  Add spend
  <li>api/submit/income</li> 
  Add income
  <li>api/general-stat</li>
  Show some informations
  <li>api/account/login</li>
  Return your token 
</ul>

<p>These APIs are currently incomplete and lack essential functionalities such as adding, deleting, and retrieving expenses or income by ID.

Additionally, you can use .sh files to interact with these APIs efficiently.
For more details about the available API endpoints, refer to the api_help.txt file.</p>

## Front end
<p>
  My goal with this project was not front-end development. However, I have aimed to create a clean, simple, and responsive user interface. That being said, there is certainly room for further improvements in the UI.
</p>

## Future Plans
<ul>
  <li>Use Ai to show report from user financial life</li>
  <li>Develope mobile app</li>
</ul>
