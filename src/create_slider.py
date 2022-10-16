import pandas as pd
import plotly.express as px


def get_updated_dataframe(sector):
    df = pd.read_json('../data/cumulative/' + sector + '.json', typ='dictionary')
    df_mod = pd.DataFrame({'date': df.index, 'value': df.values})
    df_mod["sector"] = sector
    return df_mod


df_healthcare = get_updated_dataframe("Healthcare")
df_technology = get_updated_dataframe("Technology")
df_real_estate = get_updated_dataframe("Real Estate")

final_df = pd.concat([df_healthcare, df_technology, df_real_estate])
final_df['month'] = final_df['date'].dt.strftime('%b %Y')

print(final_df)

# generate the plot
fig = px.bar(
    final_df,
    x="value",
    y="sector",
    text="value",
    orientation="h",
    animation_frame="month",
)

# a bit of formatting...
fig = fig.update_traces(texttemplate="%{text:4s}")

for f in fig.frames:
    for t in f["data"]:
        t["texttemplate"] = "%{text:4s}"

fig.update_layout(xaxis={"range": [-10, final_df["value"].max() * 1.25]})
fig.show()
