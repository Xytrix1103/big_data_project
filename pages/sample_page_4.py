from data.mongodb import cases_malaysia, cases_state, interest_rates, ridership_headline, vax_malaysia, vax_district
from streamlit import title, write, table, line_chart, bar_chart, area_chart, pydeck_chart, slider
import pandas as pd

title('Data from MongoDB')

write('## Cases Malaysia')

df = pd.DataFrame(cases_malaysia)

# Number of rows per page
rows_per_page = 20

# Calculate number of pages
pages = -(-len(df) // rows_per_page) # Equivalent to math.ceil(len(df) / rows_per_page)

# Use a slider for page navigation
page_number = slider('Select a page:', 1, pages)

# Display the table for the current page
start_index = rows_per_page * (page_number - 1)
end_index = start_index + rows_per_page
table(df.iloc[start_index : end_index])