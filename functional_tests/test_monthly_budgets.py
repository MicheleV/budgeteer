# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
def test_cannot_create_an_empty_monthly_budget(self):
  # TODO Franks wants to create a budget but being confused, leaves the amount field empty
  pass

def test_can_create_multiple_monthly_budgets(self):
  # Frank creates a category to log expenses related his rent
  self.create_a_category('Rent')

  category_name = 'Rent'
  amount= 7000
  date = '2019-10-01'
  self.create_a_monthly_budget(category_name, amount, date)

  # TODO Frank hopes that one day he will not have to do this operation every month
  # self.fail("Write me!")

def test_can_not_create_multiple_monthly_budgets_for_the_same_month(self):
  # TODO Franks wants to fix the budget he has just create, by creating a new one
  # with the same date and category, but with a different amount
  pass