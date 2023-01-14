from math import trunc

f = open("barcodes", "r")
file_contents = f.read()
file_lines = file_contents.split("\n")
num_barcodes = len(file_lines)

def get_barcode_class(barcode):
    global file_lines
    counter = 0
    barcode_index = None
    for line in file_lines:
        if line == barcode:
            barcode_index = trunc(counter / 10)
        counter += 1
    return barcode_index

def hamming_distance(str1, str2):
    d = 0
    for c1, c2 in zip(str1, str2):  # zip() Iterate over several iterables in parallel
        if c1 != c2:
            d = d + 1
    return d

num_success = 0
run_counter = 0
for barcode in file_lines:
    search_class = get_barcode_class(barcode)
    print(f"searching for closest match to barcode # {run_counter + 1} [{search_class}]")
    # print(f"searching for closest match to {barcode}")
    query_barcode = barcode
    hamming_results = []
    compared_barcodes = []
    for barcode in file_lines:
        if barcode != query_barcode:
            hamming_results.append(hamming_distance(barcode, query_barcode))
            compared_barcodes.append(barcode)
    closest_match = min(hamming_results)
    counter = 0
    for distance in hamming_results:
        if distance == closest_match:
            closest_match_index = counter
        counter += 1
    barcode_closest_match = compared_barcodes[closest_match_index]
    class_number = get_barcode_class(barcode_closest_match)
    accuracy = round((((len(barcode) - closest_match) / len(barcode)) * 100),2)
    # print(f"{run_counter} - {accuracy} {class_number} {barcode_closest_match}\n")
    if class_number == search_class:
        hit = True
        num_success += 1
    else:
        hit = False
    print(f"- {accuracy}% , class= {class_number}, hit= {hit}\n")
    run_counter += 1


print(f"num_barcodes= {num_barcodes}\nnum_success= {num_success}\nhit ratio:= {(num_success/num_barcodes)}")
