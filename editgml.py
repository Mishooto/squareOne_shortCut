import os
'''import os
# assign directory
directory = 'files'

# iterate over files in
# that directory
for filename in os.listdir(directory):
	f = os.path.join(directory, filename)
	# checking if it is a file
	if os.path.isfile(f):
		print(f)
		

for gml in 
with open(graphfile, 'r') as f:
        blob = f.read()'''

directory = "/home/mikheil/Desktop/SQ1_ShortCut-main/Topology Zoo/archive"
newdir= "newdir"

for filename in os.listdir(directory):
    currentfile=os.path.join(directory, filename)
    print(currentfile)
    if currentfile.endswith(".gml"):
        with open (currentfile, 'r') as f:
            blob = f.read()
            substring = "Developed"
            index = blob.find(substring)
            length = len(substring)
            end = index+length+2 
            breakingpoint= end+3
            new = "multigraph 1\n  "
            newblob = blob[:breakingpoint] + new + blob[breakingpoint:]
            newname=filename[:-4]+"_edited"+filename[-4:]
            print(newname)
            newpath = os.path.join(newdir,newname)
            with open (newpath, "w") as edited:
                edited.write(newblob)


#random regular graphs
                #immer 8 kantendisjunkte pfade
                #fur alle s und d alle kantendisjunkte pfade bestimmen
                #wenn nur 3 kantendisjunkte pfade darf man nur 2 fehler werfen
                #random fehler ins netzwerk schmeißen, steigende fehler von 0.9 bis 0.1, 10% fehler = 10% der edges rausnehmen schrittweise ins netzwerk werfen 
                #hops zählen auf jeden fall
                #entweder pickle oder csv dateien 