
function parse_2d_array(size, file) {
	var array = array_create(size[0]);
	for (var i = 0; i < size[0]; i++;) {
		array[i] = array_create(size[1]);
		for (var j = 0; j < size[1]; j++) {
			array[i][j] = file_bin_read_byte(file);
		}
	}
	return array;
}