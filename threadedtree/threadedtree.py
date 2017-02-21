'''
This file is part of Threadedtree.

Threadedtree is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Threadedtree is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with threadedtree.  If not, see <http://www.gnu.org/licenses/>.
'''

import types, treenodes

class ThreadedTree(object):
	def __init__(self, iterable=[], root=None, duplicate_strategy="stack"):
		"""Creates an empty threaded tree.

		Duplicate Strategy:
		stack - aggregate duplicate keys using an integer
		duplicate - allow duplicate nodes in tree
		"""
		self.root = root
		self._len = 0
		self.duplicate_strategy = duplicate_strategy
		if isinstance(iterable, ThreadedTree):
			for val in iterable.in_order():
				self.insert(val)
		else:
			try:
				for val in iterable:
					self.insert(val)
			except:
				raise TypeError("ThreadedTree can only be initialized with another ThreadedTree, a list or a generator.")

	def __len__(self):
		return self._len

	def __repr__(self):
		return str(list(self.in_order()))

	def __eq__(self, other):
		if isinstance(other, ThreadedTree):
			return list(self.in_order()) == list(other.in_order())
		elif isinstance(other, types.ListType):
			return list(self.in_order()) == other
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
		return hash(tuple(list(self.in_order())))

	def __add__(self, other):
		if isinstance(other, ThreadedTree):
			first = list(other.in_order())
			first.extend(self.in_order())
			return ThreadedTree(first)
		elif isinstance(other, types.ListType):
			first = list(other)
			first.extend(self.in_order())
			return ThreadedTree(first)
		else:
			return NotImplemented

	def __sub__(self, other):
		if isinstance(other, ThreadedTree):
			first = ThreadedTree(self.in_order())
			for val in other.in_order():
				first.remove(val)
			return first
		elif isinstance(other, types.ListType):
			first = ThreadedTree(self.in_order())
			for val in other:
				first.remove(val)
			return first
		else:
			return NotImplemented


	def _new_node(self, value):
		"""Seperated into a method so that we can return different types of nodes for different situations"""
		return treenodes.Threaded_Tree_Node(value)

	def insert(self, value):
		"""Inserts a new node containing 'value' into the tree."""
		self._len += 1

		if self.root == None:
			self.root = self._new_node(value)
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

	def find(self, value):
		current = self.root
		while True:
			if current.val > value:
				if current.lthreaded:
					current = current.left
				else:
					return False
			elif current.val < value:
				if current.rthreaded:
					current = current.right
				else:
					return False
			else:
				return True

	def remove(self, value):
		if self._len > 0 and self._remove(value): #take advantage of python short circuiting
			self._len -= 1
			return True
		return False

	def _remove(self, value):
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

	def in_order(self):
		if self._len > 0:
			current = self.root
			while current.lthreaded:
				current = current.left
			while current != None:
				yield current.val
				current = self._find_next_in_order(current)

	def _find_next_in_order(self, node):
		if not node.rthreaded:
			return node.right

		node = node.right

		while node.lthreaded:
			node = node.left
		return node