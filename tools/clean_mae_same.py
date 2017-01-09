#!/usr/bin/python
import os
import sys

from schrodinger import structure as sch_struct

PROPERTIES_TO_REMOVE = \
    [
    's_m_Source_File',
    's_m_Source_Path',
    's_m_entry_id',
    'i_m_Source_File_Index',
    'i_m_ct_format',
    'i_m_ct_stereo_status',
    
    's_st_AtomNumChirality_1',
    's_st_Chirality_1',
    's_st_Chirality_2',
    's_st_Chirality_3',
    's_st_Chirality_4',
    's_st_Chirality_5',

    's_sd_program',
    
    'b_mmod_Minimization_Converged-MM3*',
    'i_mmod_Times_Found-MM3*',
    'r_mmod_RMS_Derivative-MM3*',
    'r_mmod_Potential_Energy-MM3*',
    'r_mmod_Stretch_Energy-MM3*',
    'r_mmod_Bend_Energy-MM3*',
    'r_mmod_Torsional_Energy-MM3*',
    'r_mmod_Improper_Torsional_Energy-MM3*',
    'r_mmod_Van_der_Waal_Energy-MM3*',
    'r_mmod_Electrostatic_Energy-MM3*',
    'r_j_Gas_Phase_Energy'
    ]

ATOM_PROPERTIES_TO_REMOVE = \
    [
    's_m_mmod_res',
    'i_m_color',
    'r_m_charge1',
    'r_m_charge2',
    's_m_pdb_residue_name',
    's_m_color_rgb',
    's_m_grow_name',
    'i_m_formal_charge',
    'i_m_sculpting_atom_index',
    'i_m_sculpting_constraint',
    's_m_label_color',
    's_m_label_format',
    's_m_label_color',
    's_m_label_user_text',
    'i_sd_original_parity'
    ]

for filename in sys.argv[1:]:
    structure_reader = sch_struct.StructureReader(filename)
    structure_writer = sch_struct.StructureWriter('TEMP.mae')

    for structure in structure_reader:
        for prop in PROPERTIES_TO_REMOVE:
            try:
                del structure.property[prop]
            except KeyError:
                pass
        # Change the name too. Why not.
        structure.property['s_m_title'] = \
            structure.property['s_m_entry_name'] = \
                os.path.splitext(
                    os.path.basename(filename))[0]
        for atom in structure.atom:
            for prop in ATOM_PROPERTIES_TO_REMOVE:
                try:
                    del atom.property[prop]
                except KeyError:
                    pass
                except ValueError:
                    pass
        structure_writer.append(structure)

    structure_reader.close()
    structure_writer.close()

    os.rename('TEMP.mae', filename)


