from datetime import datetime


class Logger(object):
    @staticmethod
    def get_log_name(target_dir, base_name):
        # probably an easier way to do this, but brute force suffices ...
        now = datetime.now()
        log_suffix = str.format("{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}", now.year, now.month, now.day, now.hour, now.minute, now.second)
        return str.format("{}/{}_{}.log", target_dir, base_name, log_suffix)

