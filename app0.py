import streamlit as st
from etl import ETL
import pandas as pd
import plotly.express as px
from dotenv import dotenv_values
import os
import encrypt_decrypt as ed
from datetime import datetime
from forecast import forecast_investment_amount

config = dotenv_values(".env")  

def months(d1, d2):
            return -(d1.month - d2.month + 12*(d1.year - d2.year))

try:
    with st.spinner('Connecting to Database'):
        etl_obj = ETL(database = config.get('database'), user = config.get('user'), 
        password = config.get('password'), 
        host = config.get('host') , port = config.get('port'))
        conn = etl_obj.connect_to_db()
    st.success('Connected to Database!')
except Exception as e:
    print(e)
    st.error("Failed to connect to Database. Contact Admin!")
    

st.title('Welcome Mr./Mrs. Biswas')

options = st.sidebar.radio(label = "Select Options", options = ['Enter New Data','Show Data','Forecast Investment Amount','Update Existing Data','Delete Exsiting Data','Analytics'],)
if options == 'Enter New Data':
    with st.form("my_form"):
        st.subheader("Enter Details")
        AccNo = st.text_input(label = "Enter Account Number",help  = "Required")
        AccNo = ed.encode(AccNo)
        PrAccHol = str(st.text_input(label = "Enter Primary Account Holder Name",help  = "Required"))
        PrAccHol = ed.encode(PrAccHol)
        ScAccHol = str(st.text_input(label = "Enter Secondary Account Holder Name", value = None,help  = "Optional"))
        ScAccHol = ed.encode(ScAccHol)
        Nom = st.text_input(label = "Enter Nominee Name",value = None,help  = "Optional")
        Nom = ed.encode(Nom)
        DepAmt = float(st.number_input(label = "Enter Deposit Amount",help  = "Required"))
        MatAmt = float(st.number_input(label = "Enter Maturity Amount", help  = "Required"))
        IntGain =  float(MatAmt - DepAmt)
        IntGain0 = IntGain
        IntGain = ed.encode(str(IntGain))
        DepAmt = ed.encode(str(DepAmt))
        MatAmt = ed.encode(str(MatAmt))
        RoI = float(st.number_input(label = "Enter Rate of Interest",value = 5.0, format='%.2f'))
        RoI = ed.encode(str(RoI))
        DoD = st.date_input(label = "Enter Date of Account Creation", help  = 'Required')
        DoM = st.date_input(label = "Enter Date of Maturity", help  = 'Optional',value = DoD)
        DtM = months(DoD, DoM)
        YtM = DtM/12
        DoD = ed.encode(str(DoD))
        DoM = ed.encode(str(DoM))
        DtM = ed.encode(str(DtM))
        YtM = ed.encode(str(YtM))
        AccType = str(st.radio(label = "Enter Account Type",help  = "Required", 
                                options  = ['FD','TD','SCSS','PPF','NPS']))
        AccType = ed.encode(AccType)
        KnabName = str(st.selectbox(label = "Enter Bank Name",help  = "Required", 
                                options = ['PNB','Axis','HDFC','Ind']))
        KnabName = ed.encode(KnabName)
        
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.caption(f"Amount of Interest Gained: {IntGain0}")
        try:
            with st.spinner('Saving data to database'):
                etl_obj.insert_value(AccNo = AccNo, PrAccHol = PrAccHol, ScAccHol = ScAccHol,
                                    Nom = Nom, DepAmt = DepAmt,MatAmt = MatAmt,IntGain = IntGain,
                                    RoI = RoI,DoD = DoD,DoM = DoM,AccType = AccType, KnabName = KnabName,DtM = DtM, YtM = YtM )
                
            st.success("Data saved to database")
        except Exception as e:
            print(e)
            st.error("Failed to save data to Database. Contact Admin!")

