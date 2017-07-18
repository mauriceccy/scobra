<<<<<<< Updated upstream
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
from scipy.stats.stats import pearsonr
import pylab,math,os,itertools


def Plot_Res(res,ReacLst, XLSPath = None, X=None,Y=None, ShowLegend=False, ShowFig = False):
    
    book = xlsxwriter.Workbook(XLSPath)
    
    crs = book.add_worksheet('Reactions')

    

    if ShowFig and X==None:
        raise ValueError,"Needs X axis to plot"
        
    flg = 0    
    if X:
        crs.write(0,0,X)
        for val in res.to_dict()[X].keys():
            crs.write(val+1,0,res.to_dict()[X][val])
        flg = 1
        
    if X in ReacLst:
        ReacLst.remove(X)
    
    for reac in ReacLst:
        
        if X:

            plt.plot(res.to_dict()[X].values(),res.to_dict()[reac].values(),label=reac)
        
        crs.write(0,ReacLst.index(reac)+flg,reac)
        
        for val in res.to_dict()[reac].keys():
            
            crs.write(val+1 ,ReacLst.index(reac)+flg,res.to_dict()[reac][val])
        
    
    if X:
        plt.xlabel(X)
    if Y:
        plt.ylabel(Y)
    if ShowLegend:
        plt.legend()
    if ShowFig:  
      plt.show()

    book.close()

    

def Constants(res,tot=1e-8, XLSPath = None, X=None,Y=None, ShowLegend=False, ShowFig = False):

    """res = DataSet = pandas DataFrame object. Plot, save and returns the reactions those remain constant (no variation) throughout.
        ShowFig requires 'X - axis'
        Modify tot for constant definition"""
    #example FluxAnalysis.Constants(res,XLSPath='/home/rahul/Desktop/Cons.xls',ShowFig=True,X='R1')
    

    ReacLst=[]
    for reac in res.to_dict().keys():
        flux = res.to_dict()[reac].values()
        if all(abs(flux[0]-i)<=tot for i in flux):
            ReacLst.append(reac)
            
    Plot_Res(res,ReacLst, XLSPath = XLSPath, X=X,Y=Y, ShowLegend=ShowLegend, ShowFig = ShowFig)

    
    return ReacLst



def ONRange(res,minx=0,maxx=10, XLSPath = None, X=None,Y=None, ShowLegend=False, ShowFig = False):
    """res = DataSet = pandas DataFrame object. Plot, save and returns reactions those are remain ON between minx to maxx times (occurrence)
    ShowFig requires 'X - axis'"""

    #example FluxAnalysis.ONRange(DataSet, minx=5,maxx=10,XLSPath='/home/rahul/Desktop/OccurON.xls') --> Reactions remain ON (>0) between 5 to 10 times (occurrence)
    
    ReacLst=[]
    for reac in res.to_dict().keys():
        flux = res.to_dict()[reac].values()
        if len(flux)-flux.count(0)>=minx and len(flux)-flux.count(0)<=maxx:
            ReacLst.append(reac)
            
    Plot_Res(res,ReacLst, XLSPath = XLSPath, X=X,Y=Y, ShowLegend=ShowLegend, ShowFig = ShowFig)
            
    return ReacLst






def PlotCorHisto(res,XReactionName, XLSPath=None):
    """res = DataSet = pandas DataFrame object. Pearson's Correlation coefficient (r) with a particular reaction (XReactionName) to all other in the dataset.
    r (with Nan) and p-value will be saved in excel"""
    

    dic = {}

    book = xlsxwriter.Workbook(XLSPath,{'nan_inf_to_errors': True})
    crs = book.add_worksheet('pearson-r')
    crs.write(0,0,'Reaction')
    crs.write(0,1,'r')
    crs.write(0,2,'p-value')
    
    
    

    x = res.to_dict()[XReactionName].values()
    
    for reac in res.to_dict().keys():
        
        y = res.to_dict()[reac].values()
        
        r = pearsonr(x, y)

        if not math.isnan(r[0]):
            dic[reac]=r[0]
        
        crs.write(res.to_dict().keys().index(reac)+1,0,reac)
        crs.write(res.to_dict().keys().index(reac)+1,1,r[0])
        crs.write(res.to_dict().keys().index(reac)+1,2,r[1])

        
    n, bins, patches = pylab.hist(dic.values()) # for bins
    plt.hist(dic.values(), bins=bins)
    plt.xlabel('Correlation coefficient (r)')
    plt.ylabel('Frequency (No. of Reaction)')
    plt.legend()
    plt.show()

        
        

