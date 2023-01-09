from datetime import datetime, timedelta
from dateutil.rrule import rrule, WEEKLY
from dataclasses import dataclass

@dataclass
class DataEntryIterator:
    start_date: datetime
    end_date: datetime
    time_zone: str

    def __input_class(self, summary):
        class_data = {
            'summary': summary,
            'location': input('Location (real or virtual): '),
        }
        rep_pattern = input('Repetition pattern (MTWHFSU): ')
        class_data['billiejoe_rep_pattern'] = rep_pattern
        rep_integers = [
            int_val for (int_val, char_val) in enumerate(list('MTWHFSU')) if char_val in rep_pattern
        ]
        class_data['recurrence'] = [
            str(rrule(WEEKLY, until=self.end_date, byweekday=rep_integers)).split()[1] # rrule includes a DTSTART clause, which isn't necessary for our purposes
        ]
        start_hour = input('Start time (HH:MM): ')
        duration = input('Duration (hours): ')

        parsed_start_hour = datetime.strptime(start_hour, '%H:%M')

        start_time = datetime(
            self.start_date.year, self.start_date.month, self.start_date.day, parsed_start_hour.hour, parsed_start_hour.minute, tzinfo=self.start_date.tzinfo
        )
        shifts = [(day - start_time.weekday()) % 7 for day in rep_integers]
        start_time += timedelta(days=min(shifts))

        end_time = start_time + timedelta(hours=float(duration))

        class_data['start'] = {
            'dateTime': start_time.isoformat(),
            'timeZone': self.time_zone
        }
        class_data['end'] = {
            'dateTime': end_time.isoformat(),
            'timeZone': self.time_zone
        }

        return class_data

    def __iter__(self):
        return self
    
    def __next__(self):
        summary = input('Name (or input nothing to stop): ')
        if summary == '':
            raise StopIteration
        return self.__input_class(summary)