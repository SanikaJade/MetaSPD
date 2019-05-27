import pandas as pd
from graph_matcher import *
from gspan_parser import *

if __name__ == "__main__":
    pirated_directory = '.\\data\\MySQL\\folds\\pirated'
    innocent_directory = '.\\data\\MySQL\\folds\\innocent'
    experiment_directory = '.\\experiment\\MySQL'
    obfuscation_levels = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300', '400']

    for level in obfuscation_levels:
        for fold in range(1, 11):
            innocent_subgraphs_path = os.path.join(innocent_directory, str(fold), 'subgraph_set.txt')
            innocent_subgraphs = parse_mined_gspan_file(innocent_subgraphs_path, 'Innocent')
            pirated_subgraphs_path = os.path.join(pirated_directory, level, str(fold), 'subgraph_set.txt')
            pirated_subgraphs = parse_mined_gspan_file(pirated_subgraphs_path, 'Pirated')

            # select top 1000 subgraphs with fewest vertex count(2,3,4,...)
            all_subgraphs = pirated_subgraphs + innocent_subgraphs
            features = []
            if len(all_subgraphs) > 1000:
                # due to low count of innocent subgraphs, these features have been added prior to the pirated subgraphs
                features.extend(innocent_subgraphs)
                counter = 2
                while len(features) < 1000:
                    for i in range(0, len(pirated_subgraphs)):
                        if pirated_subgraphs[i].number_of_nodes() == counter:
                            features.append(pirated_subgraphs[i])
                            if len(features) == 1000:
                                break
                    counter += 1
            else:
                features = all_subgraphs

            # create train vector set
            pirated_vector_count = count_graphs(os.path.join(pirated_directory, level, str(fold), 'train_set.txt'))
            innocent_vector_count = count_graphs(os.path.join(innocent_directory, str(fold), 'train_set.txt'))
            train_vector_set = pd.DataFrame()
            for vector in range(0, pirated_vector_count):
                print('Training Set => Obfuscation Level %s Vector %s' % (level, vector))
                train_vector_set.loc[vector, 'Label'] = 'Pirated'
                for feature in features:
                    if str(vector) in feature.graph['parents'] and feature.graph['label'] == 'Pirated':
                        train_vector_set.loc[vector, id(feature)] = 1
                    else:
                        train_vector_set.loc[vector, id(feature)] = 0
            for vector in range(0, innocent_vector_count):
                print('Training Set => Obfuscation Level %s Vector %s' % (level, pirated_vector_count + vector))
                train_vector_set.loc[vector + pirated_vector_count, 'Label'] = 'Innocent'
                for feature in features:
                    if str(vector) in feature.graph['parents'] and feature.graph['label'] == 'Innocent':
                        train_vector_set.loc[vector + pirated_vector_count, id(feature)] = 1
                    else:
                        train_vector_set.loc[vector + pirated_vector_count, id(feature)] = 0
            train_set_path = os.path.join(experiment_directory, level, str(fold), 'train_set.csv')

            # create directory if doesn't exist
            if not os.path.exists(os.path.dirname(train_set_path)):
                os.makedirs(os.path.dirname(train_set_path))
            train_vector_set.to_csv(train_set_path, index=False)

            # create test vector set
            innocent_test_set_path = os.path.join(innocent_directory, str(fold), 'test_set.txt')
            innocent_test_set_graphs = parse_gspan_file(innocent_test_set_path, label="Innocent")
            pirated_test_set_path = os.path.join(pirated_directory, level, str(fold), 'test_set.txt')
            pirated_test_set_graphs = parse_gspan_file(pirated_test_set_path, label="Pirated")
            test_vector_set = pd.DataFrame()
            for index, vector in enumerate(pirated_test_set_graphs):
                test_vector_set.loc[index, 'Label'] = 'Pirated'
                for feature_index, feature in enumerate(features):
                    print('Test Set => Obfuscation Level %s Vector %s Feature %s' % (level, index, feature_index))
                    if subgraph_is_isomorphic(vector, feature):
                        test_vector_set.loc[index, id(feature)] = 1
                    else:
                        test_vector_set.loc[index, id(feature)] = 0
            for index, vector in enumerate(innocent_test_set_graphs):
                test_vector_set.loc[index + len(pirated_test_set_graphs), 'Label'] = 'Innocent'
                for feature_index, feature in enumerate(features):
                    print('Test Set => Obfuscation Level %s Vector %s Feature %s' % (level, index, feature_index))
                    if subgraph_is_isomorphic(vector, feature):
                        test_vector_set.loc[index + len(pirated_test_set_graphs), id(feature)] = 1
                    else:
                        test_vector_set.loc[index + len(pirated_test_set_graphs), id(feature)] = 0
            test_set_path = os.path.join(experiment_directory, level, str(fold), 'test_set.csv')

            # create directory if doesn't exist
            if not os.path.exists(os.path.dirname(test_set_path)):
                os.makedirs(os.path.dirname(test_set_path))
            test_vector_set.to_csv(test_set_path, index=False)
