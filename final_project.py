# FINAL PROJECT
# SI 507 Fall 2019
# Elizabeth Baca

import requests
import csv
import json
from bs4 import BeautifulSoup
import sys
import sqlite3
import plotly.graph_objs as go
from colour import Color
import random

# ~~~~~~~~~~~~~~~~~~RESOURCES~~~~~~~~~~~~~~~~~~
# I used the following as resources on this project, in addition to class material:
# [1] documentation at https://plot.ly/python/
# [2] documentation at https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# [3] https://stackoverflow.com/questions/8936030/using-beautifulsoup-to-search-html-for-string
# [4] https://stackoverflow.com/questions/1022141/best-way-to-randomize-a-list-of-strings-in-python
# [5] https://stackoverflow.com/questions/25668828/how-to-create-colour-gradient-in-python


# ~~~~~~~~~~~~~~~~~~Part 1 - Create Database~~~~~~~~~~~~~~~~~~
# Get list of Heroes
def get_heroes_list(csv_file):
    f = open(csv_file)
    csv_data = csv.reader(f)

    heroes = []

    for each in csv_data:
        heroes.append(each[0])
    heroes = heroes[1:]

    f.close()
    return heroes


# Get list of Villains
def get_villains_list(csv_file):
    f = open(csv_file)
    csv_data = csv.reader(f)

    villains = []

    for each in csv_data:
        villains.append(each[0])
    villains = villains[1:]

    f.close()
    return villains


# Caching of DC Comics search
CACHE_FNAME = 'dc_info_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url, header):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        # print("Making a request for new data...")
        resp = requests.get(url, headers = header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]


