import pandas as pd
import numpy as np
import xgboost as xgb
import time
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, roc_auc_score, make_scorer
from sklearn.model_selection import ParameterSampler
from sklearn.metrics import confusion_matrix


df = pd.read_csv('ctr_15.csv', sep = ',')
len(df)

