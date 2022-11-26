/*
	This extension can be used to load the file in an HTML5 export in the future. 
	This might allow the project to have a permanent web renderer available on itch.io or another site.
*/
/*
window.addEventListener('dragover', (event) => {
	
  event.stopPropagation();
  event.preventDefault();
  // Style the drag-and-drop as a "copy file" operation.
  event.dataTransfer.dropEffect = 'copy';
  
});

window.addEventListener('drop', (event) => {

  event.stopPropagation();
  event.preventDefault();
  const fileList = event.dataTransfer.files;
  console.log(fileList);
  fetch(fileList)
  .then(response => response.text())
  .then(text => console.log(text))
  
});
*/