# CoWin-Hawk
Cowin-Hawk is a python-flask based application to register users, and notify them of available vaccination slots in their concerned pincode or district, through SMS. This app internally uses Co-WIN Public APIs, so is intended to be used in India only.


### Note

```diff
- This app does NOT automatically books any vaccination slot. 
- The sole intent is to get a fast notification about any open slots with least use of third-party apps.
- Please refer https://apisetu.gov.in/public/marketplace/api/cowin and be updated with the latest govt guidelines
```


### Setup Pre-requisites
  - For the SMS facility to work, a [Fast2SMS](https://www.fast2sms.com/) account will be needed. 
  - A free account comes with a balance of around ₹50. Considering their current rate of ₹0.2/SMS, that will be more than enough for anyone's personal use.
  - `someFa15eApIKey!` has to be replaced with the personal Fast2SMS API Key, in the `config.json` file
  - Rest of the required python libraries can be installed as per `requirements.txt` file. A separate environment is recommended.
  - Fire up the app by - `python app.py`


### App Preview

**Dashboard Page**

![Dashboard Page](https://github.com/kr-prince/CoWin-Hawk/blob/main/static/img/dashboard.png)


**Register Page**

![Register Page](https://github.com/kr-prince/CoWin-Hawk/blob/main/static/img/register.png)


**Details Page**

![Details Page](https://github.com/kr-prince/CoWin-Hawk/blob/main/static/img/details.png)


**SMS Received**

<img src="https://github.com/kr-prince/CoWin-Hawk/blob/main/static/img/text.jpg" alt="SMS Pic" width="30%" height="20%"/>



**Feel free to use the app, add and contribute.**
