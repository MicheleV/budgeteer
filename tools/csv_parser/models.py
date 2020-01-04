from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import select
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker



# TODO: move this away from the global namespace
Base = declarative_base()


# NOTE: these Models are not automatically synced
#       with the one from the budgets module
# Tool valid as per migration `0005_auto_20191204_0821.py`
# Any following migration might break this script
class Category(Base):
    __tablename__ = 'budgets_category'
    id = Column(Integer, primary_key=True)
    text = Column(String)


class Expense(Base):
    """
    Mirror Category model from budgets module
    """
    __tablename__ = 'budgets_expense'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    note = Column(String(150))
    date = Column(Date)
    # Note: not definig the "ON DELETE" behaviour
    category_id = Column(Integer, ForeignKey("budgets_category.id"))


class IncomeCategory(Base):
    """
    Mirror IncomeCategory model from budgets module
    """
    __tablename__ = 'budgets_incomecategory'
    id = Column(Integer, primary_key=True)
    text = Column(String(20))


class Income(Base):
    """
    Mirror Income model from budgets module
    """
    __tablename__ = 'budgets_income'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    note = Column(String(150))
    date = Column(Date)
    # Note: not definig the "ON DELETE" behaviour
    category_id = Column(Integer, ForeignKey("budgets_incomecategory.id"))
