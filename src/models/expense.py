from datetime import datetime

from . import expense_entry
from mongoengine import ( Document,
                         StringField,
                         DateTimeField,
                         EmbeddedDocumentListField,
                         LazyReferenceField,
                         FloatField,
                         DENY )

class Expense(Document):
    day = StringField()
    expenses = EmbeddedDocumentListField(expense_entry.ExpenseEntry)
    bank = LazyReferenceField('Bank', reverse_delete_rule=DENY)
    bank_name = StringField()
    expense_total = FloatField()
    remaining_amount_till_now = FloatField() # TODO: write the logic for this later !
    created_at = DateTimeField(default=datetime.now().date())
    updated_at = DateTimeField(default=datetime.now().date())

    def get_total_of_expenses(self):
        return sum([ee.amount for ee in self.expenses])

    def get_bank(self):
        return self.bank.fetch()

    @classmethod
    def get_expenses(cls, **kwargs):
        expenses = cls.objects
        if kwargs.get('id'):
            expenses = expenses.filter(id=kwargs.get('id'))
        else:
            if kwargs.get('created_at'):
                expenses = expenses.filter(created_at=datetime.strptime(kwargs.get('created_at'), '%d-%m-%Y %H:%M'))
            elif kwargs.get('start_date') and kwargs.get('end_date'):
                expenses = expenses.filter(
                    created_at__gte=datetime.strptime(kwargs.get('start_date'), '%d-%m-%Y %H:%M'),
                    created_at__lte=datetime.strptime(kwargs.get('end_date'), '%d-%m-%Y %H:%M')
                ).order_by('created_at')

            if kwargs.get('bank_name'):
                expenses = expenses.filter(bank_name=kwargs.get('bank_name'))

        return expenses