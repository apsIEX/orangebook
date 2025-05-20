import numpy as np
import os
import fnmatch

import pandas as pd
import matplotlib.pyplot as plt

    
def _df(file='BE',debug=False):
    """
    returns the contents of the data file as a pandas datafram
    BE => binding energies
    EE => emission energies
    """
    if debug:
        print(os.path.dirname(__file__))
    fpath=os.path.join(os.path.dirname(__file__),'orangebook_'+file+'.csv')
    if debug:
        print(fpath)
    df = pd.read_csv(fpath)
    return df

def _elementNumber(element,be_ee='BE'):
    """
    returns the atomic number, symbol for a given element
    """
    df=_df(be_ee.upper())
    if type(element) == str:
        symbol = element
    else:
        symbol = df.AtomicSymbol[element-1]
    number =df.loc[df['AtomicSymbol'] == symbol]['AtomicNumber'].values[0]
    return symbol,number

def _edge2orbital(edge):
    shell=edge.split("_")[0][0]
    n=['K','L','M','N','O','P'].index(shell)
    l=1 if len(edge.split("_")[0][1:])==0 else int(edge.split("_")[0][1:]) 
    orbital=['s','p1/2','p3/2','d3/2','d5/2','f5/2','f7/2'][l-1]
    return str(n+1)+orbital   

def be(element, notation='orbital'):
    """
    element is the atomic symbol or atomic number
    prints the binding energiesfor a give atom
    notation: 'edge' or 'orbital'
    """
    df=_df('BE')
    symbol,number=_elementNumber(element)

    print(number, symbol+":")

    #col is the column header, val is the data for the given element
    for col in df.loc[df['AtomicSymbol'] == symbol].columns[2:]:
        val= df.loc[df['AtomicSymbol'] == symbol][col].values[0]
        #column in edge notion, converting to orbital notation
        if type(val)!=str and val>0:
            if notation == 'orbital':
                col = _edge2orbital(col)+'\t'
            print('\t',col,val)     

def BE(element, notation='orbital'):
    """
    element is the atomic symbol or atomic number
    prints the binding energiesfor a give atom
    notation: 'edge' or 'orbital'
    """
    be(element, notation)           

def find_be(energy,delta=5.0, notation='orbital'):
    """
    prints atomic number, element, edge and binding energy for all edges within the range: energy - delta and energy + delta
    notation: 'edge' or 'orbital'
    """
    df=_df('BE')
    Emin=energy-delta
    Emax=energy+delta
    print("Energy range: "+str(Emin)+" - "+str(Emax))
    #iterating over elements
    for i in df.index:
        symbol=df.iloc[i]['AtomicSymbol']
        number=df.iloc[i]['AtomicNumber']
        new=True  #used to print elememt
        #iterating over edges
        for key in df.iloc[i].keys()[3:]:
            val =float (df.at[i,key])
            if Emin < val <= Emax:
                if new:
                    symbol=df.iloc[i]['AtomicSymbol']
                    number=df.iloc[i]['AtomicNumber']
                    print("\n"+str(number),symbol+":")
                    new=False
                if notation == 'orbital':
                    key = _edge2orbital(key)
                print("  ",key, val)            

def find_BE(energy,delta=5.0, notation='orbital'):
    """
    prints atomic number, element, edge and binding energy for all edges within the range: energy - delta and energy + delta
    notation: 'edge' or 'orbital'
    """   
    find_be(energy,delta, notation)        

def ee(element):
    """
    element is the atomic symbol or atomic number
    prints the emission energies for a given element
    
    """
    df=_df('EE')
    symbol,number=_elementNumber(element,'EE')

    print(number, symbol+":")
    #col is the column header, val is the data for the given element
    for col in df.loc[df['AtomicSymbol'] == symbol].columns[2:]:
        val= df.loc[df['AtomicSymbol'] == symbol][col].values[0]
        if type(val)!=str and val>0:
            print('\t',col,val)     

def find_ee(energy,delta=20.0):
    """
    prints atomic number, element, edge and binding energy for all edges within the range: energy - delta and energy + delta
    notation: 'edge' or 'orbital'
    """
    df=_df('EE')
    Emin=energy-delta
    Emax=energy+delta
    print("Energy range: "+str(Emin)+" - "+str(Emax))
    for i in df.index:
        symbol=df.iloc[i]['AtomicSymbol']
        number=df.iloc[i]['AtomicNumber']
        new=True
        for key in df.iloc[i].keys()[3:]:
            val =float (df.at[i,key])
            if Emin < val <= Emax:
                if new:
                    symbol=df.iloc[i]['AtomicSymbol']
                    number=df.iloc[i]['AtomicNumber']
                    print("\n"+str(number),symbol+":")
                    new=False
                print("  ",key, val)         

def find_EE(energy,delta=20.0):
    """
    prints atomic number, element, edge and binding energy for all edges within the range: energy - delta and energy + delta
    notation: 'edge' or 'orbital'
    """     
    find_ee(energy,delta)     


def xps(element):
    fpath,fileList=_XPSfiles(element)
    if len(fileList)>0:
        fig=plt.figure(figsize=(10*len(fileList),10))
        for i,f in enumerate(fileList):
            ax = fig.add_subplot(1,len(fileList),i+1)
            img=plt.imread(os.path.join(fpath,f))
            ax.imshow(img) 
            ax.axis('off')
        plt.show()
    else:
        print("No XPS data for "+str(element))


def _XPSfiles(element):
    fpath=os.path.join(os.path.dirname(__file__),'PHI_XPS')
    
    symbol,number=_elementNumber(element)
    fileList=fnmatch.filter(os.listdir(path =fpath ), 'PHI_XPS_'+str(number)+'_*.tiff')
    
    return fpath, fileList

