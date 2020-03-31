import tcod as libtcod

from game_messages import Message


class Fighter:
	def __init__(self, hp, defense, power, magic, xp=0):
		self.base_max_hp = hp
		self.hp = hp
		self.base_defense = defense
		self.base_power = power
		self.base_magic = magic
		self.xp = xp

	@property
	def max_hp(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.max_hp_bonus
		else:
			bonus = 0

		return self.base_max_hp + bonus

	@property
	def power(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.power_bonus
		else:
			bonus = 0

		return self.base_power + bonus

	@property
	def defense(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.defense_bonus
		else:
			bonus = 0

		return self.base_defense + bonus

	@property
	def magic(self):
		if self.owner and self.owner.equipment:
			bonus = self.owner.equipment.magic_bonus
		else:
			bonus = 0

		return self.base_magic + bonus

	def take_damage(self, amount):
		results = []

		self.hp -= amount

		if self.hp <= 0:
			results.append({'dead': self.owner, 'xp': self.xp})

		return results

	def heal(self, amount):
		self.hp += amount

		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def equipment_heal(self, amount):
		self.hp += amount

		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def attack(self, target):
		results = []

		damage = round(self.power * (10 / (10 + target.fighter.defense)))

		if damage > 0:
			results.append({'message': Message("{0} attacks {1} for {2} hit points.".format(self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
			results.extend(target.fighter.take_damage(damage))
		else:
			results.append({'message': Message("{0} attacks {1} but does no damage.".format(self.owner.name.capitalize(), target.name), libtcod.white)})
			results.extend(target.fighter.take_damage(damage))
		return results