elif options == "Show Data":
    
    try:
        with st.spinner("Retrieving Data from Database"):
            rows = etl_obj.show_value()

            
            data = pd.DataFrame(rows, columns = ['Account_Number','Primary_Account_Holder','Secondary_Account_Holder','Nominee','Deposited_Amount','Maturity_Amount','Interest_Gained','Rate_of_Interest','Date_of_Deposit','Date_of_Maturity','Month_till_Maturity','Year_till_Maturity','Account_Type','Bank_Name'] )
            data = data.applymap(lambda x: ed.decode(x))
            for col in ['Deposited_Amount','Maturity_Amount','Interest_Gained','Rate_of_Interest','Month_till_Maturity','Year_till_Maturity']:
                data[col] = data[col].astype(float)   
            data.sort_values(by = 'Month_till_Maturity', inplace = True)
            st.caption("Data showing all investments based on recency of Maturity Date")
            st.dataframe(data.style.background_gradient(subset=['Deposited_Amount','Maturity_Amount','Month_till_Maturity','Year_till_Maturity'], cmap = 'YlGn'))
            total_depo_amt = data.loc[data.Date_of_Deposit.str.split('-', expand = True)[0] == str(datetime.now().year),['Primary_Account_Holder','Deposited_Amount']]
            total_depo_amt = total_depo_amt.groupby('Primary_Account_Holder')['Deposited_Amount'].sum().reset_index()
            st.caption(f"Data showing total investments by individual for the current Year {str(datetime.now().year)}")
            st.dataframe(total_depo_amt.style.background_gradient(subset=['Deposited_Amount'], cmap = 'YlOrRd'))
            total_matu_amt = data.loc[data.Date_of_Deposit.str.split('-', expand = True)[0] == str(datetime.now().year),['Primary_Account_Holder','Maturity_Amount']]
            total_matu_amt = total_matu_amt.groupby('Primary_Account_Holder')['Maturity_Amount'].sum().reset_index()
            st.caption(f"Data showing total gain by individual for the current Year {str(datetime.now().year)}")
            st.dataframe(total_matu_amt.style.background_gradient(subset=['Maturity_Amount'], cmap = 'summer'))
            
    except Exception as e:
        print(e)
        st.error("Data not availble. Contact Admin!!")
        
elif options == "Forecast Investment Amount":
        try:
                with st.spinner("Retrieving Data from Database"):
                    rows = etl_obj.show_value()

                    
                    data = pd.DataFrame(rows, columns = ['Account_Number','Primary_Account_Holder','Secondary_Account_Holder','Nominee','Deposited_Amount','Maturity_Amount','Interest_Gained','Rate_of_Interest','Date_of_Deposit','Date_of_Maturity','Month_till_Maturity','Year_till_Maturity','Account_Type','Bank_Name'] )
                    data = data.applymap(lambda x: ed.decode(x))
        except Exception as e:
            print(e)
            st.error("Data not availble. Contact Admin!!")
        try:
            with st.spinner("Forecasting Investment Amount"):
                pass
                
                forecast_obj = forecast_investment_amount(data)
                st.caption("Data showing recommended investement amount with possible investement dates")
                st.dataframe(forecast_obj[0])
                st.caption("Chart showing recommended investement amount with possible investement dates")
                st.pyplot(forecast_obj[1])
        except Exception as e:
            print(e)
                
elif options == "Analytics":     
    try:
        with st.spinner("Retrieving Data from Database"):
            rows = etl_obj.show_value()
            data = pd.DataFrame(rows, columns = ['Account_Number','Primary_Account_Holder','Secondary_Account_Holder','Nominee','Deposited_Amount','Maturity_Amount','Interest_Gained','Rate_of_Interest','Date_of_Deposit','Date_of_Maturity','Month_till_Maturity','Year_till_Maturity','Account_Type','Bank_Name'] )
            data = data.applymap(lambda x: ed.decode(x))
            st.caption("Deposit amount trend")
            fig0 = px.line(data, x="Date_of_Deposit", y="Deposited_Amount", color = 'Bank_Name',width=1100,height=900 )
            st.plotly_chart(fig0,use_container_width=True)
            st.caption("Maturity amount trend")
            fig1 = px.line(data, x="Date_of_Maturity", y="Maturity_Amount", color = 'Bank_Name', width=1100,height=900)
            st.plotly_chart(fig1,use_container_width=True)
            st.caption("ROI percentage trend by Banks")
            fig2 = px.line(data, x="Date_of_Deposit", y="Rate_of_Interest", color = 'Bank_Name', width=1100,height=900)
            st.plotly_chart(fig2,use_container_width=True)
            st.caption("Interest amount trend by Banks")
            fig3 = px.line(data, x="Date_of_Maturity", y="Interest_Gained", color = 'Bank_Name', width=1100,height=900)
            st.plotly_chart(fig3,use_container_width=True)
            st.caption("Interest amount trend by Accout Type")
            fig4 = px.line(data, x="Date_of_Maturity", y="Interest_Gained", color = 'Account_Type', width=1100,height=900)
            st.plotly_chart(fig4,use_container_width=True)
            st.caption("Total Deposit Amount by Primary Account Holder")
            fig5 = px.bar(data, x="Primary_Account_Holder", y="Deposited_Amount", width=1100,height=900)
            st.plotly_chart(fig5,use_container_width=True)
            st.caption("Total Maturity Amount by Primary Account Holder")
            fig6 = px.bar(data, x="Primary_Account_Holder", y="Maturity_Amount", width=1100,height=900)
            st.plotly_chart(fig6,use_container_width=True)


    except Exception as e:
        print(e)
        st.error("Data not availble. Contact Admin!!")
        
else:
    st.caption("Under Development")
    pass
