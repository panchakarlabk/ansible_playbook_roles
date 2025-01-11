from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {
            'filter_hosts': self.filter_hosts,
        }

    def filter_hosts(self, automation_data, inventory_hostname, db_type=None):
        """
        Filters multiple automation groups to find matching hosts.
        Supports:
        - Filtering across multiple automation groups (e.g., prod, dev).
        - Matching by `inventory_hostname` and optional `db_type`.

        :param automation_data: Dictionary containing multiple automation groups (e.g., prod, dev).
        :param inventory_hostname: Hostname to filter by.
        :param db_type: Optional database type filter (e.g., mysql, oracle).
        :return: List of matching processes with details.
        """
        if not isinstance(automation_data, dict):
            raise AnsibleFilterError("Expected 'automation_data' to be a dictionary.")

        if not inventory_hostname:
            raise AnsibleFilterError("inventory_hostname cannot be empty.")

        results = []
        for group_name, processes in automation_data.items():
            if not isinstance(processes, dict):
                continue

            for process_name, process_data in processes.items():
                if 'hosts' in process_data and inventory_hostname in process_data['hosts']:
                    if db_type is None or process_data.get('db_type') == db_type:
                        results.append({
                            "group_name": group_name,
                            "process_name": process_name,
                            "config": process_data.get('config', {}),
                            "db_type": process_data.get('db_type', 'unknown'),
                            "hosts": process_data['hosts']
                        })

        return results
