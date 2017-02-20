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
	def __init__(self, value):
		super(Instance_Count_Tree_Node, self).__init__(value)
		self.instances = 1

class Threaded_Tree_Node(Tree_Node):
	def __init__(self, value):
		super(Threaded_Tree_Node, self).__init__(value)
		self.rthreaded = False #indicates that the right pointer is to a predescessor, not a descendant
		self.lthreaded = False

class Instance_Count_Threaded_Tree_Node(Instance_Count_Tree_Node, Threaded_Tree_Node):
	def __init__(self, value):
		super(Instance_Count_Threaded_Tree_Node, self).__init__(value)