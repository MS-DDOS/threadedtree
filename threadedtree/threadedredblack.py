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
		self._balance_insert(self.access)

	def remove(self, value):
		if not self._implements_comparisons(value):
			return False
		if self._len > 0 and self._remove(value): #take advantage of python short circuiting
			self._len -= 1
			return True
		return False

	def _remove(self, value):
		"""Private method that performs actual removal of value."""
		if value == self.root.val:
			self.access = None
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
			if self._delete_with_no_children(current):
				NIL = self._new_node(None)
				NIL.parent = parent
				NIL.red = False
				self._balance_remove(NIL)
				return True
			return False
		elif current.lthreaded == True and current.rthreaded == True:
			return self._delete_with_both_children(current, parent)
		elif current.lthreaded:
			if self._delete_with_left_child(current, parent):
				self.access.parent = parent
				self.access.red = False
				return True
			return False
		else:
			if self._delete_with_right_child(current, parent):
				self.access.parent = parent
				self.access.red = False
				return True
			return False

	def _balance_remove(self, node):
		# Case 1
		if node.parent == None:
			print "Case #1"
			return
		sibling = self._sibling(node)
		print "SIBLING IS",sibling.val
		# Case 2
		if sibling.red:
			print "Case #2"
			if sibling == sibling.parent.left:
				self.rotate_left(sibling)
			else:
				self.rotate_right(sibling)
			sibling = self._sibling(node)
		# Case 3
		if node.parent.red == False and sibling.red == False and (sibling.lthreaded and sibling.left.red == False) and (sibling.rthreaded and sibling.right.red == False):
			sibling.red = True
			print "Case #3"
			self._balance_remove(node.parent)
			return
		# Case 4
		if node.parent.red == True and sibling.red == False and (sibling.left != None and sibling.left.red == False) and (sibling.right != None and sibling.right.red == False):
			sibling.red = True
			node.parent.red = True
			print "Case #4"
			return
		# Case 5
		if sibling.red == False:
			if node == node.parent.left and (sibling.right != None and sibling.right.red == False) and (sibling.left != None and sibling.left.red == True):
				print "Case #5"
				self.rotate_left(sibling.left)
			elif node == node.parent.right and (sibling.left != None and sibling.left.red == False) and (sibling.right != None and sibling.right.red == True):
				print "Case #5"
				self.rotate_right(sibling.right)
			sibling = self._sibling(node)
		# Case 6
		if sibling == sibling.parent.left:
			print "Case #6 R"
			sibling.parent.red = False
			sibling.red = True
			self.rotate_right(sibling.parent)
		else:
			print "Case #6 L"
			sibling.parent.red = False
			sibling.red = True
			self.rotate_left(sibling.parent)
		print "NODE Is",node.val, "Parent is",node.parent.val
		sibling = self._sibling(node.parent)
		print "Empty node's parent's parent", node.parent.parent.val
		print "New sibling is",sibling.val
		if sibling:
			sibling.red = False

	def _sibling(self, node):
		print "FINDING SIBLING FOR",node.val
		if node == self.root:
			return None
		elif node.parent.val > self.root.val: #This is the problem. Probably need to link NIL node up for a second to make it all work...
			return node.parent.right
		else:
			return node.parent.left

	def _balance_insert(self, node):
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
		print "Rotating left..."
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

	def rotate_right(self, node):
		print "Rotating right..."
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

	def _new_node(self, value):
		"""Private method that returns a new tree node corresponding to the selected duplicate strategy"""
		return treenodes.Threaded_Red_Black_Tree_Node(value)

