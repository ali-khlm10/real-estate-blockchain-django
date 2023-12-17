from django.contrib import admin
from .models import blockModel, blockStatusModel, transactionsModel, transactionStatusModel
# Register your models here.


class blockAdmin(admin.ModelAdmin):
    list_display = [
        'block_number',
        'block_hash',
        'mined_by',
        'block_reward',
    ]


class blockStatusAdmin(admin.ModelAdmin):
    list_display = [
        'block_id',
        'is_finalized',
    ]


class transactionsAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_from_address',
        'transaction_to_address',
        'transaction_hash',
        'transaction_block',
    ]


class transactionStatusAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id',
        'pending',
        'published',
        'not_published'
    ]


admin.site.register(blockModel, blockAdmin)
admin.site.register(blockStatusModel, blockStatusAdmin)
admin.site.register(transactionsModel, transactionsAdmin)
admin.site.register(transactionStatusModel, transactionStatusAdmin)
