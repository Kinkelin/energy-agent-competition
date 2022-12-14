//Every number is represented by 1 byte
function parse_2d_array(size, file, signed=false) {
	var array = array_create(size[0]);
	for (var i = 0; i < size[0]; i++;) {
		array[i] = array_create(size[1]);
		for (var j = 0; j < size[1]; j++) {
			
			var byte_array = array_create(4);
			for (var k = 0; k < 4; k++) {
				byte_array[k] = file_bin_read_byte(file);
			}
			array[i][j] = byte_array_to_int(byte_array,signed); //file_bin_read_byte(file);
		}
	}
	return array;
}



//Every int is represented by 4 bytes
function parse_int_array(size, file) {
	var array = array_create(size);
	for (var i = 0; i < size; i++) {
		var byte_array = array_create(4);
		for (var j = 0; j < 4; j++) {
			byte_array[j] = file_bin_read_byte(file);
		}
		array[i] = byte_array_to_int(byte_array);
	}
	return array;
}

function parse_short_array(size, file) {
	var array = array_create(size);
	for (var i = 0; i < size; i++) {
		array[i] = parse_short(file);
	}
	return array;
}

function parse_short(file) {
	var byte_array = array_create(2);
	byte_array[0] = file_bin_read_byte(file);
	byte_array[1] = file_bin_read_byte(file);
	return byte_array_to_short(byte_array);
}

function parse_string(size, file) {
	var text = "";
	for (var i = 0; i < size; i++) { 
		text += chr(file_bin_read_byte(file));	
	}
	return text;
}
	
function byte_array_to_short(a) {
	return a[0] | a[1] << 8;
}

function int_to_byte_array(n) {
	a[3] = ( n & $FF000000 ) >> 24;
	a[2] = ( n & $00FF0000 ) >> 16;
	a[1] = ( n & $0000FF00 ) >> 8;
	a[0] = ( n & $000000FF );
	return a;
}

function byte_array_to_int(a,signed=false) {
	var n = 0;
	n |= a[3] << 24;
	n |= a[2] << 16;
	n |= a[1] << 8;
	n |= a[0];
	if signed n &= 15
	return n;
}