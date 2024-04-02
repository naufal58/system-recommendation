from pyECLAT import ECLAT
from pyECLAT import Example2
import pandas as pd

# Assuming 'data' is your list of transactions
dataset = Example2().get()

# Convert your list of transactions into a DataFrame
# Ensure the separator used here matches what you'll specify in the eclat_instance.fit() call
dataset.head()
eclat_instance = ECLAT(data=dataset)
eclat_instance.df_bin
items_per_transaction = eclat_instance.df_bin.astype(int).sum(axis=1)

# Adjust min_support and min_combination as needed
min_support = 0.1  # This is a percentage, ensure your dataset size and this threshold make sense together
min_combination = 1
max_combination = max(items_per_transaction)

# Get the binary matrix (optional step, useful for insight into the transaction encoding)
rule_indices, rule_supports = eclat_instance.fit(min_support=min_support,
                                   min_combination=min_combination,
                                   max_combination=max_combination,
                                   separator=' & ',  # Make sure this matches the separator used above
                                   verbose=True)

print("Frequent itemsets:")
for itemset, support in sorted(rule_supports.items(), key=lambda x: x[1], reverse=True):
    print(f"{itemset}: {support}")
