

class History:
    def __init__(self, timestamp=1):
        self.events = []
        self.current_timestamp = timestamp

    def advance(self, incr=1):
        self.current_timestamp += incr

    def record(self, agent, action, result=None):
        evt = HistoricalEvent(self.current_timestamp, agent, action, result)
        self.events.append(evt)

class HistoricalEvent:
    def __init__(self, timestamp, agent, action, result=None):
        self.timestamp = timestamp
        self.agent = agent
        self.action = action
        self.result = result

    def __repr__(self):
        return '<HistoricalEvent ts={} agent={} action={} result={}>'.format(
            self.timestamp,
            self.agent,
            self.action,
            self.result)
