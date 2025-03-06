import ROOT
import numpy as np

file_comb = ROOT.TFile("/Users/spin/RUS_Extended_MC/Comb/MC_COMB_DUMP_MARCH2.root")
file_mc = ROOT.TFile("../Dump/MC_JPsi_Pythia8_Dump_Feb_24.root")

tree_mc = file_mc.Get("tree")
tree_comb = file_comb.Get("tree")

def save_to_npy(tree, filename):
    """Extracts px, py, pz for mu+ and mu- separately, as well as mass, pT, phi of dimuon system, and saves them as a NumPy array."""
    data_list = []
    for event in tree:
        # Initialize muon variables
        if event.rec_dimu_mass[0] < 0.01:
            continue
        px_mup, py_mup, pz_mup = 0, 0, 0
        px_mum, py_mum, pz_mum = 0, 0, 0

        # Assign first found mu+ and mu-
        for i in range(len(event.rec_pz)):
            px, py, pz, charge = event.rec_px[i], event.rec_py[i], event.rec_pz[i], event.rec_charge[i]
            if charge > 0:
                px_mup, py_mup, pz_mup = px, py, pz
            elif charge < 0:
                px_mum, py_mum, pz_mum = px, py, pz

        # Initialize dimuon variables
        mass_dimu, pt_dimu, phi_dimu = 0, 0, 0
        if len(event.rec_dimu_mass) > 0:
            px, py, pz, mass = event.rec_dimu_px[0], event.rec_dimu_py[0], event.rec_dimu_pz[0], event.rec_dimu_mass[0]
            dimu = ROOT.TLorentzVector()
            dimu.SetXYZM(px, py, pz, mass)
            mass_dimu, pt_dimu, phi_dimu = dimu.M(), dimu.Pt(), dimu.Phi()

        # Print all features for this event
#        print(f"Event: px_mup={px_mup}, py_mup={py_mup}, pz_mup={pz_mup}, "
#              f"px_mum={px_mum}, py_mum={py_mum}, pz_mum={pz_mum}, "
#              f"mass={mass_dimu}, pT={pt_dimu}, phi={phi_dimu}")

        # Append event data

        event_data = np.array([px_mup, py_mup, pz_mup, px_mum, py_mum, pz_mum, mass_dimu, pt_dimu, phi_dimu])
        if np.isnan(event_data).any():
            print(f"Skipping event {len(data_list)} due to NaN values: {event_data}")
            continue  # Skip this event
        data_list.append([px_mup, py_mup, pz_mup, px_mum, py_mum, pz_mum, mass_dimu, pt_dimu, phi_dimu])
    # Convert to NumPy array
    data_array = np.array(data_list, dtype=np.float32)

    # Save as npy file
    np.save(filename, data_array)
    print(f"Saved {filename} with {len(data_list)} events.")

# Save experimental and combined data
save_to_npy(tree_mc, "mc_data.npy")
save_to_npy(tree_comb, "comb_data.npy")

