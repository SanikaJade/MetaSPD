import pandas as pd
import os
from sklearn import linear_model
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import tree


def evaluate_model(directory_path, model):
    """
    trains and evaluates model with 10 fold cross validation method
    :param directory_path: a path which contains 10 folds for both training set and test set
    :param model: training model(NB,LR,DT)
    :return: f1, precision, recall, auc, tpr ,fpr
    """
    f1 = tpr = fpr = auc = precision = recall = 0
    for fold in range(1, 11):
        df_train = pd.read_csv(os.path.join(directory_path, str(fold), 'train_set.csv'))
        df_test = pd.read_csv(os.path.join(directory_path, str(fold), 'test_set.csv'))
        train_x = df_train.loc[:, df_train.columns != 'Label']
        train_y = df_train['Label']
        test_x = df_test.loc[:, df_test.columns != 'Label']
        test_y = df_test['Label']

        # initialize classifier model
        if model == 'CART':
            clf = tree.DecisionTreeClassifier()
        elif model == 'NB':
            clf = GaussianNB()
        elif model == 'LR':
            clf = linear_model.LogisticRegression(C=1e5)
        else:
            clf = None

        clf = clf.fit(train_x, train_y)
        y_true = test_y
        y_pred = clf.predict(test_x)
        f1 += f1_score(y_true, y_pred, pos_label='Pirated')
        precision += precision_score(y_true, y_pred, pos_label='Pirated')
        recall += recall_score(y_true, y_pred, pos_label='Pirated')
        auc += roc_auc_score([__normalize(y) for y in y_true], [__normalize(y) for y in y_pred])
        tp, fp, tn, fn = __confusion_matrix([__normalize(y) for y in y_true], [__normalize(y) for y in y_pred])
        tpr += tp / (tp + fn)
        fpr += fp / (fp + tn)
    return f1 / 10, precision / 10, recall / 10, auc / 10, tpr / 10, fpr / 10


def __confusion_matrix(y_actual, y_hat):
    """
    calculates confusion matrix
    :param y_actual: actual label
    :param y_hat: predicted label
    :return: tp, fp, tn, fn
    """
    tp = fp = tn = fn = 0
    for index in range(len(y_hat)):
        if y_actual[index] == y_hat[index] == 1:
            tp += 1
        if y_hat[index] == 1 and y_actual[index] != y_hat[index]:
            fp += 1
        if y_actual[index] == y_hat[index] == 0:
            tn += 1
        if y_hat[index] == 0 and y_actual[index] != y_hat[index]:
            fn += 1
    return tp, fp, tn, fn


def __normalize(label):
    """
    converts label to binary value
    :param label: input label
    :return: binary value
    """
    return 1 if label == 'Pirated' else 0 if label == 'Innocent' else None


if __name__ == "__main__":
    experiment_directory = '.\\experiment\\MySQL'
    obfuscation_levels = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300', '400']
    column = pd.Index(['Level', 'Classifier', 'F1-Score', 'Precision', 'Recall', 'AUC', 'TPR', 'FPR'], name="columns")
    matrix = pd.DataFrame(data=0, index=[], columns=column)
    index = 0
    for level in obfuscation_levels:
        directory_path = os.path.join(experiment_directory, level)
        print('Obfuscation Level: %s' % level)
        # Decision Tree
        matrix.loc[index] = [level, 'CART', *evaluate_model(directory_path, 'CART')]
        # Naive Bayes
        matrix.loc[index + 1] = [level, 'NB', *evaluate_model(directory_path, 'NB')]
        # Logistic Regression
        matrix.loc[index + 2] = [level, 'LR', *evaluate_model(directory_path, 'LR')]
        index += 3

    # writes experiment result to file
    matrix.to_csv('.\\experiment\\MySQL\\result.csv', index=False)