# DC Comics site crawl & scrape to get info about each character
def get_character_info():
    dc_base_url = 'https://www.dccomics.com/characters/'
    header = {'User-Agent': 'SI_CLASS'}

    heroes_list = get_heroes_list("Heroes.csv")
    villains_list = get_villains_list("Villains.csv")

    characters_dict = {}

    heroes_urls = {}

    for each in heroes_list:
        hero_name_list = []
        hero_url = ""
        hero_words = each.split()
        for word in hero_words:
            hero_name_list.append(word.lower())
        for name in hero_name_list:
            hero_url = hero_url + name + "-"
        if each not in heroes_urls:
            heroes_urls[each] = hero_url[:-1]

    for each in heroes_urls:
        hero_page_url = dc_base_url + heroes_urls[each]
        hero_page_text = make_request_using_cache(hero_page_url, header)
        hero_page_soup = BeautifulSoup(hero_page_text, 'html.parser')

        hero_info_container = hero_page_soup.find(class_="char-facts")

        hero_first_appearance_container = hero_info_container.find(class_="field field-name-field-first-appearance-text field-type-text field-label-hidden")
        hero_first_appearance_title = hero_first_appearance_container.find(class_='field-item even').text

        hero_first_appearance_issue = hero_first_appearance_title[:-6]
        hero_first_appearance_year_messy = hero_first_appearance_title[-6:]
        hero_first_appearance_year = hero_first_appearance_year_messy[1:5]
        hero_first_appearance_issue_list = hero_first_appearance_issue.split("#")
        hero_first_appearance_series = hero_first_appearance_issue_list[0]
        try:
            hero_first_appearance_issue_number = hero_first_appearance_issue_list[1]
        except IndexError:
            hero_first_appearance_issue_number = ""

        try:
            hero_occupation_container_1 = hero_info_container.find(text="Occupation").parent
            hero_occupation_container_2 = hero_occupation_container_1.parent
            hero_occupation_container_3 = hero_occupation_container_2.parent
            hero_occupation_container_sibling = hero_occupation_container_3.next_sibling
            hero_occupation = hero_occupation_container_sibling.text
        except AttributeError:
            hero_occupation = "None"

        try:
            hero_real_name_container_1 = hero_info_container.find(text="Real Name").parent
            hero_real_name_container_2 = hero_real_name_container_1.parent
            hero_real_name_container_3 = hero_real_name_container_2.parent
            hero_real_name_container_sibling = hero_real_name_container_3.next_sibling
            hero_real_name = hero_real_name_container_sibling.text
        except AttributeError:
            hero_real_name = "None"

        hero_picture_container = hero_page_soup.find(class_="thumb-trigger")
        hero_picture_url = hero_picture_container.find('img')['src']

        hero_info_dict = {}
        hero_info_dict["alignment"] = "Hero"
        hero_info_dict["first appearance series"] = hero_first_appearance_series[:-1]
        hero_info_dict["first appearance issue"] = hero_first_appearance_issue_number[:-1]
        hero_info_dict["first appearance year"] = hero_first_appearance_year
        hero_info_dict["occupation"] = hero_occupation
        hero_info_dict["real name"] = hero_real_name
        hero_info_dict["image url"] = hero_picture_url

        if each not in characters_dict :
            characters_dict[each] = hero_info_dict

    villains_urls = {}

    for each in villains_list:
        villain_name_list = []
        villain_url = ""
        villain_words = each.split()
        for word in villain_words:
            villain_name_list.append(word.lower())
        for name in villain_name_list:
            villain_url = villain_url + name + "-"
        if each not in villains_urls:
            villains_urls[each] = villain_url[:-1]

    for each in villains_urls:
        villain_page_url = dc_base_url + villains_urls[each]
        villain_page_text = make_request_using_cache(villain_page_url, header)
        villain_page_soup = BeautifulSoup(villain_page_text, 'html.parser')

        villain_info_container = villain_page_soup.find(class_="char-facts")

        villain_first_appearance_container = villain_info_container.find(class_="field field-name-field-first-appearance-text field-type-text field-label-hidden")
        villain_first_appearance_title = villain_first_appearance_container.find(class_='field-item even').text

        villain_first_appearance_issue = villain_first_appearance_title[:-6]
        villain_first_appearance_year_messy = villain_first_appearance_title[-6:]
        villain_first_appearance_year = villain_first_appearance_year_messy[1:5]
        villain_first_appearance_issue_list = villain_first_appearance_issue.split("#")
        villain_first_appearance_series = villain_first_appearance_issue_list[0]
        try:
            villain_first_appearance_issue_number = villain_first_appearance_issue_list[1]
        except IndexError:
            villain_first_appearance_issue_number = ""

        try:
            villain_occupation_container_1 = villain_info_container.find(text="Occupation").parent
            villain_occupation_container_2 = villain_occupation_container_1.parent
            villain_occupation_container_3 = villain_occupation_container_2.parent
            villain_occupation_container_sibling = villain_occupation_container_3.next_sibling
            villain_occupation = villain_occupation_container_sibling.text
        except AttributeError:
            villain_occupation = "None"

        try:
            villain_real_name_container_1 = villain_info_container.find(text="Real Name").parent
            villain_real_name_container_2 = villain_real_name_container_1.parent
            villain_real_name_container_3 = villain_real_name_container_2.parent
            villain_real_name_container_sibling = villain_real_name_container_3.next_sibling
            villain_real_name = villain_real_name_container_sibling.text
        except AttributeError:
            villain_real_name = "None"

        villain_picture_container = villain_page_soup.find(class_="thumb-trigger")
        villain_picture_url = villain_picture_container.find('img')['src']

        villain_info_dict = {}
        villain_info_dict["real name"] = villain_real_name
        villain_info_dict["alignment"] = "Villain"
        villain_info_dict["first appearance series"] = villain_first_appearance_series[:-1]
        villain_info_dict["first appearance issue"] = villain_first_appearance_issue_number[:-1]
        villain_info_dict["first appearance year"] = villain_first_appearance_year
        villain_info_dict["occupation"] = villain_occupation
        villain_info_dict["image url"] = villain_picture_url

        if each not in characters_dict :
            characters_dict[each] = villain_info_dict

    alph_characters = {}
    for each in sorted(characters_dict):
        alph_characters[each] = characters_dict[each]

    return alph_characters

