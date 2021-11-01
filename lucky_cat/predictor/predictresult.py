class PredictResult:
    def __init__(self, total_hits: int, oscillate_points: list, meet_points: list, violate_points: list):
        self.total_hits = total_hits
        self.oscillate_points = oscillate_points
        self.meet_points = meet_points
        self.violate_points = violate_points

    def __str__(self):
        if self.total_hits == 0:
            oscillate_possibility = 0
            meet_possibility = 0
            violate_possibility = 0
        else:
            oscillate_possibility = 1.0 * len(self.oscillate_points) / self.total_hits
            meet_possibility = 1.0 * len(self.meet_points) / self.total_hits
            violate_possibility = 1 - oscillate_possibility - meet_possibility

        # print("Meet Date: {}\n".format(self.meet_points))
        # print("Oscillate Date: {}\n".format(self.oscillate_points))
        # print("Violate Date: {}\n".format(self.violate_points))
        return "Total hits: {}\nOscillate possibility: {:.2f}\nMeet possibility: {:.2f}\nViolate possibility: {:.2f}\n".format(
                self.total_hits, oscillate_possibility, meet_possibility, violate_possibility)
