# The following is a simple 'hobby' class to calculate different income and house payment scenarios on a monthly basis.
# The code following the class definitions exemplifies how the class methods can be used to evaluate different scenarios.

class money:

	def __init__(self):

		self.food_cost=300
		self.gas_cost=100
		self.mortgage_cost=0
		self.allmoney=10000
		self.income=2400
		self.misc=300

	def set_food(self,amount):
		self.food_cost=amount

	def set_gas(self,amount):
		self.gas_cost=amount

	def set_mortgage(self,amount):
		self.mortgage_cost=amount

	def expense(self,amount):
		self.allmoney-=amount

	def inc_income(self,amount):
		self.income+=amount

	def add_interest(self,percent):
		print('interest added: {}'.format(int(.95*self.allmoney*percent)))
		self.income+=.95*self.allmoney*percent

	def monthly_net(self):
		local_net = self.income - (self.gas_cost + self.mortgage_cost + self.food_cost + self.misc)
		self.allmoney -= local_net
		return round(local_net,2)

	def purchase_house(self, cost, down, mortgage_rate, hoa):
		intermediate = (cost - down) / (30*12)
		intermediate = intermediate + intermediate * mortgage_rate
		prop_insurance = 0.0079 * cost/12
		intermediate += prop_insurance
		self.allmoney -= down
		self.mortgage_cost += intermediate + hoa
		print('new mortgage cost: {}'.format(self.mortgage_cost))


memoney = money()
memoney.purchase_house(100000,20000,.04,200)
memoney.inc_income(1000)
memoney.purchase_house(85000,10000,.04,200)
memoney.add_interest(.0012)

print(memoney.monthly_net(), memoney.allmoney)
