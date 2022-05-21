# Investment_Tracking_App
This is an app made using Streamlit. This app will help user to track their investments in various Banks for various schemes. I created this for my parents as they have trouble remembering maturity dates. This app will help them.
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
![image](https://user-images.githubusercontent.com/48247827/169541073-80defc42-b9b8-4051-96fc-f3eb48a2dd04.png)

# Click to wathch Demo

[![Watch the video](https://img.youtube.com/vi/cgE5kb6Xjys/maxresdefault.jpg)](https://youtu.be/cgE5kb6Xjys)

# Next Steps
  - ~Add more analytics capabilities like Forecasting or recommended investment amount~
  - Add inflation adjusted investment amount which will be recommended to the user
  - Add more visualizations maybe Altair
