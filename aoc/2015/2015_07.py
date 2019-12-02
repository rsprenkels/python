class Parser():
    def __init__(self, circuit):
        self.signal_values = {}
        self.signals_to_find = set()
        self.all_signals = set()
        self.circuit = circuit
        for line in self.circuit:
            left, right = line.split(' -> ')
            self.signals_to_find.add(right)
            self.all_signals.add(right)

    def operand(self, x):
        if x in self.all_signals:
            return self.signal_values[x]
        else:
            return int(x)

    def evaluate(self, expression):
        try:
            if 'AND' in expression:
                x, y = expression.split(' AND ')
                return (True, self.operand(x) & self.operand(y))
            if 'OR' in expression:
                x, y = expression.split(' OR ')
                return (True, self.operand(x) | self.operand(y))
            if 'LSHIFT' in expression:
                x, y = expression.split(' LSHIFT ')
                return (True, self.operand(x) << int(y))
            if 'RSHIFT' in expression:
                x, y = expression.split(' RSHIFT ')
                return (True, self.operand(x) >> int(y))
            if 'NOT' in expression:
                y = expression[4:]
                return (True, self.operand(y) ^ 65535)
            return (True, self.operand(expression))
        except KeyError:
            return (False, None)

    def calculate_circuit(self):
        # print(f"need to find {len(self.signals_to_find)}")
        while len(self.signals_to_find) > 0:
            for line in self.circuit:
                # print(f"{len(self.signals_to_find):4} processing instruction {line}")
                expression, signal = line.split(' -> ')
                expression_valid, result = self.evaluate(expression)
                if expression_valid:
                    if signal in self.signals_to_find:
                        self.set_signal(signal, result)
        return self.signal_values

    def set_signal(self, signal, result):
        self.signal_values[signal] = result
        self.signals_to_find.remove(signal)


def test_1():
    circuit = [
        '123 -> x',
        '456 -> y',
        'x AND y -> d',
        'x OR y -> e',
        'x LSHIFT 2 -> f',
        'y RSHIFT 2 -> g',
        'NOT x -> h',
        'NOT y -> i', ]

    parser = Parser(circuit)

    assert parser.calculate_circuit() == {'x': 123, 'y': 456, 'd': 72, 'e': 507, 'f': 492, 'g': 114, 'h': 65412,
                                          'i': 65079}


def test_aoc_firstpart():
    instructions = [line.rstrip() for line in open('2015_07.txt', 'r').readlines()]
    parser = Parser(instructions)
    first_answer = parser.calculate_circuit()['a']
    assert first_answer == 16076


def test_aoc_secondpart():
    instructions = [line.rstrip() for line in open('2015_07.txt', 'r').readlines()]
    second_parser = Parser(instructions)
    second_parser.set_signal('b', 16076)

    second_answer = second_parser.calculate_circuit()['a']
    assert second_answer == 2797


if __name__ == '__main__':
    instructions = [line.rstrip() for line in open('2015_07.txt', 'r').readlines()]
    parser = Parser(instructions)
    first_answer = parser.calculate_circuit()['a']
    print(f"aoc 2015 day 7, answer first part: {first_answer}")

    second_parser = Parser(instructions)
    second_parser.set_signal('b', first_answer)

    second_answer = second_parser.calculate_circuit()['a']
    print(f"aoc 2015 day 7, answer second part: {second_answer}")
