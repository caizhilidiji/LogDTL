"""
Description : This file implements the function to evaluation accuracy of log parsing
Author      : LogPAI team
License     : MIT
"""

import pandas as pd
import scipy.special
from sklearn.metrics import accuracy_score
from nltk.metrics.distance import edit_distance
import numpy as np

def evaluate(groundtruth, parsedresult):
    """ Evaluation function to benchmark log parsing accuracy
    
    Arguments
    ---------
        groundtruth : str
            file path of groundtruth structured csv file
        parsedresult : str
            file path of parsed structured csv file

    Returns
    -------
        f_measure : float
        accuracy : float
    """ 
    df_groundtruth = pd.read_csv(groundtruth)
    df_parsedlog = pd.read_csv(parsedresult, index_col=False)
 
    # Remove invalid groundtruth event Ids
    null_logids = df_groundtruth[~df_groundtruth['EventId'].isnull()].index
    df_groundtruth = df_groundtruth.loc[null_logids]
    df_parsedlog = df_parsedlog.loc[null_logids]
   
    accuracy_exact_string_matching = accuracy_score(np.array(df_groundtruth.EventTemplate.values,dtype='str'), np.array(df_parsedlog.EventTemplate.values, dtype='str'))
    
    edit_distance_result = []
    for i, j in zip(np.array(df_groundtruth.EventTemplate.values,dtype='str'), np.array(df_parsedlog.EventTemplate.values, dtype='str')):
        edit_distance_result.append(edit_distance(i,j))
        
    edit_distance_result_mean = np.mean(edit_distance_result)
    edit_distance_result_std = np.std(edit_distance_result)
    
    
    (precision, recall, f_measure, accuracy_PA) = get_accuracy(df_groundtruth['EventId'], df_parsedlog['EventId'])
    print('Precision: %.4f, Recall: %.4f, F1_measure: %.4f, accuracy_PA: %.4f, accuracy_exact_string_matching: %.4f, edit_distance_result_mean: %.4f, edit_distance_result_std: %.4f'%(precision, recall, f_measure, accuracy_PA, accuracy_exact_string_matching, edit_distance_result_mean, edit_distance_result_std))
    
    return precision, recall, f_measure, accuracy_PA, accuracy_exact_string_matching, edit_distance_result_mean, edit_distance_result_std


def get_accuracy(series_true, series_pred, debug=False):
    """ Compute accuracy metrics between log parsing results and ground truth
    
    Arguments
    ---------
        series_true : pandas.Series
            A sequence of groundtruth event Ids
        series_pred : pandas.Series
            A sequence of prediction event Ids
        debug : bool, default False
            print error log messages when set to True

    Returns
    -------
        precision : float
        recall : float
        f_measure : float
        accuracy : float
    """
    series_true_valuecounts = series_true.value_counts()
    real_pairs = 0
    for count in series_true_valuecounts:
        if count > 1:
            real_pairs += scipy.special.comb(count, 2)

    series_pred_valuecounts = series_pred.value_counts()
    parsed_pairs = 0
    for count in series_pred_valuecounts:
        if count > 1:
            parsed_pairs += scipy.special.comb(count, 2)

    accurate_pairs = 0
    accurate_events = 0 # determine how many lines are correctly parsed
    for parsed_eventId in series_pred_valuecounts.index:
        logIds = series_pred[series_pred == parsed_eventId].index
        series_true_logId_valuecounts = series_true[logIds].value_counts()
        error_eventIds = (parsed_eventId, series_true_logId_valuecounts.index.tolist())
        error = True
        if series_true_logId_valuecounts.size == 1:
            groundtruth_eventId = series_true_logId_valuecounts.index[0]
            if logIds.size == series_true[series_true == groundtruth_eventId].size:
                accurate_events += logIds.size
                error = False
        if error and debug:
            print('(parsed_eventId, groundtruth_eventId) =', error_eventIds, 'failed', logIds.size, 'messages')
        for count in series_true_logId_valuecounts:
            if count > 1:
                accurate_pairs += scipy.special.comb(count, 2)

    precision = float(accurate_pairs) / parsed_pairs
    recall = float(accurate_pairs) / real_pairs
    f_measure = 2 * precision * recall / (precision + recall)
    accuracy = float(accurate_events) / series_true.size
    return precision, recall, f_measure, accuracy






