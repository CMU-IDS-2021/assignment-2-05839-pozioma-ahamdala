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


#The map ends here, we will move it as appropraite


df = pd.read_excel('Copy of nga_subnational_covid19_hera.xlsx')








#Situation in Nigeria at a Glance

#Situation in Nigeria at a Glance

df['New Cases'] = df['CONTAMINES']
df_cases_by_date = df.groupby(df['DATE']).sum()
df_cases_by_date = df_cases_by_date.reset_index()
df_cases_by_date['Active Cases (in hundreds)'] = ((df_cases_by_date['CONTAMINES'].cumsum()) - (df_cases_by_date['GUERIS'].cumsum()) + (df_cases_by_date['DECES'].cumsum()))/100
#df_cases_by_date['Cumulative Change in Number of Cases'] = (df_cases_by_date['CONTAMINES'].cumsum())/100

df_cases_by_date['Percentage Change in New Cases'] = (df_cases_by_date['Active Cases (in hundreds)'].pct_change(fill_method='ffill'))*100


make = pd.DataFrame({'Trendline': ['New Cases', 'Active Cases (in hundreds)', 'Percentage Change in New Cases']})
df2 = df_cases_by_date[['DATE', 'New Cases', 'Active Cases (in hundreds)', 'Percentage Change in New Cases']] 
df3 = df2.melt(id_vars=['DATE'], var_name='Trendline', value_name='value')
selection = alt.selection_multi(fields=['Trendline'])
color = alt.condition(selection, alt.Color('Trendline:N'), alt.value('lightgray'))
make_selector = alt.Chart(make).mark_rect(align='right').encode(alt.Y('Trendline',axis=alt.Axis(orient='right'), title=""), color=color).add_selection(selection).properties(title='Trendline Filter')
new_and_cum_cases = alt.Chart(df3).mark_line().encode(alt.X('DATE:T', title="DATE"), y=alt.Y('value:Q', title= " "), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['DATE', 'value:Q']
                                                      ).transform_filter(selection).interactive()





#Lockdown One
lockdown1_start = datetime.datetime(2020, 3, 30)
lockdown1_end = datetime.datetime(2020, 7, 27)
make2 = pd.DataFrame({'Labels': ['Start', 'End']})
lockdown1 = pd.DataFrame(columns=['DATE', 'Labels'])
lockdown1['DATE'] = [lockdown1_start, lockdown1_end]
lockdown1['Labels'] = ['Start', 'End']
selection2 = alt.selection_multi(fields=['Labels'], empty='none')
color = alt.condition(selection2, alt.Color('Labels:N'), alt.value('lightgray'))
make_selector2 = alt.Chart(make2).mark_rect(align='right').encode(alt.Y('Labels',axis=alt.Axis(orient='right'), title=""), color=color).add_selection(selection2).properties(title='First Lockdown')
lockdown_chart = alt.Chart(lockdown1).encode(alt.X('DATE:T', title="DATE"), text='DATE:T', color=alt.Color('Labels:N', legend=None)).transform_filter(selection2)


lockdown_chart = lockdown_chart.mark_text(
    align='left',
    baseline='middle',
    dx=3,  
    dy=20
) + lockdown_chart.mark_rule()
                                                      

#Lockdown Two
lockdown2_start = datetime.datetime(2020, 12, 21)
lockdown2_end = datetime.datetime(2021, 1, 18)


make3 = pd.DataFrame({'Labels': ['Start', 'End']})
lockdown2 = pd.DataFrame(columns=['DATE', 'Labels'])
lockdown2['DATE'] = [lockdown2_start, lockdown2_end]
lockdown2['Labels'] = ['Start', 'End']
selection3 = alt.selection_multi(fields=['Labels'], empty='none')
color = alt.condition(selection3, alt.Color('Labels:N'), alt.value('lightgray'))
make_selector3 = alt.Chart(make3).mark_rect(align='right').encode(alt.Y('Labels',axis=alt.Axis(orient='right'), title=""), color=color).add_selection(selection3).properties(title='Second Lockdown')
lockdown_chart2 = alt.Chart(lockdown2).encode(alt.X('DATE:T', title="DATE"), text='DATE:T',color=alt.Color('Labels:N', legend=None)).transform_filter(selection3)


lockdown_chart2 = lockdown_chart2.mark_text(
    align='left',
    baseline='middle',
    dx=3,  
    dy=110
) + lockdown_chart2.mark_rule()

#End of Lockdown 

first_chart = (new_and_cum_cases + lockdown_chart + lockdown_chart2).properties(width=600) | (make_selector & make_selector2 & make_selector3)



