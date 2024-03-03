import pandas as pd
import numpy as np
from collections import defaultdict
np.set_printoptions(threshold=np.inf)

def open_excel_sheet_as_df(filepath,keywords_for_sheet_names,header):
    # This function returns a pd dataframe of the excel sheet whose name is 
    # in the keywords_for_sheet_names.
    excel_file = pd.ExcelFile(filepath)
    sheet_names = excel_file.sheet_names
    for sheet_name in sheet_names:
        for keyword in keywords_for_sheet_names:
            if keyword.lower() in sheet_name.lower():
                return pd.read_excel(filepath,sheet_name=sheet_name,header=header)

def has_digits(inputString):
    return any(char.isdigit() for char in inputString)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_colname_from_keywords(df,keywords,banned_words=None):
    if banned_words is None: 
        banned_words = list()
    colnames = df.columns
    for colname in colnames:
        colname = str(colname)
        for keyword in keywords:
            if not has_digits(colname) and keyword.lower() in colname.lower():
                colname_allowed = True
                for banned_word in banned_words:
                    if banned_word.lower() in colname.lower():
                        colname_allowed = False
                        break
                if colname_allowed: return colname

excel_sheet_keywords = ["record 1", "mainstream", "England"]
dfs = dict()
old_ids = set()
all_ids = set()
for year in range(2000,2015):
    print(year)
    if 2000 <= year < 2010:
        header = 0 if year != 2009 else 1 # In 2009 there is a title in the first row, the columns are in the second row
        df = open_excel_sheet_as_df(f"school_performances/performances_{year}.xls", excel_sheet_keywords,header=header)
    elif year >= 2010:
        df = pd.read_csv(f"school_performances/performances_{year}.csv")    
    
    #print(np.array(df.columns))

    # We only want record 1 schools
    rec_column = get_colname_from_keywords(df,["rec"])
    record_1 = df[rec_column].isin([1])
    df = df[record_1]

    # We use LEA and establishment number together as an id for a school
    lea_column = get_colname_from_keywords(df,["lea","lacode"])
    establishment_number_column = get_colname_from_keywords(df,["est"])

    # these ids are unique (ie len(df) == len(unique(df["id"])) )
    df["id"] = [str(int(x))+str(int(y)) for x,y in zip(df[establishment_number_column],df[lea_column])] 
    
    new_ids = set(df['id'])
    print(f"Number of new schools: {len( new_ids.difference(old_ids))}.")
    print(f"Number of lost schools: {len(old_ids.difference(new_ids))}.")
    all_ids = all_ids.union(new_ids)
    old_ids = new_ids
    
    # We get town, postcode, school name and telephone numbers to verify that the school ids match between different years
    # We also get performance for those years. 
    town_column = get_colname_from_keywords(df,["town"])
    telephone_column = get_colname_from_keywords(df,["tel"])
    school_name_column = get_colname_from_keywords(df,["name"],["unnamed"])
    postcode_column = get_colname_from_keywords(df,["code"],["lacode","estabcode"])
    performance_column =  get_colname_from_keywords(df, ["aps","average point score"])
    school_type_column = get_colname_from_keywords(df,["typ"], ["record type","rectyp"] )
    #number_of_pupils_column = get_colname_from_keywords(df,[])

    df = df.rename(columns={
            town_column:"town",
            telephone_column:"telephone",
            school_name_column:"school_name",
            postcode_column: "postcode",
            performance_column: "performance",
            school_type_column: "school_type"
        })
    df = df[["id","school_name","school_type","postcode","town","telephone", "performance"]]
    df = df.sort_values(by=['id'])
    df.set_index('id', inplace=True)
    df.to_csv(f"clean_dfs/{year}.csv")
    df = df.rename(columns={colname: f"{colname}_{year}" for colname in df.columns})
    dfs[year] = df
    
print(f"Total number of ids is {len(all_ids)}.")

df_final = dfs[2000]
for year in range(2001,2015):
    df = dfs[year]
    df_final = pd.merge(df_final,df,on="id",how="outer")

df_final = df_final.reindex(sorted(df_final.columns), axis=1)
df_final.to_csv("combined_performances.csv")
    
# N = len(dfs)
# error_rate = defaultdict(lambda: np.zeros((N,N)))

# for i in range(N):
#     for j in range(i+1,N):
#         df_merged = pd.merge(dfs[2000+i], dfs[2000+j], on="id")
#         for colname in ["telephone","school_name","postcode","town"]:
#             error_rate[colname][i,j] = round(np.mean(df_merged[f"{colname}_x"] != df_merged[f"{colname}_y"]),4)

# for colname in ["telephone","school_name","postcode","town"]:
#     error_rate[colname] += np.transpose(error_rate[colname])
#     np.savetxt(f"{colname}.csv", error_rate[colname],  delimiter = ",")