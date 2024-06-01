# ============================================       /     IMPORT LIBRARY    /      =========================================== #
# [pandas and file handling libraries]
import json
import os
import pandas as pd

# [SQL libraries]
import mysql.connector
import sqlalchemy.types
from sqlalchemy import create_engine
#clone the phonepe github repositry and save in the local path


# ===============================================    /    DATA PROCESSING     /   ===========================================================
#==============================     DATA     /     AGGREGATED     /     TRANSACTION     ===================================#
def agg_trans():
    path = "C:\\Users\\Dell\\OneDrive\\Desktop\\DS_Course\\Projects\\PhonePe_Data_Visualisation\\PhonePe_Data\\data\\aggregated\\transaction\\country\\india\\state\\"
    Agg_state_list = os.listdir(path)

    Data = {"State": [], "Year": [], "Quarter": [], "Transaction_Name": [], "Transaction_Count": [],
            "Transaction_Amount": []}

    for i in Agg_state_list:
        path_i = path + i + "\\"
        Agg_year = os.listdir(path_i)

        for j in Agg_year:
            path_j = path_i + j + "\\"
            Agg_year_list = os.listdir(path_j)

            for k in Agg_year_list:
                path_k = path_j + k
                data = open(path_k, "r")
                D = json.load(data)
                for d in D["data"]["transactionData"]:
                    Name = d["name"]
                    Count = d["paymentInstruments"][0]["count"]
                    Amount = d["paymentInstruments"][0]["amount"]
                    Data["Transaction_Name"].append(Name)
                    Data["Transaction_Count"].append(Count)
                    Data["Transaction_Amount"].append(Amount)
                    Data["State"].append(i)
                    Data["Year"].append(j)
                    Data["Quarter"].append(int(k.strip(".json")))
    Agg_trans = pd.DataFrame(Data)
    return Agg_trans

#==============================     DATA     /     AGGREGATED     /     USER     ===================================#
def agg_user():
    path = "C:\\Users\\Dell\\OneDrive\\Desktop\\DS_Course\\Projects\\PhonePe_Data_Visualisation\\PhonePe_Data\\data\\aggregated\\user\\country\\india\\state\\"
    Agg_state_list = os.listdir(path)

    Data = {"State": [], "Year": [], "Quarter": [], "Brand": [],
            "Count": [], "Percentage": []}

    for i in Agg_state_list:
        path_i = path + i + "\\"
        Agg_year = os.listdir(path_i)

        for j in Agg_year:
            path_j = path_i + j + "\\"
            Agg_year_list = os.listdir(path_j)

            for k in Agg_year_list:
                path_k = path_j + k
                data = open(path_k, "r")
                D = json.load(data)
                if D and D.get("data") and D["data"].get("usersByDevice"):
                    for d in D["data"]["usersByDevice"]:
                        Brand = d.get("brand","")
                        Count = d.get("count",0)
                        Percentage = d.get("percentage",0)
                        #Data["Registered_Users"].append(RegisteredUsers)
                        Data["Brand"].append(Brand)
                        Data["Count"].append(Count)
                        Data["Percentage"].append(Percentage)
                        Data["State"].append(i)
                        Data["Year"].append(j)
                        Data["Quarter"].append(int(k.strip(".json")))
    Agg_user = pd.DataFrame(Data)
    return Agg_user

#==============================     DATA     /     MAP     /     TRANSACTION     =========================================#
def map_trans():
    path = "C:\\Users\\Dell\\OneDrive\\Desktop\\DS_Course\\Projects\\PhonePe_Data_Visualisation\\PhonePe_Data\\data\\map\\transaction\\hover\\country\\india\\state\\"
    Map_state_list = os.listdir(path)

    Data = {"State": [], "Year": [], "Quarter": [], "Transaction_Name": [], "Transaction_Count": [],
            "Transaction_Amount": []}

    for i in Map_state_list:
        path_i = path + i + "\\"
        Map_year = os.listdir(path_i)

        for j in Map_year:
            path_j = path_i + j + "\\"
            Map_year_list = os.listdir(path_j)

            for k in Map_year_list:
                path_k = path_j + k
                data = open(path_k, "r")
                D = json.load(data)
                for d in D["data"]["hoverDataList"]:
                    Name = d["name"]
                    Count = d["metric"][0]["count"]
                    Amount = d["metric"][0]["amount"]
                    Data["Transaction_Name"].append(Name)
                    Data["Transaction_Count"].append(Count)
                    Data["Transaction_Amount"].append(Amount)
                    Data["State"].append(i)
                    Data["Year"].append(j)
                    Data["Quarter"].append(int(k.strip(".json")))
    Map_trans = pd.DataFrame(Data)
    return Map_trans
