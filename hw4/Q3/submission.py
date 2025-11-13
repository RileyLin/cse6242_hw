import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict
from platform import python_version
import numpy as np
import pandas as pd
import time
import gc
import random
from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer

class GaTech():
    # Change to your GA Tech Username
    # NOT your 9-Digit GTId
    def GTusername(self):
        gt_username = "wlin99"
        return gt_username

class Data():
    
    # points [1]
    def dataAllocation(self,path):
        # TODO: Separate out the x_data and y_data and return each
        # args: string path for .csv file
        # return: pandas dataframe, pandas series
        # -------------------------------
        # ADD CODE HERE
        df = pd.read_csv(path)
        # Last column is the label (y_data), all other columns are features (x_data)
        x_data = df.iloc[:, :-1]
        y_data = df.iloc[:, -1]
        # ------------------------------- 
        return x_data,y_data
    
    # points [1]
    def trainSets(self,x_data,y_data):
        # TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
        # Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 614.
        # args: pandas dataframe, pandas dataframe
        # return: pandas dataframe, pandas dataframe, pandas series, pandas series
        # -------------------------------
        # ADD CODE HERE
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, shuffle=True, random_state=614)
        # -------------------------------
        return x_train, x_test, y_train, y_test


class LinearRegressionModel():
    
    # points [2]
    def linearClassifier(self,x_train, x_test, y_train):
        # TODO: Create a LinearRegression classifier and train it.
        # args: pandas dataframe, pandas dataframe, pandas series
        # return: numpy array, numpy array
        # -------------------------------
        # ADD CODE HERE
        lr = LinearRegression()
        lr.fit(x_train, y_train)
        y_predict_train = lr.predict(x_train)
        y_predict_test = lr.predict(x_test)
        # -------------------------------
        return y_predict_train, y_predict_test

    # points [1]
    def lgTrainAccuracy(self,y_train,y_predict_train):
        # TODO: Return accuracy (on the training set) using the accuracy_score method.
        # Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use any method that satisfies the requriements.
        # args: pandas series, numpy array
        # return: float
        # -------------------------------
        # ADD CODE HERE 
        # Custom rounding: >=0.5 -> 1, <0.5 -> 0
        y_pred_rounded = np.where(y_predict_train >= 0.5, 1, 0)
        train_accuracy = accuracy_score(y_train, y_pred_rounded)
        # -------------------------------   
        return train_accuracy
    
    # points [1]
    def lgTestAccuracy(self,y_test,y_predict_test):
        # TODO: Return accuracy (on the testing set) using the accuracy_score method.
        # Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use any method that satisfies the requriements.
        # args: pandas series, numpy array
        # return: float
        # -------------------------------
        # ADD CODE HERE
        # Custom rounding: >=0.5 -> 1, <0.5 -> 0
        y_pred_rounded = np.where(y_predict_test >= 0.5, 1, 0)
        test_accuracy = accuracy_score(y_test, y_pred_rounded)
        # -------------------------------
        return test_accuracy
    

class RFClassifier():

    # Q3.3.1 Classification using Random Forest

    # points [2]
    def randomForestClassifier(self,x_train,x_test, y_train):
        # TODO: Create a RandomForestClassifier and train it. Set Random state to 614.
        # args: pandas dataframe, pandas dataframe, pandas series
        # return: RandomForestClassifier object, numpy array, numpy array
        # -------------------------------
        # ADD CODE HERE
        rf_clf = RandomForestClassifier(random_state=614)
        rf_clf.fit(x_train, y_train)
        y_predict_train = rf_clf.predict(x_train)
        y_predict_test = rf_clf.predict(x_test)
        # -------------------------------
        return rf_clf,y_predict_train, y_predict_test
    
    # points [1]
    def rfTrainAccuracy(self,y_train,y_predict_train):
        # TODO: Return accuracy on the training set using the accuracy_score method.
        # args: pandas series, numpy array
        # return: float
        # -------------------------------
        # ADD CODE HERE
        train_accuracy = accuracy_score(y_train, y_predict_train)
        # -------------------------------
        return train_accuracy
    
    # points [1]
    def rfTestAccuracy(self,y_test,y_predict_test):
        # TODO: Return accuracy on the test set using the accuracy_score method.
        # args: pandas series, numpy array
        # return: float
        # -------------------------------
        # ADD CODE HERE
        test_accuracy = accuracy_score(y_test, y_predict_test)
        # -------------------------------
        return test_accuracy
    
    # Q3.3.2 Feature Importance
    
    # points [1]
    def rfFeatureImportance(self,rf_clf):
        # TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
        # args: RandomForestClassifier object
        # return: float array
        # -------------------------------
        # ADD CODE HERE
        feature_importance = rf_clf.feature_importances_
        # -------------------------------
        return feature_importance
    
    # points [1]
    def sortedRFFeatureImportanceIndicies(self,rf_clf):
        # TODO: Sort them in the descending order and return the feature numbers[0 to ...].
        #       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
        # args: RandomForestClassifier object
        # return: int array
        # -------------------------------
        # ADD CODE HERE
        feature_importance = rf_clf.feature_importances_
        # argsort() returns indices in ascending order, so we reverse with [::-1] for descending
        sorted_indices = np.argsort(feature_importance)[::-1]
        # -------------------------------
        return sorted_indices
    
    # Q3.3.3 Hyper-parameter Tuning

    # points [1]
    def hyperParameterTuning(self,rf_clf,x_train,y_train):
        # TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
        # Define param_grid for GridSearchCV as a dictionary
        # args: RandomForestClassifier object, pandas dataframe, pandas series
        # return: GridSearchCV object
        # 'n_estimators': [4, 16, 256]
        # 'max_depth': [2, 8, 16]
        # -------------------------------
        # ADD CODE HERE
        param_grid = {
            'n_estimators': [4, 16, 256],
            'max_depth': [2, 8, 16]
        }
        gscv_rfc = GridSearchCV(rf_clf, param_grid, cv=5)
        gscv_rfc.fit(x_train, y_train)
        # -------------------------------
        return gscv_rfc
    
    # points [1]
    def bestParams(self,gscv_rfc):
        # TODO: Get the best params, using .best_params_
        # args:  GridSearchCV object
        # return: parameter dict
        # -------------------------------
        # ADD CODE HERE
        best_params = gscv_rfc.best_params_
        # -------------------------------
        return best_params
    
    # points [1]
    def bestScore(self,gscv_rfc):
        # TODO: Get the best score, using .best_score_.
        # args: GridSearchCV object
        # return: float
        # -------------------------------
        # ADD CODE HERE
        best_score = gscv_rfc.best_score_
        # -------------------------------
        return best_score
    

