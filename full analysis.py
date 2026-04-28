import pandas as pd
df = pd.read_excel('/users/avanickzad/desktop/python_project/fashion_retail_project_dataset.xlsx')
print(df.head())
print(df.shape)
print(df.isnull().sum())
df['campaign_type']=df['campaign_type'].fillna('No Campaign')
print(df['campaign_type'].isnull().sum())

df.groupby('campaign_type')['net_sales_try'].sum()
print(df.groupby("campaign_type").agg({"net_sales_try": ["sum", "mean", "count"]}).sort_values(by=("net_sales_try", "sum"), ascending=False))
print(df.groupby('campaign_type').agg({"estimated_cogs_try": ["sum", "mean", "count"]}).sort_values(by=("estimated_cogs_try", "sum"), ascending=False))
print(df.groupby('campaign_type').agg({"estimated_profit_try":["sum","mean","count"]}).sort_values(by=("estimated_profit_try" ,"sum"), ascending=False))
summary = df.groupby(["campaign_type", "sales_channel"]).agg(total_sales=("net_sales_try", "sum"),

total_cogs=("estimated_cogs_try", "sum"), total_profit=("estimated_profit_try", "sum"),avg_order_value=("net_sales_try", "mean"), orders=("net_sales_try", "count"))
print(df.groupby('campaign_type')["satisfaction_score"].mean().sort_values(ascending=False))

df["margin"]=df["estimated_profit_try"]/df["net_sales_try"]
print (df.groupby("campaign_type").agg({"quantity":["sum", "mean", "count"]}).sort_values(by=("quantity","sum"), ascending=False))
print(df.groupby('campaign_type').agg({"margin": ["sum", "mean", "count"]}).sort_values(by=("margin","sum"), ascending=False))

df["flag_returned"]=df["returned"].map({"Yes":1,"No":0})
print(df.groupby("campaign_type").agg({"flag_returned" :["sum", "mean", "count"]}).sort_values(by=("flag_returned","sum",), ascending=False))

df["profit_calc"]=df["net_sales_try"]-df["estimated_cogs_try"]

overview = df.groupby("campaign_type").agg(total_orders=("net_sales_try", "count"), total_sales=("net_sales_try", "sum"),total_profit=("profit_calc", "sum"),
total_quantity=("quantity", "sum")
)
overview["orders_share_%"] = (overview["total_orders"] / overview["total_orders"].sum() * 100).round(2)
overview["sales_share_%"] = (overview["total_sales"] / overview["total_sales"].sum() * 100).round(2)
overview["profit_share_%"] = (overview["total_profit"] / overview["total_profit"].sum() * 100).round(2)
overview["quantity_share_%"] = (overview["total_quantity"] / overview["total_quantity"].sum() * 100).round(2)
print(overview.sort_values(by="sales_share_%", ascending=False))
summary=df.groupby("campaign_type").agg(total_sales=("net_sales_try", "sum"), total_cogs=("estimated_cogs_try","sum"), total_profit=('profit_calc' ,"sum"), avg_order_value=("net_sales_try","mean"), avg_margin=("margin", "mean"), return_rate=("flag_returned", "mean"), satisfaction=("satisfaction_score", "mean"), total_quantity=("quantity", "sum")).sort_values(by="total_profit", ascending=False)
print(overview.sort_values(by="sales_share_%", ascending=False))
print(summary.round(2))

channel_summary=df.groupby(["campaign_type", "sales_channel"]).agg(total_sales=("net_sales_try", "sum"), total_cogs=("estimated_cogs_try","sum"), total_profit=('profit_calc' ,"sum"), avg_margin=("margin", "mean"), satisfaction = ("satisfaction_score", "mean"), return_rate = ("flag_returned", "mean")).sort_values(by="total_profit", ascending=False)
print(overview.sort_values(by="sales_share_%", ascending=False))
print(channel_summary.round(2))
sales_pivot = pd.pivot_table( df,values="net_sales_try", index="campaign_type", columns="sales_channel", aggfunc="sum")
sales_pivot["Total"] = sales_pivot.sum(axis=1)
sales_pivot.loc["Total"] = sales_pivot.sum(axis=0)
sales_pivot = sales_pivot.sort_values(by="Total", ascending=False)
print(sales_pivot.round(0))
channel_total = df.groupby("sales_channel")["net_sales_try"].sum()
import matplotlib.pyplot as plt
channel_total.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Sales Share by Channel")
plt.ylabel("")
plt.show()

product_summary=df.groupby("product_category").agg(total_sales=("net_sales_try", "sum"), total_cogs=("estimated_cogs_try","sum"), total_profit=('profit_calc' ,"sum"), avg_margin=("margin", "mean"), satisfaction = ("satisfaction_score", "mean"), return_rate = ("flag_returned", "mean")).sort_values(by="total_profit", ascending=False)
print(product_summary.reset_index().round(2))

gender_summary =df.groupby(["campaign_type", "sales_channel", "customer_gender"]).agg(total_sales=("net_sales_try", "sum"), total_cogs=("estimated_cogs_try","sum"), total_profit=('profit_calc',"sum"), avg_margin=("margin", "mean"), satisfaction=("satisfaction_score", "mean")).sort_values(by="total_profit", ascending=False)
print(gender_summary.reset_index().round(2))
gender_pivot= pd.pivot_table(df, values="net_sales_try", index=["campaign_type","sales_channel"],columns="customer_gender", aggfunc="sum")
print(gender_pivot.reset_index())
gender_pivot = gender_pivot.reset_index()
gender_pivot["difference"] = gender_pivot["Female"] - gender_pivot["Male"]

gender = df.groupby(["sales_channel","customer_gender"])["net_sales_try"].sum().unstack()
share = gender.div(gender.sum(axis=1), axis=0)
share = share.sort_index()
ax = share.plot(kind="bar", stacked=True, figsize=(10,5))

