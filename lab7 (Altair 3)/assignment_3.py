# %% [markdown]
# # **Altair Assignment 3**

# %% [markdown]
# ## Overview
# 
# Today we are going to work with Gapminder dataset and will build our visualizations of that data. Data source:
# https://www.kaggle.com/datasets/albertovidalrod/gapminder-dataset?resource=download
# 
# ## Assignment Instructions
# * Save the `altair-assignment-3.ipynb` file, rename it, and submit the modified file (use your username in the name).
# * Run every cell (do Runtime -> Restart and run all to make sure you have a clean working version), print to pdf, submit the pdf file.
# * If you end up stuck, show us your work by including links (URLs) that you have searched for. You'll get partial credit for showing your work in progress.
# 
# ## Resources
# *  [Interactive Charts Documentation](https://altair-viz.github.io/user_guide/interactions/index.html)
# *  [Interactive Charts Example Gallery](https://altair-viz.github.io/gallery/index.html#interactive-chartsb)
# *  [Multiple Interactions](https://altair-viz.github.io/gallery/multiple_interactions.html)

# %% [markdown]
# ## Environment Setup

# %%
#package that converts vega-lite charts into static images
%pip install vl-convert-python

# %%
# imports we will use
import altair as alt
import pandas as pd

# %% [markdown]
# ## Data Import

# %%
#Load the gapminder dataset
gapminderURL = "https://raw.githubusercontent.com/yellstales/si649public/refs/heads/main/altair03assignment/gapminder.csv"
gapminder = pd.read_csv(gapminderURL)

# Display first few rows of the energy prices data
gapminder.head()

# %% [markdown]
# The gapminder dataset contains:
# 
# * `country`: Country name
# * `continent`: Continent the country belongs to (Africa, Asia, Europe, North America, Oceania, South America)
# * `year`: Year of observation, ranging from 1998 to 2018
# * `life_exp`: Life expectancy at birth (in years)
# * `hdi_index`: Human Development Index score (0 to 1 scale)
# * `co2_consump`: CO₂ consumption per capita (metric tons)
# * `gdp`: GDP per capita (in USD)
# * `services`: Services sector as a percentage of GDP

# %% [markdown]
# # Part 1: Recreate Gapminder

# %% [markdown]
# ## Checkpoint 1: Gapminder 2015 Snapshot

# %% [markdown]
# The Gapminder dataset captures decades of global development data, making 2015 a compelling snapshot of the modern world.
# 
# ### Task:
# Create an interactive scatter plot of the Gapminder dataset filtered to the year 2015
# 
# ### Requirements:
# 1. Use `transform_filter()` to filter the data to the year of 2015
# 2. Place GDP per capita on the X axis (using a log scale) and life expectancy on the Y axis. Use descriptive axis titles rather than raw variable names.
# 3. Adjust the `domain` of the Y axis to be in the range `[45, 90]`
# 4. Encode continent as the color of each point
# 5. Add a legend selection so that clicking a continent highlights its countries while fading out all others (either in color or opacity, or both)
# 6. Add a tooltip that displays country name, continent, GDP per capita, life expectancy, and HDI. Tooltip elements should have a descriptive title rather than a variable name
# 7. Add a meaningful title
# 8. Add interactivity so that the user can zoom and pan across the chart
# 
# Note: Gapminder [uses log-scale (doubling in particular)](https://www.gapminder.org/tag/gapminder-world/#:~:text=LIFE%20EXPECTANCY:%20IHME%20%E2%80%93%20Institute%20for,PPP%20(constant%202011%20international%20$) for GDP per capita. You can change the scale in Altair setting `scale` to `alt.Scale(type='pow', exponent=0.5)` to achieve that

# %%
## Checkpoint 1

# legend selection for continent
legend_selection = alt.selection_point(fields=['continent'], bind='legend')

# opacity condition
opacityCondition = alt.when(legend_selection).then(alt.value(1.0)).otherwise(alt.value(0.1))