class SupportVectorMachine():
    
# Q3.4.1 Pre-process

    # points [1]
    def dataPreProcess(self,x_train,x_test):
        # TODO: Pre-process the data to standardize it, otherwise the grid search will take much longer.
        # args: pandas dataframe, pandas dataframe
        # return: pandas dataframe, pandas dataframe
        # -------------------------------
        # ADD CODE HERE
        scaler = StandardScaler()
        scaled_x_train = scaler.fit_transform(x_train)
        scaled_x_test = scaler.transform(x_test)
        # -------------------------------
        return scaled_x_train, scaled_x_test
    
# Q3.4.2 Classification

    # points [1]
    def SVCClassifier(self,scaled_x_train,scaled_x_test, y_train):
        # TODO: Create a SVC classifier and train it. Set gamma = 'auto'
        # args: pandas dataframe, pandas dataframe, pandas series
        # return: numpy array, numpy array
        # -------------------------------
        # ADD CODE HERE
        svc = SVC(gamma='auto')
        svc.fit(scaled_x_train, y_train)
        y_predict_train = svc.predict(scaled_x_train)
        y_predict_test = svc.predict(scaled_x_test)
        # -------------------------------
        return y_predict_train,y_predict_test
    
    # points [1]
    def SVCTrainAccuracy(self,y_train,y_predict_train):
        # TODO: Return accuracy on the training set using the accuracy_score method.
        # args: pandas series, numpy array
        # return: float 
        # -------------------------------
        # ADD CODE HERE
        train_accuracy = accuracy_score(y_train, y_predict_train)
        # -------------------------------
        return train_accuracy
    
    # points [1]
    def SVCTestAccuracy(self,y_test,y_predict_test):
        # TODO: Return accuracy on the test set using the accuracy_score method.
        # args: pandas series, numpy array
        # return: float 
        # -------------------------------
        # ADD CODE HERE
        test_accuracy = accuracy_score(y_test, y_predict_test)
        # -------------------------------
        return test_accuracy
    
# Q3.4.3 Hyper-parameter Tuning
    
    # points [1]
    def SVMBestScore(self, scaled_x_train, y_train):
        # TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
        # Note: Set n_jobs = -1 and return_train_score = True and gamma = 'auto'
        # args: pandas dataframe, pandas series
        # return: GridSearchCV object, float
        # -------------------------------
        svm_parameters = {'kernel':('linear', 'rbf'), 'C':[0.01, 0.1, 1.0]}
        # ADD CODE HERE
        svm = SVC(gamma='auto')
        svm_cv = GridSearchCV(svm, svm_parameters, cv=5, n_jobs=-1, return_train_score=True)
        svm_cv.fit(scaled_x_train, y_train)
        best_score = svm_cv.best_score_
        # -------------------------------
        
        return svm_cv, best_score
    
    # points [1]
    def SVCClassifierParam(self,svm_cv,scaled_x_train,scaled_x_test,y_train):
        # TODO: Calculate the training and test set predicted values after hyperparameter tuning and standardization.
        # args: GridSearchCV object, pandas dataframe, pandas dataframe, pandas series
        # return: numpy series, numpy series
        # -------------------------------
        # ADD CODE HERE
        y_predict_train = svm_cv.predict(scaled_x_train)
        y_predict_test = svm_cv.predict(scaled_x_test)
        # -------------------------------
        return y_predict_train,y_predict_test

    # points [1]
    def svcTrainAccuracy(self,y_train,y_predict_train):
        # TODO: Return accuracy (on the training set) using the accuracy_score method.
        # args: pandas series, numpy array
        # return: float
        # -------------------------------
        # ADD CODE HERE
        train_accuracy = accuracy_score(y_train, y_predict_train)
        # -------------------------------
        return train_accuracy

    # points [1]
    def svcTestAccuracy(self,y_test,y_predict_test):
        # TODO: Return accuracy (on the test set) using the accuracy_score method.
        # args: pandas series, numpy array
        # return: float
        # -------------------------------
        # ADD CODE HERE
        test_accuracy = accuracy_score(y_test, y_predict_test)
        # -------------------------------
        return test_accuracy
    
