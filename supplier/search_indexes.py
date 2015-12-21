import datetime
from haystack import indexes
from supplier.models import Buyer


class BuyerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    company_name = indexes.CharField(model_attr='company_name', boost=2)
    # product_service_category = indexes.CharField(model_attr='product_service_category__category_name', 
    #     indexed=False, null=True)

    def get_model(self):
        return Buyer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()