alt.Chart(gapminder).mark_circle(size=80).encode(
    x=alt.X('gdp:Q', title='GDP per Capita (USD)', scale=alt.Scale(type='pow', exponent=0.5)),
    y=alt.Y('life_exp:Q', title='Life Expectancy (years)', scale=alt.Scale(domain=[45, 90])),
    color='continent:N',
    opacity=opacityCondition,
    tooltip=[
        alt.Tooltip('country:N', title='Country'),
        alt.Tooltip('continent:N', title='Continent'),
        alt.Tooltip('gdp:Q', title='GDP per Capita'),
        alt.Tooltip('life_exp:Q', title='Life Expectancy'),
        alt.Tooltip('hdi_index:Q', title='HDI')
    ]
).transform_filter(
    alt.datum.year == 2015
).add_params(
    legend_selection
).properties(
    title='Gapminder 2015: GDP per Capita vs Life Expectancy',
    width=600,
    height=400
).interactive()

# %% [markdown]
# ## Checkpoint 2: Gapminder Interactive Chart

# %% [markdown]
# Now let's try to recreate part of the original Gapminder, by enabling users to view the change in data over two decades.
# 
# ###Task:
# Starting from your Checkpoint 1 code, add a slider that filters the chart to any year between 1998 and 2018.
# 
# ###Requirements:
# 
# 1. Copy your Checkpoint 1 code as a starting point
# 2. Adjust the domain of the Y axis to accommodate the full range of life expectancy values across all years
# 3. Fix the domain for the X axis, so it won't change with the change in data
# 4. Add a year slider using alt.binding_range() and the appropriate selector type that dynamically filters the chart to the selected year
# 5. Add a large, faded year label as a background watermark that updates dynamically as the slider moves.

# %%
## Checkpoint 2

# year slider
year_slider = alt.binding_range(min=1998, max=2018, step=1, name='Year: ')
year_selector = alt.param(bind=year_slider, name='yr', value=2015)

# legend selection for continent
legend_selection = alt.selection_point(fields=['continent'], bind='legend')
opacityCondition = alt.when(legend_selection).then(alt.value(1.0)).otherwise(alt.value(0.1))

# base scatter chart (copied from Checkpoint 1, with fixed domains for both axes)
base_chart = alt.Chart(gapminder).mark_circle(size=80).encode(
    x=alt.X('gdp:Q', title='GDP per Capita (USD)',
            scale=alt.Scale(type='pow', exponent=0.5, domain=[0, 130000])),
    y=alt.Y('life_exp:Q', title='Life Expectancy (years)',
            scale=alt.Scale(domain=[40, 90])),
    color='continent:N',
    opacity=opacityCondition,
    tooltip=[
        alt.Tooltip('country:N', title='Country'),
        alt.Tooltip('continent:N', title='Continent'),
        alt.Tooltip('gdp:Q', title='GDP per Capita'),
        alt.Tooltip('life_exp:Q', title='Life Expectancy'),
        alt.Tooltip('hdi_index:Q', title='HDI')
    ]
).transform_filter(
    "datum.year == yr"
).add_params(
    legend_selection
).interactive()

## background year watermark
background_year = alt.Chart(gapminder).mark_text(
    fontSize=120, opacity=0.15, color='gray'
).encode(
    text='year:N'
).transform_filter(
    "datum.year == yr"
).transform_aggregate(
    year='max(year)'
)

(background_year + base_chart).add_params(
    year_selector
).properties(
    title='Gapminder: GDP per Capita vs Life Expectancy Over Time',
    width=600,
    height=400
)

# %% [markdown]
# # Part 2: Create your own visualization

# %% [markdown]
# Design and build one original interactive visualization using this dataset.
# 
# ### Requirements
# 1. Use at least 2 different widgets (any combination of slider, dropdown, radio, checkbox)
# 2. Create a compound visualization using at least 2 different charts
# 3. Use at least 1 conditional encoding
# 4. Add a meaningful title(s)
# 5. Below the chart write 2-3 sentence summary about what questions your visualization answers and what you found

# %%
## Part 2: HDI vs CO2 Consumption Dashboard

# --- Widget 1: Year slider ---
year_slider = alt.binding_range(min=1998, max=2018, step=1, name='Year: ')
year_param = alt.param(bind=year_slider, name='sel_year', value=2015)

# --- Widget 2: Continent dropdown ---
continents = sorted(gapminder['continent'].unique().tolist())
continent_dropdown = alt.binding_select(options=[None] + continents, labels=['All'] + continents, name='Continent: ')
continent_selection = alt.selection_point(fields=['continent'], bind=continent_dropdown)

