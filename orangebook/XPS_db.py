import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import re
import orangebook as ob
import pandas as pd

def plot_atomic_cross_sections(atom, output_folder="plots"):
    """
    Reads an interpolated CSV and plots Energy vs Cross-Section for all subshells.
    """
    input_folder = "interpolated_results"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    search_pattern = os.path.join(input_folder, f"*_{atom}.csv")
    input_files = sorted(glob.glob(search_pattern))
    file_path = input_files[0]
        
    # Load the data
    df = pd.read_csv(file_path)
    energy_col = df.columns[0]
    subshell_cols = df.columns[1:]
    
    plt.figure(figsize=(10, 6))
    
    # Plot each subshell
    for subshell in subshell_cols:
        # Filter out NaNs for plotting
        valid_df = df[[energy_col, subshell]].dropna()
        if not valid_df.empty:
            plt.plot(valid_df[energy_col], valid_df[subshell], label=subshell, linewidth=1.5)
    
    # Set log scales - Crucial for photoionization data
    plt.xscale('log')
    plt.yscale('log')
    
    # Formatting
    plt.title(f"Photoionization Cross Sections: {os.path.basename(file_path)}")
    plt.xlabel("Photon Energy (eV)")
    plt.ylabel("Cross Section (Mbarn)") # Adjust unit based on your data
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
    # Save the plot
    #plot_name = os.path.basename(file_path).replace('.csv', '.png')
    #plt.savefig(os.path.join(output_folder, plot_name), dpi=300)
    plt.close() # Close to free up memory during batch processing



def transmission_factor(KE, PE):
    """Approximate transmission factor for Scienta R4000 based on kinetic energy (KE)"""

    x = KE / PE
    return 1 - 0.041*x+9.4e-4*x**2 - 1e-5*x**3 + 3.9e-8*x**4


def RSF(atom, photon_energy,PE=200,verbose=True):
    """ Calculates the Relative Sensitivity Factor (RSF) for a given atom and photon energy, relative to Carbon 1s.
        Input: atom (str), photon_energy (float, in eV)
        Output: RSF_dict (dict) with keys as subshells and values as RSF values
        Warning, can be off from actual RSF"""
    
    input_dir = "interpolated_results"
    search_pattern = os.path.join(input_dir, f"*_{atom}.csv")
    matching_files = glob.glob(search_pattern)
    atom_df = pd.read_csv(matching_files[0])
    df = atom_df.dropna(axis=1, how='all')  # Remove completely empty columns first
    if not matching_files:
        print(f"No data found for atom '{atom}' in {input_dir}.")
        return None
    C_df = pd.read_csv(input_dir+"/interp_6_C.csv")
    E_index = np.argmin(np.abs(C_df['Photon Energy / eV'] - photon_energy))
    subshell_cols = atom_df.columns[1:]
    CS_ratio = {}
    for subshell in subshell_cols:
        CS_ratio[subshell] = atom_df[subshell][E_index] / C_df['1s'][E_index]

    KE_C = photon_energy - 284.2 - 4.5 # hv - BE of C 1s - work function of spectrometer (approx 4.5)
    T_C = transmission_factor(KE_C, PE)  # Transmission factor for Carbon 1s at its kinetic energy

    KE_atom = ob.be(atom, return_dict=True)
    for key, value in KE_atom.items():
        KE_atom[key] = photon_energy - value - 4.5 # hv - BE of subshell - work function of spectrometer
    # if value < 0 delete the key from the dictionary
    for key, value in list(KE_atom.items()):
        if value < 0:
            del KE_atom[key]
    KE_ratio = {}
    
    for key, value in KE_atom.items():
        KE_ratio[key] = (value/KE_C)**0.66 * transmission_factor(value, PE) / T_C # Approximate ratio of mean free path lengths based on kinetic energy ratio times transmission factor ratio

    RSF_dict = {}

    for split_key, val2 in KE_ratio.items():
        # This regex looks for 1 or more digits (\d+) followed by one of the letters s, p, d, or f
        # It will extract "2p" from "2p3/2", or just "1s" from "1s"
        match = re.match(r"(\d+[spdf])", split_key)
        
        if match:
            base_key = match.group(1) # This is your base subshell (e.g., '2p')
            
            # Multiply the values if the base key exists in dict1
            if base_key in CS_ratio:
                RSF_dict[split_key] = CS_ratio[base_key] * val2
            else:
                print(f"Warning: '{base_key}' not found in CS_ratio. Skipping '{split_key}'.")
        else:
            print(f"Warning: Could not parse orbital format for '{split_key}'.")

    # View the result
    if verbose == True:
        for key, value in RSF_dict.items():
            print(f"{key}: {value}")

    return RSF_dict
    

