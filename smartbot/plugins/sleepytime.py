from datetime import datetime, timedelta

import smartbot.plugin


class Plugin(smartbot.plugin.Plugin):
    """Check when you should wake up."""

    names = ['sleepytime', 'sleepyti.me']

    @staticmethod
    def calculate_wake_up_times(now=None, time_to_sleep=14,
                                sleep_cycle_duration=90):
        if now is None:
            now = datetime.now()

        now += timedelta(minutes=time_to_sleep)

        for i in range(6):
            wake_up_time = now + timedelta(minutes=sleep_cycle_duration)
            yield wake_up_time
            now = wake_up_time

    def on_command(self, msg, stdin, stdout, reply):
        times = list(self.calculate_wake_up_times())
        msg = ' or '.join(time.strftime('%l:%M %p').strip() for time in times)
        reply(msg)
