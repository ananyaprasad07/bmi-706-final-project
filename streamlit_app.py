import altair as alt
import pandas as pd
import streamlit as st


neiss = pd.read_csv('neiss_head_injuries.tsv', sep='\t')

st.write("Head Injuries Across the United States")

default_products = []
products = st.multiselect("Products", options=list(neiss["Product_1"].unique()), default=default_products)
subset = neiss[neiss["Product_1"].isin(products)]

chart = alt.Chart(subset).mark_bar().encode(
    x=alt.X("Product_1:O", title="Product Type"),
    y=alt.Y("count():Q", title="Number of Injuries"),
    color=alt.Color('Disposition:O', title='Disposition', legend=alt.Legend(title="Disposition")),
    tooltips=[]
).properties(
    title='Head Injury Severity by Product',
    width=600,
    height=400
)

st.altair_chart(chart, use_container_width=True)