# Start database
def init_db():
    conn = sqlite3.connect('dc_characters.db')
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Characters';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Alignments';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Series';
    '''
    cur.execute(statement)

    conn.commit()

    statement = '''
        CREATE TABLE 'Characters' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT,
            'RealName' TEXT,
            'AlignmentId' INTEGER,
            'FirstAppearanceSeriesId' TEXT,
            'FirstAppearanceIssue' TEXT,
            'FirstAppearanceYear' TEXT,
            'Occupation' TEXT,
            'ImageURL' TEXT
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Alignments' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Alignment' TEXT
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Series' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'SeriesName' TEXT
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()


# Add character info to database
def insert_character_data():
    characters = get_character_info()

    conn = sqlite3.connect('dc_characters.db')
    cur = conn.cursor()

    for each in characters:
        insertion = (None, each, characters[each]["real name"], characters[each]["alignment"], characters[each]["first appearance series"], characters[each]["first appearance issue"], characters[each]["first appearance year"], characters[each]["occupation"], characters[each]["image url"])

        statement = 'INSERT INTO "Characters" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


# Add alignment info to database
def insert_alignment_data():
    alignments = ["Hero", "Villain"]

    conn = sqlite3.connect('dc_characters.db')
    cur = conn.cursor()

    for each in alignments:
        insertion = (None, each)
        statement = 'INSERT INTO "Alignments" '
        statement += 'VALUES (?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


# Add series info to database
def insert_series_data():
    characters = get_character_info()

    all_series = []

    for each in characters:
        if characters[each]["first appearance series"] not in all_series:
            all_series.append(characters[each]["first appearance series"])
    alph_series = sorted(all_series)

    conn = sqlite3.connect('dc_characters.db')
    cur = conn.cursor()

    for each in alph_series:
        insertion = (None, each)
        statement = 'INSERT INTO "Series" '
        statement += 'VALUES (?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()


# Update alignment foreign keys
def alignment_foreign_keys():
    conn = sqlite3.connect('dc_characters.db')
    cur = conn.cursor()

    cur.execute("Select Alignments.Id, Alignments.Alignment FROM Alignments JOIN Characters ON Alignments.Alignment = Characters.AlignmentId")

    alignments_dict = {}

    for each in cur:
        if each[0] not in alignments_dict:
            alignments_dict[each[0]] = each[1]

    for each in alignments_dict:
        new_id = str(each)
        alignment = alignments_dict[each]
        statement = 'UPDATE Characters '
        statement += 'SET AlignmentId="' + new_id + '" '
        statement += 'WHERE AlignmentId="' + alignment +'"'
        cur.execute(statement)

    conn.commit()
    conn.close()


# Update series foreign keys
def series_foreign_keys():
    conn = sqlite3.connect('dc_characters.db')
    cur = conn.cursor()

    cur.execute("Select Series.Id, Series.SeriesName FROM Series JOIN Characters ON Series.SeriesName = Characters.FirstAppearanceSeriesId")

    series_dict = {}

    for each in cur:
        if each[0] not in series_dict:
            series_dict[each[0]] = each[1]

    for each in series_dict:
        new_id = str(each)
        series = series_dict[each]
        statement = 'UPDATE Characters '
        statement += 'SET FirstAppearanceSeriesId="' + new_id + '" '
        statement += 'WHERE FirstAppearanceSeriesId="' + series +'"'
        cur.execute(statement)

    conn.commit()
    conn.close()


