class RunTracker(object):
    def __init__(self):
        self.runID = None
        self.recording = False

    def startRun(self, runID):
        self.runID = runID
        self.recording = True

    def stopRun(self):
        self.runID = None
        self.recording = False

    def getID(self):
        return self.runID

    def isRecording(self):
        return self.recording

