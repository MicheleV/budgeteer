# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import datetime
import functional_tests.helpers as Helpers


def test_cant_create_an_empty_monthly_budget(self):
    # TODO Franks wants to create a budget but being confused,
    pass


def test_can_create_multiple_monthly_budgets(self):
    # Frank creates a category to log expenses related his rent
    category_name = 'Rent'
    Helpers.create_a_category(self, category_name)

    budget_date = datetime.date.today().replace(day=1)
    amount = 7000
    Helpers.create_a_monthly_budget(self, category_name, amount,
                                    budget_date.strftime("%Y-%m-%d"))

    # TODO Frank hopes that one day he will not have to do this operation every
    #      month
    # self.fail("Write me!")


def test_cant_create_multiple_monthly_budgets_for_same_month(self):
    # TODO Franks wants to update the budget amount
    pass
