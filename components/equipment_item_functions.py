import tcod as libtcod

from game_messages import Message

def equipment_heal(*args, **kwargs):
	entity = args[0]
	amount = kwargs.get('amount')

	results = []

	if entity.fighter.hp == entity.fighter.max_hp:
		results.append({'equipment_consumed': False, 'message': Message("You're already at full health!", libtcod.yellow)})
	else:
		entity.fighter.equipment_heal(amount)
		results.append({'equipment_consumed': True, 'message': Message("You heal yourself for {0} hit points!".format(amount), libtcod.green)})

	return results