class FilterModule(object):
    def filters(self):
        return {
            'filter_nodes': self.filter_nodes,
        }

    def filter_nodes(self, nodes, ignore_conditions):
        """
        Filters out nodes that match any condition in ignore_conditions.
        Supports:
        - Forward wildcards (e.g., "Database*")
        - Backward wildcards (e.g., "*Database")
        - Bidirectional wildcards (e.g., "*Database*")
        - Exact matches
        - Case-insensitive matching

        :param nodes: List of nodes (dictionaries) to filter.
        :param ignore_conditions: List of dictionaries with key-value pairs to match.
        :return: Filtered list of nodes.
        """
        def matches_condition(node, condition):
            for key, value in condition.items():
                # Check if the node contains the key
                if key in node:
                    node_value = str(node[key]).lower()  # Convert node value to lowercase
                    condition_value = str(value).lower()  # Convert condition value to lowercase

                    # Handle prefix-based matching (e.g., "Database*")
                    if condition_value.endswith('*') and not condition_value.startswith('*'):
                        prefix = condition_value[:-1]  # Remove the '*' for prefix matching
                        if node_value.startswith(prefix):
                            return True

                    # Handle suffix-based matching (e.g., "*Database")
                    if condition_value.startswith('*') and not condition_value.endswith('*'):
                        suffix = condition_value[1:]  # Remove the '*' for suffix matching
                        if node_value.endswith(suffix):
                            return True

                    # Handle bidirectional matching (e.g., "*Database*")
                    if condition_value.startswith('*') and condition_value.endswith('*'):
                        substring = condition_value[1:-1]  # Remove '*' from both ends
                        if substring in node_value:
                            return True

                    # Handle exact matches
                    if condition_value == node_value:
                        return True

            return False

        # Filter out nodes that match any condition in ignore_conditions
        filtered_nodes = [
            node for node in nodes
            if not any(matches_condition(node, condition) for condition in ignore_conditions)
        ]

        return filtered_nodes