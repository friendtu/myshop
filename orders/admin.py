from django.contrib import admin
from .models import Order,OrderItem
import csv,datetime
from django.http import HttpResponse 
from django.utils.safestring import mark_safe
from django.urls import reverse


# Register your models here.

class OrderItemInline(admin.TabularInline):
    model=OrderItem    
    raw_id_fields=['product',]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','email','address','city','postal_code','paid','created','updated','order_detail','order_pdf']
    list_filter=['paid','created','updated']
    actions = ['export_to_csv']
    inlines=[OrderItemInline,]

    def export_to_csv(self, request, queryset):
        opts=self.model._meta
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']="attachment;filename={}.csv".format(opts.verbose_name) 


        writer=csv.writer(response)
        fields= [field for field in opts.get_fields() if not  field.many_to_many and  not field.one_to_many ]
        writer.writerow([field.verbose_name for field in fields]) 

        #write date row
        for obj in queryset:
            date_row=[]
            for field in fields:
                value=getattr(obj,field.name)
                if isinstance(value,datetime.datetime):
                    value=value.strftime('%d/%m/%Y')
                date_row.append(value)
            writer.writerow(date_row)
        return response

    def order_detail(self,obj):
        return mark_safe("<a href='{}'>View</a>".format(reverse("orders:admin_order_detail",args=[obj.id] )))

    def order_pdf(self,obj):
        return mark_safe("<a href='{}'>Invoice</a>".format(reverse("orders:admin_order_pdf",args=[obj.id]) ))
    export_to_csv.short_description="Export to CSV"
    order_detail.short_description='Order Detail'
    order_pdf.short_description='Invoice'


