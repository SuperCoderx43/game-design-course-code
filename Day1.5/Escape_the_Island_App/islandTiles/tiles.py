from IslandTile import IslandTile
from enemy.enemy import Crab, Crocodile, Deer, Dragon, Gecko, Gladiator, Monkey, Monsters, Rabbit, Samurai, Spider
from item.items import Blue_Fruit, Emerald, Purple_Fruit, Red_Fruit, Rusty_Blade, White_Fruit

# temple
temple_items = (Red_Fruit)
temple_encounters = (Monkey,)

# spring
spring_items = (Blue_Fruit)
spring_encounters = (Crocodile, )

# beach
beach_items = (Rusty_Blade)
beach_encounters = (Crab, Gecko)

# ravine
ravine_items = (Emerald)
ravine_encounters = (None)

# camp
camp_items = (None)
camp_encounters = (Deer, Gecko, Rabbit)

# pit
pit_items = (Purple_Fruit)
pit_encounters = (Gladiator, )

# ruins
ruins_items = (White_Fruit)
ruins_encounters = (Samurai,)

# cave
cave_items = (None)
cave_encounters = (Spider, )

# mountain
mountain_items = (None)
mountain_encounters = (Dragon, )




temple = IslandTile("the Temple", temple_items , temple_encounters, "As you push your way through the thick vegetation, you stumble upon an ancient Temple standing stalwart in a small clearing. The area around the temple seems quiet. Too quiet...")
spring = IslandTile("the Spring", spring_items, spring_encounters,"The soft gurgle of water leads you up a small bluff to reveal a small spring, its waters bubbling out of the rocks.")
beach = IslandTile("the Beach", beach_items, beach_encounters, "You emerge from the jungle onto the beach. 'If I weren't stuck here, this beach would be a beautiful place,' you think to yourself bitterly.")
ravine = IslandTile("the Ravine", ravine_items, ravine_encounters, "There is barely any warning as you emerge from the jungle and find yourself facing a massive ravine. You look precariously over the edge, but it is so deep you cannot see the bottom")
camp = IslandTile("your campsite",camp_items, camp_encounters,"You are back at your meager camp")
pit = IslandTile("the Fighting Pit", pit_items, pit_encounters, "An old pit used as a battleground between fighters for entertainment. Some of the fighting blood still remains...")
ruins = IslandTile("the Ancient Ruins", ruins_items, ruins_encounters, "The ruins of a civilization remain in a withered form of its old self. Ghosts of the past may still remain...")
cave = IslandTile('the Cave', cave_items, cave_encounters, 'A dark hole in the ground with a webs crawling out of the front.')
mountain = IslandTile('the Towering Mountain', mountain_items, mountain_encounters, 'A towering mountain that looms above the whole mountain. A faint glow can be seen at the top.')