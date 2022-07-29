# orangebook
Python code to look up the binding energies from the X-ray Data Booklet, a.k.a. the orange book 
(https://xdb.lbl.gov)

## Installing orangebook


    git clone https://github.com/apsIEX/orangebook
    cd orangebook
    pip install .


## Example:
    
In [1]: import orangebook as ob

In [2]: ob.binding_energy('Si')
14 Si:
	 1s	 1839.0
	 2s	 149.7
	 2p1/2	 99.82
	 2p3/2	 99.42

In [3]: ob.binding_energy(6)
6 C:
	 1s	 284.2

In [4]: ob.find_elements(283)
Energy range: 278 - 288

38 Sr:
   3p1/2 280.3

44 Ru:
   3d3/2 284.2
   3d5/2 280.0

63 Eu:
   4p1/2 284.0

64 Gd:
   4p1/2 286.0

65 Tb:
   4p3/2 284.1

76 Os:
   4d5/2 278.5

In [5]: ob.XPSbook('Ti')
