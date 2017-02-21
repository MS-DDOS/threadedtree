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