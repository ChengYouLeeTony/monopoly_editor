from storages.backends.azure_storage import AzureStorage
def get_account_key():
    ACCOUTT_KEY = '+hwPjQWHyL/Qna1J9Y1EfOeTbnjoDbfdvQbZjqZWNvZw7NvMwxFWA7Kil8l6i3NhFQhpocbNJWf4ZARWLJSohw=='
    return ACCOUTT_KEY

class AzureMediaStorage(AzureStorage):
    account_name = 'monopolyuserupload' # Must be replaced by your <storage_account_name>
    account_key = get_account_key()  # Must be replaced by your <storage_account_key>
    azure_container = 'userdata'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'monopolyuserupload' # Must be replaced by your storage_account_name
    account_key = get_account_key()  # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None