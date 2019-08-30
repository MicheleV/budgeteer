# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.db import models

class Category(models.Model):
  text = models.CharField(max_length=20, default=None)

  # def get_absolute_url(self):
  #   return reverse('category', args=[self.id])

class Expense(models.Model):

  def __str__(self):
    return f"{self.category.id} ({self.category.text}), {self.amount}, {self.note}, {self.spended_date}"
  # TODO should we really delete expenses item on Category deletion?
  # This will remove history!
  category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
  amount = models.IntegerField()
  note = models.CharField(max_length=150, default='')
  spended_date = models.DateField()

class MonthlyBudget(models.Model):
  # TODO should we really delete Monthly Budgets on Category deletion?
  # This will remove history!
  category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE)
  amount = models.IntegerField()
  date = models.DateField()