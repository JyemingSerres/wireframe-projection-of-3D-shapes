"""Create simple state machines.

Classes:
    State
    StateMachine
"""

from abc import ABC, abstractmethod
from enum import Enum

__author__ = "Jye-Ming Serres"


class State(ABC):
    """Abstract class. Manipulated by `StateMachine`.

    Methods:
        enter()
        update()
        exit()
    """

    def __init__(self) -> None:
        self.transitions = dict()

    @abstractmethod
    def enter(self) -> None:
        """Called by the state machine when entering this state."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Called by the state machine while being the current state."""
        pass

    @abstractmethod
    def exit(self) -> None:
        """Called by the state machine when exiting this state."""
        pass


class StateMachine:
    """Base class to create simple state machines.

    Methods:
        add_transition()
        add_transitions()
        update()
        reset()
        trigger()
    """

    def __init__(self, states: list[State], default_state: State = None) -> None:
        """Creates an instance from all possible states and default state.

        Args:
            states: All possible states. It is the user's responsability to make them reachable by 
                defining transitions.
            default_state: The state the state machine defaults to. If unspecified or `None`, the 
                default state is set to the first element in the list of states.
        """
        self._states = states
        self._default_state = states[0] if default_state is None else default_state
        self._current_state = self._default_state

    @property
    def states(self) -> list[State]:
        return self._states

    @property
    def default_state(self) -> State:
        return self._default_state

    @property
    def current_state(self) -> State:
        return self._current_state

    def add_transition(self, state_from: State, state_to: State, trigger: Enum) -> None:
        """Registers a transition between two states by an event.

        Args:
            state_from: State to transition from.
            state_to: State to transition to.
            trigger: The event that will trigger the state change.
        """
        if trigger in state_from.transitions:
            raise ValueError("Duplicate: trigger already defined for this state")
        state_from.transitions[trigger] = state_to

    def add_transitions(self, state_from: State, state_to: State, triggers: list[Enum]) -> None:
        """Registers transitions between the same two states by different events.

        Args:
            state_from: State to transition from.
            state_to: State to transition to.
            triggers: The list of events that will trigger the state change.
        """
        for trigger in triggers:
            self.add_transition(state_from, state_to, trigger)

    def update(self) -> None:
        """Executes the user-defined code within the current state."""
        self._current_state.update()

    def reset(self) -> None:
        """Sets the current state to default state."""
        self._current_state = self._default_state

    def trigger(self, trigger: Enum) -> None:
        """Attemps to change the state with the specified event and the current state.

        Args:
            trigger: The event.
        """
        if trigger in self._current_state.transitions:
            self._change_state(self._current_state.transitions[trigger])

    def _change_state(self, new_state: State) -> None:
        """Changes the current state and executes user defined code for exiting the old state and 
        entering the new state.

        Args:
            new_state: The new state.
        """
        self._current_state.exit()
        self._current_state = new_state
        self._current_state.enter()
