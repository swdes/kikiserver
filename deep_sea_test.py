import unittest
import deep_sea 

class TestMove(unittest.TestCase):

    def test_move_down(self):
        position = deep_sea.move_down(0,[-1,-1,-1], 4)
        self.assertEqual(position, 2)

    def test_move_down_2(self):
        position = deep_sea.move_down(0,[-1,0,1], 4)
        self.assertEqual(position, 0)

    def test_move_down_3(self):
        position = deep_sea.move_down(0,[-1,-1,0], 4)
        self.assertEqual(position, 1)

    def test_move_up(self):
        position = deep_sea.move_up(2,[-1,-1,-1], 4)
        self.assertEqual(position, -1)

    def test_move_up_2(self):
        position = deep_sea.move_up(2,[1,0,3], 1)
        self.assertEqual(position, -1)

    def test_move_up_3(self):
        position = deep_sea.move_up(2,[-1,0,3], 1)
        self.assertEqual(position, 0)

    def test_remove_cells(self):
        cells = deep_sea.remove_empty_cells([[1],[2],[0],[],[],[3],[],[1,2,3]])
        self.assertEqual(cells, [[1],[2],[0],[3],[1,2,3]])

    def test_find_cell_without_fallen_treasures(self):
        pos = deep_sea.find_position_without_fallen_treasures([[1],[2],[0],[3],[1,2,3]])
        self.assertEqual(pos, 3)

    def test_whos_on_treasure(self):
        pos = deep_sea.whos_on_treasure([[1],[2],[0],[],[],[3],[],[1,2,3]], [{ "position": 4 }, { "position": 2}])
        self.assertEqual(pos, [-1, -1, 1, -1, 0, -1, -1, -1])

    def test_score_final(self):

        players = [
            {
                "treasures_earned": [1, 2, 3]
            },
            {
                "treasures_earned": [12]
            },
            {
                "treasures_earned": [2, 0, 5]
            },
        ]

        players_results = deep_sea.compute_final_score(players)
        print(players_results)
        self.assertEqual(players_results[1]['winer'], True)
        self.assertEqual(players_results[0]['score_final'], 6)
        self.assertEqual(players_results[1]['score_final'], 12)
        self.assertEqual(players_results[2]['score_final'], 7)

if __name__ == '__main__':
    unittest.main()