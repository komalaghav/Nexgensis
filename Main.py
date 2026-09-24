
import json


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance

def find_nearest_agent(warehouse_location, agents):
    nearest_agent = None
    shortest_distance = float("inf")

    for agent in agents:
        distance = calculate_distance(
            warehouse_location,
            agent["location"]
        )

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_agent = agent

    return nearest_agent

with open("data.json", "r") as file:
    data = json.load(file)


warehouses = data["warehouses"]
agents = data["agents"]
packages = data["packages"]


#
agent_results = {}

for agent in agents:
    agent_results[agent["id"]] = {
        "packages_delivered": 0,
        "total_distance": 0
    }

for warehouse in warehouses:

    warehouse_location = warehouse["location"]

  
    nearest_agent = find_nearest_agent(
        warehouse_location,
        agents
    )

    agent_id = nearest_agent["id"]

    current_location = warehouse_location

    for package in packages:

        if package["warehouse_id"] == warehouse["id"]:

            destination = package["destination"]

          
            distance = calculate_distance(
                current_location,
                destination
            )

          
            agent_results[agent_id]["total_distance"] += distance

          
            agent_results[agent_id]["packages_delivered"] += 1

          
            current_location = destination



for agent_id in agent_results:

    packages_delivered = agent_results[agent_id]["packages_delivered"]
    total_distance = agent_results[agent_id]["total_distance"]

    if packages_delivered > 0:
        efficiency = total_distance / packages_delivered
    else:
        efficiency = 0

    agent_results[agent_id]["efficiency"] = round(
        efficiency,
        2
    )



best_agent = None
best_efficiency = float("inf")

for agent_id, result in agent_results.items():

    if result["packages_delivered"] > 0:

        if result["efficiency"] < best_efficiency:
            best_efficiency = result["efficiency"]
            best_agent = agent_id


agent_results["best_agent"] = best_agent



with open("report.json", "w") as file:
    json.dump(
        agent_results,
        file,
        indent=4
    )


print("Delivery simulation completed successfully!")
print("Report saved in report.json")
print("Best agent:", best_agent)