def plot_XPS_spectrum(atoms, photon_energy, E_start = 0, E_offset = 0, PE= 200 ):
    """ -Takes a list of atom with optional stoichiometric quantities (e.g., 'B2' for 2 Boron atoms) and plots the XPS spectrum.
        -Photon energy is the energy of the X-ray source used in the experiment (e.g., 1486.6 eV for Al K-alpha).
        -E_start allows you to set a custom starting point for the x-axis (binding energy).
        -The intensity of each peak is scaled by the quantity specified in the input string
         eg. plot_XPS_spectrum(['Sc', 'B2', 'O3.5'], 1486.6)
        -Peaks with low KE have lower accuracy for intensity predictions.
        """
    if isinstance(atoms, str):
        atoms = [atoms]
        
    # Dictionary of theoretical branching fractions based on 2j+1 multiplicity
    branching_fractions = {
        'p1/2': 1/3, 'p3/2': 2/3,
        'd3/2': 2/5, 'd5/2': 3/5,
        'f5/2': 3/7, 'f7/2': 4/7
    }

    plt.figure(figsize=(10, 6))
    colors = plt.cm.tab10.colors 
    global_max_intensity = 0 
    ax = plt.gca()
    ax.set_clip_on(True) # Enable clipping to prevent text from going outside the plot area

    for idx, atom_input in enumerate(atoms):
        # 1. Parse stoichiometry (e.g., 'B2' -> Element: 'B', Qty: 2.0)
        match = re.match(r"([A-Z][a-z]*)(\d*\.?\d*)", atom_input)
        if not match:
            continue
            
        atom = match.group(1)
        qty_str = match.group(2)
        qty = float(qty_str) if qty_str else 1.0

        BE_atom = ob.be(atom, return_dict=True)
        RSF_dict = RSF(atom, photon_energy, PE=PE, verbose=False)
        
        binding_energies = []
        intensities = []
        subshells = []

        for subshell, be in BE_atom.items():
            # 2. Extract the base orbital (e.g., '2p' from '2p3/2')
            match_base = re.match(r"(\d+[spdf])", subshell)
            if not match_base:
                continue
            base_subshell = match_base.group(1)
            
            # 3. Lookup the total RSF (checks for split name first, falls back to base name)
            total_rsf = None
            if subshell in RSF_dict:
                total_rsf = RSF_dict[subshell]
            elif base_subshell in RSF_dict:
                total_rsf = RSF_dict[base_subshell]
                
            # If we found an RSF and the photon has enough energy to excite it
            if total_rsf is not None and be <= photon_energy:
                
                # 4. Determine the spin-orbit splitting fraction
                fraction = 1.0 # Default to 1 for s-orbitals
                for split_key, frac_val in branching_fractions.items():
                    if split_key in subshell:
                        fraction = frac_val
                        break
                        
                # 5. Calculate final intensity: Total RSF * Composition * Branching Fraction
                scaled_intensity = total_rsf * qty * fraction
                
                subshells.append(f"{atom} {subshell}") 
                binding_energies.append(be-E_offset)
                intensities.append(scaled_intensity)

        if not intensities:
            continue

        global_max_intensity = max(global_max_intensity, max(intensities))
        color = colors[idx % len(colors)] 

        plt.vlines(x=binding_energies, ymin=0, ymax=intensities, color=color, linewidth=2, label=atom_input)
        plt.plot(binding_energies, intensities, 'o', color=color)

        for i, sub_name in enumerate(subshells):
            label_text = sub_name
            # Remove the box character by stripping after replacement
            # Strip any trailing invisible/box characters
            label_text = label_text.encode('utf-8', 'ignore').decode('utf-8')
            
            plt.text(binding_energies[i], intensities[i] + (global_max_intensity * 0.02), 
                     label_text, ha='center', va='bottom', fontsize=9, color=color, rotation=45, clip_on=True)

    # --- Global Formatting ---
    if E_start!= 0:
        plt.xlim(E_start, 0)
    else:        plt.xlim(photon_energy, 0)
    plt.ylim(0, global_max_intensity * 1.2) 
    plt.xlabel('Binding Energy (eV)', fontsize=12)
    plt.ylabel('Intensity (Arbitrary Units)', fontsize=12)
    plt.title(f'Simulated XPS Spectrum ($h\\nu$ = {photon_energy} eV)', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    if by_label:
        plt.legend(by_label.values(), by_label.keys(), title="Composition")
    
    plt.tight_layout()
    plt.show()

