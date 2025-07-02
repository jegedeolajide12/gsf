# utils.py or management/commands/create_recurring_events.py
from datetime import date, timedelta
from .models import Event, EventOccurence
import calendar

def create_recurring_events(start_date, end_date):
    current = start_date
    while current <= end_date:
        # Bible Study every Tuesday
        if current.weekday() == 1:
            event, _ = Event.objects.get_or_create(
                title="Bible Study",
                defaults={'description': 'Weekly Bible Study', 'location': 'GSF Excellence Cathedral, Apatapiti, FUTA South-Gate', 'is_default': True}
            )
            EventOccurence.objects.get_or_create(
                event=event,
                date=current,
                defaults={'time': '17:45'}  # Assuming a default time of 5:45 PM
            )
        # Prayer Meeting every Friday
        if current.weekday() == 4:
            # Last Friday logic
            last_day = calendar.monthrange(current.year, current.month)[1]
            last_friday = max(
                d for d in range(last_day, 0, -1)
                if date(current.year, current.month, d).weekday() == 4
            )
            if current.day == last_friday:
                event, _ = Event.objects.get_or_create(
                    title="Night of Exploits",
                    defaults={'description': 'Monthly vigil', 'is_default': True, 'location': 'GSF Excellence Cathedral, Apatapiti, FUTA South-Gate'}
                )
                EventOccurence.objects.get_or_create(
                    event=event,
                    date=current,
                    defaults={'time': '17:00'} # Assuming a default time of 5 PM
                )
            else:
                event, _ = Event.objects.get_or_create(
                    title="Prayer Meeting",
                    defaults={'description': 'Weekly Prayer Meeting', 'is_default': True, 'location': 'GSF Excellence Cathedral, Apatapiti, FUTA South-Gate'}
                )
                EventOccurence.objects.get_or_create(
                    event=event,
                    date=current,
                    defaults={'time': '17:45'}  # Assuming a default time of 5:45 PM
                )
        current += timedelta(days=1)