#Some variables resolution
#States Division
df_fct = df.loc[df['REGION']=='Federal Capital Territory'].dropna(axis=0, how='all')
df_lagos = df.loc[df['REGION'] == 'Lagos'].dropna(axis=0, how='all')
df_kano = df.loc[df['REGION']=='Kano'].dropna(axis=0, how='all')
df_rivers = df.loc[df['REGION'] == 'Rivers'].dropna(axis=0, how='all')

df_fct = df_fct.reset_index()
df_lagos = df_lagos.reset_index()
df_kano = df_kano.reset_index()
df_rivers = df_rivers.reset_index()


states_new_cases = pd.DataFrame(columns=['DATE', 'Lagos', 'Kano', 'Federal Capital Territory', 'Rivers'])
states_new_cases['DATE'] = df_lagos['DATE']
states_new_cases['Lagos'] = df_lagos['New Cases']
states_new_cases['Kano'] = df_kano['New Cases']
states_new_cases['Federal Capital Territory'] = df_fct['New Cases']
states_new_cases['Rivers'] = df_rivers['New Cases']


#New Cases each state starts here

base = alt.Chart().mark_line().encode(

).properties(
    width=200,
    height=200
).interactive()

chart = alt.vconcat(data=states_new_cases)

row= alt.hconcat()
row |= base.encode(alt.X('DATE:T'), alt.Y('Lagos:Q', title="New Cases in Lagos")).properties(height=200, width=350) + lockdown_chart + lockdown_chart2
row |= base.encode(alt.X('DATE:T'), alt.Y('Kano:Q', title="New Cases in Kano")).properties(height=200, width=350) + lockdown_chart + lockdown_chart2
chart &= row

row= alt.hconcat()
row |= base.encode(alt.X('DATE:T'), alt.Y('Rivers:Q', title="New Cases in Rivers")).properties(height=200, width=350) + lockdown_chart + lockdown_chart2
row |= base.encode(alt.X('DATE:T'), alt.Y('Federal Capital Territory:Q', title="New Cases in Federal Capital Territory")).properties(height=200, width=350) + lockdown_chart + lockdown_chart2
chart &= row

second_chart = chart

#Cumulative in the States

states_df = df[(df['REGION'] == 'Lagos') | (df['REGION'] == 'Kano') | (df['REGION'] == 'Rivers') | (df['REGION'] == 'Federal Capital Territory') ]

df_cases_by_date_states = states_df.groupby(df['DATE']).sum()
df_cases_by_date_states = df_cases_by_date_states.reset_index()
df_cases_by_date_states['Active Cases (in hundreds)'] = ((df_cases_by_date_states['CONTAMINES'].cumsum()) - (df_cases_by_date_states['GUERIS'].cumsum()) + (df_cases_by_date_states['DECES'].cumsum()))/100
#df_cases_by_date['Cumulative Change in Number of Cases'] = (df_cases_by_date['CONTAMINES'].cumsum())/100

df_cases_by_date_states['Percentage Change in New Cases'] = (df_cases_by_date_states['New Cases'].pct_change(fill_method='ffill'))*100

df_cases_by_date_states = df_cases_by_date_states.replace([np.inf, -np.inf], np.nan)
make_states = pd.DataFrame({'Trendline': ['New Cases', 'Active Cases (in hundreds)', 'Percentage Change in New Cases']})
df2_states = df_cases_by_date_states[['DATE', 'New Cases', 'Active Cases (in hundreds)', 'Percentage Change in New Cases']] 
df3_states = df2_states.melt(id_vars=['DATE'], var_name='Trendline', value_name='value')
selection_states = alt.selection_multi(fields=['Trendline'])
color_states = alt.condition(selection_states, alt.Color('Trendline:N'), alt.value('lightgray'))
make_selector_states = alt.Chart(make_states).mark_rect(align='right').encode(alt.Y('Trendline',axis=alt.Axis(orient='right'), title=""), color=color_states).add_selection(selection_states).properties(title='Trendline Filter')
new_and_cum_cases_states = alt.Chart(df3_states).mark_line().encode(alt.X('DATE:T', title="DATE"), y=alt.Y('value:Q', title= " "), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['DATE', 'value:Q']
                                                      ).transform_filter(selection_states).interactive()




first_chart_states = (lockdown_chart + lockdown_chart2 + new_and_cum_cases_states).properties(width=600, title='Active, New and Percentage Change in New Cases in Lagos, Kano, Rivers and the FCT') | (make_selector_states & make_selector2 & make_selector3)

#We put elements on screen here

st.markdown("<h2 style='text-align: center; color: black;'>Nigeria at a Glance</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Context about Nigeria?? </h2>", unsafe_allow_html=True)
components.html(html_temp, width=1000, height=700)
st.write(first_chart)
st.write(first_chart_states)
st.write(second_chart | make_selector2 & make_selector3)