plt.title("Gender Share by Campaign & Channel")
plt.xlabel("Campaign × Channel")
plt.ylabel("Share")
plt.xticks(rotation=45)
plt.legend(title="Gender")
for c in ax.containers: ax.bar_label(c, fmt="%0.1f%%", label_type="center")
plt.tight_layout()
plt.show()

city_summary = df.groupby("city").agg(total_sales=('net_sales_try', "sum"), total_cogs=("estimated_cogs_try", "sum"), total_profit=('profit_calc', "sum"), avg_margin=("margin", "mean"), satisfaction=("satisfaction_score", "mean"), orders=("net_sales_try", "count"),).sort_values(by="total_profit", ascending=False)
print(city_summary.reset_index().round(2))

df["flag_segment"]=df["customer_segment"].map({"New":1,"Returning":2,"VIP":3})
print(df.groupby(["customer_segment", "campaign_type"]).agg(total_sales=("net_sales_try", "sum"), total_cogs=("estimated_cogs_try", "sum"), total_profit=('profit_calc', "sum"), avg_margin=("margin", "mean"), satisfaction=("satisfaction_score", "mean"), orders=("net_sales_try", "count"), return_rate=("flag_returned", "mean")).sort_values(by="total_profit", ascending=False).round(2))
Customer_segment_pivot= pd.pivot_table(df, values="net_sales_try", index=["campaign_type",],columns= "customer_segment", aggfunc="sum")
print(Customer_segment_pivot.reset_index())

return_summary = df.groupby("customer_gender").agg(return_rate=("flag_returned", "mean")).sort_values(by="return_rate", ascending=False)
print(return_summary.reset_index().round(2))
return_summary = df.groupby("city").agg(return_rate=("flag_returned", "mean")).sort_values(by="return_rate", ascending=False)
print(return_summary.reset_index().round(2))

visit_summary=df.groupby("visit_frequency_last_90d").agg(total_sales=("net_sales_try", "sum"), total_cogs=("estimated_cogs_try","sum"), total_profit=('profit_calc' ,"sum"), avg_margin=("margin", "mean"), satisfaction = ("satisfaction_score", "mean"), return_rate = ("flag_returned", "mean")).sort_values(by="total_profit", ascending=False)
print(visit_summary.reset_index().round(2))

df["order_daytime"]=pd.to_datetime(df["order_datetime"]).dt.hour
order_datetime_summary= df.groupby("order_daytime").agg(total_sales=("net_sales_try", "sum"), total_cogs=("estimated_cogs_try", "sum"), total_profit=('profit_calc', "sum"), avg_margin=("margin", "mean"), satisfaction=("satisfaction_score", "mean"), orders=("net_sales_try", "count"), return_rate=("flag_returned", "mean")).sort_values(by="total_profit", ascending=False).round(2)
print(order_datetime_summary.reset_index())

df["age_group"]=pd.cut(df["customer_age"], bins=[18,25,34,42,50], labels=["18-25","26-34","35-42", "+42"])
age_group_summary=df.groupby("age_group").agg(total_sales=("net_sales_try", "sum"), total_cogs=("estimated_cogs_try","sum"), total_profit=('profit_calc' ,"sum"), avg_margin=("margin", "mean"), satisfaction = ("satisfaction_score", "mean"), return_rate = ("flag_returned", "mean")).sort_values(by="total_profit", ascending=False)
print(age_group_summary.reset_index().round(2))

import matplotlib.pyplot as plt
campaign_sales = df.groupby("campaign_type")["net_sales_try"].sum().sort_values(ascending=False)
campaign_sales.plot(kind='bar')
plt.title('Total sales by campaign')
plt.xlabel('Campaign Type')
plt.ylabel('Total Sales (TRY)')
plt.show()

channel_data=df.groupby(["campaign_type", "sales_channel"])["net_sales_try"].sum().unstack()
channel_data.plot(kind='bar', stacked=True)
plt.title('Sales by campaign for each sales channel')
plt.xlabel('campaign_type')
plt.ylabel('Net sales (TRY)')
plt.legend(title='sales_channel')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

return_rate = df.groupby(['campaign_type', 'sales_channel'])["flag_returned"].mean().unstack()
return_rate.plot(kind='bar', stacked=True)
plt.title('Return rate by campaign type')
plt.xlabel('Campaign type')
plt.ylabel('Return rate')
plt.legend(title='sales_channel')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

segment_data = df.groupby("customer_segment")["net_sales_try"].sum()
segment_data.plot(kind="bar")
plt.title("Customer Segment Sales")
plt.xlabel("Customer Segment")
plt.ylabel("Total Sales (TRY)")
plt.grid(True)
plt.tight_layout()
plt.show()

segment_return = df.groupby("customer_segment")["flag_returned"].mean()
segment_return.plot(kind="bar")
plt.title("Customer Segment Return Rate")
plt.xlabel("Cutomer Segment")
plt.ylabel("Return Rate")
plt.grid(True)
plt.tight_layout()
plt.show()
           
city_sales = df.groupby("city")["net_sales_try"].sum().sort_values()
city_sales.plot(kind="bar")
plt.title("City net sales")
plt.xlabel("City_name")
plt.ylabel("Total Sales (TRY)")
plt.grid(True)
plt.tight_layout()
plt.show()

visit_data = df.groupby("visit_frequency_last_90d")["net_sales_try"].sum()
visit_data.plot(kind="line")
plt.title("Sales by Visit Frequency (Last 90 Days)")
plt.xlabel("Visit Frequency")
plt.ylabel("Total Sales (TRY)")
plt.grid(True)
plt.tight_layout()
plt.show()