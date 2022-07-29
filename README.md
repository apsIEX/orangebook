# orangebook
Python code to look up the binding energies from the X-ray Data Booklet, a.k.a. the orange book 
(https://xdb.lbl.gov)

## Installing orangebook


    git clone https://github.com/apsIEX/orangebook
    cd orangebook
    pip install .


## Usage:
    import orangebook as ob
    
    ob.binding_energy('Si') => prints the binding energies for silicon
    ob.binding_energy(6) => prints the binding energies for carbon
    
    ob.find_elements(283) => finds the elements with a binding energy of 283 +/- delta (default = 5eV)
    
    ob.XPSbook('Ti') => show the pages of the Handbook of X-ray Photoelectron Spectroscopy for the specified element (atomic symbol or number)
