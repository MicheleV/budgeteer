# Copyright: (c) 2019, Michele Valsecchi <https://github.com/MicheleV>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from django.db import models

class Category(models.Model):
  text = models.TextField(default='')

  # def get_absolute_url(self):
  #   return reverse('category', args=[self.id])

