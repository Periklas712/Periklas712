
from re import L
import pandas as pd #vivliothiki gia to pandas
import numpy as np
from sklearn.model_selection import StratifiedKFold  #vivliothiki gia to na xoriso to data se folds
from sklearn.preprocessing import MinMaxScaler       #vivliothiki gia na kanonikopoihso ta dedomena me map minmax
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score #vivliothiki gia tis metrikes
import matplotlib.pyplot as plt #vivliothiki gia thn dhmiourgia ton plots
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier #vivliothiki gia to neuroniko diktyo

#file i want to read
file_path = 'Dataset2Use_Assignment1.xlsx'

#reading the file
df = pd.read_excel(file_path)

#calculating missing values
missing_values = df.isnull().sum()

#check and message if values are missing
if missing_values.sum() > 0:
    print("Προειδοποίηση: Βρέθηκαν ελλείπουσες εγγραφές (NaNs)!")
    for column, count in missing_values.items():
        if count > 0:
            print(f"Στήλη '{column}': {count} ελλείπουσες εγγραφές.")
else:
    print("Δεν βρέθηκαν ελλείπουσες εγγραφές (NaNs).")

print()
print()
#reading the values for every column
data_list = df.iloc[1:].values.tolist()
first_column=df.iloc[:,0]
second_column=df.iloc[:,1]
third_column=df.iloc[:,2]
fourth_column=df.iloc[:,3]
fifth_column=df.iloc[:,4]
sixth_column=df.iloc[:,5]
seventh_column=df.iloc[:,6]
eighth_column=df.iloc[:,7]
ninth_column=df.iloc[:,8]
tenth_column=df.iloc[:,9]
eleventh_column = df.iloc[:, 10]
twelfth_column = df.iloc[:, 11]
thirteenth_column = df.iloc[:, 12]
df['A']=first_column
df['B']=second_column
df['C']=third_column
df['D']=fourth_column
df['E']=fifth_column
df['F']=sixth_column
df['G']=seventh_column
df['H']=eighth_column
df['I']=ninth_column
df['J']=tenth_column
df['K']=eleventh_column
df['Value'] = twelfth_column
df['Year'] = thirteenth_column

#creating the plot for the business:solving 2a
#dhmiourgia tou plot gia ugiys kai ftoxeumenes epixeiriseis gia kathe etos
filtered_df = df[df['Value'].isin([1, 2])]
grouped_counts = filtered_df.groupby(['Year', 'Value']).size().unstack(fill_value=0)
grouped_counts.plot(kind='bar', stacked=True)
plt.title('Αριθμός Υγιών και Πτωχευμένων Επιχειρήσεων ανά Έτος')
plt.xlabel('Έτος')
plt.ylabel('Αριθμός Επιχειρήσεων')
plt.xticks(rotation=45)
plt.legend(['Υγιείς Επιχειρήσεις (1)', 'Πτωχευμένες Επιχειρήσεις (2)'],loc='lower right')
plt.tight_layout()
plt.show()
print()

#euresh ton ygiei kai xreokopimenon etairion
healthy_companies = df[df.iloc[:, 11] == 1]
bankrupt_companies = df[df.iloc[:, 11] == 2]

#creating list to store the max ,min ,average values of every pointer,healthy and non-healthy
max_values_healthy = []
min_values_healthy = []
average_values_healthy = []
max_values_bankrupt = []
min_values_bankrupt = []
average_values_bankrupt = []

#brisko kai ypologizo to max,min,average ton ygiei kai ftoxeumenon etairion gia kathe sthlh
for i in range(8):
    max_values_healthy.append(healthy_companies.iloc[:, i].max())
    min_values_healthy.append(healthy_companies.iloc[:, i].min())
    average_values_healthy.append(healthy_companies.iloc[:, i].mean())

for i in range(8):
    max_values_bankrupt.append(bankrupt_companies.iloc[:, i].max())
    min_values_bankrupt.append(bankrupt_companies.iloc[:, i].min())
    average_values_bankrupt.append(bankrupt_companies.iloc[:, i].mean())

#creating the plot
x = range(8)
width = 0.2
fig, ax = plt.subplots(figsize=(12, 6))

