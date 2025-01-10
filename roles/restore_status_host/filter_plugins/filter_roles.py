from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {
            'host_filter': self.host_filter,
        }

    def host_filter(self, hosts, conditions):
        """
        Filters a list of hosts based on multiple conditions.
        Supports:
        - Forward wildcards (e.g., "Database*")
        - Backward wildcards (e.g., "*Database")
        - Bidirectional wildcards (e.g., "*Database*")
        - Exact matches
        - Case-insensitive matching
        - Multi-condition matching (e.g., hostname and db_type)

        :param hosts: List of host dictionaries to filter.
        :param conditions: List of dictionaries with key-value pairs to match.
        :return: Filtered list of hosts.
        """
        if not isinstance(hosts, list):
            raise AnsibleFilterError("The 'hosts' parameter must be a list of dictionaries.")

        if not isinstance(conditions, list):
            raise AnsibleFilterError("The 'conditions' parameter must be a list of dictionaries.")

        def matches_condition(host, condition):
            for key, value in condition.items():
                if key in host:
                    host_value = str(host[key]).lower()
                    condition_value = str(value).lower()

                    # Forward wildcard (e.g., "Database*")
                    if condition_value.endswith('*') and not condition_value.startswith('*'):
                        prefix = condition_value[:-1]
                        if host_value.startswith(prefix):
                            return True

                    # Backward wildcard (e.g., "*Database")
                    if condition_value.startswith('*') and not condition_value.endswith('*'):
                        suffix = condition_value[1:]
                        if host_value.endswith(suffix):
                            return True

                    # Bidirectional wildcard (e.g., "*Database*")
                    if condition_value.startswith('*') and condition_value.endswith('*'):
                        substring = condition_value[1:-1]
                        if substring in host_value:
                            return True

                    # Exact match
                    if condition_value == host_value:
                        return True

                else:
                    # If a required key is missing in the host, condition doesn't match
                    return False

            return False

        # Filter hosts that match all conditions
        return [
            host for host in hosts
            if all(matches_condition(host, condition) for condition in conditions)
            and host.get("hostname") == conditions[0].get("hostname")
        ]
