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

from unittest import TestCase

import random
from threadedtree import treenodes

class TestTreeNodes(TestCase):

	@classmethod
	def setup_class(self):
		pass

	@classmethod
	def tearDown(self):
		pass

	def test_base(self):
		x = treenodes.Tree_Node()
		y = treenodes.Tree_Node(3,treenodes.Tree_Node(5), treenodes.Tree_Node(7))
		assert x.left == None
		assert x.right == None
		assert x.val == None
		assert y.val == 3
		assert y.left.val == 5
		assert y.right.val == 7

	def test_threaded_base(self):
		x = treenodes.Threaded_Tree_Node()
		y = treenodes.Threaded_Tree_Node(3,treenodes.Tree_Node(5), treenodes.Tree_Node(7))
		assert x.left == None
		assert x.right == None
		assert x.val == None
		assert x.rthreaded == False
		assert x.lthreaded == False
		assert y.val == 3
		assert y.left.val == 5
		assert y.right.val == 7
		assert y.rthreaded == True
		assert y.lthreaded == True

	def test_instance_count_base(self):
		x = treenodes.Instance_Count_Tree_Node()
		y = treenodes.Instance_Count_Tree_Node(3, treenodes.Instance_Count_Tree_Node(5), treenodes.Instance_Count_Tree_Node(7))
		assert x.left == None
		assert x.right == None
		assert x.val == None
		assert x.instances == 1
		assert y.val == 3
		assert y.left.val == 5
		assert y.right.val == 7
		assert y.instances == 1

	def test_threaded_instance_count_base(self):
		x = treenodes.Instance_Count_Threaded_Tree_Node()
		y = treenodes.Instance_Count_Threaded_Tree_Node(3, treenodes.Instance_Count_Threaded_Tree_Node(5), treenodes.Instance_Count_Threaded_Tree_Node(7))
		assert x.left == None
		assert x.right == None
		assert x.val == None
		assert x.rthreaded == False
		assert x.lthreaded == False
		assert x.instances == 1
		assert y.val == 3
		assert y.left.val == 5
		assert y.right.val == 7
		assert y.rthreaded == True
		assert y.lthreaded == True
		assert y.instances == 1