#==============================         DATA     /     MAP     /     USER         ============================================#
def map_user():
    path = "C:\\Users\\Dell\\OneDrive\\Desktop\\DS_Course\\Projects\\PhonePe_Data_Visualisation\\PhonePe_Data\\data\\map\\user\\hover\\country\\india\\state\\"
    Map_state_list = os.listdir(path)

    Data = {"State": [], "Year": [], "Quarter": [], "District": [],
            "Registered_Users": [], "App_opens": []}

    for i in Map_state_list:
        path_i = path + i + "\\"
        Map_year = os.listdir(path_i)

        for j in Map_year:
            path_j = path_i + j + "\\"
            Map_year_list = os.listdir(path_j)

            for k in Map_year_list:
                path_k = path_j + k
                data = open(path_k, "r")
                D = json.load(data)
                hover_data = D["data"].get("hoverData",{})
                for state,state_data in hover_data.items():
                    registered_users = state_data.get("registeredUsers",0)
                    app_opens = state_data.get("appOpens",0)
                    Data["District"].append(state)
                    Data["Registered_Users"].append(registered_users)
                    Data["App_opens"].append(app_opens)
                    Data["State"].append(i)
                    Data["Year"].append(j)
                    Data["Quarter"].append(int(k.strip(".json")))
    Map_user = pd.DataFrame(Data)
    return Map_user


#==============================     DATA     /     TOP     /     TRANSACTION     =========================================#
def top_trans():
    path = "C:\\Users\\Dell\\OneDrive\\Desktop\\DS_Course\\Projects\\PhonePe_Data_Visualisation\\PhonePe_Data\\data\\top\\transaction\\country\\india\\state\\"
    Top_state_list = os.listdir(path)

    Data = {"State": [], "Year": [], "Quarter": [], "Entity_Name": [],"Count": [],
            "Amount": []}

    for i in Top_state_list:
        path_i = path + i + "\\"
        Top_year = os.listdir(path_i)

        for j in Top_year:
            path_j = path_i + j + "\\"
            Top_year_list = os.listdir(path_j)

            for k in Top_year_list:
                path_k = path_j + k
                data = open(path_k, "r")
                D = json.load(data)
                """states = D["data"].get("states",[])
                if states is not None:
                    for state in states:
                        Entity_Name = state["entityName"]
                        Count = state["metric"]["count"]
                        Amount = state["metric"]["amount"]
                        Data["Entity_Name"].append(Entity_Name)
                        Data["Entity_Type"].append(state)
                        Data["Count"].append(Count)
                        Data["Amount"].append(Amount)
                        Data["State"].append(i)
                        Data["Year"].append(j)
                        Data["Quarter"].append(int(k.strip(".json")))

                districts = D["data"].get("districts",[])
                if districts is not None:
                    for district in districts:
                        Entity_Name = district["entityName"]
                        Count = district["metric"]["count"]
                        Amount = district["metric"]["amount"]
                        Data["Entity_Name"].append(Entity_Name)
                        Data["Entity_Type"].append(district)
                        Data["Count"].append(Count)
                        Data["Amount"].append(Amount)
                        Data["State"].append(i)
                        Data["Year"].append(j)
                        Data["Quarter"].append(int(k.strip(".json")))"""

                pincodes = D["data"].get("pincodes",[])
                if pincodes is not None:
                    for pincode in pincodes:
                        Entity_Name = pincode["entityName"]
                        Count = pincode["metric"]["count"]
                        Amount = pincode["metric"]["amount"]
                        Data["Entity_Name"].append(Entity_Name)
                        Data["Count"].append(Count)
                        Data["Amount"].append(Amount)
                        Data["State"].append(i)
                        Data["Year"].append(j)
                        Data["Quarter"].append(int(k.strip(".json")))
    Top_trans = pd.DataFrame(Data)
    return Top_trans

#==============================     DATA     /     TOP     /     USER     ============================================#

