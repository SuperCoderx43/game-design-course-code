from Monsters import Monsters
import item.items as Item

Crocodile = Monsters(True, "Crocodile", 10, 1, 'boss', 'A green scaled lizard the size of a minivan with foot long teeth. Bigger than any zoo Crocodile.', 'The large corpse wails its last breath and you grab a large tooth from its mouth as a souvenir.', Item.Large_Tooth, {0: ("snatch", 2), 1:("claw", 1)})
Spider = Monsters(True, "Spider", 10, 1, 'boss', 'A humongous spider with a thousand eyes and a red blotch on its stomach.', "The eight-legged monster crumbles to the ground. One of its eyes glows brighter than the rest so you pluck it as a souvenir.", Item.Spider_Eye, {0: ("bite", 2), 1:("poison", 1)})
Gladiator = Monsters(True, "Skeleton Gladiator", 50, 5, 'boss', 'An old skeleton driven by the bloodlust of its past. Its eyes glow red with rage.', 'The Gladiator\'s bones rattle to the floor and blood seeps out of its skull. You draw the blood from the skeleton and keep it as a souvenir.', Item.Gladiator_Blood, {0: ("stab", 7), 1:("slash", 3)})
Dragon = Monsters(True, "Old Dragon", 100, 10, 'boss', 'An ancient dragon guards its longstanding home. If you want something from it, it will not let you get it easily', 'The ancient dragon falls and its body turns into dust. A glow from the dragon\'s nest catches your eye and you find it to be a Mysterious Power Source.', Item.Power_Source, {0: ("fire breath", 25), 1:("chomp", 25)})
Monkey = Monsters(True, "Intelligent Ape", 25, 5, 'boss', "A large monkey who has crafted many tools. He will defend his ancient temple to the best of his ability.", "The monkey's tools were not good enough for you and he dies. You take the Golden Monkey Statuette that he was defending.", Item.Golden_Monkey, {0: ("hammer", 7), 1:("knife throw", 3)})
Samurai = Monsters(True, "Samurai", 50, 5, 'boss', "The only other human-like person on this island. A samurai who still wanders his ancient home.", "The samurai falls and drop his sword. The sword hits the ground and snaps; You collect the fragments of the sword for yourself.", Item.Blade_Frag, {0: ("slice", 10), 1:("stab", 10)})

Cliffs = Monsters(True, "Crumbling Cliffs", 0, 0, 'hazard', 'You fall to your death off the Crumbling Cliffs', '', (), {})

Deer = Monsters(True, "Deer", 1, 0, 'nature', 'The deer is simply wandering around.', '', (), {})
Rabbit = Monsters(True, "Rabbit", 1, 0, 'nature', "The rabbit quickly hides in your presence.", "", (), {})
Gecko = Monsters(True, "Gecko", 1, 0, 'nature', "The gecko stares ominously at you.", "", (), {})
Crab = Monsters(True, "Crab", 1, 0, 'nature', "The crab sidewalks away from you.", "", (), {})