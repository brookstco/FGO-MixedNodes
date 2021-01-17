# CBrooks 2021

#import numpy as np
import pandas as pd
import itertools
from itertools import chain, combinations
import math
from enum import IntEnum
#from collections import defaultdict

#Mats in the order of the csv. Value can be used as index for matweights, and .name can be used as the column names in the pd.df
class Mat(IntEnum):
    # GOLD
    # Claw of Chaos
    CLAW = 0
    # Heart of the Foreign God
    HEART = 1
    # Dragon's Reverse Scale
    SCALE = 2
    # Spirit Root
    ROOT = 3
    # Warhorse's Young Horn
    HORN = 4
    # Tearstone of Blood
    TEARSTONE = 5
    # Black Beast Grease
    GREASE = 6
    # Lamp of Evil-Sealing
    LAMP = 7
    # Scarab of Wisdom
    SCARAB = 8
    # Primordial Lanugo
    LANUGO = 9
    # Cursed Beast Gallstone
    GALLSTONE = 10
    # Mysterious Divine Wine
    WINE = 11
    # Reactor Core of Dawn
    CORE = 12
    # JP ONLY
    # Tsukumo Mirror
    MIRROR = 13
    # Egg of Truth
    EGG = 14
    # Glittering Star Shard
    STAR = 15
    # Fruit of Eternity
    FRUIT = 16
    # Demon Flame Lantern
    DEMONFLAME = 17

    # SILVER
    # Seed of Yggdrasil
    SEED = 18
    # Ghost Lantern
    LANTERN = 19
    # Octuplet Crystal
    OCTUPLET = 20
    # Serpent Jewel
    SERPENT = 21
    # Phoenix Feather
    FEATHER = 22
    # Eternal Gear
    GEAR = 23
    # Forbidden Page
    PAGE = 24
    # Homunculus Baby
    BABY = 25
    # Meteor Horseshoe
    HORSESHOE = 26
    # Great Knight Medal
    KNIGHT = 27
    # Shell of Reminiscense
    SHELL = 28
    # Refined Magatama
    MAGATAMA = 29
    # Eternal Ice
    ICE = 30
    # Giant's Ring
    RING = 31
    # Aurora Steel
    STEEL = 32
    # Soundless Bell
    BELL = 33
    # JP ONLY
    # Arrowhead of Disastrous Sin
    ARROW = 34
    # Moonlit Tiara
    TIARA = 35
    # Divine Spirit Particle
    PARTICLE = 36
    # Rainbow Thread Ball
    THREAD = 37

    # BRONZE
    # Proof of Hero
    PROOF = 38
    # Evil Bone
    BONE = 39
    # Dragon Fang
    FANG = 40
    # Void's Dust
    DUST = 41
    # Fool's Chain
    CHAIN = 42
    # Deadly Poisonous Needle
    NEEDLE = 43
    # Mystic Spinal Fluid
    FLUID = 44
    # Stake of Wailing Night
    STAKE = 45
    # Mystic Gunpowder
    GUNPOWDER = 46

def matNamesList(mats:[Mat]) -> [str]:
    return [i.name for i in mats]

class Op(IntEnum):
    AVERAGE = 0
    MAX = 1
    WEIGHTEDAVG = 2 #This is optimal I think

class SimpleNode:
    #List of row ids from the df.
    nodeId:int
    #The value of the NodeSet. Lower is better. 0 or less is invalid
    value:float = 0
    def __init__(self, nodeId, value):
        self.nodeId = nodeId
        self.value = value

class NodeSet:
    #List of row ids from the df.
    nodeIds:[int] = []
    #The value of the NodeSet. Lower is better. 0 or less is invalid
    value:float = 0


# # Returns the average APD for a list of materials or None if none of those mats drop
# def avgAPD(mats: [int]):
    #TAke in pd.df, filter by mats, use pd.sum, divide by len of mats list
#     apd = sublist(mats)
#     if not apd:
#         return None
#     return math.fsum(apd) / len(mats)

# # Returns the highest APD for a list of materials or None if none of those mats drop
# def maxAPD(mats: [int]):
    #TAke in pd.df, filter by mats, get max
#     apd = sublist(mats)
#     if not apd:
#         return None
#     return max(apd)

# Returns weighted APD for a node (in list form)
def weightedAvgAPDList(nodeAPD:[float], mats: [int], matWeights: [float]) -> float:
    weighted: float = 0
    weight: float = 0
    for i in mats:
        weighted += (nodeAPD[i] * matWeights[i])
        weight += matWeights[i]
    return weighted / weight

# Returns weighted APD for a node. The node should be passed in as a single row dataframe.
def weightedAvgAPD(nodeAPD:pd.DataFrame, mats: [Mat], matWeights: [float]) -> float:
    weighted: float = 0
    weight: float = 0
    for i in mats:
        weighted += (nodeAPD[i.name].value[0] * matWeights[i])
        weight += matWeights[i]
    return weighted / weight


