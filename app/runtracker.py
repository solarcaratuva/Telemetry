class RunTracker(object):
    def __init__(self):
        self.runID = None
        self.recording = False
        self.viewingRun = False

    def startRun(self, runID):
        self.runID = runID
        self.recording = True

    def stopRun(self):
        self.runID = None
        self.recording = False

    def viewRun(self, runID):
        self.runID = runID
        self.viewingRun = True

    def getID(self):
        return self.runID

    def isRecording(self):
        return self.recording

    def isViewing(self):
        return self.viewingRun

