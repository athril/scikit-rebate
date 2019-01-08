solved_cols = [x for x in benchmark_data_merged.columns.values if 'Solved' in x]

import seaborn as sb
import numpy as np

for problem, problem_group in benchmark_data_merged.groupby('FilePath'):
    problem_group = problem_group.loc[problem_group['AlgorithmShort'].apply(
        lambda x: x not in ['MultiSURF*', 'FixedReliefFPercent20', 'FixedReliefFPercent30',
                            'FixedReliefFPercent38.2',
                            'ReliefF-NN10', 'ReliefF-NN100', 'ReliefF-NN200'])]

    problem_group['AlgorithmShort'] = problem_group['AlgorithmShort'].apply(
        lambda x: x.replace('ANOVAFValue', 'ANOVA F-value')
                   .replace('FixedMultiSURF', 'MultiSURF*') # FixedMultiSURF == MultiSURF*
                   .replace('Fixed', '').replace('chi2', 'Chi^2')
                   .replace('SURFstar', 'SURF*').replace('ReliefFPercent50', 'ReliefF 50% NN')
                   .replace('ReliefFPercent10', 'ReliefF 10% NN').replace('ReliefF-NN100', 'ReliefF 100 NN')
                   .replace('ReliefF-NN10', 'ReliefF 10 NN').replace('RFEExtraTrees', 'RFE ExtraTrees')
                   .replace('MutualInformation', 'Mutual Information'))
    
    algo_labels = ['Random Shuffle',
                   'Chi^2',
                   'ANOVA F-value',
                   'Mutual Information', 
                   'ExtraTrees',
                   'RFE ExtraTrees',
                   'ReliefF 10 NN',
                   'ReliefF 100 NN',
                   'ReliefF 10% NN',
                   'ReliefF 50% NN',
                   'SURF',
                   'SURF*',
                   'MultiSURF*',
                   'MultiSURF'][::-1]
    
    problem_group['AlgorithmShort'] = pd.Categorical(problem_group['AlgorithmShort'],
                                                     algo_labels)

    problem_group_avg = problem_group.groupby(
        'AlgorithmShort')[solved_cols].mean().sort_index(ascending=False)

    plt.figure(figsize=(13, 10))
    
    custom_cmap = sb.color_palette('Oranges', n_colors=1000)[:800] + sb.color_palette('Blues', n_colors=1000)[800:]
    sb.heatmap(data=problem_group_avg.values, vmin=0, vmax=1, cmap=custom_cmap)#'Blues')
    plt.yticks(np.array(range(len(problem_group_avg))) + 0.5, algo_labels[::-1], rotation=0)
    plt.xticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 90],
               ['Optimal', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%'], rotation=0)
    plt.xlabel('Predictive features in top % of ranked features')
    plt.title('\n'.join(problem.split('Archive/')[-1].split('/')).replace('_', ' '))
    
    plt.savefig('figures/' + problem.split('Archive/')[-1].replace('/', '_') + '.pdf', bbox_inches='tight')
    plt.savefig('figures/' + problem.split('Archive/')[-1].replace('/', '_') + '.eps', bbox_inches='tight')