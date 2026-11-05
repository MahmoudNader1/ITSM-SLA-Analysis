import pandas as pd
import numpy as np 
df = pd.read_csv("ITSM_SLA_Raw_Dataset.csv")
# print(df.head())
# print(df.isnull().sum())
# print(df.duplicated().sum())
# print(df.describe())
# print(df.info())
df.columns=df.columns.str.strip().str.title()
text_coulmn=["Ticket_Type","Category","Priority","Status","Assigned_Team","Assigned_Agent","Channel","Location","Description"]
for col in text_coulmn:
    df[col]=df[col].str.strip().str.title()
df["Created_Date"]=pd.to_datetime(df["Created_Date"],errors="coerce")
df["First_Response_Date"]=pd.to_datetime(df["First_Response_Date"],errors="coerce")
df["Resolved_Date"]=pd.to_datetime(df["Resolved_Date"],errors="coerce")
df["Closed_Date"]=pd.to_datetime(df["Closed_Date"],errors="coerce")
# df["Customer_Satisfaction"]=df["Customer_Satisfaction"].fillna()
mising_category=df.loc[df["Category"].isnull()]
# print(mising_category[
#     ["Ticket_Id", "Ticket_Type", "Description", "Priority", "Status"]
# ])
category_mapping = {
    "Laptop Is Running Slowly": "Hardware",
    "Printer Is Not Responding": "Hardware",
    "Application Error After Update": "Software",
    "Vpn Connection Failed": "Network",
    "Suspicious Login Alert": "Security",
    "User Cannot Access Email": "Email",
    "Internet Connection Intermittent": "Network"
}
df["Category"]=df["Category"].fillna(
    df["Description"].map(category_mapping)
)
mising_Assigned_Team=df.loc[df["Assigned_Team"].isnull()]
# print(pd.crosstab(df["Category"], df["Assigned_Team"]))
mising_date = df.groupby("Status")[["First_Response_Date","Resolved_Date","Closed_Date"]].apply(lambda x :x.isnull().sum())
# print("First Response Before Created:")
# print((df["First_Response_Date"] < df["Created_Date"]).sum())

# print("Resolved Before Created:")
# print((df["Resolved_Date"] < df["Created_Date"]).sum())

# print("Closed Before Resolved:")
# print((df["Closed_Date"] < df["Resolved_Date"]).sum())
duplicates = df[df.duplicated(keep=False)]
df=df.drop_duplicates()
# print(df["Ticket_Id"].duplicated().sum())
# print(df.describe())
df.to_csv("ITSM_SLA_Cleaned.csv", index=False)