def BuildClassReacMatrix():


    typeIDlst=[]
    with open (os.path.dirname(__file__) + '/../Data/classes.dat','r') as AraClassFile:
        for bl, gr in itertools.groupby(AraClassFile, lambda line: line.startswith('//\n')):
            lgr=list(gr)
            for line in lgr:
                s = line.split()
                if (s[0] == 'UNIQUE-ID' or s[0]=='TYPES') and s[2] not in typeIDlst:
                    typeIDlst.append(s[2])
    with open (os.path.dirname(__file__) + '/../Data/pathways.dat','r') as PathFile:
        for bl, gr in itertools.groupby(PathFile, lambda line: line.startswith('//\n')):
            lgr=list(gr)
            for line in lgr:
                s = line.split()
                if (s[0] == 'UNIQUE-ID' or s[0]=='TYPES') and s[2] not in typeIDlst:
                    typeIDlst.append(s[2])
    with open (os.path.dirname(__file__) + '/../Data/pathways.dat','r') as PathFile:
        ReacLst=[]
        for bl, gr in itertools.groupby(PathFile, lambda line: line.startswith('//\n')):
            lgr=list(gr)
            for line in lgr:
                s = line.split()
                if line.startswith('REACTION-LIST') and s[2] not in ReacLst:
                    ReacLst.append(s[2])

                    
    
    with open (os.path.dirname(__file__) + '/../Data/ClassReacMatrix.txt','w') as MatFile:
        MatFile.write('\t')
        for cls in typeIDlst:
            MatFile.write(cls+'\t')
        MatFile.write('\n')
        for reac in ReacLst:
            MatFile.write(reac+'\t')
            pl=[]
            with open(os.path.dirname(__file__) +'/../Data/pathways.dat','r') as PathFile:
                for bl, gr in itertools.groupby(PathFile, lambda line:line.startswith('//\n')):
                    lgr=list(gr)
                    if 'REACTION-LIST - '+reac+'\n' in lgr:
                        for line in lgr:
                            if line.startswith('TYPES - ') or line.startswith('UNIQUE-ID - '):
                                pl.append(line.split()[2])
            for pid in typeIDlst:
                if pid in pl:
                    MatFile.write('1\t')
                else:
                    MatFile.write('0\t')
            MatFile.write('\n')


def __PathReacMap(PathList):
    
    rv = []
    try:
        with open (os.path.dirname(__file__) + '/../Data/ClassReacMatrix.txt','r') as MatFile:
            pass
    except:
        print '\n\nClassReacMatrix.txt file not found\nScobra will automatically create this file\n'
        print 'Once created, Scobra will use this file next time onwards\nFile creation requires classes.dat and pathways.dat in /Data directory of scobra\n'
        BuildClassReacMatrix()
        print 'ClassReacMatrix.txt is successfully created - it holds Pathway and Reaction map\n'
    with open (os.path.dirname(__file__) + '/../Data/ClassReacMatrix.txt','r') as MatFile:
        for no, line in enumerate(MatFile):
            if no == 0:
                pcol = line.split()
            if no > 0:
                s=line.split()
                for path in PathList:
                    if s[pcol.index(path)+1]=='1' and s[0] not in rv:
                        
                        rv.append(s[0])

            
            
            
    return rv


