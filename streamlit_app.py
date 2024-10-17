import altair as alt
import pandas as pd
import streamlit as st

neiss = pd.read_csv('neiss_head_injuries.tsv', sep='\t')

st.write("## Impact of Demographic factors in Head Injuries")

## Demographic factors
# select race through drop-down
race =  st.selectbox(
    "Race",
    neiss['Race'].unique(),
)
subset_p2 =  neiss[(neiss['Race'] == race)]

ages = [
    "Age <5",
    "Age 5-14",
    "Age 15-24",
    "Age 25-34",
    "Age 35-44",
    "Age 45-54",
    "Age 55-64",
    "Age >64",
]

grouped_data = subset_p2.groupby(['Age_group', 'Sex']).size().reset_index(name='Count')

chart_p2 = alt.Chart(grouped_data).mark_bar().encode(
    x=alt.X('Age_group:N', title='Age Group'),
    y=alt.Y('Count:Q', title='Number of Head Injuries'),
    color=alt.Color('Sex:N', legend=alt.Legend(title="Sex")), 
    tooltip=['Age_group', 'Sex', 'Count:Q']
).properties(
    title="Number of Head Injuries by Age Group and Sex",
    width=600,
    height=400
)

gender_counts = neiss.groupby('Sex').size().reset_index(name='Count')
gender_donut = alt.Chart(gender_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field='Count', type='quantitative'),
    color=alt.Color(field='Sex', type='nominal', legend=alt.Legend(title="Sex")),
    tooltip=['Sex', 'Count']
).properties(
    title="Head Injuries by Gender",
    width=300,
    height=300
)


age_group_counts = neiss.groupby('Age_group').size().reset_index(name='Count')
age_group_donut = alt.Chart(age_group_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field='Count', type='quantitative'),
    color=alt.Color(field='Age_group', type='nominal', legend=alt.Legend(title="Age Group")),
    tooltip=['Age_group', 'Count']
).properties(
    title="Head Injuries by Age Group",
    width=300,
    height=300
)

donut = alt.hconcat(gender_donut, age_group_donut).resolve_scale(
    # two donut charts should use different color schema
    color='independent'
)

chart_combined_p2 = alt.vconcat(chart_p2, donut
).resolve_scale(
    color='independent'
)

st.altair_chart(chart_combined_p2)


st.write("## Head Injuries Across the United States")
## Products vs Injury Severity Graph ##

# subseting to required data
neiss_products = neiss
top_products = neiss_products['Product_1'].value_counts().nlargest(20).index
neiss_products = neiss_products[neiss_products['Product_1'].isin(top_products)]

neiss_products['Product'] = neiss_products['Product_1'].str.replace(r'[^\w\s]', '', regex=True).str.split().str[0]

# creating product dropdown selector
default_products = ['FLOORS', 
                    'BASKETBALL', 
                    'SOFAS']

products = st.multiselect("Products", options=list(neiss_products["Product"].unique()), default=default_products)
subset = neiss_products[neiss_products["Product"].isin(products)]

# labels for legend
label = "if(datum.value == 1, '1: Treated, Released', " \
             "if(datum.value == 2, '2: Treated, Tranferred', " \
             "if(datum.value == 3, '3: Treated, Admitted', " \
             "if(datum.value == 4, '4: Held', " \
             "if(datum.value == 5, '5: Left Against Medical Advice', " \
             "'6: Death')))))"

# legend selector
selector=alt.selection_single(fields=['Disposition'], bind='legend')

# stacked bar chart of injuries
chart = alt.Chart(subset).mark_bar().encode(
    x=alt.X("Product:O", title="Product", axis=alt.Axis(labelLimit=500)),
    y=alt.Y("count():Q", title="Number of Injuries"),
    color=alt.Color('Disposition:O', title='Disposition', 
                    scale=alt.Scale(scheme='reds'), 
                    legend=alt.Legend(title="Disposition", labelExpr=label)),
    tooltip=[alt.Tooltip('Product'), alt.Tooltip('Disposition'), alt.Tooltip('count():Q', title='# of injuries')]
).add_selection(
).add_selection(
    selector
).transform_filter(
    selector
).properties(
    title='Head Injury Severity by Product',
)

st.altair_chart(chart, use_container_width=True)

st.write("## Location and Seasonal Pattern in Head Injuries")
## Demographic factors
# multiselectors for locations and year
locations = st.multiselect(
    "Locations",
     neiss['Location'].unique(),
     neiss['Location'].unique()
)
year = st.selectbox(
    "Year",
    neiss['Year'].unique()
)
subset_p3 = neiss[neiss["Location"].isin(locations)]
subset_p3 = subset_p3[subset_p3["Year"]==year]

months = ["Jan", "Feb", "Mar", "Apr",
          "May", "Jun", "Jul", "Aug",
          "Sep", "Oct", "Nov", "Dec"] 

chart_p3 = alt.Chart(subset_p3).mark_rect().encode(
    x=alt.X("Month:N",sort=months),
    y=alt.Y("Location:N"),
    color=alt.Color("Disposition:Q", title="Severity Score of Injury", 
                    legend=alt.Legend(title="Disposition", labelExpr=label),
                    scale=alt.Scale(domain=[1, 2, 3, 4, 5, 6]))
,
    tooltip=["Disposition"],
).properties(
    title="Locational Injury Pattern Across the Year",
)

st.altair_chart(chart_p3)


