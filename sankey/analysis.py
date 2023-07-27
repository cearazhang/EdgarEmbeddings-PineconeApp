import pandas as pd
import sankey as sk


def main():
    bio = pd.read_csv('data/bio.csv')
    sk.make_sankey(bio, 'organ', 'gene', 'npub')

    bike = pd.read_csv('data/Bikeshare.csv')

    brain = pd.read_csv('data/BrainCancer.csv').dropna()
    brain_male = brain[brain.sex == 'Male']
    brain_female = brain[brain.sex == 'Female']
    brain['sex_loc'] = brain['sex'] + '_' + brain['loc']

if __name__ == '__main__':


"""
in console for bike data

bike.groupby(['mnth', 'weathersit',])['bikers'].sum().reset_index()
return heiarchy of group bys: month, then types of weather, then total number of riders

in analysis under
bike = pd.read_csv(..)
bike.groupby(['mnth', 'weathersit',])['bikers'].sum().reset_index()

"""