import altair as alt
import pandas as pd
import streamlit as st


neiss = pd.read_csv('neiss_head_injuries.tsv', sep='\t')

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
    tooltip=["Disposition", "Product",  "count():Q"]
).add_selection(
    selector
).transform_filter(
    selector
).properties(
    title='Head Injury Severity by Product',
)

st.altair_chart(chart, use_container_width=True)