# ~~~~~~~~~~~~~~~~~~Part 2 - Graphs & Charts~~~~~~~~~~~~~~~~~~
# 1. Scatter plot of all first appearances
def plot_first_app_scatter():
    conn = sqlite3.connect('dc_characters.db')
    cur = conn.cursor()
    cur2 = conn.cursor()

    heroes = cur.execute("SELECT Characters.Name, Characters.RealName, Alignments.Alignment, Series.SeriesName, Characters.FirstAppearanceIssue, Characters.FirstAppearanceYear, Characters.Occupation, Characters.ImageURL FROM Characters JOIN Series ON Characters.FirstAppearanceSeriesId=Series.Id JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Alignments.Alignment='Hero'")

    villains = cur2.execute("SELECT Characters.Name, Characters.RealName, Alignments.Alignment, Series.SeriesName, Characters.FirstAppearanceIssue, Characters.FirstAppearanceYear, Characters.Occupation, Characters.ImageURL FROM Characters JOIN Series ON Characters.FirstAppearanceSeriesId=Series.Id JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Alignments.Alignment='Villain'")

    hero_dates = []
    hero_info = []
    for each in heroes:
        hero_info_string = ""
        hero_real = ""
        hero_occ = ""

        if each[1] != "None":
            hero_real = " (" + each[1] + ")"

        if each[6] != "None":
            hero_occ = ", " + each[6]

        hero_info_string = each[0] + hero_real + " - " + each[2] + hero_occ + ", " + each[3] + " #" + each[4] + " (" + each[5] + "), " + each[7]

        hero_info.append(hero_info_string)
        hero_dates.append(int(each[5]))

    villain_dates = []
    villain_info = []
    for each in villains:
        villain_info_string = ""
        villain_real = ""
        villain_occ = ""

        if each[1] != "None":
            villain_real = " (" + each[1] + ")"

        if each[6] != "None":
            villain_occ = ", " + each[6]

        villain_info_string = each[0] + villain_real + " - " + each[2] + villain_occ + ", " + each[3] + " #" + each[4] + " (" + each[5] + "), " + each[7]

        villain_info.append(villain_info_string)
        villain_dates.append(int(each[5]))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x = hero_dates,
        name = 'Heroes',
        mode = 'markers',
        marker_color = '#0A87A3',
        marker_symbol = "circle",
        text = hero_info,
        hoverinfo = 'text',
        hoverlabel = dict(font = dict(color = "white", family = "Open Sans"))
    ))

    fig.add_trace(go.Scatter(
        x = villain_dates,
        name = 'Villains',
        mode = 'markers',
        marker_color = '#A34D00',
        marker_symbol = "diamond",
        text = villain_info,
        hoverinfo = 'text',
        hoverlabel = dict(font = dict(color = "white", family = "Open Sans"))
    ))

    fig.update_traces(marker_size = 8)
    fig.update_layout(title = 'Years of First Appearances - All Characters')
    fig.update_yaxes(showticklabels = False)

    print("Generating scatter plot...")
    fig.show()

    conn.close()

    try:
        return hero_info, villain_info
    except Exception:
        pass