def GetPathFlux(res,PathSuffixDic={},XLSPath = None, X=None,Y=None, ShowLegend=False, ShowFig = False):
    """res = DataSet = pandas DataFrame object. PathSuffixDic holds the pathway and suffix information, pathway is used to fetch pathway specific reactions, suffix is used to get localization.
    Any pathway 'ID' or 'Type' name can be used. Any parent or chlid class (classes.dat and pathways.dat file; http://pmn.plantcyc.org/ARA/class-tree?object=Pathways) or ID can be entered.
    ShowFig requires 'X - axis'
    same keys need to be affix __KEY__number"""

    #Combination provided below - can be used for central carbon metabolism , need edit??
    
    #PathSuffixDic={'CALVIN-PWY':'_p_Leaf_Day','Energy-Metabolism_KEY_1':'_p_Leaf_Day','Energy-Metabolism_KEY_2':'_c_Leaf_Day','Energy-Metabolism_KEY_3':'_m_Leaf_Day','TCA-VARIANTS':'_m_Leaf_Day'} 

    
    #example rv=FluxAnalysis.GetPathFlux(DataSet,PathSuffixDic={'CALVIN-PWY':'_p_Leaf_Day','TCA-VARIANTS':'_m_Leaf_Day'},XLSPath='/home/rahul/Desktop/Calvin_TCA_Flux_at_leaf_day.xls')
    #example rv=FluxAnalysis.GetPathFlux(DataSet,PathSuffixDic={'Energy-Metabolism':'_c_Leaf_Day'},XLSPath='/home/rahul/Desktop/Energy_at_Cytosol.xls',ShowFig=True,X='time')
    #example rv=FluxAnalysis.GetPathFlux(DataSet,PathSuffixDic={'Energy-Metabolism':'_p_Leaf_Day'},XLSPath='/home/rahul/Desktop/Energy_at_plastid.xls')
    #example rv=FluxAnalysis.GetPathFlux(res,PathSuffixDic={'GLYOXYLATE-BYPASS':'_c_Leaf_Day'},XLSPath='/home/rahul/Desktop/Misc.xls')

    ReacLst=[]
    rv={}
    for path in PathSuffixDic.keys():
        Rlist=__PathReacMap([path.split('_KEY_')[0]])
        UpdatedList=[i+PathSuffixDic[path] for i in Rlist]
        
        for reac in res.to_dict().keys():
            if reac in UpdatedList:
                flux = res.to_dict()[reac].values()
                rv[reac]=flux
                if reac not in ReacLst:
                    ReacLst.append(reac)
    
            
    Plot_Res(res,ReacLst, XLSPath = XLSPath, X=X,Y=Y, ShowLegend=ShowLegend, ShowFig = ShowFig)

    return ReacLst

        
        
    
    

    
        
    

        

=======
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
from scipy.stats.stats import pearsonr
import pylab,math,os,itertools


def Plot_Res(res,ReacLst, XLSPath = None, X=None,Y=None, ShowLegend=False, ShowFig = False):
    
    book = xlsxwriter.Workbook(XLSPath)
    
    crs = book.add_worksheet('Reactions')

    

    if ShowFig and X==None:
        raise ValueError,"Needs X axis to plot"
        
    flg = 0    
    if X:
        crs.write(0,0,X)
        for val in res.to_dict()[X].keys():
            crs.write(val+1,0,res.to_dict()[X][val])
        flg = 1
        
    if X in ReacLst:
        ReacLst.remove(X)
    
    for reac in ReacLst:
        
        if X:

            plt.plot(res.to_dict()[X].values(),res.to_dict()[reac].values(),label=reac)
        
        crs.write(0,ReacLst.index(reac)+flg,reac)
        for val in res.to_dict()[reac].keys():
            
            crs.write(val+1 ,ReacLst.index(reac)+flg,res.to_dict()[reac][val])
        
    
    if X:
        plt.xlabel(X)
    if Y:
        plt.ylabel(Y)
    if ShowLegend:
        plt.legend()
    if ShowFig:  
      plt.show()

    book.close()

    

def Constants(res,tot=1e-8, XLSPath = None, X=None,Y=None, ShowLegend=False, ShowFig = False):

    """res = DataSet = pandas DataFrame object. Plot, save and returns the reactions those remain constant (no variation) throughout.
        ShowFig requires 'X - axis'
        Modify tot for constant definition"""
    #example FluxAnalysis.Constants(res,XLSPath='/home/rahul/Desktop/Cons.xls',ShowFig=True,X='R1')
    

    ReacLst=[]
    for reac in res.to_dict().keys():
        flux = res.to_dict()[reac].values()
        if all(abs(flux[0]-i)<=tot for i in flux):
            ReacLst.append(reac)
            
    Plot_Res(res,ReacLst, XLSPath = XLSPath, X=X,Y=Y, ShowLegend=ShowLegend, ShowFig = ShowFig)

    
    return ReacLst



