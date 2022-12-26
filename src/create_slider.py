import pandas as pd
import plotly.express as px


def get_updated_dataframe(sector):
    df = pd.read_json('../data/cumulative/' + sector + '.json', typ='dictionary')
    df_mod = pd.DataFrame({'date': df.index, 'price change': df.values})
    df_mod["sector"] = sector
    return df_mod


df_healthcare = get_updated_dataframe("Healthcare")
df_technology = get_updated_dataframe("Technology")
df_real_estate = get_updated_dataframe("Real Estate")
df_energy = get_updated_dataframe("Energy")
df_communication_services = get_updated_dataframe("Communication Services")
df_utilities = get_updated_dataframe("Utilities")
df_basic_materials = get_updated_dataframe("Basic Materials")
df_consumer_defensive = get_updated_dataframe("Consumer Defensive")
df_financial = get_updated_dataframe("Financial")
df_industrials = get_updated_dataframe("Industrials")
df_consumer_cyclical = get_updated_dataframe("Consumer Cyclical")


final_df = pd.concat([df_healthcare, df_technology, df_real_estate, df_energy, df_communication_services,
                      df_utilities, df_basic_materials, df_consumer_defensive, df_financial, df_industrials,
                      df_consumer_cyclical])
final_df['month'] = final_df['date'].dt.strftime('%b %Y')

print(final_df)

# generate the plot
fig = px.bar(
    final_df,
    x="price change",
    y="sector",
    text="price change",
    orientation="h",
    animation_frame="month",
)

# a bit of formatting...
fig = fig.update_traces(texttemplate="%{text:4s}")

for f in fig.frames:
    for t in f["data"]:
        t["texttemplate"] = "%{text:4s}"

fig.update_layout(xaxis={"range": [-10, final_df["price change"].max() * 1.25]})
fig.update_layout(font_size=14)
#fig.update_layout(yaxis={'categoryorder':'total ascending'})
fig.show()
