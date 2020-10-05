import queue
import time
import sys
import math
import psutil
import heapq

def bfs(root, goal):
	start_time = time.time()
	explored = dict({})
	frontier = queue.Queue(362880)
	frontier.put_nowait(tuple([int(root), None, 0, None]))
	explored[int(root)] = list([tuple([None, None]), False])
	max_depth = depth = 0
	done = False
	
	while not done and not frontier.empty():
		currentState = frontier.get_nowait()
		#print("currentState: ", currentState)
		depth = currentState[2]

		if currentState[0] == goal:
			done = True
			path = getPath(currentState[0], explored, root)
			countExpanded = getCountExpanded(explored)
			output(path, len(path), countExpanded, depth, max_depth, time.time() - start_time)
		else:
			count = 0
			newStates = getNewStates(currentState[0], depth + 1)

			for state in newStates:
				if state[0] not in explored:
					frontier.put_nowait(state)
					explored[state[0]] = list([tuple([state[1], state[3]]), False])
					count += 1

			explored[currentState[0]][1] = True
			if count > 0 and depth + 1 > max_depth:
				max_depth = depth + 1
			#print("newStates: ", newStates)
			#print("frontier: ", frontier.qsize())
			#print("explored: ", len(explored))

def dfs(root, goal):
	start_time = time.time()
	explored = dict({})
	frontier = list()
	frontier.append(tuple([int(root), None, 0, None]))
	explored[int(root)] = list([tuple([None, None]), False])
	max_depth = depth = 0
	done = False
	
	while not done and len(frontier) > 0:
		currentState = frontier.pop()
		depth = currentState[2]
		
		if currentState[0] == goal:
			done = True
			path = getPath(currentState[0], explored, root)
			countExpanded = getCountExpanded(explored)
			output(path, len(path), countExpanded, depth, max_depth, time.time() - start_time)
		else:
			count = 0
			newStates = getNewStates(currentState[0], depth + 1)
			
			for i in range(len(newStates) - 1, -1, -1):
				if newStates[i][0] not in explored:
					frontier.append(newStates[i])
					explored[newStates[i][0]] = list([tuple([newStates[i][1], newStates[i][3]]), False])
					count += 1
			if count > 0 and depth + 1 > max_depth:
				max_depth = depth + 1
			explored[currentState[0]][1] = True


def ast(root, goal):
	start_time = time.time()
	rootElement = HeapElement(getStateDistance(int(root)), tuple([int(root), None, 0, None]) )
	frontier = Heap(rootElement)
	explored = { int(root): list([tuple([None, None]), False, rootElement]) }
	#HeapElement.setFrontier(frontier)
	#HeapElement.setExplored(explored)
	max_depth = depth = 0
	done = False

#HEAP ELEMENT: [(distance, (state, direction, depth, previous state)), index]

	while not done and not frontier.isEmpty():
		currentState = frontier.extractMin()
#		print("frontier = ", frontier)
#		print("currentState = ", currentState)
		depth = currentState.data[2]
	
		if currentState.data[0] == goal:
			done = True
			path = getPath(currentState.data[0], explored, root)
			countExpanded = getCountExpanded(explored)
			output(path, len(path), countExpanded, depth, max_depth, time.time() - start_time)
		else:
			explored[currentState.data[0]][1] = True
			count = 0
			newStates = getNewStates(currentState.data[0], depth + 1)

			for state in newStates:
				if state[0] not in explored:
					distance = getStateDistance(state[0]) + depth + 1
					heapElement = HeapElement(distance, state)
					#heapq.heappush(frontier, heapElement)
					frontier.insert(heapElement)
					explored[state[0]] = list([tuple([state[1], state[3]]), False, heapElement])
					#EXPLORED ELEMENT: state -> [(direction, depth), expanded, heapElement]
					count += 1
				elif explored[state[0]][1] == False:
					newDistance = getStateDistance(state[0]) + depth + 1
					newHeapElement = HeapElement(distance, state)
					if newHeapElement < explored[state[0]][2]:
						print(newHeapElement, " < ", explored[state[0]][2])
						frontier.decreaseKey(explored[state[0]][2].index, newHeapElement)
						explored[state[0]] = list([tuple([state[1], state[3]]), False, newHeapElement])
						count += 1
			
			if count > 0 and depth + 1 > max_depth:
				max_depth = depth + 1



def getPath(solution, explored, root):
	path = []
	key = solution

	while key != int(root):
		path.append(explored[key][0][0])
		key = explored[key][0][1]
	path.reverse()
	return path
	
