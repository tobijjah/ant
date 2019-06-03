# Agent-based model - Description
This document describes the classes and core logic of the agent based model.
Each section details a class and its logic. The UML class diagram presents a
comprehensive overview of the interactions.

## Namespace - environment
### Environment
##### Description
This class describes the environment where the other classes/agents
(*Ant*, *Pheromone*, *Hole* and *Nutrient*) lives in. Basically it is
a 2D list where each list element is a *Cell* object which stores references to other classes/agents.
This class can be used to spawn holes, nutrients, and ants. Further it provides an interface to get the visible cells for
an certain agent. To instantiate the class three arguments are required which are initialized by default values.
##### Construction
- tuple size = (10, 10)
    - Defines the size of twhe 2D environment must be a tuple of two integers where
      the first element is the number of rows and the second element is the number of columns.
- int visible = 4 optional 8
    - Must be an integer. Defines the number of visible cells for an agent which moves in the environment.
- bool infinite = false
    - Must be a boolean. If an agent is at a edge or corner of the environment and infinite is false the visible cells
      are only in bounds of the field. If true the agent sees the opposite of the field (a infinite field).
##### Properties (implementation details)
- list _field
    - List comprehension to init field. Each element is a cell object init by a position object.
- list _field_flat
    - Flat field used to select random cells for spawn_nutrient and spawn_hole.
- int _rows
    - Just in case we keep it, we can use it to answer len quickly.
- int _cols
    - Just in case we keep it, we can use it to answer len quickly.
- obj _rng
    - Keep a reference of the rng and use it for spawn hole/nutrient.
    - Random Number Generator (RNG) must be an numpy.random.RandomState object. The generator is used for selecting
      random sites for holes and nutrients.
    - default np.RandomState(42) change over settings object
- list visible
    - Conditional if visible <=4 define a list of the four rules (north, east, south, west), if visible is >= 4
      define a list of the eight rules (north, north-east, east, south-east, south, south-west, west, north-west)
- bool infinite
    - Used when we determine which cells are visible for an ant. If false ants at field edges have only three or five
      visible cells and at field corners only two or three visible cells. If true the ant can see the opposite of the
      field.
##### Methods (implementation detail is the second item below the respective method)
- str draw()
    - Returns a string which represents the environment.
- obj spawn_hole(position)
    - Spawns a *hole* within the field bounds and returns it.
      If *position* argument is set it spawns
      the hole at this position (must be unoccupied), otherwise it
      spawns a *hole* at a random unoccupied position. *Position* must be
      a *position* object.
    - If position defined check if position on field than get_cell at position and delegate spawn_hole to
      to respective cell (can raise an error). If position is not defined shuffle field_flat and iterate
      over it, try to spawn a hole.
- obj spawn_nutrient(position, amount)
    - Spawns a *nutrient* within the field bounds and returns it.
      If *position* argument is set it spawns
      the *nutrient* at this *position* (must be unoccupied), otherwise it
      spawns a *nutrient* at a random unoccupied position. *Position* must be
      a *position* object.
    - If position defined check if position on field than get_cell at position and delegate spawn_nutrient to
      to respective cell (can raise an error). If position is not defined shuffle field_flat and iterate
      over it, try to spawn a nutrient.
- obj spawn_ant()
    - description
- list visible(ant)
    - Returns a list of cells visible for an *Ant* object.
- obj get_cell(position)
- bool on_field(position)
- \_\_len\_\_()
    - Delegate to field list object.
- \_\_get_item\_\_
    - Delegate to field list object.
- \_\_iter\_\_
    - Delegate to field list object.
- \_\_repr\_\_
    - Return object representation as string.
- \_\_str\_\_
    - Delegate to self.draw.

### Cell
##### Description
##### Properties
##### Methods

### Position
##### Description
##### Properties
##### Methods

## Namespace - agent
### Nutrient
##### Description
##### Properties
##### Methods

### Hole
##### Description
##### Properties
##### Methods

### Ant
##### Description
##### Properties
- an ant has a position in bounds of the environment
- an ant has a family/ant hole
- an ant has or has not food in its mandible
##### Methods

### Pheromone
##### Description
##### Properties
##### Methods

## Namespace - controller
### Controller
##### Description
##### Properties
##### Methods

## Namespace - timed
### Monitor
##### Description
##### Properties
##### Methods

### Timer
##### Description
##### Properties
##### Methods

### CLI
##### Description
##### Properties
##### Methods
First apporach
PheromoneMonitor: After each iteration it detects the maximum and minimum pheromone concentration and set it to all pheromones
Pheromone: determine the colorization by min max

Second approach