# CBrooks 2021

import os
import numpy as np
import pandas as pd
import itertools
from itertools import chain, combinations
import math
from enum import IntEnum
from collections import namedtuple #I'm not positive this needs to be imported, but it help the tool hints at least

#Mats in the order of the csv. Value can be used as index for matweights, and .name can be used as the column names in the pd.df
class Mat(IntEnum):
    """Enum of materials. Includes both column header and index to make accessing the pd dataframe easy while making it clear what materials one is choosing."""
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
    WARHORSE = 4
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
    """Returns the names of a list of mats as strings for use as column headers"""
    return [i.name for i in mats]

class Op(IntEnum):
    """Enum for the operation used to calculate the best node"""
    AVERAGE = 0
    MAX = 1
    WEIGHTEDAVG = 2 #This is optimal I think


class SimpleNode:
    """Simplified node information. Contains a pd.df index and its value"""
    #List of row ids from the df.
    nodeId:int
    #The value of the NodeSet.
    value:float = np.nan
    def __init__(self, nodeId: int, value:float = np.nan):
        self.nodeId = int(nodeId)
        self.value = value

class NodeSet:
    """Simplified node information. Contains a list of pd.df indices and the combined value"""
    #List of row ids from the df.
    nodeIds:[int] = []
    #The value of the NodeSet.
    value:float = np.nan
    # def __init__(self, nodeIds: [int], value:float = np.nan):
    #     self.nodeIds = nodeIds
    #     self.value = value
    def __init__(self, nodes:[SimpleNode]):
        self.nodeIds = []
        self.value = 0
        self.addSimpleNodes(nodes)

    def addSimpleNodes(self, nodes:[SimpleNode]):
        """Add all nodes in a list to the set."""
        for node in nodes:
            self.nodeIds.append(int(node.nodeId))
            self.value += node.value



def weightedAvgAPDList(nodeAPD:[float], mats: [int], matWeights: [float]) -> float:
    """ Returns weighted APD for a node (in list form)"""
    weighted: float = 0
    weight: float = 0
    for i in mats:
        weighted += (nodeAPD[i] * matWeights[i])
        weight += matWeights[i]
    return weighted / weight

def weightedAvgAPD(nodeAPD:pd.DataFrame, mats: [Mat], matWeights: [float]) -> float:
    """Returns weighted APD for a node. The node should be passed in as a single row dataframe."""
    weighted: float = 0
    weight: float = 0
    for i in mats:
        weighted += (nodeAPD[i.name].value[0] * matWeights[i])
        weight += matWeights[i]
    return weighted / weight

def weightedAvgAPDTuple(nodeAPD:namedtuple, mats: [Mat], matWeights: [float]) -> float:
    """Returns weighted APD for a node. The node should be passed in as a namedTuple."""
    weighted: float = 0
    weight: float = 0
    for i in mats:
        #Access a named tuple by the enum name value, then multiply by the weight
        weighted += (getattr(nodeAPD, i.name) * matWeights[i])
        weight += matWeights[i]
    return weighted / weight


def loadData(filename:str, jp = False) -> pd.DataFrame:
    """Loads and returns the drop data for the nodes into a pd.dataframe from a csv file"""
    #Could use the atlas academy db for more up to date data. Could be good if this becomes a web app.
    #column indices that are actually used - remember this is 0 indexed
    #Note that the column numbers are different on jp and NA pages - this is NA - this can be used instead of manually deleteing columns in the csv, but the rows do need to be manually filtered to allow correct typing.
    #csv needs all closed nodes, the extra headers removed. The extra cols can probably be filtered, but its easier to remove in csv, since widths may be different
    #cols = [1,2] + list(range((9-1),55)) #recheck thise before using
    matNames = ["CLAW", "HEART", "SCALE", "ROOT", "WARHORSE", "TEARSTONE", "GREASE", "LAMP", "SCARAB", "LANUGO", "GALLSTONE", "WINE", "CORE", "MIRROR", "EGG", "STAR", "FRUIT", "DEMONFLAME", "SEED", "LANTERN", "OCTUPLET", "SERPENT", "FEATHER", "GEAR", "PAGE", "BABY", "HORSESHOE", "KNIGHT", "SHELL", "MAGATAMA", "ICE", "RING", "STEEL", "BELL", "ARROW", "TIARA", "PARTICLE", "THREAD", "PROOF", "BONE", "FANG", "DUST", "CHAIN", "NEEDLE", "FLUID", "STAKE", "GUNPOWDER"]
    #index doesn't get a name
    colNames = ["id", "name"] + matNames

    with open(filename, "r") as file:
        #df = pd.read_csv(file, skiprows=skiprows, usecols=cols, header=None, names=colNames)
        df = pd.read_csv(file, header=None, names=colNames)
        return df


