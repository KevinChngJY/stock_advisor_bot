from django.db import models

# Create your models here.
class userdatabase(models.Model):
	auto_increment_id = models.IntegerField(primary_key=True)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	role = models.CharField(max_length=100)
	telegram_id = models.CharField(max_length=100,default="-")
	def __str__(self):
		return str(self.auto_increment_id) + ' ' + self.username

class bursalist(models.Model):
	auto_increment_id = models.IntegerField(primary_key=True)
	company = models.CharField(max_length=100)
	company_official = models.CharField(max_length=100)
	company_listing = models.CharField(max_length=100)
	company_tickname = models.CharField(max_length=100)
	company_status = models.CharField(max_length=100)
	exchange = models.CharField(max_length=100,default="bursa")
	trading_view_symbol = models.CharField(max_length=100,default="-")
	def __str__(self):
		return str(self.auto_increment_id) + ' ' + self.company + ' ' + self.company_tickname

class option1_selection(models.Model):
	auto_increment_id = models.IntegerField(primary_key=True)
	#username
	username = models.CharField(max_length=100)

	#Price
	current_price = models.BooleanField()
	price_change = models.BooleanField()
	price_change_percentage = models.BooleanField()
	previous_close_price = models.BooleanField()
	open_price = models.BooleanField()
	daily_low = models.BooleanField()
	daily_high = models.BooleanField()
	yearly_high = models.BooleanField()
	yearly_low = models.BooleanField()
	get_50_days_moving_average_price = models.BooleanField()
	get_200_days_moving_average_price = models.BooleanField()

	#volume
	current_volume=models.BooleanField()
	get_10_days_average_volume = models.BooleanField()
	get_3_months_average_volume = models.BooleanField()

	#Fundamental Indicator
	market_cap = models.BooleanField()
	pe_ratio = models.BooleanField()

	#technical Indicator
	rsi_14 = models.BooleanField()
	rsi_28 = models.BooleanField()
	percentage_price_oscillator = models.BooleanField()
	percentage_volume_oscillator = models.BooleanField()
	rate_of_change = models.BooleanField()
	stochastic_oscillator = models.BooleanField()
	willianR = models.BooleanField()
	ADI = models.BooleanField()
	chaikin_money_flow = models.BooleanField()
	negative_volume_index = models.BooleanField()
	On_balance_volume = models.BooleanField()
	volume_price_trend = models.BooleanField()
	volume_weighted_average_price_14days = models.BooleanField()

	def __str__(self):
		return str(self.auto_increment_id) + ' ' + self.username

class option3_stock_monitoring(models.Model):
	auto_increment_id = models.IntegerField(primary_key=True)
	username = models.CharField(max_length=100)
	company_official = models.CharField(max_length=100)
	company_tickname = models.CharField(max_length=100)
	exchange = models.CharField(max_length=100)

	def __str__(self):
		return str(self.auto_increment_id) + ' ' + self.username

class sentimentanalysistop10(models.Model):
	categories = models.CharField(max_length=200)
	top10 = models.CharField(max_length=1000)

	def __str__(self):
		return str(self.categories)
