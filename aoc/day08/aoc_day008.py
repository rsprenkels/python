with open('input_day08.txt', 'r') as f:
    input = list(map(int, f.readline().split(' ')))

# input = list(map(int, '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split()))

input = list(reversed(input))

for x in range(len(input)):
    print(input[x])

class Node:
    node_id = 0

    def __init__(self, input):
        num_children = input.pop()
        meta_entries = input.pop()
        self.node_id = Node.node_id
        print(f"creating {self.node_id} {num_children} {meta_entries}")
        Node.node_id += 1
        self.children = []
        self.metadata_entries = []
        for _ in range(num_children):
            self.children.append(Node(input))
        for _ in range(meta_entries):
            self.metadata_entries.append(input.pop())

    def __str__(self):
        output = f"id:{self.node_id} nc:{len(self.children)} meta:{self.metadata_entries}\n"
        for child in range(len(self.children)):
            output += f"{self.children[child]}"
        return output

    def get_metasum(self):
        total_sum = sum(self.metadata_entries)
        for child in self.children:
            total_sum += child.get_metasum()
        return total_sum

    def get_complexsum(self):
        sum_value = 0

        if len(self.children) == 0:
            sum_value = sum(self.metadata_entries)
        else:
            for child_index in self.metadata_entries:
                if child_index <= 0 or child_index > len(self.children):
                    pass
                else:
                    sum_value += self.children[child_index - 1].get_complexsum()
        return sum_value


root = Node(input)

print(root)

print(f"total value: {root.get_metasum()}  complex value: {root.get_complexsum()}")