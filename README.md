# Visualizing Head Injuries across the United States

#### Authors
Ananya Prasad, Lanxin Zhang

## Description
This data visualization project is for the BMI 706 Final Project

## Intructions
### Data files
1. `neiss_head_injuries.tsv`
2. `neiss2022.tsv.zip`
3. `neiss2023.tsv.zip`

If you wish to recreate `neiss_head_injuries.tsv` , follow the below steps, if not, skip to the next section of this README:
1. Download the zipped files `neiss2022.tsv.zip` and `neiss2023.tsv.zip`
2. Download the data processing script `data_processing.py`
3. Unzip the two files into a directory containing `data_processing.py`
   `unzip <filename>.zip`
4. Run `data_processing.py`
5. A file will be created named `neiss_head_injuries.tsv`

This is the file we used for our visualizations

## Details

### Demographics of Head Injuries
This graph answers the question: "Who gets head injuries?"
It visualizes the distribution of head injuries by:
1. Age
2. Sex
3. Race

How to use: 
1. Select the Race you wish to visualize using the dropdown bar
2. The stacked bar chart shows the split of genders within each age group
3. Take a look at the pie charts below the stacked bar chart to study each demographic in more detail
4. Hover over any aspect of the graph to know who that aspect represents

### Head Injury Severity by Product
This graph answers the question: "Which products cause severe head injuries?"

How to use:
1. Select a combination of products from the dropdown menu : the choices are the top 20 injury-causing products
2. Stacked bar chart shows the distribution of injury severity within that product category
3. Hover over the any aspect of the graph to know who that aspect represents
4. Click on any disposition in the legend bar to get a closer look at the distribution for that disposition

### Location and Seasonal Patterns in Head Injuries
This graph answers the question: "Are there any location based or seasonal patterns of head injuries?"

How to use:
1. Select the locations and year you wish to visualize
2. Hover over the any aspect of the graph to know the disposition 




