import qiime2
from skbio import DistanceMatrix
import pandas as pd

fp = './data/phylo_rpca_distance_matrix.qza'

metadata = qiime2.Metadata.load('./metadata/2023_03_21_3DMM_metadata_to_update_qiita.txt')
metadata_df = metadata.to_dataframe()

dm = qiime2.Artifact.load(fp).view(DistanceMatrix)

results = pd.DataFrame([])

metadata_df_f=metadata_df.reindex(dm.ids)
for from_group in metadata_df_f['module'].unique():
    from_ = metadata_df_f.loc[metadata_df_f['module']==from_group].index
    for to_group in metadata_df['module'].unique():
        to_ = metadata_df_f.loc[metadata_df_f['module']==to_group].index
        o_ = dm.between(from_,to_,allow_overlap=True)
        o_['metric']='phylo_RPCA'
        o_['from'] = from_group
        o_['to'] = to_group
        results = pd.concat([results,o_])

results.to_csv('./output/module_distances.csv')