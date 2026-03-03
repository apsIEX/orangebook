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


    NOTE: The transmission function T is defined for the scienta R4000 analyzer.
             T = 1 - 0.041*x + 9.4e-4*x^2 - 1e-5*x^3 + 3.9e-8*x^4
                        
    To use XPS plotting (Intensity vs BE): (The transmission function is defined for the scienta R4000 analyzer)
        from orangebook.XPS_db import *
        plot_XPS_spectrum(plot_XPS_spectrum(atoms, photon_energy, E_start=0, E_offset=0, PE=200)
    To find RSF factors for elemental composition analysis:
        from orangebook.XPS_db import *
        RSF(atom, photon_energy, PE=200, verbose=True)
    
