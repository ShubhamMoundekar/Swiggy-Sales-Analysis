#!/usr/bin/env python
# coding: utf-8

# # Swiggy Sales Analysis

# ### Import Libraries

# In[45]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# In[46]:


Data = pd.read_excel(r"C:\Users\ACER\Downloads\swiggy_data.xlsx")


# In[47]:


Data.head()


# In[48]:


Data.tail()


# ### Metadeta

# In[49]:


print("No of rows",Data.shape[0])


# In[50]:


print("No of Columns",Data.shape[1])


# In[51]:


Data.info


# ### Datatype

# In[52]:


Data.dtypes


# In[53]:


Data.describe()


# # KPI's

# ### Total sales 

# In[54]:


total_sales = Data["Price (INR)"].sum()
print("Total_sales (INR):", round(total_sales,2))


# ### Average Sales

# In[55]:


average_rating = Data["Rating"].mean()
print("Average rating (INR):", round(average_rating,2))


# ### Average Order Values

# In[56]:


average_order_value = Data["Price (INR)"].mean()
print("Average Order Value:",round(average_order_value,2))


# ### Rating counts

# In[57]:


rating_count = Data["Rating Count"].sum()
print("Rating count:",round(rating_count,2))


# ### Total Orders

# In[58]:


total_orders = Data["Order Date"].count()
print("Total Orders:",round(total_orders,2))


# # Chart Design 

# ### Monthly Sales Trends

# In[59]:


Data["Order Date"] = pd.to_datetime(Data["Order Date"])

Data["YearMonth"] = Data["Order Date"].dt.to_period("M").astype(str)

monthly_revenue = Data.groupby("YearMonth")["Price (INR)"].sum().reset_index()

plt.figure()
plt.plot(monthly_revenue["YearMonth"],monthly_revenue["Price (INR)"])
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Total Sales (INR)")
plt.title("Monthly Sales Trend")
plt.tight_layout()
plt.show()


# ### Daily Sales Trend

# In[60]:


Data["DayNames"] = pd.to_datetime(Data["Order Date"]).dt.day_name()

daily_revenue = (Data.groupby("DayNames")["Price (INR)"].sum()
                .reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
                )

plt.figure(figsize=(10,5))
plt.bar(daily_revenue.index, daily_revenue.values)
plt.title("Daily sales Trend")
plt.xlabel("Day")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=30)

plt.show()


# ### Total Sales by Food Type (Veg vs Non-Veg)

# In[61]:


non_veg_keywords = [
    "chicken","egg","fish","motton","prawn",
    "biryani","kabab","kebab","non-veg","non veg"
]
   
Data["food_category"] = np.where(Data["Dish Name"].str.lower().str.contains("|".join(non_veg_keywords),na=False),
                               "Non-veg","Veg")


# In[62]:


food_revenue = (
Data.groupby("food_category")["Price (INR)"].sum().reset_index())


# In[63]:


fig = px.pie(
food_revenue,
values = "Price (INR)",
names = "food_category",
hole=0.5,
title = "Revenue Contribution:  Veg vs Non-Veg"
)

fig.update_traces(
textinfo="percent+label",
pull = [0.05, 0]
)

fig.update_layout(
height = 500,
margin =dict (t=60, b=40, l=40, r=40)
)

fig.show()


# ### Total Sales by State

# In[64]:


fig = px.bar(
    Data.groupby("State",as_index=False)["Price (INR)"].sum()
    .sort_values("Price (INR)", ascending=False),
    x = "Price (INR)",
    y = "State",
    orientation="h",
    title="Revenue by state (INR)"
)

fig.update_layout(height=600,yaxis=dict(autorange="reversed"))
fig.show()


# ### Quarterly Performance Summary

# In[65]:


Data["Order_Date"] = pd.to_datetime(Data["Order Date"])
Data["Quarter"] = Data["Order Date"].dt.to_period("Q").astype(str)
Quarterly_summary = (
    Data.groupby("Quarter",as_index=False).agg(
    Total_sales=("Price (INR)", "sum"),
    Avg_Rating=("Rating","mean"),
    Total_Orders=("Order_Date","count")
    )
    .sort_values("Quarter")
)

Quarterly_summary["Total_sales"]=Quarterly_summary["Total_sales"].round(0)
Quarterly_summary["Avg_Rating"]=Quarterly_summary["Avg_Rating"].round(2)

Quarterly_summary


# ### Top 5 cities by Sales

# In[66]:


top_5_cities = (
      Data.groupby("City")["Price (INR)"].sum().nlargest()
      .sort_values()
      .reset_index()
)

fig = px.bar(
  top_5_cities,
  x="Price (INR)",
  y="City",
  orientation="h",
  title="Top 5 cities by sales (INR)",
  color_discrete_sequence=["red"]
)

fig.show()


# ### Weekly trander Analyst 

# In[67]:


Data["Order_Date"] = pd.to_datetime(Data["Order Date"])
weekly_sales = Data.resample('W', on='Order_Date')["Price (INR)"].sum()

plt.figure(figsize=(10,5))
plt.bar(weekly_sales.index, weekly_sales.values)
plt.title("Daily sales Trend")
plt.xlabel("Day")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=30)

plt.show()


# In[ ]:




