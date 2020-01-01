#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Only imports and save expense categories and expenses for now
# NOTE: This tool is not unit tested
# Refer to the sample.csv to follow the code: the format is quite unusual!
#

import csv
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Expense, IncomeCategory, Income


class Usage(Exception):
    """
    Dummy exception
    """
    pass


class Utils():
    """
    Parse, sanitize data and handle the database interactions
    """

    def __init__(self):
        engine = create_engine('sqlite:///../../db.sqlite3')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        # NOTE: assuming "," as thousand separator and no decimals
        self.CURRENCY_SYMBOL = '€'
        self.EXPENSE = 'EXPENSE'
        self.INCOME = 'INCOME'

        self.session = session
        self.cats = self.selectCategories()
        self.inc_cats = self.selectIncomeCategories()
        # Handle the case in which the first entry date is malformed
        self.last_date = '1970/01/01'
        self.last_income_date = '1970/01/01'

    def filterPrice(self, price):
        """
        Filter out white space and CURRENCY SYMBOL
        """
        return list(filter(lambda char: char not in f" {self.CURRENCY_SYMBOL},", price))

    def sanitizePrice(self, price):
        """
        Sanitize the price
        Return the sanitized price
        Return false on failure
        """
        price_chars = self.filterPrice(price)
        sanitized_price = "".join(price_chars)
        # TODO: can remove white space from here since we check in the helper
        if sanitized_price in ['Amount', ''] or not sanitized_price.isdigit():
            return False
        return sanitized_price

    def sanitizeDate(self, date, model_type):
        """
        Try to parse the date:
        On success, cache and return it
        On failure use the cached one or fall back to the default value
        """
        is_correct_format = False
        try:
            sanitized_date = datetime.strptime(date, '%Y/%m/%d')
            is_correct_format = True
        except ValueError as e:
            pass

        if date in [None, ''] or not is_correct_format:
            if model_type == self.EXPENSE:
                date = self.last_date
            else:
                date = self.last_income_date
        else:
            if model_type == self.EXPENSE:
                self.last_date = date
            else:
                self.last_income_date = date

        sanitized_date = datetime.strptime(date, '%Y/%m/%d')
        return sanitized_date

    def isHeader(self, category, category_type):
        """
        Check whether this row is an header or not
        Retrieve or Create a (Income)Category if the data is properly formatted
        Return the (Income)Category id
        Return false if this row was a header or on retrieve/creation failure
        """
        # Skip headers
        if category in ['Category', '', None]:
            return False
        return self.getOrCreateCategory(category, category_type)

    def selectCategories(self):
        """
        Select all Categories from the database
        """
        cats = self.session.query(Category).all()
        res = {}
        for cat in cats:
            c = cat.__dict__
            res[c['text']] = c['id']
        return res

    def selectIncomeCategories(self):
        """
        Select all Income Categories from the database
        """
        inc_cats = self.session.query(IncomeCategory).all()
        res = {}
        for cat in inc_cats:
            c = cat.__dict__
            res[c['text']] = c['id']
        return res

    def createCategory(self, text):
        """
        Insert a Category entry into the db
        """
        new_category = Category(text=text.capitalize())
        self.session.add(new_category)
        self.session.flush()
        self.session.commit()
        return new_category

    def createExpense(self, amount, note, date, cat):
        """
        Insert an Expense entry into the db
        """
        expense = Expense(amount=amount, note=note, date=date,
                          category_id=cat)
        self.session.add(expense)
        self.session.flush()
        self.session.commit()
        return expense

    def createIncomeCategory(self, text):
        """
        Insert an Income Category entry into the db
        """
        new_inc_category = IncomeCategory(text=text.capitalize())
        self.session.add(new_inc_category)
        self.session.flush()
        self.session.commit()
        return new_inc_category

    def CreateIncome(self, amount, note, date, cat):
        """
        Insert an Income entry into the db
        """
        income = Income(amount=amount, note=note, date=date,
                        category_id=cat)
        self.session.add(income)
        self.session.flush()
        self.session.commit()
        return income

    def getOrCreateCategory(self, name, category_type):
        """
        Return the existing Category from cache
        Create and return Categoty and update the cache
        """
        createFunc = self.createCategory
        if category_type == self.INCOME:
            createFunc = self.createIncomeCategory

        if category_type == self.EXPENSE:
            res = self.cats.get(name.capitalize(), None)
        else:
            res = self.inc_cats.get(name.capitalize(), None)

        if res is None:
            cat = createFunc(name)
            if category_type == self.EXPENSE:
                self.cats[cat.text] = cat.id
            else:
                self.inc_cats[cat.text] = cat.id
            res = cat.id
        return res

    def readExpenseData(self, row):
        """
        Determine whether the row contains Expense data or not
        Return a tuple with the data if it does
        Return False otherwise
        """
        if len(row) < 4:
            print("Csv file needs to have at least 4 colums")
            return False

        date = row[1]
        price = row[2]
        note = row[3]
        category = row[4]

        return self.prepareData(category, price, date, note, self.EXPENSE)

    def readIncomeData(self, row):
        """
        Determine whether the row contains Income data or not
        Return a tuple with the data if it does
        Return False otherwise
        """
        if len(row) < 9:
            print("Csv file needs to have at least 9 colums")
            return

        date = row[6]
        amount = row[7]
        note = row[8]
        category = row[9]
        return self.prepareData(category, amount, date, note, self.INCOME)

    def prepareData(self, category, price, date, note, model_type):
        """
        Sanitize the data and retrieve or create the (Income)Category
        Return the sanitized data on success
        Return false on failure
        """
        cat_id = self.isHeader(category, model_type)
        if not cat_id:
            return False

        sanitized_price = self.sanitizePrice(price)
        if not sanitized_price:
            return False

        sanitized_date = self.sanitizeDate(date, model_type)
        return (cat_id, sanitized_price, note, sanitized_date)

    def prepareCreateEntry(self, data, category_type):
        """
        Unpack the data and insert an Expense or Income entry into the database
        Does not return anything on both success and failure
        """
        createFunc = self.createExpense
        if category_type == self.INCOME:
            createFunc = self.CreateIncome

        cat_id = data[0]
        sanitized_price = data[1]
        note = data[2]
        safe_date = data[3]
        return createFunc(sanitized_price, note, safe_date, cat_id)


def main(argv):
    utils = Utils()
    try:
        if len(argv) != 2:
            raise Usage
    except Usage:
        print("Usage: csv_parser.py <csv-file-path>", file=sys.stderr)
        return 1

    csv_file = argv[1]
    expenses = 0
    income = 0
    with open(csv_file) as file:
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            expense_data = utils.readExpenseData(row)
            if expense_data:
                res = utils.prepareCreateEntry(expense_data, utils.EXPENSE)
                if res:
                    expenses += 1

            income_data = utils.readIncomeData(row)
            if income_data:
                res = utils.prepareCreateEntry(income_data, utils.INCOME)
                if res:
                    income += 1

    print(f"Created {expenses} expenses and {income} income entries")


if __name__ == "__main__":
    main(sys.argv)
