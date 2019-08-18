# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
def test_can_create_multiple_expense(self):
  CATEGORY_NAME = 'Rent'
  self.create_a_category(CATEGORY_NAME)

  # Frank visits the expenses url and enters the expens details
  self.create_an_expense(
    500,
    CATEGORY_NAME,
    'First month of rent',
    '2019-08-09'
  )

  # Frank visits the expenses url again and enters a second expense with its details
  self.create_an_expense(
    420,
    CATEGORY_NAME,
    'Second month of rent (discounted)',
    '2019-09-09'
  )

# TODO add negative test
# I.e. try to post with missing fields, etc
def test_can_not_create_malformed_expenses(self):
  # TODO at the moment being, empty memo field will succeed
  pass
