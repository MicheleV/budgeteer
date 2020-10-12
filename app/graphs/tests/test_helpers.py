# Copyright: (c) 2020, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.test import TestCase
import graphs.plot as p


class TestHelpers(TestCase):
    """Unit tests for helper functions."""

    def test_pie_slice_font_size(self):
        """
        Test we get the correct font size for the pie graph,
        based on the data sample size
        """
        data_categories = range(21)
        font_size = p.get_pie_slice_font_size(data_categories)
        self.assertEqual(font_size, 'xx-small')

        data_categories = range(20)
        font_size = p.get_pie_slice_font_size(data_categories)
        self.assertEqual(font_size, 'x-small')

        data_categories = range(16)
        font_size = p.get_pie_slice_font_size(data_categories)
        self.assertEqual(font_size, 'x-small')

        data_categories = range(14)
        font_size = p.get_pie_slice_font_size(data_categories)
        self.assertEqual(font_size, 'medium')

    def test_pie_legend_font_size(self):
        """
        Test we get the correct font size for the pie graph legend,
        based on the data sample size
        """
        data_categories = range(16)
        font_size = p.get_pie_legend_font_size(data_categories)
        self.assertEqual(font_size, 'xx-small')

        data_categories = range(15)
        font_size = p.get_pie_legend_font_size(data_categories)
        self.assertEqual(font_size, 'x-small')

        data_categories = range(11)
        font_size = p.get_pie_legend_font_size(data_categories)
        self.assertEqual(font_size, 'x-small')

        data_categories = range(10)
        font_size = p.get_pie_legend_font_size(data_categories)
        self.assertEqual(font_size, 'medium')

    def test_bar_x_axis_tick_font_size(self):
        """
        Test we get the correct font size for the bar graph
        ticks on the x axis, based on the data sample size
        """
        data_points = range(51)
        font_size = p.get_bar_ticket_font_size(data_points)
        self.assertEqual(font_size, 'xx-small')

        data_points = range(50)
        font_size = p.get_bar_ticket_font_size(data_points)
        self.assertEqual(font_size, 'x-small')

        data_points = range(37)
        font_size = p.get_bar_ticket_font_size(data_points)
        self.assertEqual(font_size, 'x-small')

        data_points = range(36)
        font_size = p.get_bar_ticket_font_size(data_points)
        self.assertEqual(font_size, 'medium')

    def test_goal_legend_font_size(self):
        """
        Test we get the correct font size for the goal legend
        based on the data sample size
        """
        goals = range(11)
        font_size = p.get_goal_font_size(goals)
        self.assertEqual(font_size, 'xx-small')

        goals = range(10)
        font_size = p.get_goal_font_size(goals)
        self.assertEqual(font_size, 'x-small')

        goals = range(3)
        font_size = p.get_goal_font_size(goals)
        self.assertEqual(font_size, 'x-small')

        goals = range(2)
        font_size = p.get_goal_font_size(goals)
        self.assertEqual(font_size, 'medium')
