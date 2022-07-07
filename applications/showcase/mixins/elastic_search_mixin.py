from elasticsearch import Elasticsearch


class ElasticSearchMixin:
    def add_index_to_es(self):
        data = {
            'name': self.name,
            'price': self.price,
            'slug': self.slug,
            'available': self.available,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'image': self.image.url,
            'absolute_url': self.get_absolute_url(),
            'category': {'name': self.category.name, 'slug': self.category.slug},
        }
        elastic_connection_instance =  Elasticsearch(hosts=['elastic'])
        elastic_connection_instance.index(
            'products',
            id=self.id,
            body=data,
            doc_type="_doc",
            refresh=True
        )
        elastic_connection_instance.indices.refresh('products')