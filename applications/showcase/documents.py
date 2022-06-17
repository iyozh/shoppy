from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from applications.showcase.models import Product, Category


@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
        'slug': fields.TextField(),
    })
    absolute_url = fields.TextField()

    class Index:
        name = 'products'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product

        fields = [
            'name',
            'description',
            'created_at',
            'updated_at',
            'slug',
            'price',
            'image',
            'available',
        ]

    def prepare_absolute_url(self, instance):
        return instance.get_absolute_url()

    def get_queryset(self):
        return super(ProductDocument, self).get_queryset().select_related(
            'category'
        )