# Ecosystem Simulation

This project is a simulation of a simple ecosystem where creatures with unique genetic traits interact with their environment and each other. The simulation is built using the Mesa framework for agent-based modeling and visualized with Pygame.

## About The Project

This simulation models a population of creatures in a grid-based world. Each creature has a set of genes that determine its characteristics, such as speed and sight. These traits influence their ability to find food, survive, and reproduce.

### Key Features:

* **Genetic Inheritance and Mutation:** Creatures pass their genes to offspring with a chance of mutation, leading to evolution within the population over time.
* **Agent-Based Modeling:** The simulation uses the Mesa library to model the behavior of individual creatures (agents) and their interactions.
* **Dynamic Environment:** Creatures move, consume food, and reproduce, creating a dynamic and evolving ecosystem.
* **Data Collection:** The simulation collects detailed data at each time step, which is saved to `data_collection.json`.
* **Visualization:** A separate Pygame script reads the simulation data to provide a visual representation of the ecosystem's state at each step.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

You need to have Python and the following libraries installed:

* **Mesa:** For the agent-based modeling framework.
    ```sh
    pip install mesa
    ```
* **Pygame:** For visualizing the simulation.
    ```sh
    pip install pygame
    ```

### Installation

1.  Clone the repo:
    ```sh
    git clone [https://github.com/your_username/your_project_name.git](https://github.com/your_username/your_project_name.git)
    ```
2.  Navigate to the project directory:
    ```sh
    cd your_project_name
    ```
3.  Install the required packages:
    ```sh
    pip install mesa pygame
    ```

## Usage

The simulation is a two-step process: first, you run the model to generate the data, and then you run the visualization to see the results.

1.  **Run the Simulation Model:**
    This will generate the `data_collection.json` file, which contains the state of the ecosystem at each time step.
    ```sh
    python model.py
    ```

2.  **Run the Visualization:**
    This will open a Pygame window and display the simulation based on the data from `data_collection.json`.
    ```sh
    python simulation_visualization.py
    ```
    * Press the **SPACEBAR** to pause and resume the visualization.

## Project Structure

* `model.py`: Contains the core logic for the ecosystem simulation, including the `Creature` and `Food` agent classes and the `EcosystemModel` class.
* `simulation_visualization.py`: Reads the `data_collection.json` file and uses Pygame to visualize the simulation.
* `data_collection.json`: The output file from `model.py` that stores the data for each step of the simulation.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

* [Mesa Framework](https://mesa.readthedocs.io/en/stable/)
* [Pygame Library](https://www.pygame.org/news)