def ONRange(res,minx=0,maxx=10, XLSPath = None, X=None,Y=None, ShowLegend=False, ShowFig = False):
    """res = DataSet = pandas DataFrame object. Plot, save and returns reactions those are remain ON between minx to maxx times (occurrence)
    ShowFig requires 'X - axis'"""

    #example FluxAnalysis.ONRange(DataSet, minx=5,maxx=10,XLSPath='/home/rahul/Desktop/OccurON.xls') --> Reactions remain ON (>0) between 5 to 10 times (occurrence)
    
    ReacLst=[]
    for reac in res.to_dict().keys():
        flux = res.to_dict()[reac].values()
        if len(flux)-flux.count(0)>=minx and len(flux)-flux.count(0)<=maxx:
            ReacLst.append(reac)
            
    Plot_Res(res,ReacLst, XLSPath = XLSPath, X=X,Y=Y, ShowLegend=ShowLegend, ShowFig = ShowFig)
            
    return ReacLst






def PlotCorHisto(res,XReactionName, XLSPath=None):
    """res = DataSet = pandas DataFrame object. Pearson's Correlation coefficient (r) with a particular reaction (XReactionName) to all other in the dataset.
    r (with Nan) and p-value will be saved in excel"""
    

    dic = {}

    book = xlsxwriter.Workbook(XLSPath,{'nan_inf_to_errors': True})
    crs = book.add_worksheet('pearson-r')
    crs.write(0,0,'Reaction')
    crs.write(0,1,'r')
    crs.write(0,2,'p-value')
    
    
    

    x = res.to_dict()[XReactionName].values()
    
    for reac in res.to_dict().keys():
        
        y = res.to_dict()[reac].values()
        
        r = pearsonr(x, y)

        if not math.isnan(r[0]):
            dic[reac]=r[0]
        
        crs.write(res.to_dict().keys().index(reac)+1,0,reac)
        crs.write(res.to_dict().keys().index(reac)+1,1,r[0])
        crs.write(res.to_dict().keys().index(reac)+1,2,r[1])

        
    n, bins, patches = pylab.hist(dic.values()) # for bins
    plt.hist(dic.values(), bins=bins)
    plt.xlabel('Correlation coefficient (r)')
    plt.ylabel('Frequency (No. of Reaction)')
    plt.legend()
    plt.show()

        
        

def BuildClassReacMatrix():


    typeIDlst=[]
    with open (os.path.dirname(__file__) + '/../Data/classes.dat','r') as AraClassFile:
        for bl, gr in itertools.groupby(AraClassFile, lambda line: line.startswith('//\n')):
            lgr=list(gr)
            for line in lgr:
                s = line.split()
                if (s[0] == 'UNIQUE-ID' or s[0]=='TYPES') and s[2] not in typeIDlst:
                    typeIDlst.append(s[2])
    with open (os.path.dirname(__file__) + '/../Data/pathways.dat','r') as PathFile:
        for bl, gr in itertools.groupby(PathFile, lambda line: line.startswith('//\n')):
            lgr=list(gr)
            for line in lgr:
                s = line.split()
                if (s[0] == 'UNIQUE-ID' or s[0]=='TYPES') and s[2] not in typeIDlst:
                    typeIDlst.append(s[2])
    with open (os.path.dirname(__file__) + '/../Data/pathways.dat','r') as PathFile:
        ReacLst=[]
        for bl, gr in itertools.groupby(PathFile, lambda line: line.startswith('//\n')):
            lgr=list(gr)
            for line in lgr:
                s = line.split()
                if line.startswith('REACTION-LIST') and s[2] not in ReacLst:
                    ReacLst.append(s[2])

                    
    
    with open (os.path.dirname(__file__) + '/../Data/ClassReacMatrix.txt','w') as MatFile:
        MatFile.write('\t')
        for cls in typeIDlst:
            MatFile.write(cls+'\t')
        MatFile.write('\n')
        for reac in ReacLst:
            MatFile.write(reac+'\t')
            pl=[]
            with open(os.path.dirname(__file__) +'/../Data/pathways.dat','r') as PathFile:
                for bl, gr in itertools.groupby(PathFile, lambda line:line.startswith('//\n')):
                    lgr=list(gr)
                    if 'REACTION-LIST - '+reac+'\n' in lgr:
                        for line in lgr:
                            if line.startswith('TYPES - ') or line.startswith('UNIQUE-ID - '):
                                pl.append(line.split()[2])
            for pid in typeIDlst:
                if pid in pl:
                    MatFile.write('1\t')
                else:
                    MatFile.write('0\t')
            MatFile.write('\n')


