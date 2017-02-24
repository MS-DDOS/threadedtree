# This file is part of Threadedtree.

# Threadedtree is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Threadedtree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with threadedtree.  If not, see <http://www.gnu.org/licenses/>.

class BidirectionalIterator(object):
	"""A generic bi-directional itertaor to any object that implements the BidirectionalIterator interface. A BidirectionalIterator does have its own state, but does not copy the data or mutate
	the state of the underlying object. In essense it is simply a wrapper with a pointer to a given element in the reference object. The next() and prev() methods
	call the _next() and _prev() methods of the reference object, relievin them of the duty of calculating exactly 'how' to get the next value...just ask the
	container it wraps instead!"""

	def __init__(self, reference_object):
		"""
		Initialize a BidirectionalIterator with a ``reference_object`` that implements the BidirectionalIterator interface. Sets the current pointer to the head of the tree.

		Args:
			reference_object(object): an object that implements the BidirectionalIterator interface.

		Returns:
			None
		"""
		self.reference = reference_object
		self.current_pointer = None
		self.head()

	def __len__(self):
		return len(self.reference)

	def __repr__(self):
		return str(self.peek())

	def next(self):
		"""Moves the current pointer to the next value, in order, in the tree. After advancing the pointer, the value is returned"""
		n = self.reference._next(self.current_pointer)
		if n == None:
			return None
		else:
			self.current_pointer = n
		return self.peek()

	def prev(self):
		"""Moves the current pointer to the previous value, in order, in the tree. After advancing the pointer, the value is returned"""
		p = self.reference._prev(self.current_pointer)
		if p == None:
			return None
		else:
			self.current_pointer = p
		return self.peek()

	def has_next(self):
		"""Returns True if the current pointer is not at the tail."""
		if self.reference._next(self.current_pointer) == None:
			return False
		return True

	def has_prev(self):
		"""Returns True if the current pointer is not at the head."""
		if self.reference._prev(self.current_pointer) == None:
			return False
		return True

	def head(self):
		"""Moves the current pointer to the head and returns that value."""
		self.current_pointer = self.reference._head()
		return self.peek()

	def tail(self):
		"""Moves the current pointer to the tail and returns that value."""
		self.current_pointer = self.reference._tail()
		return self.peek()

	def peek(self):
		"""Returns the value of the current pointer."""
		return self.reference._peek(self.current_pointer)