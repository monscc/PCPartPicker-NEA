"""
Undo/Redo Manager using Stack Data Structure
Demonstrates LIFO (Last In First Out) stack operations
"""
from typing import Dict, Any, Optional
from copy import deepcopy


class UndoRedoManager:
    """
    Manages undo/redo operations using two stacks
    
    Demonstrates:
    - Stack data structure (LIFO - Last In First Out)
    - Push and pop operations
    - State management
    """
    
    def __init__(self, max_history: int = 20):
        """
        Initialize the undo/redo manager
        
        Args:
            max_history: Maximum number of states to remember
        """
        self.undo_stack = []  # Stack for undo operations (LIFO)
        self.redo_stack = []  # Stack for redo operations (LIFO)
        self.max_history = max_history
        self.current_state = None
    
    def save_state(self, state: Dict[str, Any]) -> None:
        """
        Save current state to undo stack (PUSH operation)
        
        This implements the PUSH operation of a stack:
        - Adds new item to the top of the stack
        - Clears redo stack (new action invalidates redo history)
        - Limits stack size to prevent memory issues
        
        Args:
            state: Current state to save (e.g., selected parts)
        """
        # If we have a current state, push it to undo stack
        if self.current_state is not None:
            # PUSH to undo stack
            self.undo_stack.append(deepcopy(self.current_state))
            
            # Limit stack size (prevent unbounded growth)
            if len(self.undo_stack) > self.max_history:
                # Remove oldest item (bottom of stack)
                self.undo_stack.pop(0)
        
        # Update current state
        self.current_state = deepcopy(state)
        
        # Clear redo stack (new action invalidates redo history)
        self.redo_stack.clear()
    
    def undo(self) -> Optional[Dict[str, Any]]:
        """
        Undo last action (POP from undo stack, PUSH to redo stack)
        
        This demonstrates stack POP operation:
        - Removes and returns the top item from undo stack
        - Pushes current state to redo stack
        - Returns previous state
        
        Returns:
            Previous state, or None if nothing to undo
        """
        # Check if there's anything to undo
        if not self.undo_stack:
            return None
        
        # PUSH current state to redo stack
        if self.current_state is not None:
            self.redo_stack.append(deepcopy(self.current_state))
        
        # POP from undo stack (LIFO - get most recent)
        previous_state = self.undo_stack.pop()
        
        # Update current state
        self.current_state = deepcopy(previous_state)
        
        return self.current_state
    
    def redo(self) -> Optional[Dict[str, Any]]:
        """
        Redo last undone action (POP from redo stack, PUSH to undo stack)
        
        This demonstrates stack operations in reverse:
        - Removes top item from redo stack
        - Pushes current state back to undo stack
        - Returns next state
        
        Returns:
            Next state, or None if nothing to redo
        """
        # Check if there's anything to redo
        if not self.redo_stack:
            return None
        
        # PUSH current state to undo stack
        if self.current_state is not None:
            self.undo_stack.append(deepcopy(self.current_state))
        
        # POP from redo stack (LIFO - get most recently undone)
        next_state = self.redo_stack.pop()
        
        # Update current state
        self.current_state = deepcopy(next_state)
        
        return self.current_state
    
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        return len(self.redo_stack) > 0
    
    def get_undo_count(self) -> int:
        """Get number of undo operations available"""
        return len(self.undo_stack)
    
    def get_redo_count(self) -> int:
        """Get number of redo operations available"""
        return len(self.redo_stack)
    
    def clear(self) -> None:
        """Clear all history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.current_state = None
    
    def get_state_description(self) -> str:
        """Get description of current history state"""
        return f"Undo: {self.get_undo_count()} | Redo: {self.get_redo_count()}"