# Q3.4.4 Cross Validation Results

    # points [1]
    def SVMRankTestScore(self,svm_cv):
        # TODO: Return the rank test score for all hyperparameter values that you obtained in Q3.4.3. The 
        # GridSearchCV class holds a 'cv_results_' dictionary that should help you report these metrics easily.
        # args: GridSearchCV object 
        # return: int array
        # -------------------------------
        # ADD CODE HERE
        rank_test_score = svm_cv.cv_results_['rank_test_score']
        # -------------------------------
        return rank_test_score
    
    # points [1]
    def SVMMeanTestScore(self,svm_cv):
        # TODO: Return mean test score for all of hyperparameter values that you obtained in Q3.4.3. The 
        # GridSearchCV class holds a 'cv_results_' dictionary that should help you report these metrics easily.
        # args: GridSearchCV object
        # return: float array
        # -------------------------------
        # ADD CODE HERE
        mean_test_score = svm_cv.cv_results_['mean_test_score']
        # -------------------------------
        return mean_test_score


class PCAClassifier():

    def __init__(self, random_state: int = 0):
        self.random_state = random_state
        self.scaler_ = None
        self.pca_ = None
        self.feature_names_ = None
        self.X_scaled_ = None
    
    # Q3.5.1 PCA 
    # points [1]
    def pcaClassifier(self,x_data):
        # TODO: Perform dimensionality reduction of the data using PCA.
        #       Set parameters n_components to 8 and svd_solver to 'full'. Keep other parameters at their default value.
        # args: pandas dataframe
        # return: pca_object
        # -------------------------------
        # ADD CODE HERE
        pca = PCA(n_components=8, svd_solver='full')
        pca.fit(x_data)
        # -------------------------------
        self.pca_ = pca
        self.feature_names_ = list(x_data.columns)
        self.X_scaled_ = x_data
        return pca
    
    # Q3.5.2 PCA Explained Variance Ratio
    # points [1]
    def pcaExplainedVarianceRatio(self, pca):
        # TODO: Return percentage of variance explained by each of the selected components
        # args: pca_object
        # return: float array
        # -------------------------------
        # ADD CODE HERE
        explained_variance_ratio = pca.explained_variance_ratio_
        # -------------------------------
        return explained_variance_ratio
    
    # Q3.5.3 PCA Singular Values
    # points [1]
    def pcaSingularValues(self, pca):
        # TODO: Return the singular values corresponding to each of the selected components.
        # args: pca_object
        # return: float array
        # -------------------------------
        # ADD CODE HERE
        singular_values = pca.singular_values_
        # -------------------------------
        return singular_values
    
    # Q3.5.4 Cumulative Explained Variance
    # points [1]
    def n_components_for_variance(self, pca, threshold=0.90) -> int:
        # TODO: how many PCs to reach given cumulative explained variance threshold?
        # args: pca_object
        # return: int
        # -------------------------------
        # ADD CODE HERE
        cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
        n_components = np.argmax(cumulative_variance >= threshold) + 1
        # -------------------------------
        return n_components

    # Q3.5.5 Top Feature Contributors to PC1
    # points [1]
    def top_pc1_contributors(self, pca, top_n: int = 5):
        # TODO: Return the top-N feature names contributing to PC1 by |coefficient|.
        # Deterministic ordering: sort by abs(coef) desc; ties by name asc.
        # args: pca_object
        # return: list of strings
        names = getattr(pca, "feature_names_in_", None)
        if names is not None:
            names = list(names)
        # -------------------------------
        # ADD CODE HERE
        # Get PC1 coefficients (first principal component)
        pc1_coefficients = pca.components_[0]
        
        # Use feature names from instance variable if not in pca object
        if names is None:
            names = self.feature_names_
        
        # Create list of (feature_name, abs_coefficient) tuples
        feature_importance = [(names[i], abs(pc1_coefficients[i])) for i in range(len(names))]
        
        # Sort by abs coefficient descending, then by name ascending for ties
        feature_importance.sort(key=lambda x: (-x[1], x[0]))
        
        # Get top N feature names
        top_features = [f[0] for f in feature_importance[:top_n]]
        # -------------------------------
        return top_features
    