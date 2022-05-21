# Investment_Tracking_App
This is an app made using Streamlit. This app will help user to track their investments in various Banks for various schemes. I created this for my parents as they have trouble remembering maturity dates. This app will help them. Also I have added a forecasting service which will help them to choose the amount they want to invest. 
Since I am using Windows, I have made the app into a batch script which run everytime I log on my system. The reason I have not deployed this is server is because I dont want to take any risk of the encryption key getting leaked on the internet and I do not trust the security system for the free hosting platforms. :)
# How to run this app?
  - Step 1: Open terminal and perform pip install -r requirements.txt
  - Step 2: Open a python shell and execute the following to generate an encryption key  

            from cryptography.fernet import Fernet
            key = Fernet.generate_key()
            print(key.decode())
      **Save this key somewhere**
  - Step 3: Setup a relational database like MySQL etc and create a .env file. Add the following  
  
            database = "database"
            user = "user"
            password = "password"
            host = "host"
            port = "port"
            key = 'key'
            
  - Step 4: Execute the following code, streamlit run app0.py
  - Step 5: Enjoy and fix bugs if you find any.

# Architecture
![image](https://user-images.githubusercontent.com/48247827/169636090-51d29da9-8ac7-4bd4-94a4-473fd9c08bc7.png)

# Click to wathch Demo

[![Watch the video](https://img.youtube.com/vi/cgE5kb6Xjys/maxresdefault.jpg)](https://youtu.be/cgE5kb6Xjys)

# Next Steps
  - ~Add more analytics capabilities like Forecasting or recommended investment amount~
  - Add inflation adjusted investment amount which will be recommended to the user.
  - Improve on how the forecasted data is shown, more like rounding it to the nearest whole number.
  - Add more visualizations maybe Altair.
