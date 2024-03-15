import glob
import pandas as pd
from biom import Table, load_table
from qiime2 import Artifact
from assets.step_wise_anova import run_stepwise_anova
from skbio import OrdinationResults, TreeNode, DistanceMatrix

# Perform stepwise RDA-ANOVA
RDA_dict = {}
metadata_categories_to_test = ['run_prefix','sample_plate','plating','module','gmt','orientation']

#Load q2 artifacts
deblur_betadiv_no_controls_rarefied = Artifact.load('./data/katharo_deblur_gg2_feature_table_no_controls_rarefied.qza')
betadiv_ord_ = {}
for file in glob.glob('./data/*ordination.qza'):
    q2_artifact = Artifact.load(file)
    metric = file.replace('./data/','').replace('_ordination.qza','')
    betadiv_ord_.update({metric:q2_artifact})
    
# Clean up meta (only stuff to run)
keep_ = deblur_betadiv_no_controls_rarefied.view(pd.DataFrame).index
metadata_RDA = pd.read_csv('./metadata/2023_03_21_3DMM_metadata_to_update_qiita.txt',sep='\t')
metadata_RDA = metadata_RDA.set_index('#SampleID').reindex(keep_)

# Run stepwise ANOVA for all RDA ordinations
for metric_, ord_ in  betadiv_ord_.items():
    # get first three axes
    ord_ = ord_.view(OrdinationResults).samples[[0,1,2]]
    ord_.columns = ['PC1','PC2','PC3']
    # subset/match
    mf_ord_ = metadata_RDA.copy()
    shared_ids = list(set(ord_.index)\
                      & set(mf_ord_.index))
    mf_ord_ = mf_ord_.loc[shared_ids,:]
    ord_ = ord_.loc[shared_ids,:]
    RDA_dict[metric_] = run_stepwise_anova(ord_, mf_ord_, metadata_categories_to_test) #mf_ord_.columns)

# Concat output from all runs and export
RDA_results_df = pd.concat(RDA_dict, axis=0)
RDA_results_df.to_csv('./output/2024_rda_results_df.csv')