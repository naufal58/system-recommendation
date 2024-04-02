from pyECLAT import Example2
import pandas as pd

def eclat(currentItems, itemsAndTransactions, minSupport, frequentItemsets):
    while itemsAndTransactions:
        item, transactions = itemsAndTransactions.pop()
        newItemset = currentItems.union({item})
        support = len(transactions)
        
        if support >= minSupport:
            frequentItemsets[frozenset(newItemset)] = support
            
            nextItems = []
            for otherItem, otherTransactions in itemsAndTransactions:
                commonTransactions = transactions.intersection(otherTransactions)
                if commonTransactions:
                    nextItems.append((otherItem, commonTransactions))
            
            nextItems.sort(key=lambda x: len(x[1]), reverse=True)
            eclat(newItemset, nextItems, minSupport, frequentItemsets)

def run_eclat(data, minSupport):
    itemTransactions = {}
    for transactionID, transaction in enumerate(data):
        for item in transaction:
            if item not in itemTransactions:
                itemTransactions[item] = set()
            itemTransactions[item].add(transactionID)
    
    itemsAndTransactions = [(item, transactions) for item, transactions in itemTransactions.items() if len(transactions) >= minSupport]
    itemsAndTransactions.sort(key=lambda x: len(x[1]), reverse=True)
    
    frequentItemsets = {}
    eclat(set(), itemsAndTransactions, minSupport, frequentItemsets)
    return frequentItemsets

# Load dataset from pyECLAT Example2
dataset_df = Example2().get()

# Convert the DataFrame into a list of transactions
data = dataset_df.apply(lambda row: row.dropna().tolist(), axis=1).tolist()
transaction_count = len(data)
print(transaction_count)

# Define the minimum support as an absolute count
minSupport = 2  # For example, an item must appear in at least 2 transactions to be considered frequent

# Run the custom ECLAT function
print("Running ECLAT...")
frequent_itemsets = run_eclat(data, minSupport)
print("Frequent itemsets:")
for itemset, support in sorted(frequent_itemsets.items(), key=lambda x: x[1], reverse=True)[:7]:
    # Since itemset is a frozenset, convert it to a list and then get the first element for printing
    support = support / transaction_count
    if len(itemset) == 1:  # Check if the itemset contains only one item
        item = list(itemset)[0]  # Convert frozenset to list and get the item
        print(f"{item}: {support}")
