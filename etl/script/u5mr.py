# -*- coding: utf-8 -*-

import pandas as pd
import os
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file

# configure file path
source = '../source/gapdata005 v7.xlsx'
out_dir = '../../'


if __name__ == '__main__':
    data001 = pd.read_excel(source, sheetname='Data & sources by observation')

    # entities
    area = data001['Country'].unique()
    area_id = list(map(to_concept_id, area))

    ent = pd.DataFrame([], columns=['country', 'name'])
    ent['country'] = area_id
    ent['name'] = area

    path = os.path.join(out_dir, 'ddf--entities--country.csv')
    ent.to_csv(path, index=False)

    # datapoints
    data001_dp = data001[['Country', 'Year', 'Under five mortality']].copy()
    data001_dp.columns = ['country', 'year', 'under_five_mortality']
    data001_dp['country'] = data001_dp['country'].map(to_concept_id)

    path = os.path.join(out_dir, 'ddf--datapoints--under_five_mortality--by--country--year.csv')
    data001_dp.dropna().sort_values(by=['country', 'year']).to_csv(path, index=False)

    # concepts
    conc = ['under_five_mortality', 'country', 'year', 'name']
    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])
    cdf['concept'] = conc
    cdf['name'] = ['Under five mortality', 'Country', 'Year', 'Name']
    cdf['concept_type'] = ['measure', 'entity_domain', 'time', 'string']

    path = os.path.join(out_dir, 'ddf--concepts.csv')
    cdf.to_csv(path, index=False)

    # index
    create_index_file(out_dir)

    print('Done.')
