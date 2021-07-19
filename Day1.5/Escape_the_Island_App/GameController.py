from enemy.enemy import Spider
from islandTiles.tiles import temple, spring, beach, camp, ruins, pit, ravine, cave, mountain
from item.items import Blade_Frag, Blue_Fruit, Emerald, Food, Rusty_Blade, Samurai_Sword, Wood, Gladiator_Blood, Golden_Monkey, Large_Tooth, Power_Source, Spider_Eye, Tooth_Sword, Water, Beacon

import numpy as np
import time

class GameController:

    island_map = {"temple": temple, 
               "spring": spring, 
               "beach": beach, 
               "ravine": ravine, 
               "camp": camp,
               "ruins": ruins,
               "pit": pit,
               "cave": cave,
               "mountain": mountain}
    
    def __init__(self):
        self.alive = True
        self.days = 0
        self.hp = 10
        self.maxhp = 10
        self.inventory = []

    def showInv(self):
        print("\nInventory: ")
        inventory = ""
        for thing in self.inventory:
            inventory += thing['item'].name + " // Quantity: " + str(thing['quantity'])+"\n"
        print(inventory)

    def addLoot(self, loot):
        # print("Adding loot...")
        for new_item in loot:
            seen = False
            if new_item == None:
                # print("Found Nothing")
                continue
            if len(self.inventory) == 0:
                self.inventory.append({'item': new_item, 'quantity': 1})
                # print("Added Something")
                continue
            for old_item in self.inventory:
                # self.showInv()
                # print("Event A")
                if new_item.name == old_item['item'].name:
                    seen = True
                    old_item['quantity'] += 1
                    # print("Increased Something")
                    continue
            if not seen:
                self.inventory.append({'item': new_item, 'quantity': 1})
                # print("Added Something #2")
        # print("done looting!")

    def fightScene(self, encounter):
        print("\n*************\nFIGHT!\n*************\n")
        encounter.hp = encounter.maxhp
        weapon_tally = 0
        weapons = []
        for x in self.inventory:
            if x['item'].quality == "weapon":
                weapon_tally += 1
                weapons.append(x['item'])
                active_weapon = x['item']
        if weapon_tally > 1:
            print("Choose a weapon: ")
            index = 1
            for x in weapons:
                print(str(index)+": "+x.name)
                index += 1
            while True:
                try:
                    response = input("Input: ")
                    response = int(response)
                except:
                    print("Please Choose a Valid Index!")
                else:
                    if type(response) == int and response > 0 and response <= len(weapons):
                        break 
                    else:
                        print("Please Choose a Valid Index!")        
            active_weapon = weapons[response-1]  
            print("You chose: " + active_weapon.name + "\n")
        while True:
            strategy = ""
            print("Your Health: " + str(self.hp) + "/" + str(self.maxhp))
            print(encounter.name + "'s Health: " + str(encounter.hp) + "/" + str(encounter.maxhp))
            while True:
                strategy = input("Choose to Attack or Run Away (A/R) ")
                try:
                    if strategy.upper() == "A" or strategy.upper() == "R":
                        break
                except:
                    print("Invalid Input! Try Again")
                else:
                    print("Invalid Input! Try Again")
            if strategy.upper() == "R":
                print("You chose 'Run Away'!")
                return 0
            print("You chose 'Attack'!")
            damage = active_weapon.prop
            if active_weapon.prop > 5:
                damage = active_weapon.prop + int(np.random.random() * 10)
            encounter.hp -= damage
            print("You dealt " + str(damage) + " damage!")
            if encounter.hp < 1:
                print("\nYou killed " + encounter.name + "!\n")
                print(encounter.kill_message)
                self.addLoot([encounter.loot])
                encounter.alive = False
                return 1
            enemy_choice = np.random.randint(0,1)
            enemy_attack = encounter.attacks[enemy_choice][0]
            enemy_dmg = encounter.attacks[enemy_choice][1]
            self.hp -= enemy_dmg
            print(encounter.name + " chose '" + enemy_attack + "'!\n" + encounter.name + " dealt " + str(enemy_dmg) + " damage!")
            if self.hp < 1:
                print("\n" + encounter.name + " laid waste to you.\n")
                return 2

                
                       
    
    def hazardScene(self, encounter):
        print("Hazard...")
        
    def play(self):
        first_time = True
        while(self.alive):
            if first_time:
                first_time = False
                print("You have washed up on a Deserted Island! You must search the island for Food and Water to survive until rescue.\nMaybe there is something you can build to signal for help...")
            print("\nDays on the deserted island: "+str(self.days))
            print("You have "+str(self.hp)+ "/" + str(self.maxhp)+" HP.")

            #Our code to search the Island goes here
            tile = None
            while True:
                try:
                    tile = input("Where would you like to search today? (temple, spring, beach, ravine, camp, ruins, pit, cave, mountain): ")
                    if tile.upper() == 'Q':
                        break
                    tile = self.island_map[tile]
                except:
                    print("Invalid Input. Try Again")
                else:
                    break
            try:
                if tile.upper() == 'Q':
                    self.alive = False
                    continue
            except:
                print("")
            tile.enterTile()
            loot, encounter = tile.search()
            temp_loot = []

            
            if encounter == None:
                print("You encounter nothing.")
                temp_loot.append(loot)
            elif encounter.alive == False:
                print("You enter the old arena of the " + encounter.name + " that you laid to rest.")
                temp_loot.append(loot)
            elif encounter != None:
                print("You encounter "+str(encounter.name)+"\n" + str(encounter.description)+"!")
                if encounter.quality == 'boss':
                    weapon = False
                    for i in self.inventory:
                        if i['item'] != None and i['item'].quality == 'weapon':
                            weapon = True
                    if weapon: 
                        result = self.fightScene(encounter)
                        if result == 0:
                            print("You run back to camp. Return to " + tile.name + " when you are stronger.")
                            tile.lootedItems = []
                            continue
                        elif result == 2:
                            print("You lose the game!")
                            self.alive = False
                            continue
                        temp_loot.append(loot)
                    else:
                        print("You do not have any weapons! Explore somewhere else to find one and come back.")
                        continue
                elif encounter.quality == 'hazard':
                    self.hazardScene(encounter)
                    temp_loot.append(loot)
                else:
                    temp_loot.append(loot)
            
            
            for i in range(5):
                fw_prop = np.random.random()
                if fw_prop > 0.8:
                    temp_loot.append(Food)
            for i in range(5):
                fw_prop = np.random.random()
                if fw_prop > 0.8:
                    temp_loot.append(Water)
            for i in range(5):
                fw_prop = np.random.random()
                if fw_prop > 0.8:
                    temp_loot.append(Wood)
            
            if loot != None or (loot == None and len(temp_loot) > 1):
                string = ""
                self.addLoot(temp_loot)
                i = 0
                while i < len(temp_loot):
                    if temp_loot[i] == None:
                        i += 1
                        continue
                    elif i == len(temp_loot) - 1:
                        string += " " + temp_loot[i].name + "."
                    else:
                        string += " " + temp_loot[i].name + ","
                    i += 1
                print("You found these items at " + tile.name + ": " + string)
            else:
                print("You found no loot! Better luck next time.")

            tile.leaveTile()
            print("You have " + str(self.hp) + "/" + str(self.maxhp) + " HP.")
            self.showInv()
            # RIGHT HERE DO CAMP STUFF (REGENERATE HEALTH, UPGRADE, CRAFT)
            camp_stuff = input("Would you like to access the camps utilities? (Y/N) ")
            while True:
                if camp_stuff.upper() == 'Y' or camp_stuff.upper() == 'N':
                    break
                else:
                    print("Invalid Input! Try Again")
                camp_stuff = input("Would you like to access the camps utilities? (Y/N) ")
            camp = False
            if camp_stuff.upper() == 'Y': camp = True
            while camp:
                while True:
                    try:
                        user_input = input("\nWhat would you like to do:\n 0. Leave\n 1. Craft Something\n 2. Upgrade Health\n 3. Regenerate Health\n Input: ")
                        user_input = int(user_input)
                    except:
                        print("Invalid Input! Choose a number from 0-3")
                    else:
                        if user_input == 0:
                            # leave camp utilities
                            camp = False
                            break
                        elif user_input == 1:
                            # craft stuff
                            craftables = []
                            for item in self.inventory:
                                if item["item"].quality == 'craft':
                                    craftables.append(item['item'])
                            if len(craftables) == 0:
                                print("You cannot craft anything!")
                                continue
                            craft_string = "What would you like to craft: \n0: Leave\n"
                            i = 1
                            crafting = []
                            if Large_Tooth in craftables and Wood in craftables:
                                craft_string += str(i) + ": Fang Blade\n"
                                i += 1
                                crafting.append(Tooth_Sword)
                            if Blade_Frag in craftables and Wood in craftables:
                                craft_string += str(i) + ": Samurai Sword\n"
                                i += 1
                                crafting.append(Samurai_Sword)
                            if Spider_Eye in craftables and Gladiator_Blood in craftables and Golden_Monkey in craftables and Power_Source in craftables and Emerald in craftables:
                                craft_string += str(i) + ": Beacon\n"
                                i += 1
                                crafting.append(Beacon)
                            while True:
                                craft_input = input(craft_string + " Input: ")
                                try:
                                    craft_input = int(craft_input)
                                except:
                                    print("Invalid Input! Try Again")
                                else:
                                    if craft_input > len(crafting) or craft_input < 0:
                                        print("Invalid Input! Try Again!")
                                        continue
                                    if craft_input == 0:
                                        break
                                    else:
                                        crafted = crafting[craft_input-1]
                                        craftable = True
                                        print("Crafting " + crafted.name + "\n")
                                        time.sleep(1.0)
                                        if crafted.name == "Beacon":
                                            temp = 0
                                            while temp < len(self.inventory): 
                                                for i in range(len(self.inventory)):
                                                    name = self.inventory[i]['item']
                                                    if name == Spider_Eye or name == Gladiator_Blood or name == Golden_Monkey or name == Power_Source or name == Emerald:
                                                        self.inventory.remove(self.inventory[i])
                                                        break
                                                temp += 1
                                            self.inventory.append({'item': Beacon, 'quantity': 1})
                                            print("Crafted Item!")
                                        elif crafted.name == 'Fang Blade':
                                            for i in range(len(self.inventory) - 1):
                                                name = self.inventory[i]['item']
                                                wood_found = False
                                                enough_wood = True
                                                if not wood_found and name == Wood:
                                                    if self.inventory[i]['quantity'] > 5:
                                                        self.inventory[i]['quantity'] -= 5
                                                        wood_found = True
                                                    elif self.inventory[i]['quantity'] < 5:
                                                        print("Not enough Wood! Get some more and try again.")
                                                        craftable = False
                                                        enough_wood = False
                                                        wood_found = True
                                                        break
                                                    else:
                                                        self.inventory.remove(self.inventory[i])
                                                        break
                                            if enough_wood:
                                                for i in range(len(self.inventory)):
                                                    name = self.inventory[i]['item']
                                                    if name == Large_Tooth:
                                                        self.inventory.remove(self.inventory[i])
                                                        break
                                            if craftable: 
                                                self.inventory.append({'item': Tooth_Sword, 'quantity': 1})
                                                print("Crafted Item!")
                                        elif crafted.name == 'Samurai Sword':
                                            for i in range(len(self.inventory)):
                                                name = self.inventory[i]['item']
                                                wood_found = False
                                                enough_wood = True
                                                if not wood_found and name == Wood:
                                                    if self.inventory[i]['quantity'] > 10:
                                                        self.inventory[i]['quantity'] -= 10
                                                        wood_found = True
                                                    elif self.inventory[i]['quantity'] < 10:
                                                        print("Not enough Wood! Get some more and try again.")
                                                        craftable = False
                                                        enough_wood = False
                                                        wood_found = True
                                                        break
                                                    else:
                                                        self.inventory.remove(self.inventory[i])
                                                        break
                                            if enough_wood:
                                                for i in range(len(self.inventory)):
                                                    name = self.inventory[i]['item']
                                                    if name == Blade_Frag:
                                                        self.inventory.remove(self.inventory[i])
                                                        break
                                            if craftable: 
                                                self.inventory.append({'item': Samurai_Sword, 'quantity': 1})
                                                print("Crafted Item!")
                                        break    
                            continue
                        elif user_input == 2:
                            # Upgrade Health
                            upgrade_check = False
                            upgrade_list = []
                            for thing in self.inventory:
                                if thing['item'].quality == 'upgrade':
                                    upgrade_check = True
                                    upgrade_list.append(thing['item'])
                            if not upgrade_check:
                                print("\nYou have no items to upgrade with!")
                                continue
                            upgrade_string = "Upgrade Items: \n0: Leave\n"
                            i = 1
                            while i <= len(upgrade_list):
                                upgrade_string += str(i) + ": " + upgrade_list[i-1].name + " // Upgrades Health by " + str(upgrade_list[i-1].prop)+"\n"
                                i += 1
                            while True:
                                upgrade_input = input(upgrade_string + "Index: ")
                                try:
                                    upgrade_input = int(upgrade_input)
                                except:
                                    print("Invalid Input! Try Again")
                                    continue
                                else:
                                    if upgrade_input > len(upgrade_list) or upgrade_input < 0:
                                        print("Invalid Input! Try Again")
                                        continue
                                    if upgrade_input == 0:
                                        break
                                    upgrading = upgrade_list[upgrade_input - 1]
                                    print("\nYou eat the " + upgrading.name + " and your stomach feels a little sick.")
                                    self.maxhp += upgrading.prop
                                    self.hp = self.maxhp
                                    upgrade_index = 0
                                    for item in self.inventory:
                                        if item['item'].name == upgrading.name:
                                            break
                                        upgrade_index += 1
                                    self.inventory.remove(self.inventory[upgrade_index])
                                    break
                            continue
                        elif user_input == 3:
                            # Regen Health
                            if self.hp == self.maxhp:
                                print("Your health is already at the maximum level!")
                                continue
                            print("\n ***You need 5 food and 5 water to regenerate your health to max***\n***HP: "+str(self.hp) + "/" + str(self.maxhp)+"***")
                            self.showInv()
                            regen_answer = ""
                            while True:
                                regen_answer = input("Attempt to heal? (Y/N): ")
                                if regen_answer.upper() == "Y" or regen_answer.upper() == 'N':
                                    break
                                print("Invalid Input! Try Again")
                            if regen_answer.upper() == 'Y':
                                print("Healing...")
                                time.sleep(1)
                                f_index = 0
                                w_index = 0
                                for i in range(len(self.inventory) - 1):
                                    if self.inventory[i]['item'] == Food:
                                        f_index = i
                                    if self.inventory[i]['item'] == Water:
                                        w_index = i
                                if self.inventory[f_index]['quantity'] < 5 and self.inventory[w_index]['quantity'] < 5:
                                    print("Not enough Food or Water!")
                                    continue
                                elif self.inventory[f_index]['quantity'] < 5:
                                    print("Not enough Food!")
                                    continue
                                elif self.inventory[w_index]['quantity'] < 5:
                                    print("Not enough Water!")
                                    continue
                                if self.inventory[f_index]['quantity'] == 5:
                                    self.inventory.remove(self.inventory[f_index])
                                    w_index -= 1
                                else:
                                    self.inventory[f_index]['quantity'] -= 5
                                if self.inventory[w_index]['quantity'] == 5:
                                    self.inventory.remove(self.inventory[w_index])
                                else:
                                    self.inventory[w_index]['quantity'] -= 5
                                self.hp = self.maxhp
                                print("Regenerated Health to Max!")

                            continue
                        else:
                            print("Invalid Input! Try Again")
                            continue

            if {'item': Beacon, 'quantity': 1} in self.inventory:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    time.sleep(0.1)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    time.sleep(0.1)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    time.sleep(2)
                    print("You crafted the beacon!")
                    time.sleep(2)
                    print("You place your beacon at the top of mountain where the Old Dragon used to rest, and it shines like a second sun over the vast ocean.")
                    time.sleep(3)
                    print("Your bright beacon is noticed from hundreds of miles away and help is sent to rescue you.")
                    time.sleep(3)
                    print("You win!")
                    break
            print("Time to rest and go to sleep. The Day has ended.")
            self.days += 1
        else:
            print("Game over. You survived for "+str(self.days)+" days on the island.")