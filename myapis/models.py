from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sector_level1 = models.CharField(max_length=255)
    sector_level2 = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StockData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='stocks')
    asof = models.DateField()
    volume = models.BigIntegerField()
    close_usd = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"{self.company.name} - {self.asof}"
