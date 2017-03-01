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

import treenodes, threadedtree

class ThreadedRedBlackTree(threadedtree.ThreadedTree):
	def __init__(self, iterable=[], duplicate_strategy="none", root=None):
		super(ThreadedRedBlackTree, self).__init__(iterable, duplicate_strategy, root)

	def insert(self, value):
		super(ThreadedRedBlackTree, self).insert(value)
		self.balance(self.access)

	def balance(self, node):
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

	def rotate_left(self, node):
		temp = node.right
		if temp.lthreaded:
			node.right = temp.left
		else:
			node.right = temp
			node.rthreaded = False

		if temp.lthreaded and temp.left != None:
			temp.left.parent = node

		temp.parent = node.parent
		if node.parent == None:
			self.root = temp
		elif node == node.parent.left:
			node.parent.left = temp
		else:
			node.parent.right = temp
		temp.left = node
		temp.lthreaded = True
		node.parent = temp
		return temp

	def rotate_right(self, node):
		temp = node.left
		if temp.rthreaded:
			node.left = temp.right
		else:
			node.left = temp
			node.lthreaded = False

		if temp.rthreaded and temp.right != None:
			temp.right.parent = node

		temp.parent = node.parent
		if node.parent == None:
			self.root = temp
		elif node == node.parent.right:
			node.parent.right = temp
		else:
			node.parent.left = temp
		temp.right = node
		temp.rthreaded = True
		node.parent = temp
		return temp

	def _new_node(self, value):
		"""Private method that returns a new tree node corresponding to the selected duplicate strategy"""
		return treenodes.Threaded_Red_Black_Tree_Node(value)
