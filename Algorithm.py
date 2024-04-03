"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from Scraper import *

def create_data_model(distances):
    all_locations = []
    for loc in distances.keys():
        all_locations.append(loc)
    big_matrix = []
    for loc, nbrs in distances.items():
        local_matrix = []
        for nbr, dist in nbrs.items():
            local_matrix.append(int(dist))
        big_matrix.append(local_matrix)
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = big_matrix
    data["num_days"] = 1
    data["hotel"] = 0
    return data, all_locations


def print_solution(data, manager, routing, solution, all_locations):
    """Prints solution on console."""
    
    max_route_distance = 0
    for vehicle_id in range(data["num_days"]):
        index = routing.Start(vehicle_id)
        plan_output = []
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output.append(all_locations[index])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output.append(all_locations[manager.IndexToNode(index)])
        max_route_distance = max(route_distance, max_route_distance)
    return plan_output



def VRP0(addresses):
    """Entry point of the program."""
    # Instantiate the data problem.
    data, all_locations = create_data_model(calculate_distances(addresses))
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_days"], data["hotel"]
    )
    
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)
    
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    
    # Print solution on console.
    if solution:
        return print_solution(data, manager, routing, solution, all_locations)
    else:
        print("No solution found !")

addresses = {
    'Burj': '1 Mohammed Bin Rashid Boulevard, Downtown Dubai, Dubai 9440',
    'Mall': 'Sheikh Mohammed bin Rashid Boulevard Address Dubai Mall, Dubai',
    'Opera': '25898 87691, Dubai, Dubai',
    'Ski': 'Mall of the Emirates, Dubai',
    'Garden': 'Al Barsha South 3, Dubai United Arab Emirates 00000'
}
print(VRP0(addresses))