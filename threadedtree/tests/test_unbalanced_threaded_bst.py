from unittest import TestCase

import random
import threadedtree

class TestUnbalancedThreadedBST(TestCase):

	@classmethod
	def setup_class(self):
		self.upper_bound = 1000
		self.samples = 100 #This value MUST be greater than self.small_samples
		self.small_samples = 10
		assert self.samples > self.small_samples
		self.trials = 100
		self.bag = range(self.upper_bound)

	@classmethod
	def tearDown(self):
		pass
		
	def test_insert(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.samples)
			tree = threadedtree.ThreadedTree()
			for sample in test_suite:
				tree.insert(sample)
			test_suite.sort()
			assert test_suite == list(tree.in_order())

	def test_insert_with_duplicates(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.samples)
			test_suite.extend(random.sample(test_suite, random.randint(1, len(test_suite)))) #add some duplicates
			tree = threadedtree.ThreadedTree()
			for sample in test_suite:
				tree.insert(sample)
			test_suite.sort()
			assert test_suite != list(tree.in_order())

	def test_create_with_iterable(self):
		import copy
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.samples)
			tree = threadedtree.ThreadedTree(test_suite)
			another_tree = threadedtree.ThreadedTree(tree)
			test_suite.sort()
			assert test_suite == list(tree.in_order())
			assert test_suite == list(another_tree.in_order())
		try:
			tree = threadedtree.ThreadedTree(1) #Try to initialize with non-iterable
		except TypeError:
			pass

	def test_delete(self):
		import copy
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.samples)
			tree = threadedtree.ThreadedTree(test_suite)
			test_suite.sort()
			vals_to_delete = copy.deepcopy(test_suite)
			random.shuffle(vals_to_delete)
			for val_to_delete in vals_to_delete:
				test_suite.remove(val_to_delete)
				tree.remove(val_to_delete)
				assert test_suite == list(tree.in_order())
		# Have to explicitly test the case where the value being deleted is not in the tree and is greater than
		# the leftmost child of the right subtree.
		tree = threadedtree.ThreadedTree([12,25,30,22])
		assert tree.remove(23) == False

	def test_find(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.samples)
			not_included = random.sample(test_suite, self.small_samples)
			for val in not_included:
				test_suite.remove(val)
			tree = threadedtree.ThreadedTree(test_suite)
			for sample in test_suite:
				assert tree.find(sample) == True
			for sample in not_included:
				print test_suite, sample
				assert tree.find(sample) == False

	def test_len(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.small_samples)
			tree = threadedtree.ThreadedTree(test_suite)
			assert len(tree) == len(test_suite)
			vals_to_delete = random.sample(test_suite,random.randint(1,len(test_suite)))
			for val in vals_to_delete:
				tree.remove(val)
				test_suite.remove(val)
				assert len(tree) == len(test_suite)

	def test_repr(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.small_samples)
			tree = threadedtree.ThreadedTree(test_suite)
			test_suite.sort()
			assert str(test_suite) == str(tree)

	def test_add(self):
		for trial in xrange(5):
			test_suite_1 = random.sample(self.bag, self.small_samples)
			test_suite_2 = random.sample(self.bag, self.small_samples)
			test_suite_3 = test_suite_1 + test_suite_2
			tree1 = threadedtree.ThreadedTree(test_suite_1)
			tree2 = threadedtree.ThreadedTree(test_suite_2)
			tree3 = threadedtree.ThreadedTree(test_suite_3)
			assert tree1 + tree2 == tree3
			assert tree1 + test_suite_2 == tree3
		try:
			tree1 + {} #have to test the "NotImplemented" branch, so add tree to anything other than tree or list
		except TypeError:
			pass

	def test_sub(self):
		for trial in xrange(5):
			test_suite_1 = random.sample(self.bag, self.samples)
			test_suite_2 = random.sample(self.bag, self.small_samples)
			test_suite_3 = list(test_suite_1)
			for val in test_suite_2:
				try:
					test_suite_3.remove(val)
				except ValueError:
					continue
			tree1 = threadedtree.ThreadedTree(test_suite_1)
			tree2 = threadedtree.ThreadedTree(test_suite_2)
			tree3 = threadedtree.ThreadedTree(test_suite_3)
			assert tree1 - tree2 == tree3
			assert tree1 - test_suite_2 == tree3
		try:
			tree1 - {} #have to test the "NotImplemented" branch, so add tree to anything other than tree or list
		except TypeError:
			pass

	def test_comparisons(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.small_samples)
			tree1 = threadedtree.ThreadedTree(test_suite)
			random.shuffle(test_suite)
			tree2 = threadedtree.ThreadedTree(test_suite)
			tree3 = threadedtree.ThreadedTree(test_suite[1:])
			assert tree1 == tree2
			assert tree1 != tree3
			assert tree2 != tree3
			test_suite.sort()
			assert tree1 == test_suite
			assert (tree1 == {}) == False
			# We are not responsible for the following comparisons so we just call them for coverage purposes
			tree1 < tree1
			tree1 <= tree1
			tree1 > tree1
			tree1 >= tree1

	def test_hash(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.small_samples)
			tree = threadedtree.ThreadedTree(test_suite)
			d = {}
			d[tree] = None