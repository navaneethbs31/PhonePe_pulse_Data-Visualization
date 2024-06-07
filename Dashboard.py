# ==================================================       /     IMPORT LIBRARY    /      =================================================== #
import mysql.connector
import pandas as pd
import numpy as np
import json
import requests
import streamlit as st
import plotly.express as px
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="phonepe_pulse"

)
mycursor = mydb.cursor()


# =================================================== / DASHBOARD / ===================================================

st.set_page_config(layout="wide")

st.title("PhonePe Pulse:violet[ | THE BEAT OF PROGRESS]")
with st.sidebar:
    select = st.selectbox("",
                          ("Home", "Explore Data")
                          )
if select == "Home":
    st.header(":white[Introduction]")
    st.write(":white[The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving back to the digital payments ecosystem.]")
    st.header("Guide")
    st.write("This data has been structured to provide details on data cuts of Transactions and Users on the Explore tab.")
    st.write("1. All India")
    st.write("2. State Wise")
    st.write("3. Top Ten Categories")
    st.write("4. Facts and Figures")
elif select=="Explore Data":
    option = st.radio("**Select your option**",("All India","State Wise","Top Ten Categories","Facts and Figures"),horizontal=True)
    if option=="All India":
        tab1,tab2 = st.tabs(["Transaction","User"])
    #================================================= All India Transaction ==============================================
        with tab1:
            col1,col2,col3 = st.columns(3)
            with col1:
                trans_year = st.selectbox("**Select Year**",("2018","2019","2020","2021","2022","2023","2024"),key="trans_year")
            with col2:
                trans_qtr = st.selectbox("**Select Quarter**",("1","2", "3","4"),key="trans_qtr")
            with col3:
                trans_name = st.selectbox("**Select Transaction Type**",("Recharge & bill payments","Peer-to-peer payments","Merchant payments","Financial Services","Others"),key="trans_name")


            mycursor.execute(f"SELECT State,Transaction_Amount from aggregated_transaction where Year ='{trans_year}' and Quarter = '{trans_qtr}' and Transaction_Name = '{trans_name}'; ")
            trans_qry_result = mycursor.fetchall()
            df_trans_qry_result = pd.DataFrame(np.array(trans_qry_result),columns=["State","Transaction_Amount"])
            df_trans_qry_result1 = df_trans_qry_result.set_index(pd.Index(range(1,len(df_trans_qry_result)+1)))

            mycursor.execute(f"SELECT State,Transaction_Count,Transaction_Amount from aggregated_transaction where Year ='{trans_year}' and Quarter = '{trans_qtr}' and Transaction_Name = '{trans_name}';")
            trans_anls_qry_result =mycursor.fetchall()
            df_trans_anls_qry_result = pd.DataFrame(np.array(trans_anls_qry_result),columns=["State","Transaction_Count","Transaction_Amount"])
            df_trans_anls_qry_result1 = df_trans_anls_qry_result.set_index(pd.Index(range(1,len(df_trans_anls_qry_result)+1)))

            mycursor.execute(f"SELECT SUM(Transaction_Amount),AVG(Transaction_Amount) from aggregated_transaction where Year ='{trans_year}' and Quarter = '{trans_qtr}' and Transaction_Name = '{trans_name}';")
            trans_amt_qry_result = mycursor.fetchall()
            df_trans_amt_qry_result = pd.DataFrame(np.array(trans_amt_qry_result),columns=["Total","Average"])
            df_trans_amt_qry_result1 = df_trans_amt_qry_result.set_index(["Average"])

            mycursor.execute(f"SELECT SUM(Transaction_Count),AVG(Transaction_Count) from aggregated_transaction where Year ='{trans_year}' and Quarter = '{trans_qtr}' and Transaction_Name = '{trans_name}';")
            trans_count_qry_result = mycursor.fetchall()
            df_trans_count_qry_result = pd.DataFrame(np.array(trans_count_qry_result), columns=["Total", "Average"])
            df_trans_count_qry_result1 = df_trans_count_qry_result.set_index(["Average"])


            # ===========================================================Output =========================================================
            #============================================Geo Visualization Dashboard for transaction =====================

            df_trans_qry_result.drop(columns=["State"],inplace=True)
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)
            state_names_trans = [feature["properties"]["ST_NM"] for feature in data1["features"]]
            state_names_trans.sort()

            df_state_names_trans = pd.DataFrame({"State":state_names_trans})
            df_state_names_trans["Transaction_Amount"] = df_trans_qry_result

            df_state_names_trans.to_csv("State_trans.csv",index=False)
            df_trans = pd.read_csv("State_trans.csv")

            fig_trans = px.choropleth(
                df_trans,
                geojson= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey="properties.ST_NM",locations="State",color="Transaction_Amount",color_continuous_scale="thermal",title="Transaction Analysis")
            fig_trans.update_geos(fitbounds="locations",visible=False)
            fig_trans.update_layout(title_font=dict(size=33),title_font_color="#FFFFFF",height=800)
            st.plotly_chart(fig_trans,use_container_width=True)

            df_trans_qry_result1["State"]=df_trans_qry_result1["State"].astype(str)
            df_trans_qry_result1["Transaction_Amount"] = df_trans_qry_result1["Transaction_Amount"].astype(float)
            df_trans_qry_result1_fig = px.bar(df_trans_qry_result1,x="State",y="Transaction_Amount",color="Transaction_Amount",color_continuous_scale="thermal",title="Transaction Analysis Chart",height=700)
            df_trans_qry_result1_fig.update_layout(title_font=dict(size=33),title_font_color="#FFFFFF")
            st.plotly_chart(df_trans_qry_result1_fig,use_container_width=True)

            st.header(":white[Total Calculation]")
            col4,col5 = st.columns(2)
            with col4:
                st.subheader(":white[Transaction Analysis]")
                st.dataframe(df_trans_anls_qry_result1)
            with col5:
                st.subheader(":white[TransactionAmount]")
                st.dataframe(df_trans_amt_qry_result1)
                st.subheader(":white[Transaction Count]")
                st.dataframe(df_trans_count_qry_result1)
        with tab2:
            col1,col2 = st.columns(2)
            with col1:
                user_year = st.selectbox("**Select Year**", ("2018", "2019", "2020", "2021", "2022", "2023", "2024"),
                                          key="user_year")
            with col2:
                user_qtr = st.selectbox("**Select Quarter**", ("1", "2", "3", "4"), key="user_qtr")

            mycursor.execute(f"SELECT State, SUM(Count) from aggregated_user where Year='{user_year}' and Quarter='{user_qtr}' group by State;")
            user_qry_result = mycursor.fetchall()
            df_user_qry_result = pd.DataFrame(np.array(user_qry_result),columns=["State","Count"])
            df_user_qry_result1 = df_user_qry_result.set_index(pd.Index(range(1,len(df_user_qry_result)+1)))

            mycursor.execute(f"SELECT SUM(Count), AVG(Count) from aggregated_user where Year='{user_year}' and Quarter='{user_qtr}' group by State;")
            user_count_qry_result = mycursor.fetchall()
            df_user_count_qry_result = pd.DataFrame(np.array(user_count_qry_result),columns=["Total","Average"])
            df_user_count_qry_result1 = df_user_count_qry_result.set_index(["Average"])

            df_user_qry_result.drop(columns=["State"],inplace=True)
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            state_names_user = [feature["properties"]["ST_NM"] for feature in data2["features"]]
            state_names_user.sort()

            df_state_names_user = pd.DataFrame({"State":state_names_user})
            df_state_names_user["Count"]=df_user_qry_result
            df_state_names_user.to_csv("State_user.csv",index=False)

            df_user = pd.read_csv("State_user.csv")

            fig_user = px.choropleth(
                df_user,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey="properties.ST_NM", locations="State", color="Count",
                color_continuous_scale="thermal", title="User Analysis"
            )
            fig_user.update_geos(fitbounds="locations",visible=False)
            fig_user.update_layout(title_font=dict(size=33),title_font_color="#FFFFFF",height=800)
            st.plotly_chart(fig_user,use_container_width=True)

            df_user_qry_result1["State"]=df_user_qry_result1["State"].astype(str)
            df_user_qry_result1["Count"]=df_user_qry_result1["Count"].astype(int)
            df_user_qry_result1_fig = px.bar(df_user_qry_result1,x="State",y="Count",color="Count",color_continuous_scale="thermal",title="User Analysis Chart",height=700)
            df_user_qry_result1_fig.update_layout(title_font=dict(size=33),title_font_color="#FFFFFF")
            st.plotly_chart(df_user_qry_result1_fig,use_container_width=True)

            st.header(":white[Total Calculation]")

            col3,col4 = st.columns(2)
            with col3:
                st.subheader("User Analysis")
                st.dataframe(df_user_qry_result1)

            with col4:
                st.subheader("User Count")
                st.dataframe(df_user_count_qry_result1)

    #==================================================/ State Wise / ==========================================================

    elif option=="State Wise":
        tab3,tab4 = st.tabs(["Transaction","User"])
        with tab3:
            col1,col2,col3 = st.columns(3)
            with col1:
                trans_state = st.selectbox("**Select State**",("andaman-&-nicobar-islands","andhra-pradesh", "arunachal-pradesh","assam","bihar",
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh',
                'jammu-&-kashmir', 'jharkhand', "karnataka", 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur',
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana',
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key="trans_state")
            with col2:
                trans_year = st.selectbox("**Select Year**",("2018","2019","2020","2021","2022","2023","2024"),key="trans_year")
            with col3:
                trans_qtr = st.selectbox("**Select Quarter**",("1","2","3","4"),key="trans_qtr")

            mycursor.execute(f"SELECT Transaction_Name,Transaction_Amount from aggregated_transaction where State='{trans_state}' and Year='{trans_year}' and Quarter='{trans_qtr}';")
            st_trans_qry_result = mycursor.fetchall()
            df_st_trans_qry_result = pd.DataFrame(np.array(st_trans_qry_result),columns=["Transaction_Name","Transaction_Amount"])
            df_st_trans_qry_result1 = df_st_trans_qry_result.set_index(pd.Index(range(1,len(df_st_trans_qry_result)+1)))

            mycursor.execute(f"SELECT Transaction_Name,Transaction_Count,Transaction_Amount from aggregated_transaction where State='{trans_state}' and Year='{trans_year}' and Quarter='{trans_qtr}';")
            st_trans_anls_qry_result =mycursor.fetchall()
            df_st_trans_anls_qry_result = pd.DataFrame(np.array(st_trans_anls_qry_result),columns=["Transaction_Name","Transaction_Count","Transaction_Amount"])
            df_st_trans_anls_qry_result1=df_st_trans_anls_qry_result.set_index(pd.Index(range(1,len(df_st_trans_anls_qry_result)+1)))

            mycursor.execute(f"SELECT SUM(Transaction_Amount),AVG(Transaction_Amount) from aggregated_transaction where State='{trans_state}' and Year='{trans_year}' and Quarter='{trans_qtr}';")
            st_trans_amt_qry_result = mycursor.fetchall()
            df_st_trans_amt_qry_result = pd.DataFrame(np.array(st_trans_amt_qry_result),columns=["Total", "Average"])
            df_st_trans_amt_qry_result1 = df_st_trans_amt_qry_result.set_index(["Average"])

            mycursor.execute(f"SELECT SUM(Transaction_Count),AVG(Transaction_Count) from aggregated_transaction where State='{trans_state}' and Year='{trans_year}' and Quarter='{trans_qtr}';")
            st_trans_count_qry_result = mycursor.fetchall()
            df_st_trans_count_qry_result = pd.DataFrame(np.array(st_trans_count_qry_result),columns=["Total", "Average"])
            df_st_trans_count_qry_result1 = df_st_trans_count_qry_result.set_index(["Average"])

            df_st_trans_qry_result1["Transaction_Name"] = df_st_trans_qry_result1["Transaction_Name"].astype(str)
            df_st_trans_qry_result1["Transaction_Amount"]=df_st_trans_qry_result1["Transaction_Amount"].astype(float)

            df_st_trans_qry_result1_fig = px.bar(df_st_trans_qry_result1,x="Transaction_Name",y="Transaction_Amount",color="Transaction_Amount",color_continuous_scale="thermal",title="Transaction Analysis Chart",height=800)
            df_st_trans_qry_result1_fig.update_layout(title_font=dict(size=33),title_font_color="#FFFFFF")
            st.plotly_chart(df_st_trans_qry_result1_fig,use_container_width=True)

            st.header(":white[Total Calculation]")

            col4,col5 = st.columns(2)
            with col4:
                st.subheader("Transaction Analysis")
                st.dataframe(df_st_trans_anls_qry_result1)

            with col5:
                st.subheader("Transaction Amount")
                st.dataframe(df_st_trans_amt_qry_result1)
                st.subheader("Transaction Count")
                st.dataframe(df_st_trans_count_qry_result1)


        with tab4:
            col6,col7 = st.columns(2)
            with col6:
                user_state = st.selectbox("**Select State**", ("andaman-&-nicobar-islands", "andhra-pradesh", "arunachal-pradesh", "assam", "bihar",
                'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana','himachal-pradesh',
                'jammu-&-kashmir', 'jharkhand', "karnataka", 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur',
                'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu','telangana',
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), key="user_state")
            with col7:
                user_year = st.selectbox("**Select Year**",("2018","2019","2020","2021","2022","2023","2024"),key="user_year")

            mycursor.execute(f"SELECT Quarter, SUM(Count) from aggregated_user where State='{user_state}' and Year='{user_year}' group by Quarter;")
            st_user_qry_result = mycursor.fetchall()
            df_st_user_qry_result = pd.DataFrame(np.array(st_user_qry_result),columns=["Quarter","Total_Count"])
            df_st_user_qry_result1=df_st_user_qry_result.set_index(pd.Index(range(1,len(df_st_user_qry_result)+1)))

            mycursor.execute(f"SELECT SUM(Count),AVG(Count) from aggregated_user where State='{user_state}' and Year='{user_year}' group by Quarter;")
            st_user_count_qry_result = mycursor.fetchall()
            df_st_user_count_qry_result = pd.DataFrame(np.array(st_user_count_qry_result),columns=["Total","Average"])
            df_st_user_count_qry_result1 = df_st_user_count_qry_result.set_index(["Average"])

            df_st_user_qry_result1["Quarter"]= df_st_user_qry_result1["Quarter"].astype(int)
            df_st_user_qry_result1["Total_Count"]=df_st_user_qry_result1["Total_Count"].astype(int)
            df_st_user_qry_result1_fig = px.bar(df_st_user_qry_result1,x="Quarter",y="Total_Count",color="Total_Count",color_continuous_scale="thermal",title="User Analysis Chart",height=800)
            df_st_trans_qry_result1_fig.update_layout(title_font=dict(size=33),title_font_color="#FFFFFF")
            st.plotly_chart(df_st_user_qry_result1_fig,use_container_width=True)

            st.header(":violet[Total Calculation]")

            col8,col9 = st.columns(2)
            with col8:
                st.subheader("User Analysis")
                st.dataframe(df_st_user_qry_result1)
            with col9:
                st.subheader("User Count")
                st.dataframe(df_st_user_count_qry_result1)
        # ==============================================          /     Top categories       /             =========================================== #
    elif option=="Top Ten Categories":
        tab5,tab6 = st.tabs(["Transaction","User"])
        with tab5:
            trans_year=st.selectbox("**Select Year**",("2018","2019","2020","2021","2022","2023","2024"),key="trans_year")

            mycursor.execute(f"SELECT State,SUM(Amount) as Amount from top_transaction where Year='{trans_year}' group by State order by Amount DESC LIMIT 10")
            trans_qry_result = mycursor.fetchall()
            df_trans_qry_result = pd.DataFrame(np.array(trans_qry_result),columns=["State","Total Transaction Amount"])
            df_trans_qry_result1=df_trans_qry_result.set_index(pd.Index(range(1,len(df_trans_qry_result)+1)))

            mycursor.execute(f"SELECT State,SUM(Amount) as Amount,SUM(Count) as Count from top_transaction where Year='{trans_year}' group by State order by Amount DESC LIMIT 10")
            trans_count_qry_result = mycursor.fetchall()
            df_trans_count_qry_result = pd.DataFrame(np.array(trans_count_qry_result), columns=["State", "Total Transaction Amount","Total Transaction Count"])
            df_trans_count_qry_result1 = df_trans_count_qry_result.set_index(pd.Index(range(1, len(df_trans_count_qry_result) + 1)))

            df_trans_qry_result1["State"]= df_trans_qry_result1["State"].astype(str)
            df_trans_qry_result1["Total Transaction Amount"]=df_trans_qry_result1["Total Transaction Amount"].astype(float)
            df_trans_qry_result1_fig = px.bar(df_trans_qry_result1,x="State",y="Total Transaction Amount",color="Total Transaction Amount",color_continuous_scale="thermal",title="Top Transaction Analysis Chart",height=800)
            df_trans_qry_result1_fig.update_layout(title_font=dict(size =33),title_font_color="#FFFFFF")
            st.plotly_chart(df_trans_qry_result1_fig,use_container_width=True)

            st.header(":white[Total Calculation]")
            st.subheader("Top Transaction Analysis")
            st.dataframe(df_trans_count_qry_result1)

        with tab6:
            user_year = st.selectbox("**Select Year**",("2018","2019","2020","2021","2022","2023","2024"),key="user_year")

            mycursor.execute(f"SELECT State, SUM(Registered_Users) as Top_user from top_user where Year='{user_year}' group by State order by Top_user DESC LIMIT 10")
            user_qry_result = mycursor.fetchall()
            df_user_qry_result = pd.DataFrame(np.array(user_qry_result),columns=["State","Total User Count"])
            df_user_qry_result1 = df_user_qry_result.set_index(pd.Index(range(1,len(df_user_qry_result)+1)))

            df_user_qry_result1["State"]= df_user_qry_result1["State"].astype(str)
            df_user_qry_result1["Total User Count"]= df_user_qry_result1["Total User Count"].astype(float)
            df_user_qry_result1_fig = px.bar(df_user_qry_result1,x="State",y="Total User Count",color="Total User Count",color_continuous_scale="thermal",title="Top User Analysis Chart",height=800)
            df_user_qry_result1_fig.update_layout(title_font=dict(size =33),title_font_color="#FFFFFF")
            st.plotly_chart(df_user_qry_result1_fig,use_container_width=True)

            st.header("Total Calculation")
            st.subheader("Total User Analysis")
            st.dataframe(df_user_qry_result1)

    else:
            year = st.selectbox("**Select Year**", ("2018", "2019", "2020", "2021", "2022", "2023", "2024"),key="year")
            selected_option = st.selectbox("**Select Category**",
                                           ("Total Transaction Amount",
                                            "Total Transaction Count",
                                            "Average Transaction Amount",
                                            "Average Transaction Count",
                                            "Registered PhonePe Users",
                                            "PhonePe app opens",
                                            "Recharge & bill payments",
                                            "Peer-to-peer payments",
                                            "Merchant payments",
                                            "Financial services",
                                            "Other payments",
                                            "Top 10 states transaction based on Amount",
                                            "Top 10 states Transaction on Count",
                                            "Top 10 states based on Users")
                                           )
            if selected_option=="Total Transaction Amount":
                mycursor.execute(f"SELECT SUM(Transaction_Amount) from aggregated_transaction where Year = '{year}' ")
                total_trans_amt_result = mycursor.fetchall()
                df_total_trans_amt_result = pd.DataFrame(np.array(total_trans_amt_result), columns=["Total Transaction Amount"])
                df_total_trans_amt_result1 = df_total_trans_amt_result.set_index(pd.Index(range(1, len(df_total_trans_amt_result) + 1)))
                st.dataframe(df_total_trans_amt_result1)

            elif selected_option=="Total Transaction Count":
                mycursor.execute(f"SELECT SUM(Transaction_Count) from aggregated_transaction where Year ='{year}'")
                total_trans_count_result = mycursor.fetchall()
                df_total_trans_count_result = pd.DataFrame(np.array(total_trans_count_result), columns=["Total Transaction Count"])
                df_total_trans_count_result1 = df_total_trans_count_result.set_index(pd.Index(range(1, len(df_total_trans_count_result) + 1)))
                st.dataframe(df_total_trans_count_result1)

            elif selected_option == "Average Transaction Amount":
                mycursor.execute(f"SELECT AVG(Transaction_Amount) from aggregated_transaction where Year ='{year}'")
                avg_trans_amt_result = mycursor.fetchall()
                df_avg_trans_amt_result = pd.DataFrame(np.array(avg_trans_amt_result), columns=["Average Transaction Amount"])
                df_avg_trans_amt_result1 = df_avg_trans_amt_result.set_index(
                    pd.Index(range(1, len(df_avg_trans_amt_result) + 1)))
                st.dataframe(df_avg_trans_amt_result1)

            elif selected_option=="Average Transaction Count":
                mycursor.execute(f"SELECT AVG(Transaction_Count) from aggregated_transaction where Year ='{year}' ")
                avg_trans_count_result = mycursor.fetchall()
                df_avg_trans_count_result = pd.DataFrame(np.array(avg_trans_count_result), columns=["Average Transaction Count"])
                df_avg_trans_count_result1 = df_avg_trans_count_result.set_index(pd.Index(range(1, len(df_avg_trans_count_result) + 1)))
                st.dataframe(df_avg_trans_count_result1)

            elif selected_option== "Registered PhonePe Users":
                mycursor.execute(f"SELECT SUM(Registered_Users) from map_user where Year ='{year}' ")
                total_user_count_result = mycursor.fetchall()
                df_total_user_count_result = pd.DataFrame(np.array(total_user_count_result),columns=["Registered PhonePe Users"])
                df_total_user_count_result1 = df_total_user_count_result.set_index(pd.Index(range(1, len(df_total_user_count_result) + 1)))
                st.dataframe(df_total_user_count_result1)

            elif selected_option == "PhonePe app opens":
                mycursor.execute(f"SELECT SUM(App_opens) from map_user where Year ='{year}'")
                avg_user_count_result = mycursor.fetchall()
                df_avg_user_count_result = pd.DataFrame(np.array(avg_user_count_result), columns=["PhonePe app opens"])
                df_avg_user_count_result1 = df_avg_user_count_result.set_index(pd.Index(range(1, len(df_avg_user_count_result) + 1)))
                st.dataframe(df_avg_user_count_result1)

            elif selected_option=="Recharge & bill payments":
                mycursor.execute(f"SELECT State,SUM(Transaction_Amount) from aggregated_transaction where Year ='{year}' and Transaction_Name = 'Recharge & bill payments' group by State")
                trans_qry_result = mycursor.fetchall()
                df_trans_qry_result = pd.DataFrame(np.array(trans_qry_result), columns=["State", "Transaction_Amount"])
                df_trans_qry_result1 = df_trans_qry_result.set_index(pd.Index(range(1, len(df_trans_qry_result) + 1)))
                st.dataframe(df_trans_qry_result1)

            elif selected_option=="Peer-to-peer payments":
                mycursor.execute(
                    f"SELECT State,SUM(Transaction_Amount) from aggregated_transaction where Year ='{year}' and Transaction_Name = 'Peer-to-peer payments' group by State")
                trans_qry_result = mycursor.fetchall()
                df_trans_qry_result = pd.DataFrame(np.array(trans_qry_result), columns=["State", "Transaction_Amount"])
                df_trans_qry_result1 = df_trans_qry_result.set_index(pd.Index(range(1, len(df_trans_qry_result) + 1)))
                st.dataframe(df_trans_qry_result1)

            elif selected_option=="Merchant payments":
                mycursor.execute(
                    f"SELECT State,SUM(Transaction_Amount) from aggregated_transaction where Year ='{year}' and Transaction_Name = 'Merchant payments' group by State")
                trans_qry_result = mycursor.fetchall()
                df_trans_qry_result = pd.DataFrame(np.array(trans_qry_result), columns=["State", "Transaction_Amount"])
                df_trans_qry_result1 = df_trans_qry_result.set_index(pd.Index(range(1, len(df_trans_qry_result) + 1)))
                st.dataframe(df_trans_qry_result1)

            elif selected_option =="Financial services":
                mycursor.execute(
                    f"SELECT State,SUM(Transaction_Amount) from aggregated_transaction where Year ='{year}' and Transaction_Name = 'Financial Services' group by State")
                trans_qry_result = mycursor.fetchall()
                df_trans_qry_result = pd.DataFrame(np.array(trans_qry_result), columns=["State", "Transaction_Amount"])
                df_trans_qry_result1 = df_trans_qry_result.set_index(pd.Index(range(1, len(df_trans_qry_result) + 1)))
                st.dataframe(df_trans_qry_result1)

            elif selected_option =="Other payments":
                mycursor.execute(
                    f"SELECT State,SUM(Transaction_Amount) from aggregated_transaction where Year ='{year}' and Transaction_Name = 'Others' group by State")
                trans_qry_result = mycursor.fetchall()
                df_trans_qry_result = pd.DataFrame(np.array(trans_qry_result), columns=["State", "Transaction_Amount"])
                df_trans_qry_result1 = df_trans_qry_result.set_index(pd.Index(range(1, len(df_trans_qry_result) + 1)))
                st.dataframe(df_trans_qry_result1)

            elif selected_option == "Top 10 states transaction based on Amount":
                mycursor.execute(f"SELECT State,SUM(Amount) as Amount from top_transaction where Year = '{year}' group by State order by Amount DESC LIMIT 10")
                top_trans_result = mycursor.fetchall()
                df_top_trans_result = pd.DataFrame(np.array(top_trans_result),columns=["State", "Total Transaction Amount"])
                df_top_trans_result1 = df_top_trans_result.set_index(pd.Index(range(1, len(df_top_trans_result) + 1)))
                st.dataframe(df_top_trans_result1)

            elif selected_option=="Top 10 states Transaction on Count":
                mycursor.execute(f"SELECT State,SUM(Count) as Count from top_transaction where Year='{year}' group by State order by Count DESC LIMIT 10")
                top_trans_count_result = mycursor.fetchall()
                df_top_trans_count_result = pd.DataFrame(np.array(top_trans_count_result),columns=["State","Total Transaction Count"])
                df_top_trans_count_result1 = df_top_trans_count_result.set_index(pd.Index(range(1, len(df_top_trans_count_result) + 1)))
                st.dataframe(df_top_trans_count_result1)

            elif selected_option=="Top 10 states based on Users":
                mycursor.execute(f"SELECT State, SUM(Registered_Users) as Top_user from top_user where Year='{year}' group by State order by Top_user DESC LIMIT 10")
                top_user_qry_result = mycursor.fetchall()
                df_top_user_qry_result = pd.DataFrame(np.array(top_user_qry_result), columns=["State", "Phonepe Registered Users"])
                df_top_user_qry_result1 = df_top_user_qry_result.set_index(pd.Index(range(1, len(df_top_user_qry_result) + 1)))
                st.dataframe(df_top_user_qry_result1)