def getWeights(nodes: pd.DataFrame) -> [float]:
    """Returns a list of the minimum value from each material column"""
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
    '''Return all partitions of an iterable.'''
    s = sliceable(iterable)
    n = len(s)
    b, mid, e = [0], list(range(1, n)), [n]
    #getslice = s.__getitem__
    splits = (d for i in range(n) for d in combinations(mid, i))
    return [[s[sl] for sl in map(slice, chain(b, d), chain(d, e))]
            for d in splits]


def filterNodes(nodes: pd.DataFrame, mats:[Mat]) -> pd.DataFrame:
    """Returns a pd.df with all the ineligible nodes (rows) removed."""
    return nodes.dropna(subset = matNamesList(mats))

def filterSlicedNodes(nodes: pd.DataFrame, slicedMats:[[Mat]]) -> [pd.DataFrame]:
    """Returns a list of pd.df that are filtered to sets of mats from a given list of lists"""
    #Goes through each set of mats in the combo
    filteredNodes = []
    for i in slicedMats:
        #Get a filtered dataframe for each mat. This might be really inefficient, but since the data set is pretty small, we'll survive for now.
        filtered = filterNodes(nodes, i)
        if filtered.empty:
            #If any are empty, it means the whole thing is impossible, so return an empty list
            return []
        else:
            filteredNodes.append(filtered)
    return filteredNodes


def getFilteredSlicedSimpleNodes(nodes: pd.DataFrame, slicedMats:[[Mat]], op:Op, matWeights: [float])->[[SimpleNode]]:
    """Return a list of SimpleNodes for a list of mats"""
    output = []
    slicedNodes = filterSlicedNodes(nodes, slicedMats)
    if not slicedNodes:
        return []
    else:
        #Also gets the index, so it can access the correct set of mats
        for matindex, df in enumerate(slicedNodes):
            #yeah, yeah, this isn't the most efficient. It is the easiest here though.
            #https://stackoverflow.com/questions/58567199/memory-efficient-way-for-list-comprehension-of-pandas-dataframe-using-multiple-c
            rows = []
            for rowtuple in df.itertuples():
                if op == Op.WEIGHTEDAVG:
                    n = SimpleNode(rowtuple[0], weightedAvgAPDTuple(rowtuple, slicedMats[matindex], matWeights))
                #implement the other types here
                #elif op == Op
                else:
                    return []
                rows.append(n)
            output.append(rows)
    return output


#maxNodeCombinations is the limit of how many combinations from one node set can be generated. Value <= 0 mean all are generated.
def getNodeSets(nodes: pd.DataFrame, mats:[Mat], op:Op, matWeights: [float], maxNodeCombinations:int = 0) -> [NodeSet]:
    #Preemptively rows that don't contain any mats?  - dropna frops everything in the list, not just some.
    allSets = []
    #figures out every combination of mats
    for combo in partition(mats):
        #get list of df that each are filtered to the mat combinations. If its empty, skip.
        filtered = getFilteredSlicedSimpleNodes(nodes, combo, op, matWeights)
        if not filtered:
            #goes back to top of loop on next set, since this one was impossible
            continue
        else:
            #go through the combination of nodes and build up a list of possible sets
            #This is the main area to increase efficiency. Reduce copying the df, and get only the top combinations, not all of them.
            permutations = list(itertools.product(*filtered))
            for s in permutations:
                ns = NodeSet(s)
                allSets.append(ns)
    #Reverse mean descending. Need bool flag for this based on levels or sets? Different func?            
    allSets.sort(key=lambda x: x.value, reverse=False)
    return allSets

