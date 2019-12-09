from collections import defaultdict


def image_checksum(all_layers, image_size):
    histogram = []
    for index, layer in enumerate(range(0, len(all_layers), image_size)):
        histogram.append(defaultdict(int))
        layer_data = all_layers[layer:layer + image_size]
        for pixel in layer_data:
            histogram[index][pixel] += 1
    least = min(histogram, key=lambda x: x['0'])
    return least['1'] * least['2']

def image_render(all_layers, im_w=25, im_h=6):
    pixels = defaultdict(list)
    for index, layer in enumerate(range(0, len(all_layers), im_w * im_h)):
        layer_data = all_layers[layer:layer + im_w * im_h]
        for y in range(im_h):
            for x in range(im_w):
                pixels[(x,y)].append(layer_data[y * im_w + x])
    output_lines = []
    for y in range(im_h):
        one_line = []
        for x in range(im_w):
            stacked_pixel = [p for p in pixels[(x,y)] if p != '2'][0]
            one_line.append({'0':' ', '1':'*'}[stacked_pixel])
        output_lines.append(''.join(one_line))
    return output_lines

def test_1():
    assert image_checksum('123456789012', 6) == 1


def test_part1():
    lines = open('aoc2019_08_input.txt', 'r').readlines()
    assert image_checksum((lines[0]), 150) == 1703


def test_part2():
    lines = open('aoc2019_08_input.txt', 'r').readlines()
    result = image_render((lines[0]), 25, 6)
    print()
    for line in result:
        print(line)







