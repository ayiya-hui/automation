import os

def  getResult(localhost):
    itemList=os.listdir("../Results")
    folderList=[]
    mapList=[]

    for folder in itemList:
        if (os.path.isdir("../Results/"+folder)):
            folderList.append(folder)

    for item in folderList:
        mapping=[]
        subFolder=os.listdir("../Results/"+item)
        subFolder.sort()
        subFolder.reverse()
        mapping=[item, subFolder]
        mapList.append(mapping)

    html="""
    <TITLE>Accelops Automation Test</TITLE>
    <H1>Welcome to Accelops Automation Test!</H1>
    <P>To view the most recent test results, please click the links to see the result:</P>
    <HR>
    """
    treeString=""
    for map in mapList:
        folder=map[0]
        subfolder=map[1]
        treeString=treeString+"<LI>"+folder+"\n"

        if (len(subfolder)!=0):
            treeString=treeString+"<UL>\n"
            for sub in subfolder:
                link="http://"+localhost+"/testresult/"+folder+"/"+sub+"/report.html"
                treeString=treeString+"<LI><A HREF="+link+">"+sub+"</LI>\n"
            treeString=treeString+"</UL>\n"
        else:
            treeString=treeString+"</LI>\n"

        treeString=treeString+"</LI>\n"

    final=html+treeString+"</BODY>\n"+"</HTML>\n"

    outFile=open("../Public/index.html", 'w')
    outFile.write(final)
    outFile.close()

    return 1
