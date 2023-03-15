from azure.cosmos import exceptions, CosmosClient

class CosmosDB:
    def __init__(self, url, key, db_name, container_name):
        self.client = CosmosClient(url, credential=key)
        self.db_name = db_name
        self.container_name = container_name
        self.database = None
        self.container = None
    
    def create_database(self):
        try:
            self.database = self.client.create_database(self.db_name)
            print(f"Created database {self.db_name}")
        except exceptions.CosmosResourceExistsError:
            self.database = self.client.get_database_client(self.db_name)
            print(f"Database {self.db_name} already exists")
    
    def create_container(self):
        container_definition = {'id': self.container_name}
        partition_key = '/pk'
        try:
            self.container = self.database.create_container(
                id=self.container_name,
                partition_key=partition_key,
                offer_throughput=400
            )
            print(f"Created container {self.container_name}")
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client(self.container_name)
            print(f"Container {self.container_name} already exists")
            
    def insert_item(self, item):
        self.container.upsert_item(item)
        print(f"Inserted item into container {self.container_name}: {item}")
    
    def query_items(self, query):
        query_results = self.container.query_items(
            query=query,
            enable_cross_partition_query=True
        )
        items = list(query_results)
        print(f"Query returned {len(items)} items")
        return items
    
    def delete_item(self, item):
        self.container.delete_item(item['id'], partition_key=item['pk'])
        print(f"Deleted item from container {self.container_name}: {item}")
