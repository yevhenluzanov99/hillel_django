from datetime import date
import calendar
from django import forms
from django.forms import ChoiceField

from first_app.models import Employee

from common.enums import WorkDayEnum


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("username", "first_name", "last_name", "email", "position")


class SalaryForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = date.today()
        week_day, num_days = calendar.monthrange(today.year, today.month)

        for day in range(1, num_days + 1):
            day_coord = today.year, today.month, day
            weekday = calendar.weekday(*day_coord)
            weekday_name = calendar.day_name[weekday]
            field_name = f"day_{day}"

            if weekday >= 5:  # weekend
                self.fields[field_name] = ChoiceField(
                    label=f"{day} - {weekday_name}",
                    choices=[(WorkDayEnum.WEEKEND.name, WorkDayEnum.WEEKEND.value)],
                    initial=WorkDayEnum.WEEKEND.name,
                )
            else:
                self.fields[field_name] = ChoiceField(
                    label=f"{day} - {weekday_name}",
                    choices=[(option.name, option.value) for option in WorkDayEnum],
                    initial=WorkDayEnum.WORKING_DAY.name,
                )

    def clean_employee(self):
        employee = self.cleaned_data.get("employee")
        if not employee:
            raise forms.ValidationError("Поле 'Employee' обов'язкове для заповнення.")
        return employee

    def clean(self):
        cleaned_data = super().clean()

        sick_leave_count = 0
        holiday_count = 0

        for field_name, value in cleaned_data.items():
            if field_name.startswith("day_"):
                if value == WorkDayEnum.SICK_DAY.name:
                    sick_leave_count += 1
                elif value == WorkDayEnum.HOLIDAY.name:
                    holiday_count += 1

        if sick_leave_count > 5:
            raise forms.ValidationError(
                "Кількість лікарняних днів не може перевищувати 5."
            )

        if holiday_count > 3:
            raise forms.ValidationError(
                "Кількість днів відпочинку не може перевищувати 3."
            )
