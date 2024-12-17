import os.path
import glob
import pandas as pd
from biom import Table, load_table
import time

import warnings

from qiime2 import Artifact
from qiime2 import Metadata

from skbio import OrdinationResults, TreeNode, DistanceMatrix
from qiime2.plugins.gemelli.actions import (rpca,phylogenetic_rpca_without_taxonomy,phylogenetic_rpca_with_taxonomy)
import numpy as np
from q2_diversity._procrustes import procrustes_analysis

from skbio.stats.distance import permanova, bioenv
import skbio
import bp
from q2_types.tree import NewickFormat

meta_ft = Artifact.load('./data/16S_feature-table-with-10689.gg2-2022.10.min1000.biom.qza')
og_bp = Artifact.load('./data/phyloRPCA-with-10689/biplot.qza')
og_tax = Artifact.load('./data/phyloRPCA-with-10689/t2t_taxonomy.qza')
og_cbn = Artifact.load('./data/phyloRPCA-with-10689/counts_by_node.qza')
og_cbnt = Artifact.load('./data/phyloRPCA-with-10689/counts_by_node_tree.qza')
og_dm = Artifact.load('./data/phyloRPCA-with-10689/distance_matrix.qza')

parsed_tree = bp.parse_newick(open('./data/2022.10.phylogeny.id.nwk').read())
taxonomy = Artifact.load('./data/16S_feature-table-with-10689.gg2-2022.10.taxonomy.qza')

og_dm = og_dm.view(DistanceMatrix)
meta_ft_biom = meta_ft.view(Table)

n_samples = len(meta_ft_biom.ids())
results = []
dim = 3
start = time.time()
for min_depth in np.arange(1000, 10001, 1000):
    cur = time.time() - start
    print(f"delta (seconds)={cur:0.3}; min_depth={min_depth}", flush=True)
    start = time.time()
    for min_prev in np.arange(0.01, 0.101, 0.01):
        print(f"min_prev={min_prev}", flush=True)
        tab = meta_ft_biom.filter(lambda v, i, m: ((v > 0).sum() / n_samples) > min_prev, axis='observation', inplace=False)
        tab = tab.filter(lambda v, i, m: v.sum() >= min_depth, inplace=False).remove_empty()
        sheared_tree = parsed_tree.shear(set(tab.ids(axis='observation'))).collapse()
        tree_ar = Artifact.import_data('Phylogeny[Rooted]', bp.to_skbio_treenode(sheared_tree))
        bplot, dm, cbnt, cbn, tax = phylogenetic_rpca_with_taxonomy(Artifact.import_data('FeatureTable[Frequency]',
                                                                                      tab),
                                                                 phylogeny=tree_ar,
                                                                 taxonomy=Metadata(taxonomy.view(pd.DataFrame)))
        dm = dm.view(DistanceMatrix)
        common_ids = sorted(set(dm.ids) & set(og_dm.ids))
        dm_common = dm.filter(common_ids)
        original_dm_common = og_dm.filter(common_ids)
        mantel_r, mantel_p, n_ = skbio.stats.distance.mantel(dm_common, original_dm_common, permutations=0)
        pc_common = skbio.stats.ordination.pcoa(dm_common, number_of_dimensions=dim)
        pc_original_common = skbio.stats.ordination.pcoa(original_dm_common, number_of_dimensions=dim)
        _, _, procrustes_results = procrustes_analysis(pc_common, pc_original_common, dimensions=dim, permutations=0)
        results.append((len(common_ids), mantel_r, procrustes_results.iloc[0]['true M^2 value'], min_depth, min_prev))

results = pd.DataFrame(results, columns=['n_samples', 'mantel_r', 'procrustes_m2', 'depth', 'prev'])
results.to_csv('./output/meta_beta_robustness.csv')