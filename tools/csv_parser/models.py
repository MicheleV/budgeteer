from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy import select, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc

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
