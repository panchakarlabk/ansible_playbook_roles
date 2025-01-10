from ansible.errors import AnsibleFilterError

def filter_roles(config, inventory_hostname, db_type=None):
    """
    Filters processes based on inventory_hostname and db_type.
    Args:
        config (dict): The YAML configuration dictionary.
        inventory_hostname (str): The host to match.
        db_type (str, optional): The database type to filter (e.g., 'mysql', 'oracle').
    Returns:
        dict: Matching configuration for the role.
    """
    if not isinstance(config, dict):
        raise AnsibleFilterError("Expected a dictionary for the config parameter.")
    
    if not isinstance(inventory_hostname, str):
        raise AnsibleFilterError("Expected a string for the inventory_hostname parameter.")
    
    if db_type is not None and not isinstance(db_type, str):
        raise AnsibleFilterError("Expected a string or None for the db_type parameter.")
    
    # Iterate through processes and find matches
    for process_name, process_details in config.get("dba_automation_prod", {}).items():
        if inventory_hostname in process_details.get("hosts", []) and (
            db_type is None or process_details.get("db_type", None) == db_type
        ):
            return {
                "process_name": process_name,
                "config": process_details
            }
    
    # If no match is found, return None
    return None

class FilterModule(object):
    def filters(self):
        return {
            'filter_roles': filter_roles
        }
