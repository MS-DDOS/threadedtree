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

"""This module contains an AVL double threaded binary search tree which is optimized for in-order traversal and uses no stack or recursion to perform its functions."""

import treenodes, threadedtree, balancedtree

class ThreadedAVLTree(balancedtree.BalancedThreadedTree):
	def __init__(self, iterable=[], duplicate_strategy="none", root=None):
		super(ThreadedAVLTree, self).__init__(iterable, duplicate_strategy, root)

	def insert(self, value):
		new_node = super(ThreadedAVLTree, self).insert(value)
		self.balance(new_node.parent)

	def balance(self, node):

		if(node == None):
			return

		node.balance = self.calculate_balance(node)

		if(node.balance == -2):
			(left, right) = self.children_heights(node.left)
			if(left > right):
				node = self.rotate_right(node)
			else:
				node = self.rotate_left_right(node)

		elif(node.balance == 2):
			(left, right) = self.children_heights(node.right)
			if(right > left):
				node = self.rotate_left(node)
			else:
				node = self.rotate_right_left(node)

		if(node.parent != None):
			self.balance(node.parent)
		else:
			self.root = node

	def children_heights(self, node):
		left = 0
		if(node.lthreaded):
			left = self.height_of_node(node.left)
		right = 0
		if(node.rthreaded):
			right = self.height_of_node(node.right)
		return(left, right)

	def rotate_right_left(self, node):
		node.right = self.rotate_right(node.right)
		return self.rotate_left(node)

	def rotate_left_right(self, node):
		node.left = self.rotate_left(node.left)
		return self.rotate_right(node)

	def calculate_balance(self, node):
		return (0 if not node.rthreaded else self.height_of_node(node.right)) - (0 if not node.lthreaded else self.height_of_node(node.left))

	def height_of_node(self, node):
		if node == None:
			return 0

		return 1 + max((0 if not node.lthreaded else self.height_of_node(node.left)), \
			   (0 if not node.rthreaded else self.height_of_node(node.right)))


	def _new_node(self, value):
		"""Private method that returns a new tree node corresponding to the selected duplicate strategy"""
		return treenodes.Threaded_AVL_Tree_Node(value)
