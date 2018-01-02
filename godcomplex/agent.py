
import uuid
import random
from .biome import Biome

class AgentActionFailed(Exception): pass

class PrerequisiteActionsNeeded(AgentActionFailed):
    def __init__(self, *deps):
        self.dependencies = deps

class AgentType:
    SETTLER = 'SETTLER'
    WARBAND = 'WARBAND'
    SETTLEMENT = 'SETTLEMENT'

SETTLE_RADIUS = 5

class AgentActions:
    def spawn(agent, **kwargs):
        pass

    def wander(agent, **kwargs):
        if agent.agent_type == AgentType.SETTLEMENT:
            return

        neighbors = [neighbor for neighbor
            in agent.world.get_neighbors(*agent.position)
            if Biome.is_passable(agent.world.get_biome(*neighbor))]
        if neighbors:
            agent.world.move_agent(agent, *random.choice(neighbors))
        return

    def navigate(agent, **kwargs):
        pass

    def wait(agent, **kwargs):
        return None

    def settle(agent, **kwargs):
        if random.random() < 0.9:
            raise PrerequisiteActionsNeeded(AgentActions.wander)

        for dx in range(-SETTLE_RADIUS, SETTLE_RADIUS):
            for dy in range(-SETTLE_RADIUS, SETTLE_RADIUS):
                pos = agent.world.get_neighbor(*agent.position,
                    direction=(dx, dy))
                if pos and agent.world.get_settlement(*pos):
                    raise PrerequisiteActionsNeeded(AgentActions.wander)

        settlement = Settlement.copy(agent)
        settlement.agent_type = AgentType.SETTLEMENT
        settlement.id = agent.id  # reuse ID -- effectively GCs current agent.
        settlement.origin = agent.origin
        settlement.position = agent.position
        agent.world.add_pending_agent(settlement)
        agent.world.set_settlement(*agent.position, val=settlement)
        agent.world.move_agent(agent, *agent.position)
        return None

    def attack(agent, **kwargs):
        pass

    def combine(agent, **kwargs):
        pass

class Agent:
    def __init__(self, world, agent_type, origin=None, faction=None,
            goals=[]):
        self.id = uuid.uuid4()
        self.world = world
        self.queue = goals
        self.position = None
        self.origin = origin
        self.agent_type = agent_type
        self.faction = faction

    @classmethod
    def copy(cls, agent):
        return cls(
            world=agent.world,
            agent_type=agent.agent_type,
            origin=agent.origin,
            faction=agent.faction)

    def __repr__(self, extra=''):
        return '<{} id={} faction={} type={} position={} queue={} {}>' \
            .format(self.__class__.__name__, self.id, self.faction,
                self.agent_type, self.position, self.queue, extra)

    def __hash__(self):
        return hash(self.id)

    def set_position(self, x, y):
        self.position = (x, y)

    def step(self):
        action = self.queue.pop(0) if len(self.queue) else AgentActions.wander
        try:
            result = action(self)
        except PrerequisiteActionsNeeded as e:
            self.queue = list(e.dependencies) + [action] + self.queue
            return (action, e)
        except AgentActionFailed as e:
            return (action, e)

        return (action, None)

class Settlement(Agent):
    def __init__(self, world, agent_type, origin=None, faction=None,
            goals=[]):
        super().__init__(world, agent_type, origin, faction, goals)

        self.population = random.randint(100, 500)
        self.stored_resources = 0

    # super hacky initial proof-of-concept population growth simulation
    def grow(self):
        new_resources = (self.population // 8)

        # calculate needed resources for growth/stagnation/starvation
        needed_food = self.population // 10
        excess_food = self.stored_resources + new_resources - needed_food

        new_settler_cost = 1000
        if excess_food > new_settler_cost and random.random() > 0.7:
            new_agent = Agent.copy(self)
            new_agent.agent_type = AgentType.SETTLER
            new_agent.queue = [AgentActions.settle]
            new_agent.origin = self
            self.world.add_pending_agent(new_agent)
            self.world.move_agent(new_agent, *self.position)
            self.population -= random.randint(100, 500)
            excess_food -= new_settler_cost

        growth_rate = min(1.03, 1.0 + ((excess_food / needed_food) / 10))
        self.population = int(self.population * growth_rate)
        self.stored_resources = excess_food

    def step(self):
        self.grow()
        return super().step()

    def __repr__(self):
        return super().__repr__('pop={} resources={}'.format(
            self.population, self.stored_resources))