def getCountExpanded(explored):
	count = 0
	for value in explored.values():
		if value[1] == True:
			count += 1
	return count

def output(path, cost, countExpanded, depth, max_depth, time_elapsed):
	with open('output.txt','w') as out:
		out.write("path_to_goal: " + str(path) + \
				  "\ncost_of_path: " + str(cost) + \
				  "\nnodes_expanded: " + str(countExpanded) + \
				  "\nsearch_depth: " + str(depth) + \
				  "\nmax_search_depth: " + str(max_depth) + \
				  "\nrunning_time: " + str(time_elapsed) + \
				  "\nmax_ram_usage: " + str(psutil.Process().memory_info().rss * 0.000001))

def getNewStates(currentState, depth):
	newStates = []
	currState = str(currentState).zfill(9)
	pos = currState.index('0') + 1
	rem = pos % 3
	
	if rem == 1:
		if pos < 4:			# position = 1
			newStates.append(tuple([getNewState(currState,1,4), 'Down', depth, currentState])) #swap with 4, Down
			newStates.append(tuple([getNewState(currState,1,2), 'Right', depth, currentState])) #swap with 2, Right
		elif pos < 7:		# position = 4
			newStates.append(tuple([getNewState(currState,4,1), 'Up', depth, currentState])) #swap with 1, Up
			newStates.append(tuple([getNewState(currState,4,7), 'Down', depth, currentState])) #swap with 7, Down
			newStates.append(tuple([getNewState(currState,4,5), 'Right', depth, currentState])) #swap with 5, Right
		else:				# position = 7
			newStates.append(tuple([getNewState(currState,7,4), 'Up', depth, currentState])) #swap with 4, Up
			newStates.append(tuple([getNewState(currState,7,8), 'Right', depth, currentState])) #swap with 8, Right
	elif rem == 2:
		if pos < 4:			# position = 2
			newStates.append(tuple([getNewState(currState,2,5), 'Down', depth, currentState])) #swap with 5, Down
			newStates.append(tuple([getNewState(currState,2,1), 'Left', depth, currentState])) #swap with 1, Left
			newStates.append(tuple([getNewState(currState,2,3), 'Right', depth, currentState])) #swap with 3, Right
		elif pos < 7:		# position = 5
			newStates.append(tuple([getNewState(currState,5,2), 'Up', depth, currentState])) #swap with 2, Up
			newStates.append(tuple([getNewState(currState,5,8), 'Down', depth, currentState])) #swap with 8, Down
			newStates.append(tuple([getNewState(currState,5,4), 'Left', depth, currentState])) #swap with 4, Left
			newStates.append(tuple([getNewState(currState,5,6), 'Right', depth, currentState])) #swap with 6, Right
		else:				# position = 8
			newStates.append(tuple([getNewState(currState,8,5), 'Up', depth, currentState])) #swap with 5, Up
			newStates.append(tuple([getNewState(currState,8,7), 'Left', depth, currentState])) #swap with 7, Left
			newStates.append(tuple([getNewState(currState,8,9), 'Right', depth, currentState])) #swap with 9, Right
	elif rem == 0:
		if pos < 4:			# position = 3
			newStates.append(tuple([getNewState(currState,3,6), 'Down', depth, currentState])) #swap with 6, Down
			newStates.append(tuple([getNewState(currState,3,2), 'Left', depth, currentState])) #swap with 2, Left
		elif pos < 7:		# position = 6
			newStates.append(tuple([getNewState(currState,6,3), 'Up', depth, currentState])) #swap with 3, Up
			newStates.append(tuple([getNewState(currState,6,9), 'Down', depth, currentState])) #swap with 9, Down
			newStates.append(tuple([getNewState(currState,6,5), 'Left', depth, currentState])) #swap with 5, Left
		else:				# position = 9
			newStates.append(tuple([getNewState(currState,9,6), 'Up', depth, currentState])) #swap with 6, Up
			newStates.append(tuple([getNewState(currState,9,8), 'Left', depth, currentState])) #swap with 8, Left
	else:
		print("invalid value for remainder, exiting")
		sys.exit()
	return newStates

def getNewState(currState, pos, newPos):
	if pos < newPos:
		return int(currState[:(pos - 1)] + currState[newPos - 1] + currState[pos:(newPos - 1)] + currState[pos - 1] + (currState[newPos:] if newPos < len(currState) else ''))
	elif newPos < pos:
		return int(currState[:(newPos - 1)] + currState[pos - 1] + currState[newPos:(pos - 1)] + currState[newPos - 1] + (currState[pos:] if pos < len(currState) else ''))
	else:
		print("current and target positions cannot be equal, exiting")
		sys.exit()

