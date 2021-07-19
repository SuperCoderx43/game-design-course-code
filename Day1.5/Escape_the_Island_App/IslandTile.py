import numpy as np

class IslandTile:

    
    
    def __init__(self, name, items, encounters, description):
        self.name = name
        self.items = items
        self.encounters = encounters
        self.description = description
        #Now variables that have default values
        self.discovered = False
        self.lootedItems = []     #By keeping track of these, we make
        self.pastEncounters = []  #sure we don't find the same thing twice
        
    def enterTile(self):
        #Your code here
        if self.discovered:
            print("\nYou enter the "+self.name)
        else:
            print("\n" + self.description)
            self.discovered = True
            
    def leaveTile(self):
        #Your code here
        print("After a long day of searching, you leave "+self.name+" and head back to camp")
    
    def search(self):
        #your code here
        loot = self.items
        try:
            encounter = self.encounters[np.random.randint(len(self.encounters))]
        except:
            encounter = None
        finally:
            if loot in self.lootedItems:
                loot = None
            else:
                self.lootedItems.append(loot)
            """
            try:
                encounter = self.encounters[np.random.randint(len(self.encounters))]
                loot = self.items[np.random.randint(len(self.items))]
            except:
                print("The items you've collected on the island are strewn about your camp")
            else:
                if encounter in self.pastEncounters:
                    encounter = None
                    loot = None
                else:
                    self.pastEncounters.append(encounter)
                    if loot in self.lootedItems:
                        loot = None
                    else:
                        self.lootedItems.append(loot)
            """
            return loot, encounter