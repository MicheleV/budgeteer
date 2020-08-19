# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import json

from django.urls import resolve
from django.urls import reverse
import functional_tests.helpers as Helpers

# Use this syntax to get plain json
# http://example.com/<route-name>?format=json&json=true'
@Helpers.register_and_login
def test_create_and_delete_expenses(tester):

    # Frank can create a category to log his food expenses
    Helpers.create_a_category(tester, 'Food')

    url = reverse('api:categories')
    # Frank has knowledge of how to force the site to display json
    secret_url = f"{tester.live_server_url}{url}?format=json&json=true'"
    tester.browser.get(secret_url)

    html = tester.browser.find_element_by_tag_name('html')
    json_res = json.loads(html.text)

    # Franks is happy with the resutls
    tester.assertEqual(len(json_res), 1)
    tester.assertEqual(json_res[0]['id'], 1)
    tester.assertEqual(json_res[0]['text'], 'Food')

    # Frank does not trust the API, and he wants to check if new Categories
    # will appear in his next call or not
    Helpers.create_a_category(tester, 'Rent')

    tester.browser.get(secret_url)

    html = tester.browser.find_element_by_tag_name('html')
    json_res = json.loads(html.text)

    # Franks is happy with the results
    tester.assertEqual(len(json_res), 2)
    tester.assertEqual(json_res[1]['id'], 2)
    tester.assertEqual(json_res[1]['text'], 'Rent')
