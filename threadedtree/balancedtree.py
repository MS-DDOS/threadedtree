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

class BalancedThreadedTree(threadedtree.ThreadedTree):
	def __init__(self, iterable=[], duplicate_strategy="none", root=None):
		super(BalancedThreadedTree, self).__init__(iterable, duplicate_strategy, root)

	def balance(self, node):
		pass

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
