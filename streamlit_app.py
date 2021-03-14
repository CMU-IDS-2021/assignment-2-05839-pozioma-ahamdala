import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
import datetime

st.markdown("<h1 style='text-align: center; color: black;'>COVID-19, Restrictions and Mobility in Nigeria</h1>", unsafe_allow_html=True)
st.title("COVID-19, Restrictions and Mobility in Nigeria")

#@st.cache  # add caching so we load the data only once
def load_data():
    # Load the penguin data from https://github.com/allisonhorst/palmerpenguins.
    penguins_url = "nga_subnational_covid19_hera.xlsx - Feuil1.csv"
    return pd.read_csv(penguins_url)

#The map starts here

html_temp = """
    <div class='tableauPlaceholder' id='viz1615584326049' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_16155695091580&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Book1_16155695091580&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_16155695091580&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1615584326049');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='900px';vizElement.style.height='527px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='900px';vizElement.style.height='527px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
components.html(html_temp, width=1000, height=1000)

#The map ends here, we will move it as appropraite


df = pd.read_excel('Copy of nga_subnational_covid19_hera.xlsx')



#Situation in Nigeria at a Glance

df['New Cases'] = df['CONTAMINES']
df_cases_by_date = df.groupby(df['DATE']).sum()
df_cases_by_date = df_cases_by_date.reset_index()
df_cases_by_date['Active Cases (in hundreds)'] = ((df_cases_by_date['CONTAMINES'].cumsum()) - (df_cases_by_date['GUERIS'].cumsum()) + (df_cases_by_date['DECES'].cumsum()))/100
#df_cases_by_date['Cumulative Change in Number of Cases'] = (df_cases_by_date['CONTAMINES'].cumsum())/100

df_cases_by_date['Percentage change in active cases (from yesterday)'] = (df_cases_by_date['Active Cases (in hundreds)'].pct_change(fill_method='ffill'))*100


make = pd.DataFrame({'Trendline': ['New Cases', 'Active Cases (in hundreds)', 'Percentage change in active cases (from yesterday)']})
df2 = df_cases_by_date[['DATE', 'New Cases', 'Active Cases (in hundreds)', 'Percentage change in active cases (from yesterday)']] 
df3 = df2.melt(id_vars=['DATE'], var_name='Trendline', value_name='value')
selection = alt.selection_multi(fields=['Trendline'])
color = alt.condition(selection, alt.Color('Trendline:N'), alt.value('lightgray'))
make_selector = alt.Chart(make).mark_rect().encode(y='Trendline', color=color).add_selection(selection)
new_and_cum_cases = alt.Chart(df3).mark_line().encode(alt.X('DATE:T', title="DATE"), y=alt.Y('value:Q', title= " "), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['DATE', 'value:Q']
                                                      ).transform_filter(selection).interactive()






lockdown_date = datetime.datetime(2020,3,30)
lockdown2_date = datetime.datetime(2020,12,21)
no_of_cases_first_lockdown = df_cases_by_date.loc[ df_cases_by_date['DATE']==lockdown_date, 'CONTAMINES'].values[0]
no_of_cases_second_lockdown = df_cases_by_date.loc[ df_cases_by_date['DATE']==lockdown2_date, 'CONTAMINES'].values[0]

no_of_active_cases_first_lockdown = df_cases_by_date.loc[ df_cases_by_date['DATE']==lockdown_date, 'Active Cases (in hundreds)'].values[0]
no_of_active_cases_second_lockdown = df_cases_by_date.loc[ df_cases_by_date['DATE']==lockdown2_date, 'Active Cases (in hundreds)'].values[0]


lockdown_starts = {"DATE": [lockdown_date, lockdown2_date], "New Cases": [no_of_cases_first_lockdown, no_of_cases_second_lockdown ], "Active Cases (in hundreds)": [no_of_active_cases_first_lockdown, no_of_active_cases_second_lockdown ], "Label":["First Lockdown Starts", "Second Lockdown Starts"] }
first_lockdown_start = pd.DataFrame(lockdown_starts, columns=["DATE", "New Cases", "Active Cases (in hundreds)", "Label"])
lockdown_start = pd.DataFrame([{"DATE": lockdown_date, "New Cases": no_of_cases_first_lockdown} ])

first_lockdown_start_line = alt.Chart(first_lockdown_start).mark_point(size=200).encode(
    alt.X('DATE:T', title=''), color=alt.Color('Label:N'), y='New Cases:Q',
        
    tooltip=['DATE', 'New Cases', 'Active Cases (in hundreds)'],
).interactive()

df_cases_by_date['lockdown_date'] = lockdown_date 
first_lockdown_start = alt.Chart(df_cases_by_date).mark_rule().encode(
    alt.X('lockdown_date', title=""), color=alt.value('green'))



df_cases_by_date['lockdown2_date'] = lockdown2_date 
second_lockdown_start = alt.Chart(df_cases_by_date).mark_rule().encode(
    alt.X('lockdown2_date', title=""), color=alt.value('green'),
    tooltip=['lockdown2_date'])


text_first_lockdown = first_lockdown_start.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='lockdown_date:T'
)


text_second_lockdown = second_lockdown_start.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='lockdown2_date:T'
)

lockdown1_end = datetime.datetime(2020, 7, 27)
df_cases_by_date['lockdown1_end'] = lockdown1_end 
first_lockdown_end = alt.Chart(df_cases_by_date).mark_rule().encode(
    alt.X('lockdown1_end', title=""), color=alt.value('black'))


text_first_lockdown_end = first_lockdown_end.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='lockdown1_end:T'
)


lockdown2_end = datetime.datetime(2021, 1, 18)
df_cases_by_date['lockdown2_end'] = lockdown2_end 
second_lockdown_end = alt.Chart(df_cases_by_date).mark_rule().encode(
    alt.X('lockdown2_end', title=""), color=alt.value('black'))


text_second_lockdown_end = second_lockdown_end.mark_text(
    align='left',
    baseline='middle',
    dx=3,  # Nudges text to right so it doesn't appear on top of the bar
    dy=20
).encode(
    text='lockdown2_end:T'
)









combined = new_and_cum_cases+first_lockdown_start+second_lockdown_start +text_first_lockdown + text_second_lockdown + first_lockdown_end + text_first_lockdown_end + second_lockdown_end + text_second_lockdown_end
to_plot1 = combined.interactive().properties(width=800, title='COVID-19 in Nigeria as at 3rd of March 2020 -- Green and black lines represent start and end of major restrictions resp.')
st.write(make_selector | to_plot1)



#Situation in Nigeria at a Glance Ends
