def read_numbers(filename):
  arrays = []
  with open(filename, "r") as f:
    for line in f:
      numbers = line.strip().replace('-','').split(",")
      array = [double(num) for num in numbers]
      arrays.append(array)
  return arrays
def max_second_elements(arrays):
  second_elements = []
  for array in arrays:
    if len(array) >= 2:
      second_element = array[1]
      second_elements.append(second_element)
  if second_elements:
    max_second_element = max(second_elements)
    max_index = second_elements.index(max_second_element)
    first_element = arrays[max_index][0]
    return (first_element,-max_second_element )
  else:
  
    return None
voltage=read_numbers("/afs/ihep.ac.cn/users/z/zhangjunrui/raser/output/t1.txt")
max=max_second_elements(voltage)
print(max)