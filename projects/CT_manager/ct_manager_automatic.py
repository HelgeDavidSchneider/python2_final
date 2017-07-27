import pandas as pd
import numpy as np
import os
from math import tan, log, pi


# Final
def ako_folder(folderpath):
    """
    ako_folder iterates over all knot files given in folderpath
    for every file it calculates the two wanted output frames and adds them to
    the final output
    the output database is then written to an excel file
    """

    # CREATE output data frames
    df_final = pd.DataFrame(columns=['Tree', 'Log', 'Knot'])
    df2_final = pd.DataFrame(columns=['Tree', 'Log', 'Knot'])
    knot_table = pd.DataFrame(columns=['file', 'Knots in total',
                                       'Excluded knots', 'Remaining knots',
                                       'Percentage of usable knots'])
    df_index = 0

    # ITERATE over all knot files in the folderpath
    for filename in os.listdir(folderpath):
        if 'knotsParametric' in filename:

            filepath = folderpath + '/' + filename
            # Database 1
            dff, knot_tablef = ako_multi(filepath, df_index)
            df_index += 1

            # Database 2
            dff2 = ako_one(filepath)

            # ADD frames to the final output
            df_final = pd.concat([df_final, dff])
            df2_final = pd.concat([df2_final, dff2])
            knot_table = pd.concat([knot_table, knot_tablef])

    # PROCESS output frames
    df2_final['Knot'] = np.arange(1, df2_final.shape[0] + 1)

    # convert True/False to 0/1
    df_final.Heartwood_point = df_final.Heartwood_point.astype(int)
    df_final.Sound_pos = df_final.Sound_pos.astype(int)
    df2_final.Sound_knot = df2_final.Sound_knot.astype(int)

    # round values by 2 digits
    df_final = df_final.round(2)
    df2_final = df2_final.round(2)

    # sort the columns
    df_final = df_final[['Tree', 'Log', 'Knot', 'RadialPosition_mm',
                         'Diameter_mm', 'Zposition_mm',
                             'Azimuth_deg', 'Sound_pos', 'HSlimit_mm',
                         'WBlimit_mm', 'Outlimit_mm', 'Heartwood_point']]
    df2_final = df2_final[['Tree', 'Log', 'Knot', 'Azimuth_deg', 'KE_mm',
                           'DKB_mm', 'Sound_knot', 'C_mm', 'HSlimit_mm',
                           'WBlimit_mm', 'Outlimit_mm']]

    # CREATE new folder if needed
    if not os.path.exists(folderpath + '/output'):
        os.makedirs(folderpath + '/output')

    # WRITE to excel
    writer = pd.ExcelWriter(folderpath + '/output/CT_KnotData.xlsx')
    df_final.to_excel(writer, 'Multi_CT')
    df2_final.to_excel(writer, 'One_CT')
    knot_table.to_excel(writer, 'Knot Table')
    writer.save()

    return df_final, df2_final, knot_table


# Multi_CT
def ako_multi(filepath, df_index):
    """
    ako_multi creates returns the multi database for a single knot file
    first it creates a table with information about the used knots
    afterwards it iterates over the rows of the given file and calculates
    the wanted information
    """

    # IMPORT file
    df = pd.read_csv(filepath, delimiter=';', header=None)
    tree_id = os.path.basename(filepath).split('_')[1]
    log_id = os.path.basename(filepath).split('_')[2]

    # PROCESS rows
    total = df.shape[0]
    df = df[df.iloc[:, 4] != 0]
    df = df[df.iloc[:, 5] != 0]
    df = df[df.iloc[:, 6] != 0]

    remaining = df.shape[0]
    excluded = total - remaining
    percentage = remaining / total * 100

    # CREATE table
    knot_table = pd.DataFrame({'file': os.path.basename(filepath),
                               'Knots in total': total,
                               'Excluded knots': excluded,
                               'Remaining knots': remaining,
                               'Percentage of usable knots': percentage},
                              index=[df_index])

    # CREATE output
    df_out = pd.DataFrame(columns=['Tree', 'Log', 'Knot'])

    # ITERATE over all rows
    knot = 1
    for row in range(0, df.shape[0]):
        dfr_out = ako_row(df.iloc[row, :])
        dfr_out['Knot'] = knot
        knot += 1
        df_out = pd.concat([df_out, dfr_out])

    # PROCESS output
    df_out['Tree'] = tree_id
    df_out['Log'] = log_id

    # GET polar values
    df_out = ako_combine(filepath, df_out, tree_id, log_id)

    df_out['Heartwood_point'] = df_out.RadialPosition_mm > df_out.HSlimit_mm

    return df_out, knot_table


def ako_row(dfr):
    """
    ako_row calculates the wanted variables of a knot file for a single row
    """

    dfr_out = pd.DataFrame({'RadialPosition_mm':
                                list(np.arange(20, dfr.iloc[7], 20))})
    dfr_out['Diameter_mm'] = [abs(tan((dfr[0] + (dfr[1] * R ** 0.25))) * 2 * R)
                              for R in dfr_out.RadialPosition_mm]
    dfr_out['Zposition_mm'] = [dfr[4] + (dfr[5] * R ** 0.5 + dfr[6] * R)
                               for R in dfr_out.RadialPosition_mm]
    dfr_out['Azimuth_deg'] = [((dfr[2] + dfr[3] * log(R)) * 360) / (2 * pi)
                              for R in dfr_out.RadialPosition_mm]
    dfr_out['Sound_pos'] = dfr_out.RadialPosition_mm < dfr[8]

    return dfr_out