def getStateDistance(state):
	state = str(state).zfill(9)
	distance = 0
	for i in range(0, len(state)):
		distance += getNumberDistance(int(state[i]), i)
	return distance

def getNumberDistance(number, index):
	if number == 0:
		return 0
	else:
		numberRow = math.floor(number / 3)
		numberCol = number % 3
		indexRow = math.floor(index / 3)
		indexCol = index % 3
		
		return max(numberCol, indexCol) - min(numberCol, indexCol) + \
			   max(numberRow, indexRow) - min(numberRow, indexRow)


#HEAP ELEMENT: [(distance, (state, direction, depth, previous state)), index]
#@total_ordering
class HeapElement:
	frontier = None
	explored = None
	
	def setFrontier(frontier):
		HeapElement.frontier = frontier
	def setExplored(explored):
		HeapElement.explored = explored
	
	def __init__(self, distance, data):
		self.distance = distance
		self.data = data
		self.index = -1
	
	def __lt__(self, element):
		if self == element:
			return False
		if element == None:
			return True
		if self.distance < element.distance: # compare distance from goal
			return True
		if self.distance > element.distance:
			return False
		if self.data[2] < element.data[2]: # compare depth
			return True
		if self.data[2] > element.data[2]:
			return False
		udlrResult = HeapElement.udlrCompare(self.data[1], element.data[1]) # compare udlr order
		if udlrResult < 0:
			return True
		if udlrResult > 0:
			return False
		if self.data[0] < element.data[0]: # compare states
			return True
		return False
	
	def __str__(self):
		return "(" + str(self.distance) + ", " + str(self.data) + ", " + str(self.index) + ")"

	def udlrCompare(order1, order2):
		if order1 == order2:
			return 0
		elif order1 == 'None':
			return -1
		elif order2 == 'None':
			return 1
		elif order1 == 'Up':
			return -1
		elif order2 == 'Up':
			return 1
		elif order1 == 'Down':
			return -1
		elif order2 == 'Down':
			return 1
		elif order1 == 'Left':
			return -1
		elif order2 == 'Left':
			return 1
		return 1


class Heap:
	def __init__(self, root):
		if root == None:
			raise Exception
		else:
			root.index = 0
			self.elements = [root]

	def isEmpty(self):
		return len(self.elements) < 1

	def insert(self, element):
		self.elements.append(None)
		Heap.decreaseKey(self, len(self.elements) - 1, element)

	def extractMin(self):
		if len(self.elements) < 1:
			raise Exception
		elif len(self.elements) == 1:
			min = self.elements.pop()
			min.index = -1
		else:
			min = self.elements[0]
			self.elements[0] = self.elements.pop()
			min.index = -1
			self.elements[0].index = 0
			Heap.minHeapify(self, 0)
		return min
		
	def minHeapify(self, i):
		l = Heap.left(i)
		r = Heap.right(i)
		s = (l if l < len(self.elements) and self.elements[l] < self.elements[i] else i)
		s = (r if r < len(self.elements) and self.elements[r] < self.elements[s] else s)
		if s != i:
			temp = self.elements[i]							# swap elements
			self.elements[i] = self.elements[s]
			self.elements[s] = temp
			self.elements[i].index = i
			self.elements[s].index = s
			Heap.minHeapify(self, s)

	def decreaseKey(self, i, elem):
		if not elem < self.elements[i]:
			raise Exception
		elem.index = i
		self.elements[i] = elem
		while i > 0 and self.elements[i] < self.elements[Heap.parent(i)]:
			temp = self.elements[i]									# swap elements
			self.elements[i] = self.elements[Heap.parent(i)]
			self.elements[Heap.parent(i)] = temp
			self.elements[i].index = i
			self.elements[Heap.parent(i)].index = Heap.parent(i)
			i = Heap.parent(i)
	
	def parent(i):
		return math.ceil(i / 2) - 1
	def left(i):
		return 2 * i + 1
	def right(i):
		return 2 * i + 2

	def __str__(self):
		s = "["
		for elem in self.elements:
			s += str(elem) + ","
		if len(s) > 1:
			s = s[:-1] + "]"
		else:
			s += "]"
		return s


def main():
	algo = sys.argv[1]
	root = sys.argv[2][::2]
	goal = 12345678

	if algo == 'bfs':
		bfs(root, goal)
	elif algo == 'dfs':
		dfs(root, goal)
	elif algo == 'ast':
		ast(root, goal)
	else:
		print("invalid arguments, exiting")


if __name__ == '__main__':
    main()


