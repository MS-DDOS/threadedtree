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

"""This module contains an unbalanced double threaded binary search tree which is optimized for in-order traversal and uses no stack or recursion to perform its functions."""

import types, treenodes, bidirectionaliterator

class ThreadedTree(object):
	"""A carefully implemented unbalanced double threaded binary search tree. Threaded binary search trees are optimized for in-order (ascending or descending) traversal and use no stack or recursion to perform its functions."""
	def __init__(self, iterable=[], duplicate_strategy="none", root=None):
		"""
		Creates and empty unbalanced double threaded binary search tree.

	    A tree can be intialized using a valid python iterable object as a parameter to the constructor.

	    Args:
			iterable(collections.Iterable): A python iterable used to initialize an empty tree. Items are added to tree in order of iteration (i.e a sorted list will create a tree that is the equivalent of a doubly linked list).
			duplicate_strategy(str):
				``none`` - do not allow duplicates.
				``stack`` - aggregate duplicate keys using an integer. (not yet implemented)
				``duplicate`` - allow duplicate nodes in tree. (not yet implemented)
			root(Threaded_Tree_Node): A Threaded_Tree_Node to assign to ``root``. Could be useful if you assembled a tree manually and wanted to mutate it via the tree interface.

		Returns:
			None

		"""
		if not isinstance(root, treenodes.Threaded_Tree_Node) and root != None:
			raise TypeError("You can only initialize the root of a ThreadedTree with an object with a base class of Threaded_Tree_Node, or None.")
		self.root = self.head = self.tail = root
		self._len = 0
		self.duplicate_strategy = duplicate_strategy
		if isinstance(iterable, ThreadedTree):
			for val in iterable:
				self.insert(val)
		else:
			try: # This is more broad than specifically testing for collections.Iterable
				for val in iterable:
					self.insert(val)
			except:
				raise TypeError("ThreadedTree can only be initialized with another ThreadedTree or other Python iterable.")

	def __len__(self):
		return self._len

	def __repr__(self):
		return str(list(self))

	def __eq__(self, other):
		if isinstance(other, ThreadedTree):
			return list(self) == list(other)
		elif isinstance(other, types.ListType):
			return list(self) == other
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def __lt__(self, other):
		return NotImplemented

	def __le__(self, other):
		return NotImplemented

	def __gt__(self, other):
		return NotImplemented

	def __ge__(self, other):
		return NotImplemented

	def __hash__(self):
		return hash(tuple(list(self)))

	def __add__(self, other):
		if isinstance(other, ThreadedTree):
			first = list(other)
			first.extend(self)
			return ThreadedTree(first)
		elif isinstance(other, types.ListType):
			first = list(other)
			first.extend(self)
			return ThreadedTree(first)
		else:
			return NotImplemented

	def __sub__(self, other):
		if isinstance(other, ThreadedTree):
			first = ThreadedTree(self)
			for val in other:
				first.remove(val)
			return first
		elif isinstance(other, types.ListType):
			first = ThreadedTree(self)
			for val in other:
				first.remove(val)
			return first
		else:
			return NotImplemented

	def __iter__(self):
		if self._len > 0:
			current = self.root
			while current.lthreaded:
				current = current.left
			while current != None:
				yield current.val
				if not current.rthreaded:
					current = current.right
				else:
					node = current.right
					while node.lthreaded:
						node = node.left
					current = node

	def __contains__(self, item):
		current = self.root
		while True:
			if current.val > item:
				if current.lthreaded:
					current = current.left
				else:
					return False
			elif current.val < item:
				if current.rthreaded:
					current = current.right
				else:
					return False
			else:
				return True

	def insert(self, value):
		"""
		Inserts a new node containing ``value`` into the tree.

		Args:
			value (object): A python object that implements ``__cmp__()`` or rich comparisons, to be inserted into the tree.

		Returns:
			None
		"""
		if not self._implements_comparisons(value):
			return

		self._len += 1

		if self.root == None:
			self.root = self._new_node(value)
			self.head = self.tail = self.root
			return

		current = self.root
		left = False
		right = False

		while True:
			if current.val > value:
				if not current.lthreaded:
					#Add as left child
					left = True
					break
				else:
					current = current.left
			elif current.val < value:
				if not current.rthreaded:
					right = True
					break
				else:
					current = current.right
			else:
				break #allows equal cases to be skipped and a stub in case that behavior should change

		if left:
			new_node = self._new_node(value)
			new_node.left = current.left
			current.left = new_node
			new_node.lthreaded = current.lthreaded
			current.lthreaded = True
			new_node.right = current
		elif right:
			new_node = self._new_node(value)
			new_node.right = current.right
			current.right = new_node
			new_node.rthreaded = current.rthreaded
			current.rthreaded = True
			new_node.left = current

		try:
			if new_node.left == None:
				self.head = new_node
			elif new_node.right == None:
				self.tail = new_node
		except UnboundLocalError:
			pass

	def remove(self, value):
		"""
		Removes a node containing ``value`` from the tree.
		
		Args:
			value (object): A python object that implements ``__cmp__()`` or rich comparisons, to be removed from the tree.

		Returns:
			boolean: operation success
		"""
		if not self._implements_comparisons(value):
			return False
		if self._len > 0 and self._remove(value): #take advantage of python short circuiting
			self._len -= 1
			return True
		return False

	def bi_iter(self):
		"""
		Returns a BidrectionalIterator to the tree, allowing a user to step through the tree in either the forward or backward direction.

		Returns:
			BidirectionalIterator: iterator allowing forward or backward traversal of the underlying tree.
		""" 
		return bidirectionaliterator.BidirectionalIterator(self)

	def reverse(self):
		"""
		Returns a generator that yields values from the tree in reverse order, from the tail to the head of the tree.

		Returns:
			Generator : yields values from the tree in reverse order.
		"""
		if self._len > 0:
			current = self.root
			while current.rthreaded:
				current = current.right
			while current != None:
				yield current.val
				if not current.lthreaded:
					current = current.left
				else:
					node = current.left
					while node.rthreaded:
						node = node.right
					current = node

	def _next(self, pointer):
		""" Private method that returns the next value in the tree, in order, given a random pointer. The time complexity of this method is O(n)."""
		current = pointer
		while current != None:
			if current != pointer:  # Pretty likely this is Theta(1)
				return current
			if not current.rthreaded:
				current = current.right
			else:
				node = current.right
				while node.lthreaded:
					node = node.left
				current = node

	def _prev(self, pointer):
		""" Private method that returns the previous value in the tree, in order, given a random pointer. The time complexity of this method is O(n)."""
		current = pointer
		while current != None:
			if current != pointer: # Pretty likely this is Theta(1)
				return current
			if not current.lthreaded:
				current = current.left
			else:
				node = current.left
				while node.rthreaded:
					node = node.right
				current = node

	def _head(self):
		""" Private method that returns the head of the tree in constant time."""
		return self.head

	def _tail(self):
		""" Private method that returns the tail of the tree in constant time."""
		return self.tail

	def _peek(self, pointer):
		try:
			return pointer.val
		except:
			return pointer

	def _implements_comparisons(self, value):
		"""Private method that determines if value implements either __cmp__ or both __lt__ and __gt__"""
		if not hasattr(value, "__cmp__") and not (hasattr(value, "__lt__") or hasattr(value, "__gt__")):
			return False
		return True

	def _new_node(self, value):
		"""Private method that returns a new tree node corresponding to the selected duplicate strategy"""
		return treenodes.Threaded_Tree_Node(value)

	def _remove(self, value):
		"""Private method that performs actual removal of value."""
		if value == self.root.val:
			return self._delete_root()

		current = parent = self.root
		while True:
			if current.val > value:
				if current.lthreaded:
					parent = current
					current = current.left
				else:
					return False
			elif current.val < value:
				if current.rthreaded:
					parent = current
					current = current.right
				else:
					return False
			else:
				break
		if current.lthreaded == False and current.rthreaded == False:
			return self._delete_with_no_children(current)
		elif current.lthreaded == True and current.rthreaded == True:
			return self._delete_with_both_children(current, parent)
		elif current.lthreaded:
			return self._delete_with_left_child(current, parent)
		else:
			return self._delete_with_right_child(current, parent)

	def _delete_root(self):
		"""Private method that provides functionality for removing the ``root`` from the tree."""
		if self._len == 1:
			self.root = None
			return True
		if self.root.right == None:
			if not self.root.left.rthreaded:
				self.root.left.right = None
			else:
				far_right = self.root.left
				while far_right.right != self.root:
					far_right = far_right.right
				far_right.right = None
			new_root = self.root.left
			del self.root
			self.root = new_root
			return True
		elif not self.root.left:
			if not self.root.right.lthreaded:
				self.root.right.left = None
			else:
				far_left = self.root.right
				while far_left.left != self.root:
					far_left = far_left.left
				far_left.left = None
			new_root = self.root.right
			del self.root
			self.root = new_root
			return True

		new_root = self.root.right
		far_left = new_root
		while far_left.left != self.root:
			far_left = far_left.left

		far_right = self.root.left
		while far_right.right != self.root:
			far_right = far_right.right


		far_left.lthreaded = True
		far_left.left = self.root.left
		far_right.right = far_left
		del self.root
		self.root = new_root
		return True

	def _delete_with_both_children(self, current, parent):
		"""Private method that provides functionality for removing a node with neither right or left threads from the tree."""
		on_right = False
		if parent.right == current:
			on_right = True

		far_left = current.right
		while far_left.left != current:
			far_left = far_left.left
		far_left.left = current.left
		far_left.lthreaded = current.lthreaded

		far_right = current.left
		while far_right.right != current:
			far_right = far_right.right

		far_right.right = far_left
		
		if on_right:
			parent.right = current.right
		else:
			parent.left = current.right
		del current
		return True

	def _delete_with_no_children(self, current):
		"""Private method that provides functionality for removing a node with both right and left threads from the tree."""
		if current.left == None:
			current.right.lthreaded = False
			current.right.left = None
			del current
			return True
		elif current.right == None:
			current.left.rthreaded = False
			current.left.right = None
			del current
			return True
		else:
			if current.left.right == current:
				current.left.rthreaded = False
				current.left.right = current.right
				del current
				return True
			else:
				current.right.lthreaded = False
				current.right.left = current.left
				del current
				return True

	def _delete_with_left_child(self, current, parent):
		"""Private method that provides functionality for removing a node with a right thread from the tree."""
		far_right = current.left
		while far_right.right != None and far_right.right != current:
			far_right = far_right.right
		far_right.right = current.right

		on_right = False
		if parent.right == current:
			on_right = True

		if on_right:
			parent.right = current.left
		else:
			parent.left = current.left

		del current
		return True

	def _delete_with_right_child(self, current, parent):
		"""Private method that provides functionality for removing a node with a left thread from the tree."""
		far_left = current.right
		while far_left.left != None and far_left.left != current:
			far_left = far_left.left
		far_left.left = current.left

		on_right = False
		if parent.right == current:
			on_right = True

		if on_right:
			parent.right = current.right
		else:
			parent.left = current.right
		del current
		return True