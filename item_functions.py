import tcod as libtcod

import math

from components.ai import ConfusedMonster

from game_messages import Message

def heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount') + (entity.fighter.magic * 2)

	results = []

	if entity.fighter.hp == entity.fighter.max_hp:
		results.append({'consumed': False, 'message': Message("You're already at full health!", libtcod.orange)})
	else:
		entity.fighter.heal(amount)
		results.append({'consumed': True, 'message': Message("You heal yourself for {0} hit points. Your wounds start to feel better!".format(amount), libtcod.green)})

	return results

def cast_lightning(*args, **kwargs):
	caster = args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage') + caster.fighter.magic
	maximum_range = kwargs.get('maximum_range')

	results = []

	target = None
	closest_distance = maximum_range + 1

	for entity in entities:
		if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
			distance = caster.distance_to(entity)

			if distance < closest_distance:
				target = entity
				closest_distance = distance

	if target:
		results.append({'consumed': True, 'target': target, 'message': Message("A lightning bolt strikes the {0} with a loud thunder! It dealt {1} damage.".format(target.name, damage))})
		results.extend(target.fighter.take_damage(damage))
	else:
		results.append({'consumed': False, 'target': None, 'message': Message("No enemy is close enough to strike...", libtcod.orange)})

	return results

def cast_fireball(*args, **kwargs):
	player = args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage') + (player.fighter.magic * 2)
	radius = kwargs.get('radius') + math.floor(player.fighter.magic / 2)
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')

	results = []

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'consumed': False, 'message': Message("You can't target a location outside your field of view.", libtcod.red)})
		return results

	results.append({'consumed': True, 'message': Message("The fireball explodes, burning everything within {0} tiles!".format(radius), libtcod.orange)})

	for entity in entities:
		if entity.distance(target_x, target_y) <= radius and entity.fighter:
			results.append({'message': Message("The {0} gets burned for {1} HP.".format(entity.name, damage), libtcod.orange)})
			results.extend(entity.fighter.take_damage(damage))

	return results

def cast_confusion(*args, **kwargs):
	player = args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	target_x = kwargs.get('target_x')
	target_y = kwargs.get('target_y')
	turns_confused = 10 + player.fighter.magic

	results = []

	if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
		results.append({'consumed': False, 'message': Message("You can't target a location outside your field of view.", libtcod.red)})
		return results

	for entity in entities:
		if entity.x == target_x and entity.y == target_y and entity.ai:
			confused_ai = ConfusedMonster(entity.ai, turns_confused)

			confused_ai.owner = entity
			entity.ai = confused_ai

			results.append({'consumed': True, 'message': Message("The eyes of the {0} look vacant, as it starts to stumble around! They are confused for {1} turns!".format(entity.name, turns_confused), libtcod.light_green)})

			break
	else:
		results.append({'consumed': False, 'message': Message("There is no targetable enemy at that location.", libtcod.red)})

	return results

def cast_magic(*args, **kwargs):
	caster = args[0]
	entities = kwargs.get('entities')
	fov_map = kwargs.get('fov_map')
	damage = kwargs.get('damage') + caster.fighter.magic
	maximum_range = kwargs.get('maximum_range') + math.floor(caster.fighter.magic / 2)

	results = []

	target = None
	closest_distance = maximum_range + 1

	for entity in entities:
		if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
			distance = caster.distance_to(entity)

			if distance < closest_distance:
				target = entity
				closest_distance = distance

	if target:
		results.append({'staff_used': True, 'target': target, 'message': Message("You blast the {0} with magic! It dealt {1} damage.".format(target.name, damage), libtcod.red)})
		results.extend(target.fighter.take_damage(damage))
	else:
		results.append({'consumed': False, 'target': None, 'message': Message("No enemy is close enough to blast...", libtcod.orange)})

	return results