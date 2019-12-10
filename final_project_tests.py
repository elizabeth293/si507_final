import requests
import csv
import json
from bs4 import BeautifulSoup
import sys
import sqlite3
import plotly.graph_objs as go
from colour import Color
import random
import unittest
import final_project as proj



class TestDataRetrieval(unittest.TestCase):

    def testHeroesList(self):
        csv = "Heroes.csv"
        heroes = proj.get_heroes_list(csv)
        self.assertEqual(heroes[4], "Green Lantern")
        self.assertEqual(heroes[-1], "Rip Hunter")

    def testVillainsList(self):
        csv = "Villains.csv"
        villains = proj.get_villains_list(csv)
        self.assertEqual(villains[4], "Black Adam")
        self.assertEqual(villains[-1], "Doctor Sivana")

    def testCharacterInfo(self):
        all_characters = proj.get_character_info()
        self.assertEqual(len(all_characters), 100)
        self.assertEqual(all_characters["Aquaman"]["alignment"], "Hero")
        self.assertEqual(all_characters["Captain Cold"]["first appearance series"], "SHOWCASE")
        self.assertEqual(all_characters["Hawkman"]["first appearance year"], "1940")
        self.assertEqual(all_characters["Deadshot"]["occupation"], "Assassin")
        self.assertEqual(all_characters["Wonder Woman"]["real name"], "Diana")
        self.assertEqual(all_characters["Darkseid"]["image url"], "https://www.dccomics.com/sites/default/files/styles/character_thumb_160x160/public/Char_Profile_Darkseid_5c48a0ddca62a1.25457560.jpg?itok=kDwRB8Fh")


class TestDatabase(unittest.TestCase):

    def testCharacterTable(self):
        conn = sqlite3.connect('dc_characters.db')

        cur1 = conn.cursor()
        query1 = cur1.execute("SELECT Characters.Name, Characters.RealName, Characters.FirstAppearanceYear FROM Characters WHERE Characters.AlignmentId=1")
        data1 = []
        for each in query1:
            data1.append(each)
        self.assertEqual(data1[0][0], "Alfred Pennyworth")
        self.assertEqual(data1[0][1], "None")
        self.assertEqual(data1[0][2], "1943")

        cur2 = conn.cursor()
        query2 = cur2.execute("SELECT Characters.Name, Characters.RealName, Characters.FirstAppearanceYear FROM Characters WHERE Characters.AlignmentId=2")
        data2 = []
        for each in query2:
            data2.append(each)
        self.assertEqual(data2[-1][0], "Zoom")
        self.assertEqual(data2[-1][1], "None")
        self.assertEqual(data2[-1][2], "2001")

        conn.close()

    def testAlignmentsTable(self):
        conn = sqlite3.connect('dc_characters.db')

        cur = conn.cursor()
        query = cur.execute("SELECT * FROM Alignments")
        data = []
        for each in query:
            data.append(each)
        self.assertEqual(data[0][1], "Hero")
        self.assertEqual(data[1][1], "Villain")

        conn.close()

    def testSeriesTable(self):
        conn = sqlite3.connect('dc_characters.db')

        cur = conn.cursor()
        query = cur.execute("SELECT * FROM Series")
        data = []
        for each in query:
            data.append(each)
        self.assertEqual(data[1][1], "ACTION COMICS")
        self.assertEqual(data[44][1], "THE BRAVE AND THE BOLD")

        conn.close()


class TestDataProcessing(unittest.TestCase):

    def testScatterPlot(self):
        data = proj.plot_first_app_scatter()
        heroes = data[0]
        villains = data[1]
        self.assertEqual(heroes[31], 'Jimmy Olsen - Hero, SUPERMAN #13 (1941), https://www.dccomics.com/sites/default/files/styles/character_thumb_160x160/public/Char_Profile_JimmyOlsen_5c4fa2975d6739.57945186.jpg?itok=F1Nrjlms')
        self.assertEqual(villains[34], 'The Cheetah - Villain, WONDER WOMAN #6 (1943), https://www.dccomics.com/sites/default/files/styles/character_thumb_160x160/public/Char_Profile_Cheetah_5d79b0ed720745.29138707.jpg?itok=0TSyF9m8')

    def testBarGraph(self):
        data = proj.plot_first_app_bar("Both")
        heroes = data[0]
        villains = data[1]
        self.assertEqual(heroes["1940"], 7)
        self.assertEqual(villains["1959"], 2)

    def testSeriesPie(self):
        data = proj.plot_first_app_series_pie("Heroes oldest 20")
        self.assertEqual(data[0], "ACTION COMICS")
        self.assertEqual(data[-1], "CAPTAIN MARVEL ADVENTURES")

    def testDecadePie(self):
        data = proj.plot_first_app_year_pie("1940")
        heroes = data[0]
        villains = data[1]
        self.assertEqual(heroes[1], " Aquaman - 1941")
        self.assertEqual(villains[2], " Joker - 1940")


unittest.main(verbosity = 2)
