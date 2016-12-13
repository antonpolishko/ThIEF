from random import randrange, random, gauss
import numpy as np
import sys
import TrNM as hg
import os
import LPsolMerge as lp
import csv

def ReadNucTable(inputStr, headerFlag=None):
    '''
    Takes table in csv format, skips first line (headerFlag) if needed and creates a table of float numbers
    '''
    if headerFlag is None:
        headerFlag = False
    points = []
    with open(inputStr, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        if (headerFlag):
            print 'skip header'
            csvreader.next()
        for row in csvreader:
            points.append(map(float, row))
    return np.array(points)

def SaveToFile(layer, fileName):
    from os.path import isfile
    # if isfile(fileName):
    #     print "file " + fileName + " already exists"
    #     print "output will go to " + fileName + "_1"
    #     fileName = fileName + '_1'
    with open(fileName, 'w') as fout:
        for line in layer:
            if line[1] == 1:
                print >> fout, line[0]


def SaveTracksToFile(listOfLayers, fileName):
    from os.path import isfile
    # if isfile(fileName):
    #     print "file " + fileName + " already exists"
    #     print "output will go to " + fileName + "_1"
    #     fileName = fileName + '_1'
    numLayer = len(listOfLayers)
    numLines = len(listOfLayers[0])
    with open(fileName, 'w') as fout:
        for i in range(numLines):
            strToWrite = ''
            for j in range(numLayer):
                strToWrite += str(listOfLayers[j][i][0])+'\t'+ str(listOfLayers[j][i][1]) + '\t'
            print >> fout, strToWrite


def main(fileName='default.out', missPenalty=30):
    """function to generate a set of points on a plane that are at least "linker" apart
    returns a matrix (location, isPresentFlag), where first coordinate is location, second - boolen True if the point is present

    """
    numTracks = 0
    flag1 = False
    flag2 = False
    flag3 = False
    flag4 = False
    flag5 = False
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        print ">python process.py <output file> <track 1> <track 2> [<track 3>] [<track 4>] [<track 5>] [<track 6>] [<track 7>] [<track 8>] [<track 9>]"
        return 0
    if len(sys.argv) > 2:
        fileNameIn1 = sys.argv[2]
        flag1 = True
    else:
        print "Not enough input files to create tracks..."
        print ">python process.py <output file> <track 1> <track 2> [<track 3>] [<track 4>] [<track 5>]"
        return 0 
    if len(sys.argv) > 3:
        fileNameIn2 = sys.argv[3]
        numTracks = numTracks + 1
        flag2 = True
    else:
        print "Only one input file present, just use it as your track :) ..."
        return 0 
    if len(sys.argv) > 4:
        fileNameIn3 = sys.argv[4]
        numTracks = numTracks + 1
        flag3 = True

    if len(sys.argv) > 5:
        fileNameIn4 = sys.argv[5]
        numTracks = numTracks + 1
        flag4 = True

    if len(sys.argv) > 6:
        fileNameIn5 = sys.argv[6]
        numTracks = numTracks + 1
        flag5 = True  

    if len(sys.argv) > 7:
        fileNameIn6 = sys.argv[7]
        numTracks = numTracks + 1
        flag6 = True

    if len(sys.argv) > 8:
        fileNameIn7 = sys.argv[8]
        numTracks = numTracks + 1
        flag7 = True 

    if len(sys.argv) > 9:
        fileNameIn8 = sys.argv[9]
        numTracks = numTracks + 1
        flag8 = True

    if len(sys.argv) > 10:
        fileNameIn9 = sys.argv[10]
        numTracks = numTracks + 1
        flag9 = True    

    node0 = ReadNucTable(fileNameIn1)
    numAttributes = len(node0[0])
    node1 = ReadNucTable(fileNameIn2)
    if (flag3):
        node2 = ReadNucTable(fileNameIn3)
    if (flag4):
        node3 = ReadNucTable(fileNameIn4)
    if (flag5):
        node4 = ReadNucTable(fileNameIn5)
    if (flag6):
        node5 = ReadNucTable(fileNameIn6)
    if (flag7):
        node6 = ReadNucTable(fileNameIn7)
    if (flag8):
        node7 = ReadNucTable(fileNameIn8)
    if (flag9):
        node8 = ReadNucTable(fileNameIn9)
    #modifications to add more layers go here
    
##this part for building solution
##NB!!! It requires gpsol installed (no check for this) 
   
    layer0 = hg.layerOfNodes(node0)
    layer1 = hg.layerOfNodes(node1)
    if (flag3):
        layer2 = hg.layerOfNodes(node2)
    if (flag4):
        layer3 = hg.layerOfNodes(node3)
    if (flag5):
        layer4 = hg.layerOfNodes(node4)
    if (flag6):
        layer5 = hg.layerOfNodes(node5)
    if (flag7):
        layer6 = hg.layerOfNodes(node6)
    if (flag8):
        layer7 = hg.layerOfNodes(node7)
    if (flag9):
        layer8 = hg.layerOfNodes(node8)
    #modifications to add more layers go here
    print 'layers processed'
    graph = hg.hyperGraph(layer0)
    graph.missPenalty = missPenalty
    graph.okil = missPenalty*2
    print "layer0 done"
    graph.AddLayer(layer1)
    print "layer1 done"
    if (flag3):
        graph.AddLayer(layer2)
        print "layer2 done"
    if (flag4):
        graph.AddLayer(layer3)
        print "layer3 done"
    if (flag5):
        graph.AddLayer(layer4)
        print "layer4 done"
    if (flag6):
        graph.AddLayer(layer5)
        print "layer5 done"
    if (flag7):
        graph.AddLayer(layer6)
        print "layer6 done"
    if (flag8):
        graph.AddLayer(layer7)
        print "layer7 done"
    if (flag9):
        graph.AddLayer(layer8)
        print "layer8 done"
    #modifications to add more layers go here

    graph.EdgeCostComputation()
    print 'done building graph'
    hg.CPLEXprint(graph, fileName+'_tmp.lp')
    # run linear solver gpsol and parse it's output
    print 'start linear solver'
    os.system('./runLS.sh '+fileName+'_tmp.lp')
    print 'linear solution done'
    lpSol = lp.ReadColumn(fileName+'_tmp.csv')
    print 'solution read'
    os.system('rm '+fileName+'_tmp.lp')
    os.system('rm '+fileName+'_tmp.csv')
    os.system('rm '+fileName+'_tmp.sol')
    table = graph.GetTrackStat(lpSol, numAttributes)
    print table
    np.savetxt(fileName,
               table, delimiter='\t', fmt='%.2f')
    print "Finally Done"
    return 1

if __name__ == '__main__':
    main()
