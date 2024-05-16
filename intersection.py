class intersection:
    def __init__(self,road_index_map): ## road 0: roads index on map clockwise
        self.road_index_map = road_index_map
        self.phases = dict()
        # todo