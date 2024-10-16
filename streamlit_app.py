import altair as alt
import pandas as pd
import streamlit as st


neiss = pd.read_csv('neiss_head_injuries.tsv', sep='\t')

st.write("Head Injuries Across the United States")

## Products vs Injury Severity Graph ##

# subseting to required data
neiss_products = neiss
top_products = neiss_products['Product_1'].value_counts().nlargest(20).index
neiss_products = neiss_products[neiss_products['Product_1'].isin(top_products)]

# creating product dropdown selector
default_products = ['FLOORS OR FLOORING MATERIALS', 
                    'BASKETBALL, ACTIVITY AND RELATED EQUIPMENT', 
                    'SOFAS, COUCHES, DAVENPORTS, DIVANS OR STUDIO COUCHES']

products = st.multiselect("Products", options=list(neiss_products["Product_1"].unique()), default=default_products)
subset = neiss_products[neiss_products["Product_1"].isin(products)]

# labels for legend
label = "if(datum.value == 1, '1: Treated, Released', " \
             "if(datum.value == 2, '2: Treated, Tranferred', " \
             "if(datum.value == 3, '3: Treated, Admitted', " \
             "if(datum.value == 4, '4: Held', " \
             "if(datum.value == 5, '5: Left Against Medical Advice', " \
             "'6: Death')))))"

# stacked bar chart of injuries
chart = alt.Chart(subset).mark_bar().encode(
    x=alt.X("Product_1:O", title="", axis=alt.Axis(labelAngle=0, labelLimit=500)),
    y=alt.Y("count():Q", title="Number of Injuries"),
    color=alt.Color('Disposition:O', title='Disposition', 
                    scale=alt.Scale(scheme='reds'), 
                    legend=alt.Legend(title="Disposition", labelExpr=label)),
    tooltip=["Disposition", "Product_1",  "count():Q"]
).properties(
    title='Head Injury Severity by Product',
)

st.altair_chart(chart, use_container_width=True)
