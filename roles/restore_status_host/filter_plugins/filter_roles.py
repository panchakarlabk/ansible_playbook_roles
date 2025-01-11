from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {
            'filter_hosts': self.filter_hosts,
        }

    def filter_hosts(self, dba_automation_prod, inventory_hostname, db_type):
        """
        Filters the dba_automation data to return processes where:
        - inventory_hostname matches the 'hosts' list
        - db_type matches the provided value
        """
        if not isinstance(dba_automation_prod, dict):
            raise AnsibleFilterError("Expected 'dba_automation' to be a dictionary.")

        if not inventory_hostname:
            raise AnsibleFilterError("inventory_hostname cannot be empty.")

        if not db_type:
            raise AnsibleFilterError("db_type cannot be empty.")

        filtered_processes = []
        for process_name, process_data in dba_automation_prod.items():
            if 'hosts' in process_data and 'db_type' in process_data:
                if (inventory_hostname in process_data['hosts'] and 
                        process_data['db_type'] == db_type):
                    filtered_processes.append({
                        "process_name": process_name,
                        "config": process_data['config'],
                        "db_type": process_data['db_type'],
                        "hosts": process_data['hosts']
                    })

        return filtered_processes
