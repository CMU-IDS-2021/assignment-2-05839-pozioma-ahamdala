import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
import datetime

st.title("Hamdy, Let's analyze some Penguin Data 🐧📊.")

#@st.cache  # add caching so we load the data only once
def load_data():
    # Load the penguin data from https://github.com/allisonhorst/palmerpenguins.
    penguins_url = "nga_subnational_covid19_hera.xlsx - Feuil1.csv"
    return pd.read_csv(penguins_url)

#The map starts here

#html_temp = """
   # <div class='tableauPlaceholder' id='viz1615584326049' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_16155695091580&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Book1_16155695091580&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_16155695091580&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1615584326049');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='900px';vizElement.style.height='527px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='900px';vizElement.style.height='527px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
 #   """
#components.html(html_temp, width=1000, height=1000)

#The map ends here, we will move it as appropraite


df = pd.read_excel('Copy of nga_subnational_covid19_hera.xlsx')


#The new cases and cumulative cases
df['New Cases'] = df['CONTAMINES']
df_cases_by_date = df.groupby(df['DATE']).sum()
df_cases_by_date = df_cases_by_date.reset_index()
df_cases_by_date['Active Cases (in hundreds)'] = (df_cases_by_date['CONTAMINES'].cumsum())/100

new_and_cum_cases = alt.Chart(df_cases_by_date).transform_fold(
    ['New Cases', 'Active Cases (in hundreds)'],
).mark_line().encode(
    alt.X('DATE:T'),
    alt.Y('value:Q', title=''),
    color='key:N'
).interactive()

lockdown_date = datetime.datetime(2020,3,30)
no_of_cases_first_lockdown = df_cases_by_date.loc[ df_cases_by_date['DATE']==lockdown_date, 'CONTAMINES']

first_lockdown_start = pd.DataFrame([{"first_lockdown": lockdown_date, "CONTAMINES": no_of_cases_first_lockdown} ])
 
first_lockdown_start_line = alt.Chart(first_lockdown_start).mark_point(size=300).encode(
    alt.X('first_lockdown:T', title='fghjj '), color=alt.value('red'), y='CONTAMINES:Q'
)

st.write((new_and_cum_cases+first_lockdown_start_line).interactive().properties(width=800))
#(new_and_cum_cases+first_lockdown_start_line).interactive().properties(width=800)
st.write(first_lockdown_start_line)
