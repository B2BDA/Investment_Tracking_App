import pandas as pd
from fbprophet import Prophet

def forecast_investment_amount(data):
    try:
        data = data.loc[:,['Date_of_Deposit','Deposited_Amount']]
    except Exception as e:
        pass
    data.rename(columns = {'Date_of_Deposit':'ds','Deposited_Amount':'y'}, inplace = True)
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    fig1 = m.plot(forecast)
    forecast = forecast[['ds', 'yhat']]
    forecast.rename(columns = {'ds':'Possible Investment Date','yhat':'Recommended Investment Amount'}, inplace = True)
    return forecast, fig1

