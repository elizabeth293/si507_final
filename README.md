SI 507
FINAL PROJECT
Elizabeth Baca

RESOURCES
I used the following as resources on this project, in addition to class material:
1.	documentation at https://plot.ly/python/
2.	documentation at https://www.crummy.com/software/BeautifulSoup/bs4/doc/
3.	https://stackoverflow.com/questions/8936030/using-beautifulsoup-to-search-html-for-string
4.	https://stackoverflow.com/questions/1022141/best-way-to-randomize-a-list-of-strings-in-python
5.	https://stackoverflow.com/questions/25668828/how-to-create-colour-gradient-in-python


DATA SOURCE
I crawled and scraped all character pages starting at https://www.dccomics.com/characters and collected the following pieces of information:
1.	First appearance (series, issue, year)
2.	Real name
3.	Occupation
4.	Image URL


STRUCTURE OF CODE
1.	Part 1 (functions: “get_heroes_list”, “get_villains_list”, caching, “get_character_info”, “init_db”, “insert_character_data”, “insert_alignment_data”, “insert_series_data”, “alignment_foreign_keys”, “series_foreign_keys”)
a.	Get list of 60 heroes and 40 villains from csv files “Heroes.csv” & “Villains.csv”
b.	Crawl & scrape each character’s page on https://www.dccomics.com/characters and store info (plus character name & alignment) in “alph_characters” dictionary
c.	Create database (“dc_characters.db”) & add information about characters
2.	Part 2 (functions: “plot_first_app_scatter”, “plot_first_app_bar”, “plot_first_app_series_pie”, “plot_first_app_year_pie”)
a.	Build graphs with plotly
3.	Part 3 (functions: “execute_command”, “search_prompt”)
a.	Get command from user
b.	Generate 1 of 4 graphs based on command:
i.	Scatterplot timeline of first appearance for every character 
ii.	Bar chart of number of first appearances occurring in each year according to alignment 
iii.	Pie chart with titles of series that selection of characters first appeared in 
iv.	Pie chart with all Heroes and Villains first appearing in the same decade as input year 


USER GUIDE
1.	In order to run Part 1 of code, input in command line must end in “--init” (ex: “$ python final_project.py --init”) 
2.	When code runs normally (no “--init”), user is given full set of instructions: 
	“ Options: 
	1) type 'Scatter' to see scatterplot timeline of first appearance for every character 
 	2) type 'Bar: <Heroes, Villains, or Both>' to see bar chart of number of first appearances occurring in each year according to alignment 
	3) type 'Series Pie: <Heroes or Villains> <newest or oldest> <number between 1 and 60 for Heroes or number between 1 and 40 for Villains>' to see pie chart with titles of series that selection of characters first appeared in 
	4) type 'Decade Pie: <any year between 1938 and 2015>' to see pie chart with all Heroes and Villains first appearing in the same decade as input year 
	5) type 'exit' to quit program Enter Command: ”
