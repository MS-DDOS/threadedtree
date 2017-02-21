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

class Tree_Node(object):
	def __init__(self, val=None, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

class Instance_Count_Tree_Node(Tree_Node):
	def __init__(self, val=None, left=None, right=None):
		super(Instance_Count_Tree_Node, self).__init__(val, left, right)
		self.instances = 1

class Threaded_Tree_Node(Tree_Node):
	def __init__(self, val=None, left=None, right=None):
		super(Threaded_Tree_Node, self).__init__(val, left, right)
		self.rthreaded = False #False indicates that the pointer on that side is a thread, not an "official" node pointer
		self.lthreaded = False
		if self.left != None:
			self.lthreaded = True
		if self.right != None:
			self.rthreaded = True

class Instance_Count_Threaded_Tree_Node(Instance_Count_Tree_Node, Threaded_Tree_Node):
	def __init__(self, val=None, left=None, right=None):
		super(Instance_Count_Threaded_Tree_Node, self).__init__(val, left, right)