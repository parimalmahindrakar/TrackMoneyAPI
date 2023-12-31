from datetime import datetime
from mongoengine import ( Document,
                          StringField,
                          FloatField,
                          DateTimeField,
                          ListField,
                          LazyReferenceField )

from helpers import helper

class Bank(Document):
    name = StringField(max_length=20)
    initial_balance = FloatField()
    current_balance = FloatField()
    total_disbursed_till_now = FloatField()
    expenses = ListField(LazyReferenceField('Expense'))
    created_at = DateTimeField(default=datetime.now().date())
    updated_at = DateTimeField(default=datetime.now().date())

    def __repr__(self):
        return f'<Bank:{self.name}>'

    @classmethod
    def get_banks(cls, **kwargs):
        banks = cls.objects
        if kwargs.get('name'):
            banks = banks.filter(name=kwargs['name'])
        if kwargs.get('id'):
            banks = banks.filter(id=kwargs['id'])

        return banks

    def get_expenses(self):
        all_expenses = [expense.fetch() for expense in self.expenses]
        return sorted(all_expenses, key=lambda e: e.created_at)

    def store_remaining_amount(self):
        sorted_expenses = self.get_expenses()
        for expense in sorted_expenses:
            self.update_bank_and_expense_data(expense)

    def update_bank_data_after_expense_deletion(self, expense):
        current_balalnce = self.current_balance + expense.expense_total
        total_disbursed_till_now = self.total_disbursed_till_now - expense.expense_total
        self.update(
            set__total_disbursed_till_now=total_disbursed_till_now,
            set__current_balance=current_balalnce
        )
        self.reload()
