import streamlit as st

overview_page = st.Page("interface/overview.py", title="Overview", icon="🦠")
vaccination_page = st.Page("interface/vaccination.py", title="Vaccination", icon="💉")
covid19_page = st.Page("interface/covid19.py", title="COVID-19", icon="😷")
economy_page = st.Page("interface/economy.py", title="Economy", icon="💰")
public_transportation_ridership_page = st.Page("interface/public_transportation_ridership.py", title="Public Transportation Ridership", icon="🚇")

pg = st.navigation([overview_page, vaccination_page, covid19_page, economy_page, public_transportation_ridership_page])
pg.run()