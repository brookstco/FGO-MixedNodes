# CBrooks 2021

import numpy as np
import pandas as pd
import itertools
import math
from enum import IntEnum
from collections import defaultdict

#These were used in an older test version. Still here since they do make customizing selections easier. We'll see.
class Mat(IntEnum):
    # BRONZE
    # Proof of Hero
    PROOF = 0
    # Evil Bone
    BONE = 1
    # Dragon Fang
    FANG = 2
    # Void's Dust
    DUST = 3
    # Fool's Chain
    CHAIN = 4
    # Deadly Poisonous Needle
    NEEDLE = 5
    # Mystic Spinal Fluid
    FLUID = 6
    # Stake of Wailing Night
    STAKE = 7
    # Mystic Gunpowder
    GUNPOWDER = 8

    # SILVER
    # Seed of Yggdrasil
    SEED = 9
    # Ghost Lantern
    LANTERN = 10
    # Octuplet Crystal
    OCTUPLET = 11
    # Serpent Jewel
    SERPENT = 12
    # Phoenix Feather
    FEATHER = 13
    # Eternal Gear
    GEAR = 14
    # Forbidden Page
    PAGE = 15
    # Homunculus Baby
    BABY = 16
    # Meteor Horseshoe
    HORSESHOE = 17
    # Great Knight Medal
    KNIGHT = 18
    # Shell of Reminiscense
    SHELL = 19
    # Refined Magatama
    MAGATAMA = 20
    # Eternal Ice
    ICE = 21
    # Giant's Ring
    RING = 22
    # Aurora Steel
    STEEL = 23
    # Soundless Bell
    BELL = 24
    # JP ONLY
    # Arrowhead of Disastrous Sin
    ARROW = 25
    # Moonlit Tiara
    TIARA = 26
    # Divine Spirit Particle
    PARTICLE = 27
    # Rainbow Thread Ball
    THREAD = 28

    # GOLD
    # Claw of Chaos
    CLAW = 29
    # Heart of the Foreign God
    HEART = 30
    # Dragon's Reverse Scale
    SCALE = 31
    # Spirit Root
    ROOT = 32
    # Warhorse's Young Horn
    HORN = 33
    # Tearstone of Blood
    TEARSTONE = 34
    # Black Beast Grease
    GREASE = 35
    # Lamp of Evil-Sealing
    LAMP = 36
    # Scarab of Wisdom
    SCARAB = 37
    # Primordial Lanugo
    LANUGO = 38
    # Cursed Beast Gallstone
    GALLSTONE = 39
    # Mysterious Divine Wine
    WINE = 40
    # Reactor Core of Dawn
    CORE = 41
    # JP ONLY
    # Tsukumo Mirror
    MIRROR = 42
    # Egg of Truth
    EGG = 43
    # Glittering Star Shard
    STAR = 44
    # Fruit of Eternity
    FRUIT = 45
    # Demon Flame Lantern
    DEMONFLAME = 46

class Criteria(IntEnum):
    AVERAGE = 0
    MAX = 1
    WEIGHTEDAVG = 2 #This is optimal I think


class Node:
    # returns True if this node drops all of the materials
    def hasMats(self, mats: [int]):
        for i in mats:
            if self.matAPD[i] is None:
                return False
        return True

    # Gets a filtered sublist
    def sublist(self, mats: [int]):
        # return [matAPD[i] for i in ids if matAPD[i] != None] #Should have already been checked.
        return [self.matAPD[i] for i in mats]

    def sublistWeighted(self, mats: [int]):
        sublist = []
        weight = 0
        for i in mats:
            # if matAPD[i] != None: #Should have already been checked.
            sublist.append(self.matAPD[i] * matWeights[i])
            weight += matWeights[i]
        return sublist, weight

    # Returns the average APD for a list of materials or None if none of those mats drop
    def avgAPD(self, mats: [int]):
        apd = self.sublist(mats)
        if not apd:
            return None
        return math.fsum(apd) / len(mats)

    # Returns the highest APD for a list of materials or None if none of those mats drop
    def maxAPD(self, mats: [int]):
        apd = self.sublist(mats)
        if not apd:
            return None
        return max(apd)

    # def DropsPerAP(mats):
    #    apd = sublist(mats)

    def weightedAvgAPD(self, mats: [int]):
        apd, weight = self.sublistWeighted(mats)
        if not apd:
            return None
        return math.fsum(apd) / weight


#Loads the drop data for the nodes into a pd.dataframe 
def loadData(filename:str, jp = False) -> pd.DataFrame:
    #Could use the atlas academy db for more  up to date data. Could be good if this becomes a web app.
    #column indices that are actually used - remember this is 0 indexed
    #Note that the column numbers are different on jp and NA pages - this is NA
    cols = [1,2] + list(range((9-1),55))
    skiprows = [0,1,2]
    matNames = ["CLAW", "HEART", "SCALE", "ROOT", "HORN", "TEARSTONE", "GREASE", "LAMP", "SCARAB", "LANUGO", "GALLSTONE", "WINE", "CORE", "MIRROR", "EGG", "STAR", "FRUIT", "DEMONFLAME", "SEED", "LANTERN", "OCTUPLET", "SERPENT", "FEATHER", "GEAR", "PAGE", "BABY", "HORSESHOE", "KNIGHT", "SHELL", "MAGATAMA", "ICE", "RING", "STEEL", "BELL", "ARROW", "TIARA", "PARTICLE", "THREAD", "PROOF", "BONE", "FANG", "DUST", "CHAIN", "NEEDLE", "FLUID", "STAKE", "GUNPOWDER"]
    #index doesn't get names
    colNames = ["id", "name"] + matNames

    #csv needs all closed nodes, the extra headers removed. The extra cols can probably be filtered, but its easier to remove in csv, since widths may be different
    filename="apd_na2.csv"


    with open(filename, "r") as file:
        #df = pd.read_csv(file, skiprows=skiprows, usecols=cols, header=None, names=colNames)
        df = pd.read_csv(file, header=None, names=colNames)
        #remove jp only rows
        #jponlyrows = [170-1-3] + list(range(218-1-3, 260-3))
        #df.drop(jponlyrows, inplace=True)
        #df = df.astype(np.float64, errors='ignore')
        return df

#Returns a pd.df with all the ineligible nodes removed.
def filterNodes(mats:[int]) -> pd.DataFrame:
    return nodes.dropna(subset=mats)

#Sets Matweights above to a list of the lowest apd for each mat
def getWeights(nodes: pd.DataFrame) -> [float]:
    mats = nodes.drop(["id", "name"], axis=1)
    minCols = mats.min()
    matWeights = mats.min().tolist()

if __name__ == "__main__":

    # combo1 = list(itertools.combinations(range(0,31), 1))
    # combo2 = list(itertools.combinations(range(0,31), 2))

    #################################################
    # ONLY EDIT IN THIS BOX
    # 
    
    # Set currentMats to a specific set of mats. Larger sets will take longer to run.
    mats = [Mat.NEEDLE, Mat.HEART, Mat.BONE]

    # JP or NA server
    jp = False

    # Don't edit below this line (unless you want to)
    ##################################################

    filename = ""
    if jp:
        filename = "apd_jp2.csv"
    else:
        filename = "apd_na2.csv"

    nodes = loadData(filename, jp)
    print(nodes)
    matWeights = getWeights(nodes)
    print(matWeights)