# creating bars for healthy
ax.bar([p - width for p in x], max_values_healthy, width=width, label='Max Υγιείς', color='lightgreen')
ax.bar([p - width for p in x], min_values_healthy, width=width, label='Min Υγιείς', bottom=max_values_healthy, color='darkgreen')
ax.bar(x, average_values_healthy, width=width, label='Average Υγιείς', color='green')

# creating bars for non healthy
ax.bar([p + width for p in x], max_values_bankrupt, width=width, label='Max Πτωχευμένες', color='salmon')
ax.bar([p + width for p in x], min_values_bankrupt, width=width, label='Min Πτωχευμένες', bottom=max_values_bankrupt, color='red')
ax.bar(x, average_values_bankrupt, width=width, label='Average Πτωχευμένες', color='orange')

#creating the tickets and labels for the plot
ax.set_title('Max, Min, και Μέσες Τιμές Υγιών και Πτωχευμένων Επιχειρήσεων')
ax.set_xlabel('Στήλες')
ax.set_ylabel('Τιμές')
ax.set_xticks(x)
ax.set_xticklabels([df.columns[i] for i in range(8)], rotation=45)
ax.legend()
plt.tight_layout()
plt.show()

#kanonikopoihsh ton dedomenon me thn methodo mixmaxscaler
columns_to_normalize = df.columns[:8]
scaler = MinMaxScaler()
df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])

X= df[columns_to_normalize]
Y= df['ΕΝΔΕΙΞΗ ΑΣΥΝΕΠΕΙΑΣ (=2) (ν+1)']

#Dhimourgo ta folds dld xorizo ta dedomena se 4 folds
skf = StratifiedKFold(n_splits=4)

#dhmiourgia mias domh poy exei ta montela ekpaideushs moy kai tis methodous gia kathe ena
models={
    'LDA': LinearDiscriminantAnalysis(),
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'k-Nearest Neighbors': KNeighborsClassifier(),
    'Naive Bayes': GaussianNB(),
    'Support Vector Machine': SVC()
    }

#dhmirgia toy dikoy moy monteloy , epilego neuroniko diktyo
nn_model = MLPClassifier(hidden_layer_sizes=(100, 100), max_iter=2000, random_state=45)

#dhmiourgia ton sthlvn gia to arxeio csv pou tha apothikeyso ta dedomena
columns = ['Classifier Name', 'Set Type', 'Train Set Type', 'Number of Training Samples',
           'Number of Non-Healthy Companies in Training Sample', 'TP', 'TN', 'FP', 'FN', 'ROC-AUC']
results_df = pd.DataFrame(columns=columns)

#synartisi gia thn apothikeusi ton dedomenon sto arxeio csv
def record_results(model_name, dataset_type, train_set_type, num_samples, num_non_healthy, cm, auc_roc):
    tn, fp, fn, tp = cm.ravel()  # Ανάλυση του confusion matrix me thn synartisi ravel
    new_row = pd.DataFrame({
        'Classifier Name': [model_name],
        'Set Type': [dataset_type],
        'Train Set Type': [train_set_type],
        'Number of Training Samples': [num_samples],
        'Number of Non-Healthy Companies in Training Sample': [num_non_healthy],
        'TP': [tp],
        'TN': [tn],
        'FP': [fp],
        'FN': [fn],
        'ROC-AUC': [auc_roc]
    })
    global results_df
    results_df = pd.concat([results_df, new_row], ignore_index=True)

#Fuction to create and print the confusion matrix
def plot_confusion_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title(title)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

#Function to print and calculate the metrics
def print_metrics_and_record(y_true, y_pred, y_prob, dataset_type, model_name, train_set_type, num_samples, num_non_healthy):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, pos_label=2)
    recall = recall_score(y_true, y_pred, pos_label=2)
    f1 = f1_score(y_true, y_pred, pos_label=2)

    if len(y_prob.shape) == 1:
        auc_roc = roc_auc_score(y_true, y_prob)
    else:
        auc_roc = roc_auc_score(y_true, y_prob[:, 1])

    print(f"{model_name} - {dataset_type} Set:")
    print(f"  Accuracy: {accuracy:.2f}")
    print(f"  Precision: {precision:.2f}")
    print(f"  Recall: {recall:.2f}")
    print(f"  F1 Score: {f1:.2f}")
    print(f"  AUC ROC: {auc_roc:.2f}")
    print()

    # Καταγραφή του confusion matrix και καταχώρηση των αποτελεσμάτων στο DataFrame
    cm = confusion_matrix(y_true, y_pred)
    record_results(model_name, dataset_type, train_set_type, num_samples, num_non_healthy, cm, auc_roc)

