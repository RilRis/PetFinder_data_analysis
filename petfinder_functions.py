import pandas as pd

#define function to identify top two breeds in a dataset
def top_breeds(dataframe, ignore_mixed=True):
    breedlist = []
    for i in dataframe['breeds']:
        breedlist.extend(i)
    #now that we have a flat list of breeds, create a frequency table containing the breed names as the index (in order of most to least frequent) and count as the value
    breed_freq = pd.DataFrame([pd.Series(breedlist).value_counts()]).T
    #ignore 'Mixed Breed' unless otherwise speficied, since it is an odd category that is sort of arbitrary    
    if ignore_mixed is True: 
        ##check if 'Mixed Breed' is in the data before deleting it
        if 'Mixed Breed' in breed_freq.index:
            breed_freq = breed_freq.drop(index=('Mixed Breed'))
    #find top two breeds, accounting for ties in 1st or 2nd place
    ##identify the top unique values, then fetch the breeds associated with them
    sortvals = list(breed_freq['count'].sort_values(ascending=False).drop_duplicates())

    ##if you only had 'Mixed Breed', then sortvals will be an empty list and an error will result. Deal with that using this:
    if len(sortvals) == 0:
        num1breed = 'breeds unspecified'
        num2breed = 'breeds unspecified'
    ##if there is no number 1 or number 2 breed because all breeds have the same count, write 'N/A'
    ###if all have same count, there will be only 1 unique value in the counts column 
    elif len(breed_freq['count'].unique()) == 1:
        num1breed = 'n/a'
        num2breed = 'n/a'
    ##otherwise...
    else:
        num1breed = list(breed_freq.index[breed_freq['count']==sortvals[0]])
    #if len(sortvals) > 1:
        num2breed = list(breed_freq.index[breed_freq['count']==sortvals[1]])
    return{'first': num1breed,
           'second': num2breed}

#define function to create a table (with each state as a row) showing data about the dogs from that state
##ARGUMENTS:
###dataframe: the 
def state_analysis(dataframe, total_row=True, ignore_mixed=True):
    #collect every unique state ID in a list
    states = list(dataframe['state'].sort_values().unique())

    #create empty list to put the data for each row into 
    for_df = []
    
    #for each state in the dataset...
    for state in states:
        #filter the df to get just the entries for that state
        tempdf = dataframe[dataframe['state']==state]
        
        #count the number of entries
        count = len(tempdf)
        
        #determine most common breeds using top_breeds function, which returns a dictionary with the first/second most popular breeds
        top2breeds = top_breeds(dataframe=tempdf, ignore_mixed=ignore_mixed)
    
        #determine most common male name
        m_name_des = (tempdf
                      .query('gender == "Male"')
                      .name
                      .describe())
        if m_name_des['freq'] > 1:
            m_name = m_name_des['top']
        else:
            m_name = 'N/A'
        
        #determine most common female name
        f_name_des = (tempdf
                      .query('gender == "Female"')
                      .name
                      .describe())
        if f_name_des['freq'] > 1:
            f_name = f_name_des['top']
        else: 
            f_name = 'N/A'
        
        rowdata = [state, count, top2breeds['first'], top2breeds['second'], f_name, m_name]
        for_df.append(rowdata)
    #if total_row parameter is set to 'True', repeat everything you did per state on the whole dataset
    if total_row is True:
        count = len(dataframe)
        top2breeds = top_breeds(dataframe=dataframe, ignore_mixed=ignore_mixed)
        m_name_des = (dataframe
                      .query('gender == "Male"')
                      .name
                      .describe())
        if m_name_des['freq'] > 1:
            m_name = m_name_des['top']
        else:
            m_name = 'N/A'

        f_name_des = (dataframe
                      .query('gender == "Female"')
                      .name
                      .describe())
        if f_name_des['freq'] > 1:
            f_name = f_name_des['top']
        else: 
            f_name = 'N/A'
        rowdata = ['Total', count, top2breeds['first'], top2breeds['second'], f_name, m_name]
        for_df.append(rowdata)
        final_df = pd.DataFrame(for_df)
        final_df.columns = ['state', 'count', 'top_breed', 'runner_up', 'top_f_name', 'top_m_name']
    return(final_df)

