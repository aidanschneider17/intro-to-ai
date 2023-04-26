from Problem import BitString

def test_eval(type):

    if type == 1:
        problem = BitString(10, [1 for i in range(10)])
        assert problem.evaluation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
        assert problem.evaluation([1, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0.1
        assert problem.evaluation([1, 0, 1, 0, 1, 0, 1, 0, 1, 0]) == 0.5
        assert problem.evaluation([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 1
    elif type == 2:
        problem = BitString(10, [0 for i in range(10)])
        assert problem.evaluation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1
        assert problem.evaluation([1, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0.9
        assert problem.evaluation([1, 0, 1, 0, 1, 0, 1, 0, 1, 0]) == 0.5
        assert problem.evaluation([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 0
    elif type == 3:
        problem = BitString(10, [1,0,1,0,1,0,1,0,1,0])
        assert problem.evaluation([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0.5
        assert problem.evaluation([1, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0.6
        assert problem.evaluation([1, 0, 1, 0, 1, 0, 1, 0, 1, 0]) == 1
        assert problem.evaluation([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 0.5
    elif type == 4:
        problem = BitString(4, [1, 0, 1, 0])
        assert problem.evaluation([0, 0, 1, 0]) == 0.75
        assert problem.evaluation([1, 1, 0, 1]) == 0.25
        assert problem.evaluation([1, 0, 1, 0]) == 1
        assert problem.evaluation([1, 1, 1, 1]) == 0.5

def test_succ(type):
    if type == 1:
        problem = BitString(4, [1 for i in range(4)])
        neighbors = problem.successors([0,0,0,0])
        assert len(neighbors) == 4
        expected = [[1,0,0,0], [0,1,0,0],[0,0,1,0],[0,0,0,1]]
        for n in neighbors:
            assert n in expected
    elif type == 2:
        problem = BitString(4, [1 for i in range(4)])
        neighbors = problem.successors([1, 0, 1, 0])
        assert len(neighbors) == 4
        expected = [[0, 0, 1, 0], [1, 1, 1, 0], [1, 0, 0, 0], [1, 0, 1, 1]]
        for n in neighbors:
            assert n in expected


if __name__ == '__main__':
    for i in range(4):
        test_eval(i)
    for i in range(2):
        test_succ(i)


