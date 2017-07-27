import pandas as pd
import numpy as np
import os
import openpyxl


def imk_folder(folderpath):
    """
    imk_folder iterates over all knot files in folderpath and calculates the
    wanted data the data is stored in df_final and df2_final, processed and
    finally written to an excel sheet

    """
    # CREATE output data frames
    df_final = pd.DataFrame(columns=['Tree', 'Log', 'Knot',
                                     'RadialPosition_mm', 'DiameterV_mm',
                                     'DiameterH_mm', 'MeanDiameter_mm',
                                     'Zposition_mm', 'Sound_pos'])
    df2_final = pd.DataFrame(columns=['Tree', 'Log', 'Knot'])

    knot = 1
    # ITERATE over all files
    for filename in os.listdir(folderpath):
        if filename not in ['output']:
            filepath = folderpath + '/' + filename
            dff, dff2, knot = imk_file(filepath, knot)
            df_final = pd.concat([df_final, dff])
            df2_final = pd.concat([df2_final, dff2])

    # PROCESS data
    df2_final['Knot'] = np.arange(1, df2_final.shape[0] + 1)
    df2_final = df2_final[['Tree', 'Log', 'Knot', 'DKB_mm', 'KE_mm',
                           'Azimuth_deg', 'sound_knot']]

    # CREATE new folder if needed
    if not os.path.exists(folderpath + '/output'):
        os.makedirs(folderpath + '/output')

    writer = pd.ExcelWriter(folderpath + '/output/Manual_KnotData.xlsx')
    df_final.to_excel(writer, 'Multi_imgMan')
    df2_final.to_excel(writer, 'One_imgMan')
    writer.save()

    return df_final, df2_final


def imk_file(filepath, knot):
    # IMPORT (very unpypythonic, ignore)
    heading = pd.read_csv(filepath, delim_whitespace=True, nrows=2,
                          header=None)  # first two rows
    df = pd.read_csv(filepath, delim_whitespace=True, skiprows=[0, 1, 2],
                     header=None)  # data frame without third line
    with open(filepath) as f:  # get the third line extra
        for i, line in enumerate(f):
            if i == 3:
                third = line.split()
    df.loc[-1] = third  # adding third line as first row
    df.index = df.index + 1  # shift index
    df = df.sort_index()  # sort by index

    # GET name
    tree_id = int(heading.iloc[0, 0].split('_')[1])
    log_id = int(heading.iloc[0, 0].split('_')[2])

    # CREATE new output_frames
    df_out = pd.DataFrame(columns=['Tree', 'Log', 'Knot', 'RadialPosition_mm',
                                   'DiameterV_mm', 'DiameterH_mm',
                                   'MeanDiameter_mm', 'Zposition_mm',
                                   'Sound_pos'])
    df2_out = pd.DataFrame(columns=['Tree', 'Log', 'Knot', 'DKB_mm', 'ke_mm',
                                    'Azimuth_deg'])

    for index in range(0, df.shape[0] - df.shape[0] % 4, 4):
        # EXTRACT group
        dfg = df[index:index + 4]

        # PROCESS Group of 4
        dfg_out = imk_group(dfg)
        dfg2_out = imk_knot(dfg)

        dfg_out['Knot'] = knot
        knot += 1

        # CONCAT output to dataframe
        df_out = pd.concat([df_out, dfg_out])
        df2_out = pd.concat([df2_out, dfg2_out])

    # SET tree and log variables
    df_out['Tree'] = tree_id
    df_out['Log'] = log_id
    df2_out['Tree'] = tree_id
    df2_out['Log'] = log_id

    # RETURN data frame
    return df_out, df2_out, knot


# Database 1 function
def imk_group(dfg):
    # save val for coming calculations
    _dfg = dfg

    # DROP columns where value in the second row is 0
    dfg = dfg.loc[:, dfg.iloc[2, :] != 0]

    # CREATE output data frame
    dfg_out = pd.DataFrame(columns=['Tree', 'Log', 'Knot'])

    # CREATE rows
    dfg_out['RadialPosition_mm'] = list(range(20, dfg.shape[1] * 20 + 20, 20))
    dfg_out['DiameterV_mm'] = dfg.iloc[2, :]
    dfg_out['DiameterH_mm'] = dfg.iloc[1, :]
    dfg_out['MeanDiameter_mm'] = [np.mean([x, y]) for x, y in
                                  zip(dfg.iloc[2, :], dfg.iloc[1, :])]
    dfg_out['Zposition_mm'] = dfg.iloc[dfg.shape[0] - 1, :] \
                              + float(_dfg.iloc[0, 2])
    dfg_out['Sound_pos'] = [_ > float(_dfg.iloc[0, 3]) for _ in
                            dfg_out['RadialPosition_mm']]
    dfg_out.Sound_pos = dfg_out.Sound_pos.astype(int)

    return dfg_out


# Database 2 function
def imk_knot(dfg):
    df2_out = pd.DataFrame(data=[[0] * 3], columns=['Tree', 'Log', 'Knot'])

    if dfg.iloc[0, 4] is not -1:
        dkb_mm = 0
    else:
        dkb_mm = dfg.iloc[0, 3]
    df2_out['DKB_mm'] = dkb_mm

    if dfg.iloc[0, 4] is not -1:
        ke_mm = dfg.iloc[0, 4]
    else:
        ke_mm = dfg.iloc[0, 3]
    df2_out['KE_mm'] = ke_mm

    df2_out['Azimuth_deg'] = dfg.iloc[0, 6]

    if dfg.iloc[0, 4] is -1:
        sound_knot = 1
    else:
        sound_knot = 0
    df2_out['sound_knot'] = sound_knot

    return df2_out


if __name__ == '__main__':

    # DEFINE data path
    folderpath = "C:/Users/helge/Dropbox/Uni/Python 2/python2_final/projects" \
                 "/CT_manager/Data_Part_1"
    filepath = folderpath + '/Knots@Dgl_623_10_2015_05_28.kno'

    folderpath = 'E:/DropBox/Dropbox/STUDIGEDÖNS/fächer/python 2/projekte' \
                 '/final_git/python2_final/projects/CT_manager/Data_Part_1'

    df1, df2 = imk_folder(folderpath)

