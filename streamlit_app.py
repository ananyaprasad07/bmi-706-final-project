import altair as alt
import pandas as pd
import streamlit as st

neiss = pd.read_csv('neiss_head_injuries.tsv', sep='\t')

st.write("Injury Severity by Product")

default_products = []
products = st.multiselect("Products", options=list(neiss["Product_1"].unique()), default=default_products)
subset = neiss[neiss["Products"].isin(products)]

chart_product = alt.Chart(subset).mark_bar().encode(
    x=alt.X("Product_1", title="Product Type"),
    y=alt.Y("sum()").sort('-x')
)

st.altair_chart(chart_product, use_container_width=True)