# 2. Bar chart of number of first appearances in each year for Heroes, Villains, or Both
def plot_first_app_bar(search):
    conn = sqlite3.connect('dc_characters.db')

    search_words = search.split()
    if len(search_words) == 1:
        if search == "Heroes":
            cur = conn.cursor()
            heroes = cur.execute("SELECT Characters.Name, Characters.RealName, Alignments.Alignment, Series.SeriesName, Characters.FirstAppearanceIssue, Characters.FirstAppearanceYear, Characters.Occupation, Characters.ImageURL FROM Characters JOIN Series ON Characters.FirstAppearanceSeriesId=Series.Id JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Alignments.Alignment='Hero'")
            hero_dates = {}
            for each in heroes:
                if each[5] not in hero_dates:
                    hero_dates[each[5]] = 1
                else:
                    hero_dates[each[5]] += 1

            hero_years = []
            hero_amount = []
            hero_labels = []
            for each in hero_dates:
                hero_years.append(each)
                hero_amount.append(hero_dates[each])
                hero_labels.append(str(each) + " - " + str(hero_dates[each]) + " heroes")

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x = hero_years,
                y = hero_amount,
                name = 'Heroes',
                marker_color = '#0A87A3',
                text = hero_labels,
                hoverinfo = 'text',
                hoverlabel = dict(font = dict(color = "white", family = "Open Sans"))
            ))

            fig.update_layout(title = 'Number of First appearances Each Year - Heroes')
            print("Generating bar chart...")
            fig.show()

            villain_dates = {}

        elif search == "Villains":
            cur = conn.cursor()
            villains = cur.execute("SELECT Characters.Name, Characters.RealName, Alignments.Alignment, Series.SeriesName, Characters.FirstAppearanceIssue, Characters.FirstAppearanceYear, Characters.Occupation, Characters.ImageURL FROM Characters JOIN Series ON Characters.FirstAppearanceSeriesId=Series.Id JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Alignments.Alignment='Villain'")
            villain_dates = {}
            for each in villains:
                if each[5] not in villain_dates:
                    villain_dates[each[5]] = 1
                else:
                    villain_dates[each[5]] += 1

            villain_years = []
            villain_amount = []
            villain_labels = []
            for each in villain_dates:
                villain_years.append(each)
                villain_amount.append(villain_dates[each])
                villain_labels.append(str(each) + " - " + str(villain_dates[each]) + " villains")

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x = villain_years,
                y = villain_amount,
                name = 'Villains',
                marker_color = '#A34D00',
                text = villain_labels,
                hoverinfo = 'text',
                hoverlabel = dict(font = dict(color = "white", family = "Open Sans"))
            ))

            fig.update_layout(title = 'Number of First appearances Each Year - Villains')
            print("Generating bar chart...")
            fig.show()

            hero_dates = {}

        elif search == "Both":
            cur1 = conn.cursor()
            cur2 = conn.cursor()
            heroes = cur1.execute("SELECT Characters.Name, Characters.RealName, Alignments.Alignment, Series.SeriesName, Characters.FirstAppearanceIssue, Characters.FirstAppearanceYear, Characters.Occupation, Characters.ImageURL FROM Characters JOIN Series ON Characters.FirstAppearanceSeriesId=Series.Id JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Alignments.Alignment='Hero'")
            villains = cur2.execute("SELECT Characters.Name, Characters.RealName, Alignments.Alignment, Series.SeriesName, Characters.FirstAppearanceIssue, Characters.FirstAppearanceYear, Characters.Occupation, Characters.ImageURL FROM Characters JOIN Series ON Characters.FirstAppearanceSeriesId=Series.Id JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Alignments.Alignment='Villain'")
            hero_dates = {}
            for each in heroes:
                if each[5] not in hero_dates:
                    hero_dates[each[5]] = 1
                else:
                    hero_dates[each[5]] += 1

            hero_years = []
            hero_amount = []
            hero_labels = []
            for each in hero_dates:
                hero_years.append(each)
                hero_amount.append(hero_dates[each])
                hero_labels.append(str(each) + " - " + str(hero_dates[each]) + " heroes")

            villain_dates = {}
            for each in villains:
                if each[5] not in villain_dates:
                    villain_dates[each[5]] = 1
                else:
                    villain_dates[each[5]] += 1

            villain_years = []
            villain_amount = []
            villain_labels = []
            for each in villain_dates:
                villain_years.append(each)
                villain_amount.append(villain_dates[each])
                villain_labels.append(str(each) + " - " + str(villain_dates[each]) + " villains")

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x = hero_years,
                y = hero_amount,
                name = 'Heroes',
                marker_color = '#0A87A3',
                text = hero_labels,
                hoverinfo = 'text',
                hoverlabel = dict(font = dict(color = "white", family = "Open Sans"))
            ))

            fig.add_trace(go.Bar(
                x = villain_years,
                y = villain_amount,
                name = 'Villains',
                marker_color = '#A34D00',
                text = villain_labels,
                hoverinfo = 'text',
                hoverlabel = dict(font = dict(color = "white", family = "Open Sans"))
            ))

            fig.update_layout(barmode='stack')
            fig.update_layout(title = 'Number of First appearances Each Year - All Characters')
            print("Generating bar chart...")
            fig.show()

        else:
            print("~~~~~Pleast enter a valid command~~~~~")

    else:
        print("~~~~~Pleast enter a valid command~~~~~")

    conn.close()

    try:
        return hero_dates, villain_dates
    except Exception:
        pass


