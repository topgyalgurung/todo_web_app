#!/usr/bin/python

import sqlite3

with sqlite3.connect("database.db") as connection:
	c = connection.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS posts(List Text, Note Text)")
	c.execute("CREATE TABLE IF NOT EXISTS users(Name Text)")