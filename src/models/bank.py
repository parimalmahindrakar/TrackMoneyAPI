from datetime import datetime
from mongoengine import ( Document,
                          StringField,
                          FloatField,
                          DateTimeField,
                          ListField,
                          LazyReferenceField )

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

    def get_expenses(self):
        all_expenses = [expense.fetch() for expense in self.expenses]
        return sorted(all_expenses, key=lambda e: e.created_at)

    def store_remaining_amount(self):
        sorted_expenses = self.get_expenses()
        for expense in sorted_expenses:
            remaining_amount_till_now = self.current_balance - expense.expense_total
            total_disbursed_till_now = self.total_disbursed_till_now + expense.expense_total

            # Update the expense document
            expense.update(set__remaining_amount_till_now=remaining_amount_till_now)

            # Update the Bank document
            self.update(
                set__total_disbursed_till_now=total_disbursed_till_now,
                set__current_balance=remaining_amount_till_now
            )
            self.reload()
