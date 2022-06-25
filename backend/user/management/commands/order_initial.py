from django.core.management import BaseCommand
from organization.models import Company, Contracting
from item.models import Item, ItemTable, ItemCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        contracting = Contracting.objects.get(contracting_code='123')
        item_table = ItemTable.objects.create(item_table_compound_id='123*123', contracting=contracting, item_table_code='123', 
                description="ItemTable")
        company = Company.objects.get(company_compound_id='123*123')
        company.item_table=item_table
        company.save()
        category=ItemCategory.objects.create(item_table=item_table,category_compound_id='123*123*11111111', category_code='11111111', 
                description='Category test')
        Item.objects.create(item_table=item_table,item_compound_id='123*123*111111111111111', item_code='111111111111111', 
                category=category, description='Item test', unit='un')

