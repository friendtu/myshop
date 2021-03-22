import redis
from django.conf import settings
from .models import Product

r=redis.StrictRedis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB)

class Recommender(object):
    def get_product_key(self,id):
        return "product:{}:purchased_with".format(id)

    def products_bought(self,products):
        ids=[p.id for p in products]
        for id in ids:
            for with_id in ids:
                if id!=with_id:
                    r.zincrby(self.get_product_key(id),1, with_id)

    def suggest_products_for(self,products,max_results=6):
        ids=[p.id for p in products]
        if len(ids)==1:
            suggestions=r.zrange(self.get_product_key(ids[0]),0,-1,desc=True)[:max_results]
        else:
            product_keys=[self.get_product_key(id) for id in ids]
            joined_id_key="tmp_"+".".join([str(id) for id in ids])
            r.zunionstore(joined_id_key,product_keys)
            r.zrem(joined_id_key,*ids)
            suggestions=r.zrange(joined_id_key,0,-1,desc=True)[:max_results]
            r.delete(joined_id_key)

        suggested_ids=[int(id) for id in suggestions]
        suggested_products=list(Product.objects.filter(id__in=suggested_ids))
        suggested_products.sort(key=lambda x: suggested_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id',flat=True):
            r.delete(self.get_product_key(id))

    
    




