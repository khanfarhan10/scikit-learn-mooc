# %% [markdown]
# # 📃 Solution for Exercise 02
#
# The aim of this exercise is to find out whether a decision tree
# model is able to extrapolate.
#
# By extrapolation, we refer to values predicted by a model outside of the
# range of feature values seen during the training.
#
# We will first load the regression data.

# %%
import pandas as pd

penguins = pd.read_csv("../datasets/penguins_regression.csv")

data_columns = ["Flipper Length (mm)"]
target_column = "Body Mass (g)"

data_train, target_train = penguins[data_columns], penguins[target_column]

# %% [markdown]
# ```{note}
# If you want a deeper overview regarding this dataset, you can refer to the
# Appendix - Datasets description section at the end of this MOOC.
# ```

# %% [markdown]
# First, create two models, a linear regression model and a decision tree
# regression model, and fit them on the training data. Limit the depth at
# 3 levels for the decision tree.

# %%
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

linear_regression = LinearRegression()
tree = DecisionTreeRegressor(max_depth=3)

linear_regression.fit(data_train, target_train)
tree.fit(data_train, target_train)

# %% [markdown]
# Create a testing dataset, ranging from the minimum to the maximum of the
# flipper length of the training dataset. Get the predictions of each model
# using this test dataset.

# %%
import numpy as np

data_test = pd.DataFrame(np.arange(data_train[data_columns[0]].min(),
                                   data_train[data_columns[0]].max()),
                         columns=data_columns)

# %%
target_predicted_linear_regression = linear_regression.predict(data_test)
target_predicted_tree = tree.predict(data_test)

# %% [markdown]
# Create a scatter plot containing the training samples and superimpose the
# predictions of both model on the top.

# %%
import matplotlib.pyplot as plt
import seaborn as sns

sns.scatterplot(data=penguins, x="Flipper Length (mm)", y="Body Mass (g)",
                color="black", alpha=0.5)
plt.plot(data_test, target_predicted_linear_regression,
         label="Linear regression")
plt.plot(data_test, target_predicted_tree, label="Decision tree")
plt.legend()
_ = plt.title("Prediction of linear model and a decision tree")

# %% [markdown]
# The predictions that we got were within the range of feature values seen
# during training. In some sense, we observe the capabilities of our model to
# interpolate.
#
# Now, we will check the extrapolation capabilities of each model. Create a
# dataset containing the value of your previous dataset. Besides, add values
# below and above the minimum and the maximum of the flipper length seen
# during training.

# %%
offset = 30
data_test = pd.DataFrame(np.arange(data_train[data_columns[0]].min() - offset,
                                   data_train[data_columns[0]].max() + offset),
                         columns=data_columns)

# %% [markdown]
# Finally, make predictions with both models on this new testing set. Repeat
# the plotting of the previous exercise.

# %%
target_predicted_linear_regression = linear_regression.predict(data_test)
target_predicted_tree = tree.predict(data_test)

# %%
sns.scatterplot(data=penguins, x="Flipper Length (mm)", y="Body Mass (g)",
                color="black", alpha=0.5)
plt.plot(data_test, target_predicted_linear_regression,
         label="Linear regression")
plt.plot(data_test, target_predicted_tree, label="Decision tree")
plt.legend()
_ = plt.title("Prediction of linear model and a decision tree")

# %% [markdown]
# The linear model will extrapolate using the fitted model for flipper lengths
# < 175 mm and > 235 mm. In fact, we are using the model parametrization to
# make this predictions.
#
# As mentioned, decision trees are non-parametric models and we observe that
# they cannot extrapolate. For flipper lengths below the minimum, the mass of
# the penguin in the training data with the shortest flipper length will always
# be predicted. Similarly, for flipper lengths above the maximum, the mass of
# the penguin in the training data with the longest flipper will always be
# predicted.
