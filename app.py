import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


st.title("Aircrash Analysis")


def load_data():
    df = pd.read_csv("aircrahesFullDataUpdated_2024 (4).csv")
    df = df.sort_values(by = "Year")
    df = df.reset_index(drop=True)
    df.loc[:,"Country/Region"]=df.loc[:,"Country/Region"].str.replace("'-",'').str.replace("?",'').str.replace("10",'').str.replace("100",'').str.replace("110","None").str.replace("116","None").str.replace("18","None").str.replace("325","None").str.replace("570","None").str.replace("800","None")
    df.loc[:,"Country/Region"]=df.loc[:,"Country/Region"].fillna("None")
    df.loc[:,"Aircraft Manufacturer"]=df.loc[:,"Aircraft Manufacturer"].str.replace("?",'').str.replace("139","None").str.replace("42","None")
    df.loc[:,"Aircraft"]=df.loc[:,"Aircraft"].str.replace("?",'')
    df.loc[:,"Location"]=df.loc[:,"Location"].str.replace("?",'')
    df.loc[:,"Operator"]=df.loc[:,"Operator"].fillna("None")
    df.loc[:,"Survival"]= df["Aboard"]- df["Fatalities (air)"]
    return df

data = load_data()



filters = {
    "Year":data["Year"].unique(),
    "Month":data["Month"].unique(),
    "Country/Region":data["Country/Region"].unique(),
    "Aircraft Manufacturer":data["Aircraft Manufacturer"].unique(),
    "Aircraft":data["Aircraft"].unique(),
    "Location":data["Location"].unique(),
    "Operator":data["Operator"].unique()
}

selected_filters = {}

for key, options in filters.items():
    selected_filters[key] = st.sidebar.multiselect(key,options)

filtered_data = data 
for key,selected_values in selected_filters.items():
    if selected_values:
        filtered_data = filtered_data[filtered_data[key].isin(selected_values)]

st.dataframe(filtered_data)

no_of_items=len(filtered_data)
total_Aboard = filtered_data["Aboard"].sum()
avg_Aboard = filtered_data["Aboard"].mean()
total_fatalities = filtered_data["Fatalities (air)"].sum()
avg_fatalities = filtered_data["Fatalities (air)"].mean()
total_Survived = filtered_data["Survival"].sum()
avg_survived = filtered_data["Survival"].mean()

# streamlit column component
col1, col2, col3, col4, col5= st.columns(5)
with col1:
    st.metric("NO OF CRASHES",no_of_items)
    
with col2:
    st.metric("TOTAL ABOARD",total_Aboard)
    
with col3:
    st.metric("AVERAGE ABOARD",avg_Aboard)

with col4:
    st.metric("AVERAGE FATALITIES", avg_fatalities)
    
with col5:
    st.metric("AVERAGE SURVIVAL", avg_survived)
    

### 1.  What is the total fatalities in the last 15 years?

dead_cases = data.groupby(["Year"])["Fatalities (air)"].sum().reset_index()
last_15_dead = dead_cases.sort_values(by="Year",ascending=True).tail(15)
bar1=px.bar(last_15_dead,x="Year",y="Fatalities (air)", title = "Total Number of People That Died In The Last 15 Years")
np.arange(2010,2024)

st.plotly_chart(bar1)

### 2. What is the number of survivors in the last 15 years?

survived_cases = data.groupby(["Year"])["Survival"].sum().reset_index()
last_15 = survived_cases.sort_values(by="Year",ascending=True).tail(15)
bar1=px.bar(last_15,x="Year",y="Survival", title = "Total Number of People That Survived In The Last 15 Years")
np.arange(2010,2024)

st.plotly_chart(bar1)


### 3. Which month has the highest number of Aircrashes?

top_10= data["Month"].value_counts().reset_index()
bar1=px.bar(top_10,x="Month",y="count", title = "Month With The Highest Number of Crashes")

st.plotly_chart(bar1)


### 4. Which country has the highest number of crashes?

country_counts= data["Country/Region"].value_counts().reset_index().head(10)
country_counts.columns = ["Country/Region", "Count"]

fig= px.choropleth(country_counts,locations="Country/Region",
                   locationmode="country names",
                   color="Count",
                   color_continuous_scale="Viridis",
                   title= "Country With The Highest Number of Crashes")
st.plotly_chart(fig)










    



    






