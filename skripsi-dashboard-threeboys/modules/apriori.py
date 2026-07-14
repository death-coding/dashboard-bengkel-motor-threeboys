import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def proses_apriori(keranjang_list, min_support=0.005, min_confidence=0.10):
    # 1. Encoding
    te = TransactionEncoder()
    te_array = te.fit(keranjang_list).transform(keranjang_list)
    df_matrix = pd.DataFrame(te_array, columns=te.columns_)
    df_matrix = df_matrix.astype(bool)

    # 2. Frequent Itemset
    frequent_itemsets = apriori(df_matrix, min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        return frequent_itemsets, pd.DataFrame(), df_matrix

    # 3. Association Rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    if rules.empty:
        return frequent_itemsets, rules, df_matrix

    # 4. Sorting berdasarkan Lift terkuat
    rules = rules.sort_values(by=["lift", "confidence"], ascending=False).reset_index(drop=True)
    return frequent_itemsets, rules, df_matrix