def convertNodeSet(nodes: pd.DataFrame, nodeSet: NodeSet, readableOutput:bool = True):
    """Converts a nodeset into a string. readableOutput does not currently have any affect"""
    #Round value to 2 place, and start the output string
    output = [str(round(nodeSet.value, 2))]
    for i in nodeSet.nodeIds:
        output.append(", (")
        output.append(nodes.at[i, "id"])
        output.append(", ")
        output.append(nodes.at[i, "name"])
        output.append(")")
    output.append("\n")
    #Joining a list is faster than repeatedly adding to a string
    return "".join(output)

def outputNodeSets(outFilename:str, nodeSets: [NodeSet], nodes: pd.DataFrame, useSubdirectory:bool = True, subdirectory:str = "", readableOutput:bool = True):
    """Saves the nodeSets to a file"""
    if useSubdirectory:
        try:
            os.mkdir(subdirectory)
        except Exception:
            pass
        f = open(os.path.join(subdirectory,outFilename), "w")

    else:
        f = open(outFilename, "w")

    for ns in nodeSets:
        f.write(convertNodeSet(nodes, ns, readableOutput))

    f.close()
              


# combo1 = list(itertools.combinations(range(0,31), 1))
# combo2 = list(itertools.combinations(range(0,31), 2))

if __name__ == "__main__":

    #################################################
    # Only edit variables below

    
    # Set currentMats to a specific set of mats. Larger sets will take longer to run.
    mats:[Mat] = [Mat.CLAW, Mat.SERPENT]

    # JP or NA server
    jp:bool = False

    # Operation to judge which mixed modes are better. Weighted average is recommended
    op:Op = Op.WEIGHTEDAVG

    #Should the results be saved to a file or just printed in the terminal? - Doesn't display in terminal yet
    saveToFile:bool = True #Not implemented
    #Should the result have extra text to make it easily human readable? -  Currently only changes filetype
    readableOutput:bool = True 

    #Use an auto output filename with region and materials, and optionally the op
    autoname:bool = True
    includeOp:bool = False
    #The filename Excluding the ending. Ignored if autoname is True
    outFilename:str = "matsResult"

    #Save output into a subfolder
    useSubdirectory = True
    subdirectoryName = "Output"

    # Total results in the output file. 0 will allow the maximum amount.
    maxOutputNodes:int = 10



    ##################################################
    # Advanced Settings 

    # When multiple mats are selected, it check each grouping of mats.
    # This controls how many results can come from a single combination. 0 will allow the maximum amount.
    maxNodeCombinations:int = 0 #Not implemented yet

    # Don't edit below this line (unless you want to)
    ##################################################



    filename = ""
    if jp:
        filename = "apd_jp2.csv"
    else:
        filename = "apd_na2.csv"



    nodes = loadData(filename, jp)

    matWeights = getWeights(nodes)
    #If adding custom weights, deal with them here.

    outputNodes:[NodeSet] = []

    nodeSet = getNodeSets(nodes, mats, op, matWeights, maxNodeCombinations)
    if maxOutputNodes > 0:
        nodeSet = nodeSet[:maxOutputNodes]


    if saveToFile:
        if autoname:
            if jp:
                outFilename = "jp_"
            else:
                outFilename = "na_"

            if includeOp:
                outFilename += (str(op.name) + "_")

            for mat in mats:
                outFilename += (str(mat.name) + "_")

        if readableOutput:
            outFilename += ".txt"
        else:
            outFilename += ".csv"
        outputNodeSets(outFilename, nodeSet, nodes, useSubdirectory, subdirectoryName, readableOutput)
    

    print("Complete.")
        