import numpy as np
def abs_error_of_data(array):
    value = np.mean(array)
    error = 0
    for element in array:
        error += abs(element - value)
    return error


def mean_squared_error_of_data(array):
    value = np.mean(array)
    error = 0
    for element in array:
        error += (element - value) ** 2
    return error


error_function = mean_squared_error_of_data

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


# Function to prune the tree
def prune(tree, test_data):

    # First acquire the root node and list of parents of leaves in the tree
    leaves_id = [element.nid for element in tree if element.right == 0]
    leaf_parents = [element for element in tree if (element.right in leaves_id or element.left in leaves_id)]

    # Every leaf-parent must be checked for pruning
    for leaf_parent in leaf_parents:

        condition_to_arrive_at_leaf_parent = condition_to_reach_node(tree=tree, element_to_reach=leaf_parent)

        # Finding the database at the leaf_parent, left child and right child
        # Df to store the pruned data
        df = test_data
        leaf_parent_test_df = test_data[eval(condition_to_arrive_at_leaf_parent)]
        df = leaf_parent_test_df
        #if len(leaf_parent_test_df["output"]) == 0:
        if len(leaf_parent_test_df[leaf_parent_test_df.columns[-1]]) == 0:
            continue
        left_condition = leaf_parent.data.split_condition.replace("<", ">=")
        left_child_test_df = leaf_parent_test_df[eval(left_condition)]
        right_child_test_df = leaf_parent_test_df[eval(leaf_parent.data.split_condition)]

        # Storing the children
        left_child = next(element for element in tree if element.nid == leaf_parent.left)
        right_child = next(element for element in tree if element.nid == leaf_parent.right)

        # Finding parent error and children error
        parent_error = error_function(leaf_parent_test_df[leaf_parent_test_df.columns[-1]])
        left_child_error = error_function(left_child_test_df[left_child_test_df.columns[-1]])
        right_child_error = error_function(right_child_test_df[right_child_test_df.columns[-1]])
        children_error = (left_child_error * len(left_child.data.df[left_child.data.df.columns[-1]])) + (
                    right_child_error * len(right_child.data.df[right_child.data.df.columns[-1]]))

        children_error /= len(leaf_parent_test_df[leaf_parent_test_df.columns[-1]])

        # If children have more error than leaf prune both
        if children_error > parent_error:

            tree[tree.index(leaf_parent)].left = 0
            tree[tree.index(leaf_parent)].right = 0

            # remove all the elements in the tree which originate from branches which have no parents
            while True:

                # Changes represents the changes made to the tree in one iteration
                changes = 0
                for node in tree:

                    # If flag does not change we remove the node as the node has no parents
                    flag = 1
                    if node.nid == 1:
                        continue
                    for element in tree:
                        if element.right == node.nid or element.left == node.nid:
                            flag = 100
                            break

                    if flag == 1:
                        changes += 1
                        if node in leaf_parents:
                            leaf_parents.remove(node)
                        tree.remove(node)

                # If no changes made terminate loop
                if changes == 0:
                    break
    return tree
