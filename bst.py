class TeamNode:

    def __init__(self, team):

        self.team = team
        self.left = None
        self.right = None


class TeamBST:

    def __init__(self):

        self.root = None

    def insert(self, team):

        new_node = TeamNode(team)

        if self.root is None:

            self.root = new_node
            return True

        current = self.root

        while True:

            if team.name.lower() == current.team.name.lower():

                return False

            elif team.name.lower() < current.team.name.lower():

                if current.left is None:

                    current.left = new_node
                    return True

                current = current.left

            else:

                if current.right is None:

                    current.right = new_node
                    return True

                current = current.right

    def search(self, name):

        current = self.root

        while current is not None:

            if name.lower() == current.team.name.lower():

                return current.team

            elif name.lower() < current.team.name.lower():

                current = current.left

            else:

                current = current.right

        return None

    def inorder(self, node=None, result=None):

        if result is None:

            result = []

        if node is None:

            node = self.root

            if node is None:
                return result

        if node.left is not None:

            self.inorder(node.left, result)

        result.append(node.team)

        if node.right is not None:

            self.inorder(node.right, result)

        return result