def top_user():
    path = "C:\\Users\\Dell\\OneDrive\\Desktop\\DS_Course\\Projects\\PhonePe_Data_Visualisation\\PhonePe_Data\\data\\top\\user\\country\\india\\state\\"
    Top_state_list = os.listdir(path)

    Data = {"State": [], "Year": [], "Quarter": [], "Name": [], "Registered_Users":[]}

    for i in Top_state_list:
        path_i = path + i + "\\"
        Top_year = os.listdir(path_i)

        for j in Top_year:
            path_j = path_i + j + "\\"
            Top_year_list = os.listdir(path_j)

            for k in Top_year_list:
                path_k = path_j + k
                data = open(path_k, "r")
                D = json.load(data)
                """states = D["data"].get("states", [])
                if states is not None:
                    for state in states:
                        Name = state["name"]
                        Registered_users = state["registeredUsers"]
                        Data["Name"].append(Name)
                        Data["Type"].append(state)
                        Data["Registered_Users"].append(Registered_users)
                        Data["State"].append(i)
                        Data["Year"].append(j)
                        Data["Quarter"].append(int(k.strip(".json")))

                districts = D["data"].get("districts", [])
                if districts is not None:
                    for district in districts:
                        Name = district["name"]
                        Registered_users = district["registeredUsers"]
                        Data["Name"].append(Name)
                        Data["Type"].append(district)
                        Data["Registered_Users"].append(Registered_users)
                        Data["State"].append(i)
                        Data["Year"].append(j)
                        Data["Quarter"].append(int(k.strip(".json")))"""

                pincodes = D["data"].get("pincodes", [])
                if pincodes is not None:
                    for pincode in pincodes:
                        Name = pincode["name"]
                        Registered_users = pincode["registeredUsers"]
                        Data["Name"].append(Name)
                        Data["Registered_Users"].append(Registered_users)
                        Data["State"].append(i)
                        Data["Year"].append(j)
                        Data["Quarter"].append(int(k.strip(".json")))
    Top_user = pd.DataFrame(Data)
    return Top_user

Agg_trans = agg_trans()
Agg_user = agg_user()
Map_trans = map_trans()
Map_user = map_user()
Top_trans = top_trans()
Top_user = top_user()

#connecting to mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456"

)
mycursor = mydb.cursor()
mycursor.execute("create database if not exists phonepe_pulse")
mycursor.close()
mydb.close()
Engine = create_engine('mysql+pymysql://root:123456@localhost/phonepe_pulse')

Agg_trans.to_sql("aggregated_transaction", Engine,if_exists="replace",index=False,
                 dtype={"State":sqlalchemy.types.VARCHAR(length=50),
                        "Year":sqlalchemy.types.Integer,
                        "Quarter":sqlalchemy.types.Integer,
                        "Transaction_Name": sqlalchemy.types.VARCHAR(length=255),
                        "Transaction_Count": sqlalchemy.types.Integer,
                        "Transaction_Amount": sqlalchemy.types.FLOAT(precision=5, asdecimal=True)
                 })

Agg_user.to_sql("aggregated_user", Engine,if_exists="replace",index=False,
                 dtype={"State":sqlalchemy.types.VARCHAR(length=50),
                        "Year":sqlalchemy.types.Integer,
                        "Quarter":sqlalchemy.types.Integer,
                        "Brand": sqlalchemy.types.VARCHAR(length=255),
                        "Count": sqlalchemy.types.Integer,
                        "Percentage": sqlalchemy.types.FLOAT(precision=5, asdecimal=True)
                 })

Map_trans.to_sql("map_transaction", Engine,if_exists="replace",index=False,
                 dtype={"State":sqlalchemy.types.VARCHAR(length=50),
                        "Year":sqlalchemy.types.Integer,
                        "Quarter":sqlalchemy.types.Integer,
                        "Transaction_Name": sqlalchemy.types.VARCHAR(length=255),
                        "Transaction_Count": sqlalchemy.types.Integer,
                        "Transaction_Amount": sqlalchemy.types.FLOAT(precision=5, asdecimal=True)
                 })

Map_user.to_sql("map_user", Engine,if_exists="replace",index=False,
                 dtype={"State":sqlalchemy.types.VARCHAR(length=50),
                        "Year":sqlalchemy.types.Integer,
                        "Quarter":sqlalchemy.types.Integer,
                        "District": sqlalchemy.types.VARCHAR(length=255),
                        "Registered_Users": sqlalchemy.types.Integer,
                        "App_opens": sqlalchemy.types.Integer
                 })

Top_trans.to_sql("top_transaction", Engine,if_exists="replace",index=False,
                 dtype={"State":sqlalchemy.types.VARCHAR(length=50),
                        "Year":sqlalchemy.types.Integer,
                        "Quarter":sqlalchemy.types.Integer,
                        "Entity_Name": sqlalchemy.types.VARCHAR(length=255),
                        "Count": sqlalchemy.types.Integer,
                        "Amount": sqlalchemy.types.FLOAT(precision=5, asdecimal=True)
                 })

Top_user.to_sql("top_user", Engine,if_exists="replace",index=False,
                 dtype={"State":sqlalchemy.types.VARCHAR(length=50),
                        "Year":sqlalchemy.types.Integer,
                        "Quarter":sqlalchemy.types.Integer,
                        "Name": sqlalchemy.types.VARCHAR(length=255),
                        "Registered_Users": sqlalchemy.types.Integer,

                 })