def ako_combine(filepath, df_out, tree_id, log_id):
    """
    ako_combine extracts all the information for the output of ako_multi
    """

    for filename in os.listdir(os.path.dirname(filepath)):

        if 'sapPolar' in filename \
                and filename.split('_')[1] == '%s' % tree_id \
                and filename.split('_')[2] == '%s' % log_id:
            sappath = os.path.dirname(filepath) + '/' + filename
            df_sap = pd.read_csv(sappath, delimiter=',', header=None)

        if 'barkPolar' in filename \
                and filename.split('_')[1] == '%s' % tree_id \
                and filename.split('_')[2] == '%s' % log_id:
            barkpath = os.path.dirname(filepath) + '/' + filename
            df_bark = pd.read_csv(barkpath, delimiter=',', header=None)

        if 'borderPolar' in filename \
                and filename.split('_')[1] == '%s' % tree_id \
                and filename.split('_')[2] == '%s' % log_id:
            borderpath = os.path.dirname(filepath) + '/' + filename
            df_border = pd.read_csv(borderpath, delimiter=',', header=None)

    # would've been better with list comprehension
    HSlimit_mm = []
    WBlimit_mm = []
    Outlimit_mm = []

    for i in range(0, df_out.shape[0]):
        row = int(round(df_out.Zposition_mm.iloc[i] / 5))
        column = int(round(df_out.Azimuth_deg.iloc[i]))
        if column >= 360:
            column -= 360
        try:
            HSlimit_mm.append(df_sap.iloc[row, column])
            WBlimit_mm.append(df_bark.iloc[row, column])
            Outlimit_mm.append(df_border.iloc[row, column])
        except IndexError:
            HSlimit_mm.append(0)
            WBlimit_mm.append(0)
            Outlimit_mm.append(0)

    df_out['HSlimit_mm'] = HSlimit_mm
    df_out['WBlimit_mm'] = WBlimit_mm
    df_out['Outlimit_mm'] = Outlimit_mm

    return df_out


# One_CT
def ako_one(filepath):

    """
    ako_one creates the database for the One_Ct
    """
    # IMPORT file
    df = pd.read_csv(filepath, delimiter=';', header=None)
    tree_id = os.path.basename(filepath).split('_')[1]
    log_id = os.path.basename(filepath).split('_')[2]

    # CREATE output frame
    df_out = pd.DataFrame(columns=['Tree', 'Log', 'Knot'])

    # ITERATE over the rows
    for row in range(0, df.shape[0]):
        dfr_out = ako_one_row(df.iloc[row, :])
        dfr_out['C_mm'] = df.iloc[0, 4]
        df_out = pd.concat([df_out, dfr_out])

    # GET polar values
    df_out = ako_one_combine(df_out, filepath, tree_id, log_id)

    # PROCESS
    df_out['Tree'] = tree_id
    df_out['Log'] = log_id

    return df_out


def ako_one_row(dfr):

    dfr_out = pd.DataFrame({'Azimuth_deg': [((dfr[2] + dfr[3]
                                             * log(abs(dfr.iloc[7] + 0.001)))
                                             * 360) / (2 * pi)]})
    dfr_out['RadialPosition_mm'] = dfr.iloc[7]
    dfr_out['DKB_mm'] = dfr[8]
    dfr_out['KE_mm'] = dfr[7]
    dfr_out['Sound_knot'] = dfr_out.KE_mm < dfr_out.DKB_mm

    return dfr_out


def ako_one_combine(df_out, filepath, tree_id, log_id):

    for filename in os.listdir(os.path.dirname(filepath)):

        if 'sapPolar' in filename \
                and filename.split('_')[1] == '%s' % tree_id \
                and filename.split('_')[2] == '%s' % log_id:
            sappath = os.path.dirname(filepath) + '/' + filename
            df_sap = pd.read_csv(sappath, delimiter=',', header=None)

        if 'barkPolar' in filename \
                and filename.split('_')[1] == '%s' % tree_id \
                and filename.split('_')[2] == '%s' % log_id:
            barkpath = os.path.dirname(filepath) + '/' + filename
            df_bark = pd.read_csv(barkpath, delimiter=',', header=None)

        if 'borderPolar' in filename \
                and filename.split('_')[1] == '%s' % tree_id \
                and filename.split('_')[2] == '%s' % log_id:
            borderpath = os.path.dirname(filepath) + '/' + filename
            df_border = pd.read_csv(borderpath, delimiter=',', header=None)

    HSlimit_mm = []
    WBlimit_mm = []
    Outlimit_mm = []

    for i in range(0, df_out.shape[0]):
        row = int(round(df_out.RadialPosition_mm.iloc[i] / 5))
        column = int(round(df_out.Azimuth_deg.iloc[i]))
        if column >= 360:
            column -= 360
        try:
            HSlimit_mm.append(df_sap.iloc[row, column])
            WBlimit_mm.append(df_bark.iloc[row, column])
            Outlimit_mm.append(df_border.iloc[row, column])
        except IndexError:
            HSlimit_mm.append(0)
            WBlimit_mm.append(0)
            Outlimit_mm.append(0)

    df_out['HSlimit_mm'] = HSlimit_mm
    df_out['WBlimit_mm'] = WBlimit_mm
    df_out['Outlimit_mm'] = Outlimit_mm

    return df_out

if __name__ == '__main__':
    # Test
    folderpath = "C:/Users/helge/Dropbox/Uni/Python 2/python2_final/projects" \
                 "/CT_manager/Data_Part_2"
    filepath = folderpath + '/knotsParametric@Dgl_623_1_2015_05_20.csv'
    df1, df2, knot_table = ako_folder(folderpath)