def PathReacMap(PathList):
    #Only internal call
    rv = []
    try:
        with open (os.path.dirname(__file__) + '/../Data/ClassReacMatrix.txt','r') as MatFile:
            pass
    except:
        print '\n\nClassReacMatrix.txt file not found\nScobra will automatically create this file\n'
        print 'Once created, Scobra will use this file next time onwards\nFile creation requires classes.dat and pathways.dat in /Data directory of scobra\n'
        BuildClassReacMatrix()
        print 'ClassReacMatrix.txt is successfully created - it holds Pathway and Reaction map\n'
    with open (os.path.dirname(__file__) + '/../Data/ClassReacMatrix.txt','r') as MatFile:
        for no, line in enumerate(MatFile):
            if no == 0:
                pcol = line.split()
            if no > 0:
                s=line.split()
                for path in PathList:
                    if s[pcol.index(path)+1]=='1' and s[0] not in rv:
                        
                        rv.append(s[0])

            
            
            
    return rv


def GetPathFlux(res,PathSuffixDic={},XLSPath = None, X=None,Y=None, ShowLegend=False, ShowFig = False):
    """res = DataSet = pandas DataFrame object. PathSuffixDic holds the pathway and suffix information, pathway is used to fetch pathway specific reactions, suffix is used to get localization.
    Any pathway 'ID' or 'Type' name can be used. Any parent or chlid class (classes.dat and pathways.dat file; http://pmn.plantcyc.org/ARA/class-tree?object=Pathways) or ID can be entered.
    ShowFig requires 'X - axis'"""
    
    #example FluxAnalysis.GetPathFlux(DataSet,PathSuffixDic={'CALVIN-PWY':'_p_Leaf_Day','TCA-VARIANTS':'_m_Leaf_Day'},XLSPath='/home/rahul/Desktop/Calvin_TCA_Flux_at_leaf_day.xls')
    #example FluxAnalysis.GetPathFlux(DataSet,PathSuffixDic={'Energy-Metabolism':'_c_Leaf_Day'},XLSPath='/home/rahul/Desktop/Energy_at_Cytosol.xls',ShowFig=True,X='time')
    #example FluxAnalysis.GetPathFlux(DataSet,PathSuffixDic={'Energy-Metabolism':'_p_Leaf_Day'},XLSPath='/home/rahul/Desktop/Energy_at_plastid.xls')
    #example FluxAnalysis.GetPathFlux(res,PathSuffixDic={'GLYOXYLATE-BYPASS':'_c_Leaf_Day'},XLSPath='/home/rahul/Desktop/Misc.xls')

    ReacLst=[]
    rv={}
    for path in PathSuffixDic.keys():
        Rlist=PathReacMap([path])
        UpdatedList=[i+PathSuffixDic[path] for i in Rlist]
    
        for reac in res.to_dict().keys():
            if reac in UpdatedList:
                flux = res.to_dict()[reac].values()
                rv[reac]=flux
                ReacLst.append(reac)
            
    Plot_Res(res,ReacLst, XLSPath = XLSPath, X=X,Y=Y, ShowLegend=ShowLegend, ShowFig = ShowFig)

    return rv

        
        
    
    

    
        
    

        

>>>>>>> Stashed changes
