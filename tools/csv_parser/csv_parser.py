#
# Only imports and save expense categories and expenses for now
#

import csv
import sys
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy import select, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# NOTE: this Model not synced with the models
#       Any migration involving Categories might break this
class Category(Base):
    __tablename__ = 'budgets_category'
    id = Column(Integer, primary_key=True)
    text = Column(String)


class Expense(Base):
    __tablename__ = 'budgets_expense'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    note = Column(String(150))
    date = Column(Date)
    # Note: not definig the "ON DELETE" behaviour
    category_id = Column(Integer, ForeignKey("budgets_category.id"))


class IncomeCategory(Base):
    __tablename__ = 'budgets_incomecategory'
    id = Column(Integer, primary_key=True)
    text = Column(String(20))


class Income(Base):
    __tablename__ = 'budgets_income'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    note = Column(String(150))
    date = Column(Date)
    # Note: not definig the "ON DELETE" behaviour
    category_id = Column(Integer, ForeignKey("budgets_incomecategory.id"))


class DBManager():

    def __init__(self):
        engine = create_engine('sqlite:///../../db.sqlite3')
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        self.session = session

    def selectCategories(self):
        cats = self.session.query(Category).all()
        res = {}
        for cat in cats:
            c = cat.__dict__
            res[c['text']] = c['id']
        return res

    def selectIncomeCategories(self):
        cats = self.session.query(IncomeCategory).all()
        res = {}
        for cat in cats:
            c = cat.__dict__
            res[c['text']] = c['id']
        return res

    def insertCategory(self, text):
        new_category = Category(text=text.capitalize())
        self.session.add(new_category)
        self.session.flush()
        self.session.commit()
        return new_category

    def insertExpense(self, amount, note, date, cat):
        expense = Expense(amount=amount, note=note, date=date,
                          category_id=cat)
        self.session.add(expense)
        self.session.flush()
        self.session.commit()
        return expense

    def InsertIncome(self, amount, note, date, cat):
        expense = Expense(amount=amount, note=note, date=date,
                          category_id=cat)
        self.session.add(expense)
        self.session.flush()
        self.session.commit()
        return expense

    def getCategory(self, cats, name):
        if name is None:
            print('error', name)
            pass
        res = cats.get(name.capitalize(), None)

        if res is None:
            cat = self.insertCategory(name)
            cats[cat.text] = cat.id
            res = cat.id
        return res


class Usage(Exception):
    pass


def ExpenseOrIncome(row):
    pass


def main(argv):
    dbm = DBManager()
    try:
        if len(argv) != 2:
            raise Usage
    except Usage:
        print("Usage: csv_parser.py <csv-file-path>", file=sys.stderr)
        return 1
    csv_file = argv[1]

    cats = dbm.selectCategories()
    inc_cats = dbm.selectIncomeCategories()
    filename = csv_file
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # Handle the case in which the first entry date is malformed
        last_date = '1970/01/01'
        for row in csv_reader:
            # Expense
            date = row[1]
            price = row[2]
            note = row[3]
            cat_text = row[4]

            # Income
            date = row[6]
            amout = row[7]
            description = row[8]
            category = row[9]

            # Skip headers
            if cat_text in ['Category', '']:
                continue
            cat_id = dbm.getCategory(cats, cat_text)

            price_chars = list(filter(lambda char: char not in " ¥,", price))
            price_safe = "".join(price_chars)
            # Skip headers and lines without prices
            if price_safe in ['Amount', ''] or not price_safe.isdigit():
                continue

            # Save the last non-malfomed date if the entry has no date
            if date in [None, '']:
                date = last_date
            else:
                last_date = date
            safe_date = datetime.strptime(date, '%Y/%m/%d')

            try:
                dbm.insertExpense(price_safe, note, safe_date, cat_id)
            except:
                print(f'INSERT INTO "budget_expenses" VALUES ({price_safe},"{note}","{date}",{cat_id})')


if __name__ == "__main__":
    main(sys.argv)
