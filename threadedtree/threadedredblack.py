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

"""This module contains an red/black double threaded binary search tree which is optimized for in-order traversal and uses no stack or recursion to perform its functions."""

import treenodes, threadedtree, balancedtree

class ThreadedRedBlackTree(balancedtree.BalancedThreadedTree):
	def __init__(self, iterable=[], duplicate_strategy="none", root=None):
		super(ThreadedRedBlackTree, self).__init__(iterable, duplicate_strategy, root)

	def insert(self, value):
		new_node = super(ThreadedRedBlackTree, self).insert(value)
		self.balance(new_node.parent)

	def balance(self, node):

		if(node == None):
			return

		while node != self.root and node.parent.red:
			if node.parent == node.parent.parent.left:
				temp = node.parent.parent.right
				if temp != None and temp.red:
					node.parent.red = False
					temp.red = False
					node.parent.parent.red = True
					node = node.parent.parent
				else:
					if node == node.parent.right:
						node = node.parent
						self.rotate_left(node)
					node.parent.red = False
					node.parent.parent.red = True
					self.rotate_right(node.parent.parent)
			else:
				temp = node.parent.parent.left
				if temp != None and temp.red:
					node.parent.red = False
					temp.red = False
					node.parent.parent.red = True
					node = node.parent.parent
				else:
					if node.lthreaded and node == node.parent.left:
						node = node.parent
						self.rotate_right(node)
					node.parent.red = False
					node.parent.parent.red = True
					self.rotate_left(node.parent.parent)
		self.root.red = False

	def _new_node(self, value):
		"""Private method that returns a new tree node corresponding to the selected duplicate strategy"""
		return treenodes.Threaded_Red_Black_Tree_Node(value)