# --- Conditional encoding: highlight high-HDI countries (>= 0.8) ---
colorCondition = alt.when(
    alt.datum.hdi_index >= 0.8
).then(alt.value('steelblue')).otherwise(alt.value('orange'))

# --- Chart 1: Scatter plot of HDI vs CO2 consumption ---
scatter = alt.Chart(gapminder).mark_circle(size=70).encode(
    x=alt.X('hdi_index:Q', title='Human Development Index',
            scale=alt.Scale(domain=[0.2, 1.0])),
    y=alt.Y('co2_consump:Q', title='CO₂ per Capita (metric tons)',
            scale=alt.Scale(domain=[0, 50])),
    color=colorCondition,
    tooltip=[
        alt.Tooltip('country:N', title='Country'),
        alt.Tooltip('continent:N', title='Continent'),
        alt.Tooltip('hdi_index:Q', title='HDI'),
        alt.Tooltip('co2_consump:Q', title='CO₂ per Capita'),
        alt.Tooltip('year:Q', title='Year')
    ]
).transform_filter(
    "datum.year == sel_year"
).transform_filter(
    continent_selection
).properties(
    width=400, height=350,
    title='HDI vs CO₂ Consumption (blue = HDI ≥ 0.8)'
)

# --- Chart 2: Bar chart of mean CO2 by continent ---
bars = alt.Chart(gapminder).mark_bar().encode(
    x=alt.X('mean(co2_consump):Q', title='Mean CO₂ per Capita'),
    y=alt.Y('continent:N', sort='-x', title=None),
    color='continent:N'
).transform_filter(
    "datum.year == sel_year"
).transform_filter(
    continent_selection
).properties(
    width=400, height=350,
    title='Mean CO₂ Consumption by Continent'
)

(scatter | bars).add_params(
    year_param, continent_selection
).properties(
    title='Global Development: HDI and CO₂ Emissions'
)

# %% [markdown]
# **Summary:**
# 
# This visualization explores the relationship between human development (HDI) and CO₂ emissions per capita across countries and continents over time. The scatter plot reveals a clear positive correlation: countries with higher HDI tend to have higher CO₂ consumption, with most high-HDI countries (blue, HDI ≥ 0.8) clustering in the upper-right region. The bar chart shows that Europe and North America consistently lead in mean CO₂ emissions, while Africa remains the lowest emitter despite having the lowest HDI scores. Using the year slider, we can observe that global CO₂ emissions have generally increased from 1998 to 2018, though the HDI-CO₂ relationship remains stable across all years.
# 

# %% [markdown]
# #Submission

# %% [markdown]
# * Save the altair-assignment-3.ipynb file, rename it, and submit the modified file (use your username in the name).
# * You need to turn in two deliverables to Canvas: 1) Combined html with all 3 visualizations and summary for the last visualization; 2) .ipynb file

# %% [markdown]
# You can use this code as a starting point to combine your scripts:
# ```
# <!DOCTYPE html>
# <html>
# <head>
#   <meta charset="UTF-8">
#   <style>
#     #vis.vega-embed {
#       width: 100%;
#       display: flex;
#     }
# 
#     #vis.vega-embed details,
#     #vis.vega-embed details summary {
#       position: relative;
#     }
#   </style>
#   <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/vega@5"></script>
#   <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/vega-lite@5.20.1"></script>
#   <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
# </head>
# <body>
#   <h1>Part 1: Checkpoint 1</h1>
#   <div id="checkpoint1"></div>
# 
#   <br/>
#   <br/>
# 
#   <h1>Part 1: Checkpoint 2</h1>
#   <div id="checkpoint2"></div>
# 
#   <br/>
#   <br/>
# 
#   <h1>Part 2</h1>
#   <div id="part2"></div>
# 
# 
#    <!-- Add script for checkpoint 1. Don't forget to change id in the selector from 'vis' to 'checkpoint1'-->
# 
#    <!-- Add script for checkpoint 2. Don't forget to change id in the selector from 'vis' to 'checkpoint2'-->
# 
#    <!-- Add script for checkpoint 3. Don't forget to change id in the selector from 'vis' to 'part2'-->
# 
# </body>
# </html>
# ```


