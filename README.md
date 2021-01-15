# FGO-MixedNodes
Finds the best mixed drop nodes for Fate Grand Order.

Uses a weighted average AP per Drop based on the lowest APD for each material to select the best combination of nodes for 

For example, if you need Mystic Spinal Fluid (32 APD at Concrete Dungeon) and Heart of the Foreign God (163 at Crow's Nest)
But the node Demon's Garden drops both at 69 APD and 172 APD respectively.

The average AP for one of each, running seperately, is 195. 
Running the combined is less obvious though: The average is 120.5, but that values low rarities over high-rarities, even though hearts are rarer and probably more in demand. 
The max gives 172, since the hearts are higher than the fluid. However, multiple fluids can be expected to drop in that time (~2.5).

The weighted average gives a slightly more representative number where low-rarities are worth less but are still counted.
The weighted APD is (69*32 + 172*163)/(32+163) = 155



Data is imported from a csv. The csv should be preprocessed to save time and complexity in the programs running. Delete any rows that don't have data (closed) and the header rows. Delete the columns for monuments xp, etc (Letters in the header are A___ for mats and B___etc for the others. Also delete the info rows at the start except for the ids and the names (eg. LDN5, Westminster).



Drop data from [r/grandorder](https://www.reddit.com/r/grandorder/), specifically the [advanced drop tables](https://docs.google.com/spreadsheets/d/1NY7nOVQkDyWTXhnK1KP1oPUXoN1C0SY6pMEXPcFuKyI/edit?usp=sharing).