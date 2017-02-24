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

	def test_next_hasnext(self):
		tree = threadedtree.ThreadedTree([])
		x = tree.bi_iter()
		assert x.next() == None
		assert x.prev() == None
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.samples)
			tree = threadedtree.ThreadedTree(test_suite)
			known = list(tree)
			x = tree.bi_iter()
			assert x.has_next() == True
			for val in known:
				assert x.peek() == val
				assert str(x) == str(val) # TEST __repr__ WHILE IM AT IT
				x.next()
			assert x.has_next() == False
			assert x.next() == None
			assert x.next() == None
			if len(x) > 0:
				assert x.prev() != None

	def test_prev_hasprev(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.samples)
			tree = threadedtree.ThreadedTree(test_suite)
			known = list(tree)
			x = tree.bi_iter()
			x.tail()
			assert x.has_prev() == True
			for val in known[::-1]:
				assert x.peek() == val
				x.prev()
			assert x.has_prev() == False
			assert x.prev() == None
			assert x.prev() == None
			if len(x) > 0:
				assert x.next() != None

	def test_special_methods(self):
		for trial in xrange(self.trials):
			test_suite = random.sample(self.bag, self.samples)
			tree = threadedtree.ThreadedTree(test_suite)
			x = tree.bi_iter()
			assert len(x) == len(tree)
		