# 3. Pie chart of series titles that selection of characters first appeared in
def plot_first_app_series_pie(search):
    conn = sqlite3.connect('dc_characters.db')

    search_words = search.split()
    if len(search_words) == 3:
        alignment_search = search_words[0]
        newest_oldest = search_words[1]
        number = search_words[2]

        if alignment_search == "Heroes":
            cur = conn.cursor()

            order = " ORDER BY Characters.FirstAppearanceYear"
            if int(number) > 0 and int(number) < 61:
                limit = " LIMIT " + number
            else:
                print("~~~~~Pleast enter a valid command~~~~~")
            base_statement = "SELECT Characters.Name, Series.SeriesName FROM Characters JOIN Series ON Characters.FirstAppearanceSeriesId=Series.Id JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Alignments.Alignment='Hero'"

            if newest_oldest == "newest":
                order += " DESC"
            elif newest_oldest == "oldest":
                pass
            else:
                print("~~~~~Pleast enter a valid command~~~~~")

            try:
                statement = base_statement + order + limit
                heroes = cur.execute(statement)

                series_count = {}
                for each in heroes:
                    series_info = [0, "Characters: "]
                    if each[1] not in series_count:
                        series_count[each[1]] = series_info
                    series_count[each[1]][0] += 1
                    series_count[each[1]][1] += each[0] + ", "

                series_names = []
                series_numbers = []
                character_names = []
                for each in series_count:
                    series_names.append(each)
                    series_numbers.append(series_count[each][0])
                    character_names.append(series_count[each][1][:-2])

                blue = Color("#043D45")
                gradient = list(blue.range_to(Color("#A3F4FF"), len(series_names)))
                colors = []
                for each in gradient:
                    colors.append(str(each))
                random.shuffle(colors)

                fig = go.Figure()

                fig.add_trace(go.Pie(
                    labels = series_names,
                    values = series_numbers,
                    marker_colors = colors,
                    text = character_names,
                    textinfo = "value",
                    textposition = "inside",
                    textfont_color = "white",
                    hoverinfo = "text+label",
                    hoverlabel = dict(font = dict(color = "white", family = "Open Sans")),
                    hole = .5,
                    showlegend = False
                ))

                fig.update_layout(title = 'Series Titles of First Appearances - ' + newest_oldest + ' ' + number + ' heroes')
                print("Generating pie chart...")
                fig.show()
            except Exception:
                pass

        elif alignment_search == "Villains":
            cur = conn.cursor()

            order = " ORDER BY Characters.FirstAppearanceYear"
            if int(number) > 0 and int(number) < 41:
                limit = " LIMIT " + number
            else:
                print("~~~~~Pleast enter a valid command~~~~~")
            base_statement = "SELECT Characters.Name, Series.SeriesName FROM Characters JOIN Series ON Characters.FirstAppearanceSeriesId=Series.Id JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Alignments.Alignment='Villain'"

            if newest_oldest == "newest":
                order += " DESC"
            elif newest_oldest == "oldest":
                pass
            else:
                print("~~~~~Pleast enter a valid command~~~~~")

            try:
                statement = base_statement + order + limit
                villains = cur.execute(statement)

                series_count = {}
                for each in villains:
                    series_info = [0, "Characters: "]
                    if each[1] not in series_count:
                        series_count[each[1]] = series_info
                    series_count[each[1]][0] += 1
                    series_count[each[1]][1] += each[0] + ", "

                series_names = []
                series_numbers = []
                character_names = []
                for each in series_count:
                    series_names.append(each)
                    series_numbers.append(series_count[each][0])
                    character_names.append(series_count[each][1][:-2])

                orange = Color("#662C00")
                gradient = list(orange.range_to(Color("#F0BE98"), len(series_names)))
                colors = []
                for each in gradient:
                    colors.append(str(each))
                random.shuffle(colors)

                fig = go.Figure()

                fig.add_trace(go.Pie(
                    labels = series_names,
                    values = series_numbers,
                    marker_colors = colors,
                    text = character_names,
                    textinfo = "value",
                    textposition = "inside",
                    textfont_color = "white",
                    hoverinfo = "text+label",
                    hoverlabel = dict(font = dict(color = "white", family = "Open Sans")),
                    hole = .5,
                    showlegend = False
                ))

                fig.update_layout(title = 'Series Titles of First Appearances - ' + newest_oldest + ' ' + number + ' villains')
                print("Generating pie chart...")
                fig.show()
            except Exception:
                pass

        else:
            print("~~~~~Pleast enter a valid command~~~~~")

    else:
        print("~~~~~Pleast enter a valid command~~~~~")

    conn.close()

    try:
        return series_names
    except Exception:
        pass