#Loads the drop data for the nodes into a pd.dataframe 
def loadData(filename:str, jp = False) -> pd.DataFrame:
    #Could use the atlas academy db for more up to date data. Could be good if this becomes a web app.
    #column indices that are actually used - remember this is 0 indexed
    #Note that the column numbers are different on jp and NA pages - this is NA - this can be used instead of manually deleteing columns in the csv, but the rows do need to be manually filtered to allow correct typing.
    #csv needs all closed nodes, the extra headers removed. The extra cols can probably be filtered, but its easier to remove in csv, since widths may be different
    #cols = [1,2] + list(range((9-1),55)) #recheck thise before using
    matNames = ["CLAW", "HEART", "SCALE", "ROOT", "HORN", "TEARSTONE", "GREASE", "LAMP", "SCARAB", "LANUGO", "GALLSTONE", "WINE", "CORE", "MIRROR", "EGG", "STAR", "FRUIT", "DEMONFLAME", "SEED", "LANTERN", "OCTUPLET", "SERPENT", "FEATHER", "GEAR", "PAGE", "BABY", "HORSESHOE", "KNIGHT", "SHELL", "MAGATAMA", "ICE", "RING", "STEEL", "BELL", "ARROW", "TIARA", "PARTICLE", "THREAD", "PROOF", "BONE", "FANG", "DUST", "CHAIN", "NEEDLE", "FLUID", "STAKE", "GUNPOWDER"]
    #index doesn't get a name
    colNames = ["id", "name"] + matNames

    with open(filename, "r") as file:
        #df = pd.read_csv(file, skiprows=skiprows, usecols=cols, header=None, names=colNames)
        df = pd.read_csv(file, header=None, names=colNames)
        return df


#Sets Matweights above to a list of the lowest apd for each mat
def getWeights(nodes: pd.DataFrame) -> [float]:
    mats = nodes.drop(["id", "name"], axis=1)
    matWeights = mats.min().tolist()
    return matWeights



#Gotten from http://wordaligned.org/articles/partitioning-with-python
def sliceable(xs):
    '''Return a sliceable version of the iterable xs.'''
    try:
        xs[:0]
        return xs
    except TypeError:
        return tuple(xs)
def partition(iterable):
    s = sliceable(iterable)
    n = len(s)
    b, mid, e = [0], list(range(1, n)), [n]
    #getslice = s.__getitem__
    splits = (d for i in range(n) for d in combinations(mid, i))
    return [[s[sl] for sl in map(slice, chain(b, d), chain(d, e))]
            for d in splits]


#Returns a pd.df with all the ineligible nodes removed.
def filterNodes(nodes: pd.DataFrame, mats:[Mat]) -> pd.DataFrame:
    return nodes.dropna(subset = matNamesList(mats))

def getFilteredSlices(nodes: pd.DataFrame, slicedMats:[[Mat]]) -> [pd.DataFrame]:
        #Goes through each set of mats in the combo
        filteredNodes = []
        for i in slicedMats:
            filtered = filterNodes(nodes, i)
            if filtered.empty:
                return []
            else:
                filteredNodes.append(filtered)


#https://stackoverflow.com/questions/58567199/memory-efficient-way-for-list-comprehension-of-pandas-dataframe-using-multiple-c
def getFilteredSimpleNodes(nodes: pd.DataFrame, slicedMats:[[Mat]], op:Op)->[SimpleNode]:
    filteredNodes = getFilteredSlices(nodes, slicedMats)
    print ([row for row in zip([filteredNodes[i].values for i in nodes.columns])])


#maxNodeCombinations is the limit of how many combinations from one node set can be generated. Value <= 0 mean all are generated.
def getNodeSets(nodes: pd.DataFrame, mats:[Mat], op:Op, maxNodeCombinations:int = 0):
    #Preemptively rows that don't contain any mats?  - dropna frops everything in the list, not just some.
    allSets = []
    #figures out every combination of mats
    for combo in partition(mats):
        filtered = getFilteredSimpleNodes(nodes, combo, op)
        if not filtered:
            #goes back to top of loop on next set, since this one was impossible
            continue
        else:
            print("here")

                


# combo1 = list(itertools.combinations(range(0,31), 1))
# combo2 = list(itertools.combinations(range(0,31), 2))

if __name__ == "__main__":

    #################################################
    # Only edit variables below
    # 
    
    # Set currentMats to a specific set of mats. Larger sets will take longer to run.
    mats:[Mat] = [Mat.NEEDLE, Mat.HEART, Mat.BONE]

    # JP or NA server
    jp:bool = False

    # Operation to judge which mixed modes are better. Weighted average is recommended
    op:Op = Op.WEIGHTEDAVG

    #Should the results be saved to a file or just printed in the terminal?
    saveToFile:bool = False
    #Should the result have extra text to make it easily human readable? - may also change filetype
    readableOutput:bool = True
    #The filename Excluding the ending.
    outFilename:str = "mats"

    ##################################################
    # Advanced Settings 

    # When multiple mats are selected, it check each grouping of mats.
    # This controls how many results can come from a single combination. 0 will allow the maximum amount.
    maxNodeCombinations:int = 0

    # Total results in the output file. 0 will allow the maximum amount.
    maxOutputNodes:int = 0

    # Don't edit below this line (unless you want to)
    ##################################################

    filename = ""
    if jp:
        filename = "apd_jp2.csv"
    else:
        filename = "apd_na2.csv"

    nodes = loadData(filename, jp)
    #print(nodes)
    matWeights = getWeights(nodes)


    filteredTest = filterNodes(nodes, mats)
    if not filteredTest.empty:
        print(filteredTest)
    else:
        print("No possible nodes")


    outputNodes:[NodeSet] = []

    n = getNodeSets(nodes, mats, op)


    if saveToFile:
        if readableOutput:
            outFilename = outFilename + ".txt"
        else:
            outFilename = outFilename + ".csv"