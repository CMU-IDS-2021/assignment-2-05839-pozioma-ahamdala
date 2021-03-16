# Understanding How Mobility Restrictions Affected COVID Cases in 4 Major Nigerian States

![image](https://user-images.githubusercontent.com/60380962/111293030-7f3b5580-8651-11eb-9aca-b3a2e72a95b5.png)

TODO: Update screenshot

TODO: Short abstract describing the main goals and how you achieved them.

## Project Goals

TODO: **A clear description of the goals of your project.** Describe the question that you are enabling a user to answer. The question should be compelling and the solution should be focused on helping users achieve their goals. 

We intend to explore how the COVID-19 pandemic progressed in Nigeria pre- and post-lockdown. The major question we are trying to answer is to see if the lockdown and mobility restrictions had significant impact on the COVID-19 progression in Nigeria and if it is an effective method of containment. Our intended audience is government bodies, or individuals who may be seeking to understand the COVID-19 pandemic, what measures were useful for containment, and how to progress further. The insights we hope to get from this project entails, the effectiveness of lockdowns, the compliance of the citizens with lockdown measures, the adoption of remote working by employers and panic buying in post-lockdown in the states. We hope this solution allows our intended audience and users understand the relationship between COVID-19 cases and mobility restrictions, within the context of the four Nigerian states in focus (Lagos, Kano, Rivers and the Federal Capital Territory(Abuja)).

## Design

TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices?

The application can be splitted into two sections. A section that allows a broad view of the COVID-19 situation in Nigeria and another that explores COVID-19, lockdown and mobility in 4 major Nigerian states: Lagos, Kano, Rivers and the Federal Capital Territory(Abuja). These states represent 4 major geo-political zones, hence our choosing them out of the 36 states in Nigeria

To allow a broad overview of the states in Nigeria, we used a map of the country that gives a report of the number of cases and deaths in each of the states. We chose a map because it allows for easy comparison of total cases and deaths by color in each of the states. Clicking on the states rather than scrolling is also an easier way for the user to access data compared to scrolling through a table or interpreting bar charts. We settled on using Tableau for the map as it is easy to implement a map with it. Then, we integrated it into StreamLit.

For visualizing how daily recorded cases increase in the country, a line chart was used. As it will be useful to know how the number of active cases and percentage increase in daily cases, we added this to the chart too. To allow the user interact better, by focusing on a feature at a time, we added a filter that doubles as a legend to the chart. We also included a tooltip to allow the user to get dates and values corresponding to each point on the graph.

We also included lines that show the starts and ends of the two lockdowns in Nigeria. These can be selected and deselected with a filter which doubles as a legend. We also printed the dates beside these lines so that the user can easily have an idea of when the lockdowns started and ended. To allow for interactivity, we added tool tips to the charts so that the users can have easy access to examine the data points.

To explore how many cases are recorded daily in the four states, we used line graphs for each state. These graphs are linked to allow the user to compare values across the states. We opted not to plot the lines on the same graph because they would overlap and the data points were too much to read at once. We also included a tooltip to allow the user to get dates and values corresponding to each point on the graph. We also included lines that showed when the lockdowns started and ended. We also explored the total number of daily cases per day in each of the states. We used legends and a tooltip as earlier described.  

For the mobility section, we used a grid format to represent how mobility varied across the four different states. The grid contain 4 charts, one for each state. Then, each chart showed the percentage increase from baseline of 6 mobility measures: workplaces, retail_and_recreation, parks, transit_stations, residential and groceries_and_pharmacy as the virus progressed for the past year. This percentage increase was captured by Google represents the movement trends over time. It represents how visits to these places varied. For instance, -4% mobility for workplaces represents a fall by 4% in movement to workplaces and +4% depicts a rise from the baseline. Also, before plotting, we decided to reindex the dat by week instead of having it by days because the data points were a lot and reading it was difficult.

This grid format and layered representation of the states and mobility measures was used to allow for interactivity and ability to view a large amount of information at once. A legend was also included with the lines for lockdown dates included above to allow the user properly interact with the visualization.

## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?

Both of us sourced and cleaned up the COVID data and mobility data from HDX and Google respectively. Then, Hamdalat focused on the representation of the COVID cases while Ozioma focused on the visualizations on mobility data. Both of us also worked together on putting the documentation. 

The development process began from deciding what question we wanted to answer.

After this, we went sourcing the data. We considered the relevance of the data in terms of how it relates to our question, the source and also, how recent it was. Afterward, we cleaned up the data by extracting the states we were interested in and remobing unwanted fields. This was to make data visualization easy. 

After this, we began to visualize the data we have on streamlit to understand what patterns existed and how we could make it interactive for the users and intended audience. 

We spent roughly 40 hours in people-hours, meaning each of us spent about 20 hours. This time was spent in meetings to discuss the project, sourcing the data, understanding how to use the tools (Tableau, Streamlit and GitHub), visualizing the data, and documenting the process. The parts that took the most time was understanding how to use what tool and the actual process of visualizing.

## Success Story

TODO:  **A success story of your project.** Describe an insight or discovery you gain with your application that relates to the goals of your project.

The major insight we gathered from the first lockdown, was that across the different states, there was a sharp drop in cases just about the time when the lockdown was instituted but the after about a month, it started to steadily rise again and it continued even after the end of the first lockdown. The same was observed in the second lockdown. It seems as though the level of strictness of enforcing the lockdown wore out as the period extended to the point where it made almost no difference again. Also, the cases did not drop immediately after the lockdown was instituted. This is intuitive because it does take a while for the human body to begin to show symptoms after the virus has entered the system. 

This can mean different things. First, the lockdown is effective for containment as long as it can be enforced and followed strictly. Second, extended lockdowns are not as effective because mobility, and consequently the cases begin to rise regardless of the lockdown after a certain point. This may mean that humans are difficult to contain for extended period, maybe because people have to go out to earn, or the social impact isolation has on humans. 

Learning this is an interesting insight and can be useful for government bodies in designing lockdowns. For effectiveness, they may increase the enforcement as the months wear on or allow for breaks in between. 

We also sought to answer the question of whether the pandemic has affected mode of working. We do know that some people are exploring the concept of remote working but how wide-spread is the thought? From the graph below, we observe that though places like Kano and FCT seems to have gone back to normal. This may be because it is in the northern part of the country, where lesser cases are reported compared to the south. Also, Lagos and Rivers which are in the south did not seem to go back to the baseline. This means, lesser people are working from their workplaces. In Laghos, this may be due to the high number of cases and also, traffic situation. People may have experienced working from home and realised the traffic situation, cost of transportation and other vices are not commensurate to the benefits of wrking from the offices. 

![image](https://user-images.githubusercontent.com/60380962/111324033-12d14e00-8673-11eb-96f3-4d0b7a6c6951.png)

Also, we noticed a significant dip and sharp rise afterward, towards the end of October, just before November which is due to the nationwide #EndSars campaign against police bruatility. The campaign led to some violence which caused curfews, and a lot of people to staying indoors. 

From the chart below, we see that panic buying wasn't as rampant because they was no significant dip/rise at lockdown points. It just seemed to differ as the other places.
Also, from the image below, we noticed that there was not as much compliance to the second lockdown restrictions compared to the first. This may be because they were not as strict or because it was during the festive season. One would expect some traffic around the retail_and_recreation points, but we don't see that here. 

Comparing the four states, Kano seems to be the least compliant to these lockdown restrictions. Again, this may be due to the fact that the cases there are lesser compared to what is observed in other states. 

![image](https://user-images.githubusercontent.com/60380962/111325739-a5262180-8674-11eb-8e72-098976e079fd.png)




