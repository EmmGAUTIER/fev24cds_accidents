#!/usr/bin/python3

import sys
import json
import numpy as np
import pandas as pd
from tabulate import tabulate
import argparse

def premier_rapport(csvfile,
                    sep=',',
                    encoding="utf-8",
                    max_list_len=10,
                    index=None,
                    target=None,
                    csv_desc_name=None,
                    outfile=None):
    """
    premier_rapport : 
    """
    # File informations retreived from DataFrame and description file
    csv_desc = {}

    if type(csvfile) == "str":
        print("File name          : ", csvfile, file = outfile)

    if csv_desc_name != None:
        try :
            with open(csv_desc_name, 'r', encoding='utf-8') as fichier:
                csv_desc = json.load(fichier)
        except FileNotFoundError :
            # File not found, usually after first reading to write json file
            pass
    if csv_desc.get("columns") == None:
        csv_desc["columns"] = []
    cols_desc = csv_desc["columns"]
    #print ("===> Colonnes :", csv_desc["columns"], file = outfile)
    #print ("===> Colonnes :", type(csv_desc["columns"]), file = outfile)

    # read_csv emit a warning if it finds mixed type in a column
    # so giving a dictionnary of types helps it.
    forced_dtypes = {}
    for col in cols_desc:
        forced_dtypes[col["name"]] = col["dtype"]

    if isinstance(csvfile, str):
        df = pd.read_csv(csvfile, sep=sep, encoding=encoding, engine='c', dtype=forced_dtypes)
    else:
        df = csvfile

    tablefmt = "psql"  # option de formattage pour tabulate

    nb_rows, nb_cols = df.shape
    cells_nb = nb_rows * nb_cols
    csv_desc["nb_rows"] = nb_rows
    csv_desc["nb_cols"] = nb_cols

    nb_dec = int(np.log10(nb_rows)) + 1
    fmt_int = "{:" + str(nb_dec) + "d}"
    fmt_pc = "{:" + str(nb_dec + 2) + "." + str(nb_dec - 2) + "f}"
    # print("format nombre      : ", fmt_int)  # for debugging purpose only
    # print("format pourcentage : ", fmt_pc)   # for debugging purpose only

    print("Rows number    : ", fmt_int.format(nb_rows), file = outfile)
    print("Columns number : ", fmt_int.format(nb_cols), file = outfile)
    print("Cells          : ", cells_nb, file = outfile)

    print(file = outfile)

    ######################################################################
    # Display info of csv_desc : name, type, number of na and ratio of na
    ######################################################################
    headers = ("Feature", "Type", "Na", "ratio(%)")
    lines = []
    lines2 = []
    max_name_width = 0
    total_nb_na = 0

    #for col in df.columns:
    #    name_width = len(col)
    #    if name_width > max_name_width:
    #        max_name_width = name_width
    #    nb_na = df[col].isnull().sum()
    #    total_nb_na += nb_na
    #    lines.append([col, df.dtypes[col], nb_na, 100. * nb_na / nb_rows])

    line_num = 1
    for col in df.columns:
        nb_na = df[col].isnull().sum()
        pc_s = "" if nb_na == 0 else fmt_pc.format(100. * nb_na / nb_rows)
        lines2.append([line_num, col, df.dtypes[col], fmt_int.format(nb_na), pc_s])
        line_num += 1

    print(tabulate(lines2,
                   headers=["#", "Column", "Type", "Nulls", "Prop (%)"],
                   colalign=("left", "left", "left", "right", "right"),
                   tablefmt=tablefmt),
                   file = outfile)

    ######################################################################
    # Display stats of values of each column :
    # describe(), value_counts, values according to type of column and 
    # values.
    ######################################################################
    icol = 0
    for col in df.columns:
        nb_null = int(df[col].isnull().sum())
        typecol = str(df.dtypes.iloc[icol])

        col_desc = None
        idxcol_desc = 0
        while idxcol_desc < len(cols_desc) and col_desc == None:
            c = cols_desc[idxcol_desc]
            nom = c.get("name")
            if c.get("name") == col:
                col_desc = c
            else:
                idxcol_desc += 1

        if col_desc == None:
            col_desc = {}
            col_desc["name"] = col

        col_desc["dtype"] = typecol
        col_desc["index"] = icol

        print(file = outfile)
        print("====================================================================", file = outfile)
        print(file = outfile)
        column_name = col
        zzz  = col_desc.get("label")
        if col_desc.get("label") is not None:
            column_name += " :  " + col_desc.get("label")
        print("  " + column_name, file = outfile)
        if col_desc.get("description") is not None:
            print(col_desc.get("description"), file = outfile)
        print(file = outfile)
        print("Type        : ", df.dtypes[col], file = outfile)
        print("nulls       : {:d}".format(nb_null), file = outfile)
        print("Proportion  : ", 100. * nb_null / nb_rows, "%", file = outfile)
        print(file = outfile)

        if typecol == 'float64' or typecol == 'int64':
            print(tabulate(pd.DataFrame(df[col].describe()),
                           headers=["stat", "Value"],
                           tablefmt=tablefmt),
                           file = outfile)

        if typecol == 'bool':
            true_nb = df[col].sum()
            false_nb = (df[col] == False).sum()
            null_nb = df[col].isnull().sum()
            lines = [["True", true_nb, 100. * true_nb / nb_rows], ["False", false_nb, 100. * false_nb / nb_rows],
                     ["Null", null_nb, 100. * null_nb / nb_rows]]
            print(tabulate(lines,
                           headerFalses=["Values", "Count", "Prop (%)"],
                           tablefmt=tablefmt),
                           file = outfile)

        if typecol in ['object', 'int64', 'int32']:
            print("Nombre de valeurs uniques  : ", df.shape[0] - df[col].duplicated().sum(), file = outfile)
            print("Nombre de valeurs répétées : ", df[col].duplicated().sum(), file = outfile)

            values_dict = None
            values_dict = col_desc.get("values")
            value_counts = pd.DataFrame(df[col].value_counts())

            lines = []
            cumul = 0
            nb_lines = value_counts.shape[0]
            if nb_lines > max_list_len :
                nb_lines = max_list_len

            for i in range(nb_lines):
                mod_val = value_counts.index[i]
                mod_label = None
                if values_dict != None:
                    pass
                    mod_label = values_dict.get(str(mod_val))
                    pass
                if mod_label == None:
                    mod_label = ""
                mod_nb = int(value_counts.values[i])
                cumul += mod_nb
                mod_pc = 100. * mod_nb / nb_rows
                lines.append((mod_val, mod_label, mod_nb, mod_pc))
                pass
            if nb_lines < value_counts.shape[0]:
                nb_others_modalities = value_counts.shape[0]-nb_lines
                nb_others_sum = nb_rows - (nb_null + cumul)
                lines.append((f"Others ({nb_others_modalities} modalities)", "", nb_others_sum, mod_pc))
            pass

            print(tabulate(lines,
                           headers=["Modalities", "", "Count", "Prop (%)"],
                           tablefmt=tablefmt),
                           file = outfile)

            if values_dict != None:
                value_counts["labels"] = value_counts.index
                value_counts["labels"] = value_counts["labels"].replace(values_dict)
                pass


            #if values_desc != None:
            #    for val in values_desc :
            #        v = val
            #        pass

            cumul_nb = 0
            value_counts = pd.DataFrame(df[col].value_counts(), columns = ["value", "count"]).head(max_list_len)
            value_counts = pd.DataFrame(df[col].value_counts()).head(max_list_len)
            #u = value_counts.columns
            #print ("columns :", file = outfile)
            #print (value_counts.columns, file = outfile)
            value_counts["labels"] = value_counts.index
            u = value_counts
            #print (value_counts, file = outfile)
            cumul_nb = 0
            value_counts = pd.DataFrame(df[col].value_counts())
            categories_nb = value_counts.shape[0]

            if categories_nb <= max_list_len: # target
                lines_nb = categories_nb
            else:  # List has to be truncated
                lines_nb = max_list_len
                value_counts = value_counts.head(lines_nb)

            lines = []
            for i in range(lines_nb):
                mod_nb = int(value_counts.values[i])
                lines.append([value_counts.index[i], mod_nb, fmt_pc.format(100. * mod_nb / nb_rows)])
                cumul_nb += mod_nb

            if lines_nb < categories_nb:  # display others when list is truncated
                others_nb = nb_rows - (nb_null + cumul_nb)
                lines.append([f"Others, {categories_nb - lines_nb} modalitie(s)", others_nb,
                          fmt_pc.format(100. * others_nb / nb_rows)])

            if nb_null > 0:
                lines.append(["Nulls", nb_null, fmt_pc.format(100. * nb_null / nb_rows)])

        if idxcol_desc >= len (cols_desc):
            cols_desc.append(col_desc)
        else:
            cols_desc[idxcol_desc] = col_desc

        icol += 1
        print(file = outfile)
    pass
    ######################################################################
    #  Duplicates search
    #  Search and counting is done with duplicated().sum()
    #  Search is done in the DataFrame and DataFrame with ech column droped
    ######################################################################


    print("=====================================", file = outfile)
    print(file = outfile)
    print("Duplicated search", file = outfile)
    print("With all csv_desc : ", df[df.duplicated()].shape[0], file = outfile)

    if index != None:
        indexes = index.split(",")
        df1 = df.drop(indexes, axis=1)
        print("Without index(es) : ", df1[df1.duplicated()].shape[0], file = outfile)
    else:
        df1 = df

    print(file = outfile)
    # En comptant les doublons en supprimmant chaque colonne
    lines = []
    if index != None:
        indexes = index.split(",")
        df1 = df.drop(indexes, axis=1)
    else:
        indexes = []
        df1 = df

    for col in df1.columns:
        df2 = df1.drop(col, axis=1)
        lines.append([col, str(df2.duplicated().sum())])
    print(tabulate(lines, headers=["Without", "duplicated"]), file = outfile)

    print("=====================================", file = outfile)
    print(file = outfile)
    print("Correlations", file = outfile)
    print(file = outfile)
    corr = df.corr(numeric_only=True)
    print(tabulate(corr, headers=corr.columns), file = outfile)


    if csv_desc_name != None:
        try :
            with open(csv_desc_name, 'w', encoding='utf-8') as fichier:
                json.dump(csv_desc, fichier, ensure_ascii = True, indent=True)
                pass
        except RuntimeError:
            print ("Erreur lors de l'enregistrement des résultats", file = outfile)
            pass
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='premier_rapport: statistiques exploratoires pour aborder un jeu de données.')
    parser.add_argument('filename')  # positional argument
    parser.add_argument('-s', '--sep', default=',')  # option that takes a value
    parser.add_argument('--target', default=None)
    parser.add_argument('--index', default=None)
    parser.add_argument('--max_list_len', default=10)
    parser.add_argument('--encoding', default='utf-8')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--csv_desc', default=None)
    args = vars(parser.parse_args())

    filename = args["filename"]
    sep = args["sep"]
    encoding = args["encoding"]
    max_list_len = int(args["max_list_len"])
    index = args["index"]
    target = args["target"]
    csv_desc = args["csv_desc"]

    print("---->", args["index"])

    premier_rapport(filename,
                    sep=sep,
                    encoding=encoding,
                    max_list_len=max_list_len,
                    index=index,
                    target=target,
                    csv_desc_name=csv_desc)

    sys.exit()