#ylopoihsh ton montelwn
fold = 1
for train_index, test_index in skf.split(X, Y):
    print(f"Fold {fold}:")

    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = Y.iloc[train_index], Y.iloc[test_index]

    #Counting and printing healthy and bankrupt in training set
    train_counts = y_train.value_counts()
    healthy_count = train_counts.get(1, 0)
    bankrupt_count = train_counts.get(2, 0)

    print(f"  Training set: {healthy_count} Υγιείς , {bankrupt_count} Χρεωκοπημένες")

    #Changing the training set if the analogy is bigger than 1;3
    if healthy_count / bankrupt_count > 3:
        healthy_companies = X_train[y_train == 1]
        bankrupt_companies = X_train[y_train == 2]
        required_healthy_count = bankrupt_count * 3

        if required_healthy_count < healthy_count:
            healthy_sample = healthy_companies.sample(n=required_healthy_count, random_state=45)
        else:
            healthy_sample = healthy_companies

        X_train_balanced = pd.concat([healthy_sample, bankrupt_companies])
        y_train_balanced = pd.concat([pd.Series([1]*len(healthy_sample)), pd.Series([2]*len(bankrupt_companies))])

        print(f"  Balanced Training set: {len(healthy_sample)} Υγιείς, {len(bankrupt_companies)} Χρεωκοπημένες")
        train_set_type = "Balanced"
    else:
        X_train_balanced, y_train_balanced = X_train, y_train
        train_set_type = "Unbalanced"

    num_samples = len(X_train_balanced)
    num_non_healthy = len(y_train_balanced[y_train_balanced == 2])


    X_test_filtered = X_test[~X_test.isin(X_train_balanced)].dropna()
    y_test_filtered = y_test[X_test.index.isin(X_test_filtered.index)]

    #Counting the number of healthy and bankrupt companies in the new modified training set
    test_counts = y_test.value_counts()
    print(f"  Test set: {test_counts.get(1, 0)} Υγιείς, {test_counts.get(2, 0)} Χρεωκοπημένες")

   #Training the models
    for model_name, model in models.items():
        model.fit(X_train_balanced, y_train_balanced)
        # Πρόβλεψη στο train set
        y_train_pred = model.predict(X_train_balanced)
        # Πρόβλεψη στο test set
        y_test_pred = model.predict(X_test)

       #Printing the confusion matrices  #Printing the metrics for every model in test set and train set
        print_metrics_and_record(y_train_balanced, y_train_pred, y_train_pred, 'Train', model_name, train_set_type, num_samples, num_non_healthy)
        plot_confusion_matrix(y_train_balanced, y_train_pred, f'{model_name} - Confusion Matrix - Train Set')

        print_metrics_and_record(y_test, y_test_pred, y_test_pred, 'Test', model_name, train_set_type, num_samples, num_non_healthy)
        plot_confusion_matrix(y_test, y_test_pred, f'{model_name} - Confusion Matrix - Test Set')

    #neural network training
    nn_model.fit(X_train_balanced, y_train_balanced)
    y_pred = nn_model.predict(X_test)
    print_metrics_and_record(y_train_balanced, y_train_pred, y_train_pred, 'Train', 'Neural Network', train_set_type, num_samples, num_non_healthy)
    plot_confusion_matrix(y_train_balanced, y_train_pred, 'Neural Network - Confusion Matrix - Train Set')
    print_metrics_and_record(y_test, y_test_pred, y_test_pred, 'Test', 'Neural Network', train_set_type, num_samples, num_non_healthy)
    plot_confusion_matrix(y_test, y_test_pred, 'Neural Network - Confusion Matrix - Test Set')

    print('------------------------------------------------------------------------------------------------------------')
    print()

    fold += 1

results_df.to_csv('balancedDataOutcomes.csv', index=False)
print("Τα αποτελέσματα αποθηκεύτηκαν στο αρχείο 'balancedDataOutcomes.csv'.")
