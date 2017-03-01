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

import treenodes, threadedtree

class ThreadedAVLTree(threadedtree.ThreadedTree):
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
			if(self.height_of_node(node.left.left) > self.height_of_node(node.left.right)):
				node = self.rotate_right(node)
			else:
				node = self.rotate_left_right(node)

		elif(node.balance == 2):
			if(self.height_of_node(node.right.right) > self.height_of_node(node.right.left)):
				node = self.rotate_left(node)
			else:
				node = self.rotate_right_left(node)

		print(node.balance)
		print(node.val)
		# if(node.parent != None):
		# 	self.balance(node.parent)
		# else:
		# 	self.root = node
		self.root = node

	def rotate_right_left(self, node):
		node.right = self.rotate_right(node.right)
		return self.rotate_left(node)

	def rotate_left_right(self, node):
		node.left = self.rotate_left(node.left)
		return self.rotate_right(node)

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

	def calculate_balance(self, node):
		return self.height_of_node(node.right) - self.height_of_node(node.left)

	def height_of_node(self, node):
		return (0 if node == None else 1+max((self.height_of_node(node.left) if node.lthreaded else 0), (self.height_of_node(node.right) if node.rthreaded else 0)))

	def _new_node(self, value):
		"""Private method that returns a new tree node corresponding to the selected duplicate strategy"""
		return treenodes.Threaded_AVL_Tree_Node(value)
