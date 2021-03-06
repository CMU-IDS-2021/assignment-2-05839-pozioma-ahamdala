import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
import datetime
import numpy as np

st.markdown("<h1 style='text-align: center; color: black;'>Understanding How Mobility Restrictions Affected COVID Cases in 4 Major Nigerian States</h1>", unsafe_allow_html=True)

#@st.cache  # add caching so we load the data only once
def load_data():
    # Load the penguin data from https://github.com/allisonhorst/palmerpenguins.
    penguins_url = "nga_subnational_covid19_hera.xlsx - Feuil1.csv"
    return pd.read_csv(penguins_url)

#The map starts here

html_temp = """
<div class='tableauPlaceholder' id='viz1615851281279' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_16155695091580&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Book1_16155695091580&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_16155695091580&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1615851281279');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='527px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='527px';} else { vizElement.style.width='100%';vizElement.style.height='777px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
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


trend = pd.DataFrame({'Trendline': ['New Cases', 'Active Cases (in hundreds)', 'Percentage Change in New Cases']})
df2 = df_cases_by_date[['DATE', 'New Cases', 'Active Cases (in hundreds)', 'Percentage Change in New Cases']] 
df3 = df2.melt(id_vars=['DATE'], var_name='Trendline', value_name='value')
selection = alt.selection_multi(fields=['Trendline'])
color = alt.condition(selection, alt.Color('Trendline:N'), alt.value('lightgray'))
trend_selector = alt.Chart(trend).mark_rect(align='right').encode(alt.Y('Trendline',axis=alt.Axis(orient='right'), title=""), color=color).add_selection(selection).properties(title='Trendline Filter')
new_and_cum_cases = alt.Chart(df3).mark_line().encode(alt.X('DATE:T', title="DATE"), y=alt.Y('value:Q', title= " "), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['DATE', 'value:Q']
                                                      ).transform_filter(selection).interactive()

#Lockdown One
lockdown1_start = datetime.datetime(2020, 3, 30)
lockdown1_end = datetime.datetime(2020, 7, 27)
trend2 = pd.DataFrame({'Labels': ['Start', 'End']})
lockdown1 = pd.DataFrame(columns=['DATE', 'Labels'])
lockdown1['DATE'] = [lockdown1_start, lockdown1_end]
lockdown1['Labels'] = ['Start', 'End']
selection2 = alt.selection_multi(fields=['Labels'], empty='none')
color = alt.condition(selection2, alt.Color('Labels:N'), alt.value('lightgray'))
trend_selector2 = alt.Chart(trend2).mark_rect(align='right').encode(alt.Y('Labels',axis=alt.Axis(orient='right'), title=""), color=color).add_selection(selection2).properties(title='First Lockdown (2020)')
lockdown_chart = alt.Chart(lockdown1).encode(alt.X('DATE:T', title="DATE"), text='monthdate(DATE):O', color=alt.Color('Labels:N', legend=None)).transform_filter(selection2)


lockdown_chart = lockdown_chart.mark_text(
    align='center',
    baseline='middle',
    dx=3,  
    dy=20
) + lockdown_chart.mark_rule()
                                                      

#Lockdown Two
lockdown2_start = datetime.datetime(2020, 12, 21)
lockdown2_end = datetime.datetime(2021, 1, 18)


trend3 = pd.DataFrame({'Labels': ['Start', 'End']})
lockdown2 = pd.DataFrame(columns=['DATE', 'Labels'])
lockdown2['DATE'] = [lockdown2_start, lockdown2_end]
lockdown2['Labels'] = ['Start', 'End']
selection3 = alt.selection_multi(fields=['Labels'], empty='none')
color = alt.condition(selection3, alt.Color('Labels:N'), alt.value('lightgray'))
trend_selector3 = alt.Chart(trend3).mark_rect(align='right').encode(alt.Y('Labels',axis=alt.Axis(orient='right'), title=""), color=color).add_selection(selection3).properties(title='Second Lockdown (2021)')
lockdown_chart2 = alt.Chart(lockdown2).encode(alt.X('DATE:T', title="DATE"), text='monthdate(DATE):O',color=alt.Color('Labels:N', legend=None)).transform_filter(selection3)


lockdown_chart2 = lockdown_chart2.mark_text(
    align='center',
    baseline='middle',
    dx=3,  
    dy=1
) + lockdown_chart2.mark_rule()

#End of Lockdown 

first_chart = (new_and_cum_cases + lockdown_chart + lockdown_chart2).properties(width=600) | (trend_selector & trend_selector2 & trend_selector3)


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
row |= base.encode(alt.X('DATE:T'), alt.Y('Lagos:Q', title="Daily Cases"), tooltip=['DATE', 'Lagos:Q']).properties(height=200, width=350, title="Lagos") + lockdown_chart + lockdown_chart2
row |= base.encode(alt.X('DATE:T'), alt.Y('Kano:Q', title="Daily Cases"), tooltip=['DATE', 'Kano:Q']).properties(height=200, width=350, title="Kano") + lockdown_chart + lockdown_chart2
chart &= row

row= alt.hconcat()
row |= base.encode(alt.X('DATE:T'), alt.Y('Rivers:Q', title="Daily Cases"), tooltip=['DATE', 'Rivers:Q']).properties(height=200, width=350, title="Rivers") + lockdown_chart + lockdown_chart2
row |= base.encode(alt.X('DATE:T'), alt.Y('Federal Capital Territory:Q', title="Daily Cases"), tooltip=['DATE', 'Federal Capital Territory:Q']).properties(height=200, width=350, title="Federal Capital Territory") + lockdown_chart + lockdown_chart2
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
trend_states = pd.DataFrame({'Trendline': ['New Cases', 'Active Cases (in hundreds)', 'Percentage Change in New Cases']})
df2_states = df_cases_by_date_states[['DATE', 'New Cases', 'Active Cases (in hundreds)', 'Percentage Change in New Cases']] 
df3_states = df2_states.melt(id_vars=['DATE'], var_name='Trendline', value_name='value')
selection_states = alt.selection_multi(fields=['Trendline'])
color_states = alt.condition(selection_states, alt.Color('Trendline:N'), alt.value('lightgray'))
trend_selector_states = alt.Chart(trend_states).mark_rect(align='right').encode(alt.Y('Trendline',axis=alt.Axis(orient='right'), title=""), color=color_states).add_selection(selection_states).properties(title='Trendline Filter')
new_and_cum_cases_states = alt.Chart(df3_states).mark_line().encode(alt.X('DATE:T', title="DATE"), y=alt.Y('value:Q', title= " "), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['DATE', 'value:Q']
                                                      ).transform_filter(selection_states).interactive()




first_chart_states = (lockdown_chart + lockdown_chart2 + new_and_cum_cases_states).properties(width=600, title='Active, New and Percentage Change in New Cases in Lagos, Kano, Rivers and the FCT') | (trend_selector_states & trend_selector2 & trend_selector3)

#MOBILITY
df_m = pd.read_excel('NigeriaMobilityData.xlsx')

lag = df_m[df_m.State == "Lagos"]
kan = df_m[df_m.State == "Kano"]
abj = df_m[df_m.State == "FCT"]
riv = df_m[df_m.State == "Rivers"]

lag.set_index("date", inplace=True)
lag = lag.resample('W').mean()
lag = lag.reset_index()

kan.set_index("date", inplace=True)
kan = kan.resample('W').mean()
kan = kan.reset_index()

abj.set_index("date", inplace=True)
abj = abj.resample('W').mean()
abj = abj.reset_index()

riv.set_index("date", inplace=True)
riv = riv.resample('W').mean()
riv = riv.reset_index()

df_m.set_index("date", inplace=True)
df_m = df_m.resample('W').mean()
df_m = df_m.reset_index()

trend = pd.DataFrame({'Trendline': ['retail_and_recreation', 'grocery_and_pharmacy', 'parks_percent', 'transit_stations', 'workplaces', 'residential']})
df2 = lag[['date', 'retail_and_recreation', 'grocery_and_pharmacy', 'parks_percent', 'transit_stations', 'workplaces', 'residential']] 
df3 = lag.melt(id_vars=['date'], var_name='Trendline', value_name='value')
selection = alt.selection_multi(fields=['Trendline'])

color = alt.condition(selection, alt.Color('Trendline:N'), alt.value('lightgray'))
trend_selector_m = alt.Chart(trend).mark_rect(align='right').encode(alt.Y('Trendline',axis=alt.Axis(orient='right'), title=""), color=color).add_selection(selection).properties(title='Trendline Filter')
lag_mob = alt.Chart(df3).mark_line().encode(alt.X('date:T', title="DATE"), y=alt.Y('value:Q', title= "Percentage Change  from Baseline"), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['date', 'value:Q']
                                                      ).transform_filter(selection)

df2 = kan[['date', 'retail_and_recreation', 'grocery_and_pharmacy', 'parks_percent', 'transit_stations', 'workplaces', 'residential']] 
df3 = kan.melt(id_vars=['date'], var_name='Trendline', value_name='value')
kan_mob = alt.Chart(df3).mark_line().encode(alt.X('date:T', title="DATE"), y=alt.Y('value:Q', title= "Percentage Change from Baseline"), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['date', 'value:Q']
                                                      ).transform_filter(selection)

df2 = abj[['date', 'retail_and_recreation', 'grocery_and_pharmacy', 'parks_percent', 'transit_stations', 'workplaces', 'residential']] 
df3 = abj.melt(id_vars=['date'], var_name='Trendline', value_name='value')
abj_mob = alt.Chart(df3).mark_line().encode(alt.X('date:T', title="DATE"), y=alt.Y('value:Q', title= "Percentage Change from Baseline"), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['date', 'value:Q']
                                                      ).transform_filter(selection)

df2 = riv[['date', 'retail_and_recreation', 'grocery_and_pharmacy', 'parks_percent', 'transit_stations', 'workplaces', 'residential']] 
df3 = riv.melt(id_vars=['date'], var_name='Trendline', value_name='value')
riv_mob = alt.Chart(df3).mark_line().encode(alt.X('date:T', title="DATE"), y=alt.Y('value:Q', title= "Percentage Change from Baseline"), color=alt.Color('Trendline:N', legend=None),
                                                      tooltip=['date', 'value:Q']
                                                      ).transform_filter(selection)

base = alt.Chart().mark_line().encode(

).properties(
    width=200,
    height=200
).transform_filter(selection).interactive()

empty_df = pd.DataFrame(columns = ['Date'])
chart_m = alt.vconcat(data=empty_df)

row= alt.hconcat()
row |= base.encode(alt.X('date:T', title="DATE")).properties(height=200, width=350, title="Lagos") + lag_mob + lockdown_chart + lockdown_chart2
row |= base.encode(alt.X('date:T', title="DATE")).properties(height=200, width=350, title="Kano") + kan_mob + lockdown_chart + lockdown_chart2
chart_m &= row

row= alt.hconcat()
row |= base.encode(alt.X('date:T', title="DATE")).properties(height=200, width=350, title="Federal Capital Territory") + abj_mob + lockdown_chart + lockdown_chart2
row |= base.encode(alt.X('date:T', title="DATE")).properties(height=200, width=350, title="Rivers") + riv_mob + lockdown_chart + lockdown_chart2
chart_m &= row


#Workplace Mobility vs Daily Cases per week

#Mobility vs Number of Cases
df_lagos = df[df.REGION == 'Lagos'] 
df_lagos.set_index('DATE', inplace=True)
df_lagos = df_lagos.resample("W").sum()
df_lagos = df_lagos.reset_index()


lag_workplace = lag['workplaces']
lag_cases = df_lagos['New Cases']

cases_workplace = pd.DataFrame(columns=['workplaces', 'New Cases'])

cases_workplace['workplaces'] = lag['workplaces']
cases_workplace['New Cases'] = df_lagos['New Cases']

lag_w = alt.Chart(cases_workplace).mark_point().encode(y=alt.Y('workplaces:Q', title=""), x=alt.X('New Cases', title= ""), tooltip=['New Cases:Q', 'workplaces:Q']).properties(width=600)


#Mobility vs Number of Cases
df_kano = df[df.REGION == 'Kano'] 
df_kano.set_index('DATE', inplace=True)
df_kano = df_kano.resample("W").sum()
df_kano = df_kano.reset_index()


kano_workplace = kan['workplaces']
kano_cases = df_kano['New Cases']

cases_workplace_kano = pd.DataFrame(columns=['workplaces', 'New Cases'])

cases_workplace_kano['workplaces'] = kan['workplaces']
cases_workplace_kano['New Cases'] = df_kano['New Cases']

kano_w = alt.Chart(cases_workplace_kano).mark_point().encode(y=alt.Y('workplaces:Q', title=""), x=alt.X('New Cases', title= ""), tooltip=['New Cases:Q', 'workplaces:Q']).properties(width=600)


#Mobility vs Number of Cases
df_fct = df[df.REGION == 'Federal Capital Territory'] 
df_fct.set_index('DATE', inplace=True)
df_fct = df_fct.resample("W").sum()
df_fct = df_fct.reset_index()

fct_workplace = abj['workplaces']
fct_cases = df_fct['New Cases']

cases_workplace_fct = pd.DataFrame(columns=['workplaces', 'New Cases'])

cases_workplace_fct['workplaces'] = abj['workplaces']
cases_workplace_fct['New Cases'] = df_fct['New Cases']

fct_w = alt.Chart(cases_workplace_fct).mark_point().encode(y=alt.Y('workplaces:Q', title=""), x=alt.X('New Cases', title= ""), tooltip=['New Cases:Q', 'workplaces:Q']).properties(width=600)


#Mobility vs Number of Cases
df_rivers = df[df.REGION == 'Rivers'] 
df_rivers.set_index('DATE', inplace=True)
df_rivers = df_rivers.resample("W").sum()
df_rivers = df_rivers.reset_index()

rivers_workplace = riv['workplaces']
rivers_cases = df_rivers['New Cases']

cases_workplace_rivers = pd.DataFrame(columns=['workplaces', 'New Cases'])

cases_workplace_rivers['workplaces'] = riv['workplaces']
cases_workplace_rivers['New Cases'] = df_rivers['New Cases']

rivers_w = alt.Chart(cases_workplace_rivers).mark_point().encode(y=alt.Y('workplaces:Q', title=""), x=alt.X('New Cases', title= ""), tooltip=['New Cases:Q', 'workplaces:Q']).properties(width=600)


base_w = alt.Chart().mark_line().encode(

).properties(
    width=400,
    height=400, 
).interactive()

empty_df2 = pd.DataFrame(columns = ['New Cases', 'workplaces'])
chart_w = alt.vconcat(data=empty_df2)

row= alt.hconcat()
row |= base_w.encode(alt.X('New Cases:Q', title="Weekly Cases"), alt.Y('workplaces:Q', title="% Change in workplace mobility ")).properties(height=200, width=350, title="Lagos") + lag_w 
row |= base_w.encode(alt.X('New Cases:Q', title="Weekly Cases"), alt.Y('workplaces:Q', title="% Change in workplace mobility ")).properties(height=200, width=350, title="Kano") + kano_w
chart_w &= row

row= alt.hconcat()
row |= base_w.encode(alt.X('New Cases:Q', title="Weekly Cases"), alt.Y('workplaces:Q', title="% Change in workplace mobility ")).properties(height=200, width=350, title="Federal Capital Territory") + fct_w
row |= base_w.encode(alt.X('New Cases:Q', title="Weekly Cases"), alt.Y('workplaces:Q', title="% Change in workplace mobility")).properties(height=200, width=350, title="Rivers") + rivers_w
chart_w &= row








#We put elements on screen here

st.markdown("<h2 style='text-align: center; color: black;'>Nigeria at a Glance</h2>", unsafe_allow_html=True)
#st.markdown("<h2 style='text-align: center; color: black;'>Context about Nigeria?? </h2>", unsafe_allow_html=True)
st.write("Nigeria, also known as the Giant of Africa, belongs to the western part of Nigeria. The country recorded its first COVID-19 case on the 27th of February, 2020. Cases increased steadily after this. The country has had two major restrictions on movement and activities.")
st.write("There are 36 states in the country. The most populated is Kano and this followed by Lagos. Lagos is the economic hub of the country and has by far, the highest number of recorded COVID-19 cases.")

st.markdown("<h2 style='text-align: center; color: black;'>Total COVID-19 cases and COVID-19 related Deaths in Nigerian States</h2>", unsafe_allow_html=True)
components.html(html_temp, width=900, height=600)
#st.write(first_chart)

st.markdown("<h2 style='text-align: center; color: black;'>Total COVID Cases Across Lagos, Kano, FCT and Rivers</h2>", unsafe_allow_html=True)
st.write("Lagos, Kano, Rivers and the Federal Capital Territory are some of the most populated states in the country. These states are mostly urbanized and represent the four geographical regions in the country")
st.write(first_chart_states)

st.markdown("<h2 style='text-align: center; color: black;'>Daily COVID Cases Across Lagos, Kano, FCT and Rivers</h2>", unsafe_allow_html=True)
st.write(second_chart | trend_selector2 & trend_selector3)

st.markdown("<h2 style='text-align: center; color: black;'>Mobility Changes Across Lagos, Kano, FCT and Rivers as the Virus Progressed</h2>", unsafe_allow_html=True)
st.write(chart_m | trend_selector_m & trend_selector2 & trend_selector3)

st.markdown("<h2 style='text-align: center; color: black;'>Correlation between Weekly Cases and Workplaces' Mobility</h2>", unsafe_allow_html=True)
st.write(chart_w)
