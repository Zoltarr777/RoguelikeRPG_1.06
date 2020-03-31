class Equipment_Item:
	def __init__(self, use_equipment_function=None, **kwargs):
		self.use_equipment_function = use_equipment_function
		self.equipment_function_kwargs = kwargs