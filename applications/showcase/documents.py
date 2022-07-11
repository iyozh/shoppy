from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer

from applications.showcase.models import Product, Category


html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@registry.register_document
class ProductDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
        'slug': fields.TextField(),
    })
    absolute_url = fields.TextField()

    name = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    class Index:
        name = 'products'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Product

        fields = [
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