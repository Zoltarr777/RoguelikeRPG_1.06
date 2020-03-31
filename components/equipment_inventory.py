import tcod as libtcod

from game_messages import Message

class Equipment_Inventory:
	def __init__(self, capacity):
		self.capacity = capacity
		self.equipment_items = []

	def add_equipment_item(self, equipment_item):
		results = []

		if len(self.equipment_items) >= self.capacity:
			results.append({
				'equipment_item_added': None,
				'message': Message("You can't carry any more equipment, your equipment inventory is full!", libtcod.yellow)
			})
		else:
			results.append({
				'equipment_item_added': equipment_item,
				'message': Message("You pick up the {0}!".format(equipment_item.name), libtcod.blue)
			})

			self.equipment_items.append(equipment_item)

		return results

	def use_equipment(self, equipment_item_entity, **kwargs):
		results = []

		equipment_item_component = equipment_item_entity.equipment_item

		if equipment_item_component.use_equipment_function is None:
			results.append({'message': Message("The {0} can't be used".format(equipment_item_entity.name), libtcod.yellow)})
		else:
			kwargs = {**equipment_item_component.equipment_function_kwargs, **kwargs}
			equipment_item_use_results = equipment_item_component.use_equipment_function(self.owner, **kwargs)

			for equipment_item_use_result in equipment_item_use_results:
				if equipment_item_use_result.get("equipment_consumed"):
					self.remove_equipment_item(equipment_item_entity)

			results.extend(equipment_item_use_results)

		return results


	def remove_equipment_item(self, equipment_item):
		self.equipment_items.remove(equipment_item)