import pandas as pd


def find_parent(element_to_be_found, tree):
    parent_of_element_to_be_found = next((element for element in tree if (
                (element.right == element_to_be_found.nid) or (element.left == element_to_be_found.nid))), None)

    is_right_child = (parent_of_element_to_be_found.right == element_to_be_found.nid)
    return parent_of_element_to_be_found, is_right_child


def condition_to_reach_node(tree, element_to_reach):
    (parent, right) = find_parent(element_to_be_found=element_to_reach, tree=tree)
    if right:
        condition_to_arrive_at_node = "( " + parent.data.split_condition + " )"
    else:
        condition_to_arrive_at_node = "( " + parent.data.split_condition.replace("<", ">=") + " )"

    # Run a loop till from leaf_parent to the root to find the conditions to reach the leaf_parent
    node = parent
    while node.nid != 1:
        (parent, is_right_child) = find_parent(element_to_be_found=node, tree=tree)
        node = parent
        condition = "( " + node.data.split_condition + " )"
        if not is_right_child:
            condition = condition.replace("<", ">=")
        condition_to_arrive_at_node += " & " + condition
    return condition_to_arrive_at_node


# Adds a prediction column to the dataframe
def prediction(df, tree):
    df['index'] = range(1, len(df[df.columns.values[0]]) + 1)
    leaves = [element for element in tree if element.right == 0]
    cols = (df.columns.values.tolist())
    cols.append("prediction")
    final_df = pd.DataFrame(columns=cols)
    if len(tree) == 1:
        final_df["prediction"] = tree[0].data.mean
        return final_df
    for leaf in leaves:
        condition_to_reach_at_leaf = condition_to_reach_node(tree, leaf)
        new_df = df[eval(condition_to_reach_at_leaf)]
        new_df["prediction"] = leaf.data.mean
        final_df = final_df.append(new_df, ignore_index=True)
    final_df.sort_values('index', inplace=True)
    return final_df
