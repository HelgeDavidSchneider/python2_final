import pandas as pd
import numpy as np
import os

"""

"""

# DEFINE data path
folderpath = "C:/Users/helge/Dropbox/Uni/Python 2/python2_final/projects/CT manager/Data_Part_1"
filepath = folderpath + '/Knots@Dgl_623_1_2015_05_20.kno'

imk_folder(folderpath)


def imk_folder(folderpath):

    # CREATE output data frames
    df_final = pd.DataFrame(columns=['Tree', 'Log', 'Knot', 'RadialPosition_mm', 'DiameterV_mm', 'DiameterH_mm',
                                   'MeanDiameter_mm', 'Zposition_mm', 'Sound_pos'])
    df2_final = pd.DataFrame(columns=['Tree', 'Log', 'Knot'])

    # ITERATE over all files
    for filename in os.listdir(folderpath):
        if filename not in ['output']:
            print(filename)
            filepath = folderpath + '/' + filename
            dff, dff2 = imk_file(filepath)
            df_final = pd.concat([df_final, dff])
            df2_final = pd.concat([df2_final, dff2])

    df_final['Knot'] = np.arange(1, df_final.shape[0] + 1)
    df2_final['Knot'] = np.arange(1, df2_final.shape[0] + 1)

    # CREATE new folder if needed
    if not os.path.exists(folderpath + '/output'):
        os.makedirs(folderpath + '/output')

    # WRITE to excel
    writer = pd.ExcelWriter(folderpath + '/output/Manual_KnotData.xlsx')
    df_final.to_excel(writer, 'Multi_imgMan')
    df2_final.to_excel(writer, 'One_imgMan')
    writer.save()

    return (df_final, df2_final)


def imk_file(filepath):

    # IMPORT
    df = pd.read_table(filepath)

    # GET name
    tree_id = int(os.path.basename(filepath).split('-')[0])
    log_id = int(os.path.basename(filepath).split('-')[1])

    # CREATE new output_frames
    df_out = pd.DataFrame(columns=['Tree', 'Log', 'Knot', 'RadialPosition_mm', 'DiameterV_mm', 'DiameterH_mm',
                                     'MeanDiameter_mm', 'Zposition_mm', 'Sound_pos'])
    df2_out = pd.DataFrame(columns=['Tree', 'Log', 'Knot', 'DKB_mm', 'ke_mm', 'Azimuth_deg'])

    # TODO ITERATE over all groups of 4 rows until the blank line
    for index in range(0, df.shape[0] - df.shape[0] % 4, 4):

        # EXTRACT group
        dfg = df[index:index + 4]

        # PROCESS Group of 4
        dfg_out = imk_group(dfg, df)
        dfg2_out = imk_knot(dfg)

        # CONCAT output to dataframe
        df_out = pd.concat([df_out, dfg_out])
        df2_out = pd.concat([df2_out, dfg2_out])

    # SET tree and log variables
    df_out['Tree'] = tree_id
    df_out['Log'] = log_id
    df2_out['Tree'] = tree_id
    df2_out['Log'] = log_id

    # RETURN data frame
    return (df_out, df2_out)


def imk_group(dfg, df):

    # DROP columns where value in the second row is 0
    dfg = dfg[dfg[1] != 0]
    # dfg = dfg.dropna(axis=1)

    # CREATE output data frame
    dfg_out = pd.DataFrame(columns=['Tree', 'Log', 'Knot'])

    # CREATE rows
    dfg_out['RadialPosition_mm'] = list(range(20, dfg.shape[1] * 20 + 20, 20))
    dfg_out['DiameterV_mm'] = dfg.iloc[2, :]
    dfg_out['DiameterH_mm'] = dfg.iloc[1, :]
    dfg_out['MeanDiameter_mm'] = [np.mean([x, y]) for x, y in zip(dfg.iloc[2, :], dfg.iloc[1, :])]
    dfg_out['Zposition_mm'] = dfg.iloc[3, :] + dfg.iloc[0, 2]
    dfg_out['Sound_pos'] = [_ > df.iloc[0, 3] for _ in dfg_out['RadialPosition_mm']]

    return dfg_out


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
    df2_out['ke_mm'] = ke_mm

    df2_out['Azimuth_deg'] = dfg.iloc[0, 6]

    if dfg.iloc[0, 4] is -1:
        sound_knot = 1
    else:
        sound_knot = 0
    df2_out['sound_knot'] = sound_knot

    return df2_out
