# orangebook
Python code to look up the binding energies from the X-ray Data Booklet, a.k.a. the orange book 
(https://xdb.lbl.gov)

## Installing orangebook


    git clone https://github.com/apsIEX/orangebook
    cd orangebook
    pip install .


## Usage:
    import orangebook as ob

    # Binding Energies
    
    ob.be('Si') => prints the binding energies for silicon
    ob.be(6) => prints the binding energies for carbon
    
    ob.find_be(283) => finds the elements with a binding energy of 283 +/- delta (default = 5eV)
    
    ob.xps('Ti') => show the pages of the Handbook of X-ray Photoelectron Spectroscopy 

    # Emission Energies
    ob.ee('Cu') => prints the emission energies for Copper
    ob.ee(54) =>
  
