# FGO-MixedNodes
Finds the best mixed drop nodes in the game Fate Grand Order.


#### How to use

Download fgo-MixedNodes.py and either apd_jp.csv or apd_na.csv based on your server.
You will need to have python 3 installed, and some packages may need to be installed (pandas may need to be installed seperately, but the rest should be default, I think). See online tutorials for help - there are plenty.

Open fgo in an editor, do not just run it. Near the bottom, there is a section surrounded by lines of `#`. Edit the vars in this section to have the server and materials that you want the output for. Then run the program. A file will be created, or overwritten if it already exists, with the list of nodes.
Materials are in an Enum format - Mat.MATERIAL (These are listed at the top of the file or in the mats txt files for reference). You add materials into the list seperate by commas. For example [Mat.BONE, Mat.HEART]. 
Note: Larger numbers of materials can take longer to process. "Complete" will always be printed in the terminal when the program finishes.

The output shows a list from best to worst of the combination of nodes that is best for getting all of the materials that you listed. The number is the value of the operation that was done.


#### How it works

This uses a weighted average AP per Drop based on the lowest APD for each material to select the best combination of nodes.

For example, if you need Mystic Spinal Fluid (32 APD at *Shinjuku Station - Concrete Dungeon*) and Heart of the Foreign God (163 at *Carter Residence - Crow's Nest*)
But the node *Shinjuku Gyoen - Demon's Garden* drops both at 69 APD and 172 APD respectively.

The average AP for one of each, running seperately, is 195. 
Running the combined is less obvious though: The average is 120.5, but that values low rarities over high-rarities, even though hearts are rarer and probably more in demand. 
The max gives 172, since the hearts are higher than the fluid. However, multiple fluids can be expected to drop in that time (~2.5).

The weighted average gives a slightly more representative number where low-rarities are worth less but are still counted.
The weighted APD is (69*32 + 172*163)/(32+163) = 155


#### Using different data

Data is imported from a csv. The csv should be preprocessed to save time and complexity in the programs running. Delete any rows that don't have data (closed) and the header rows. Delete the columns for monuments xp, etc (Letters in the header are A___ for mats and B___etc for the others. Also delete the info rows at the start except for the ids and the names (eg. LDN5, Westminster).
Any data can be imported. They should be in the same format as the included .csv, where it is an id string, a name, then the materials in the order shown in the mats.txt file


##### Credits

Drop data from [r/grandorder](https://www.reddit.com/r/grandorder/), specifically the [advanced drop tables](https://docs.google.com/spreadsheets/d/1NY7nOVQkDyWTXhnK1KP1oPUXoN1C0SY6pMEXPcFuKyI/edit?usp=sharing).