# 4. Pie chart of all characters that first appeared in selected decade
def plot_first_app_year_pie(search):
    conn = sqlite3.connect('dc_characters.db')
    cur = conn.cursor()

    if len(search) == 4 and int(search) > 1937 and int(search) < 2016:
        like = "%"
        year = "'" + search[:3] + like + "'"

        statement = "SELECT Characters.Name, Characters.FirstAppearanceYear, Alignments.Alignment FROM Characters JOIN Alignments ON Characters.AlignmentId=Alignments.Id WHERE Characters.FirstAppearanceYear LIKE " + year

        characters = cur.execute(statement)

        alignment_dict = {}
        for each in characters:
            dict_info = []
            if each[2] not in alignment_dict:
                alignment_dict[each[2]] = dict_info
            alignment_dict[each[2]].append(" " + each[0] + " - " + each[1])

        alignment_names = []
        character_info = []
        count = []
        for each in alignment_dict:
            alignment_names.append(each)
            character_info.append(alignment_dict[each])
            count.append(len(alignment_dict[each]))
        colors = []
        if alignment_names[0] == "Hero":
            colors = ["#0A87A3", "#A34D00"]
        elif alignment_names[0] == "Villain":
            colors = ["#A34D00", "#0A87A3"]

        fig = go.Figure()

        fig.add_trace(go.Pie(
            labels = alignment_names,
            values = count,
            marker_colors = colors,
            text = character_info,
            textinfo = "value",
            textfont_color = "white",
            hoverinfo = "text",
            hoverlabel = dict(font = dict(color = "white", family = "Open Sans")),
            hole = .5
        ))

        fig.update_layout(title = 'All Characters First Appearing in the ' + search[:3] + '0s')
        print("Generating pie chart...")
        fig.show()

    else:
        print("~~~~~Pleast enter a valid command~~~~~")

    conn.close()

    try:
        return character_info
    except Exception:
        pass


# ~~~~~~~~~~~~~~~~~~Part 3 - User Interaction~~~~~~~~~~~~~~~~~~
if __name__=="__main__":
# Check to see if database should be created/updated
    if len(sys.argv) > 1 and sys.argv[1] == '--init':
        print('Deleting old database and starting over...')
        init_db()
        insert_character_data()
        insert_alignment_data()
        insert_series_data()
        alignment_foreign_keys()
        series_foreign_keys()
    else:
        print(' ')

        # Process user command
        def execute_command(command):
            command_list = command.split(": ")
            if command_list[0] == "Scatter":
                if len(command_list) == 1:
                    plot_first_app_scatter()
                else:
                    print("~~~~~Please enter a valid command~~~~~")
            elif command_list[0] == "Bar":
                plot_first_app_bar(command_list[1])
            elif command_list[0] == "Series Pie":
                plot_first_app_series_pie(command_list[1])
            elif command_list[0] == "Decade Pie":
                plot_first_app_year_pie(command_list[1])
            else:
                print("~~~~~Please enter a valid command~~~~~")

        # Prompt for user command
        def search_prompt():
            response = ""
            while response != "exit":
                response = input("Options: \n 1) type 'Scatter' to see scatterplot timeline of first appearance for every character \n 2) type 'Bar: <Heroes, Villains, or Both>' to see bar chart of number of first appearances occurring in each year according to alignment \n 3) type 'Series Pie: <Heroes or Villains> <newest or oldest> <number between 1 and 60 for Heroes or number between 1 and 40 for Villains>' to see pie chart with titles of series that selection of characters first appeared in \n 4) type 'Decade Pie: <any year between 1938 and 2015>' to see pie chart with all Heroes and Villains first appearing in the same decade as input year \n 5) type 'exit' to quit program \n Enter Command: ")

                if response == 'exit':
                    print("Goodbye!")
                    break
                else:
                    execute_command(response)

        search_prompt()
