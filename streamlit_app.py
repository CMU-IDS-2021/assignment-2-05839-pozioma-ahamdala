import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components

st.title("Hamdy, Let's analyze some Penguin Data 🐧📊.")

@st.cache  # add caching so we load the data only once
def load_data():
    # Load the penguin data from https://github.com/allisonhorst/palmerpenguins.
    penguins_url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/v0.1.0/inst/extdata/penguins.csv"
    return pd.read_csv(penguins_url)

  html_temp = """<div class='tableauPlaceholder' id='viz1615582637083' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;BF&#47;BF86NR4ZC&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;BF86NR4ZC' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;BF&#47;BF86NR4ZC&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1615582637083');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1300px';vizElement.style.height='527px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1300px';vizElement.style.height='527px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
  components.html(html_temp)
df= load_data()

st.write("Let's look at raw data in the Pandas Data Frame.")

st.write(df)

st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")

chart = alt.Chart(df).mark_point().encode(
    x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
    y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
    color=alt.Y("species")
).properties(
    width=600, height=400
).interactive()

st.write(chart)

