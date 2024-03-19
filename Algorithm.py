from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class VehicleRoutingProblemAlgorithm:
    def __init__(self, distance_matrix, num_days, hotel_index):
        self.data = self._create_data_model(distance_matrix, num_days, hotel_index)

    def _create_data_model(self, distance_matrix, num_days, hotel_index):
        """Stores the data for the problem."""
        data = {}
        data["distance_matrix"] = distance_matrix
        data["num_days"] = num_days
        data["hotel"] = hotel_index
        return data

    def _distance_callback(self, from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)
        return self.data["distance_matrix"][from_node][to_node]

    def _print_solution(self, solution):
        """Prints solution on console."""
        print(f"Objective: {solution.ObjectiveValue()}")
        max_route_distance = 0
        for vehicle_id in range(self.data["num_days"]):
            index = self.routing.Start(vehicle_id)
            plan_output = f"Route for day {vehicle_id}:\n"
            route_distance = 0
            while not self.routing.IsEnd(index):
                plan_output += f" {self.all_locations[index]} -> "
                previous_index = index
                index = solution.Value(self.routing.NextVar(index))
                route_distance += self.routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id
                )
            plan_output += f"{self.all_locations[self.manager.IndexToNode(index)]}\n"
            plan_output += f"Distance of the route: {route_distance}km\n"
            print(plan_output)
            max_route_distance = max(route_distance, max_route_distance)
        print(f"Maximum of the route distances: {max_route_distance}km")

    def solve(self, all_locations):
        self.all_locations = all_locations
        self.manager = pywrapcp.RoutingIndexManager(
            len(self.data["distance_matrix"]), self.data["num_days"], self.data["hotel"]
        )
        self.routing = pywrapcp.RoutingModel(self.manager)

        transit_callback_index = self.routing.RegisterTransitCallback(self._distance_callback)
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = "Distance"
        self.routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            3000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name,
        )
        distance_dimension = self.routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        solution = self.routing.SolveWithParameters(search_parameters)

        if solution:
            self._print_solution(solution)
        else:
            print("No solution found!")

