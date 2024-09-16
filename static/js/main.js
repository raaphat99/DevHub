// grabbing the search form
let searchForm = document.getElementById("searchForm");
// grabbing page pagination buttons
let pageLinks = document.getElementsByClassName("page-link");

// ensures that the search form exists
if (searchForm) {
  // looping through every single item in pageLinks and adding an event handler to it
  for (let i = 0; pageLinks.length > i; i++) {
    // every time a button is clicked, we are gonna fire off this event
    pageLinks[i].addEventListener("click", function (e) {
      e.preventDefault();

      // 'this' refers to the button that we click on, and 'page' contains the page number
      let page = this.dataset.page;

      // adding hidden search input to the form and passing 'page' to it
      // this is done using java script and template literals
      // the value attribute here defines the initial (default) value of the input field
      searchForm.innerHTML += `<input value=${page} name='page' hidden/>`;
      // submit form
      searchForm.submit();
    });
  }
}


// this is gonna query all the tags we have inside of our DOM in the page 
let tags = document.getElementsByClassName('project-tag')

for (let i=0; tags.length>i; i++)
{
  tags[i].addEventListener('click', (e) => {
    // e.target is the current item that we clicked on
    // we can access our custom data by using 'dataset.ourCustomDataName'
    let tagId = e.target.dataset.tag
    let projectId = e.target.dataset.project
    
    fetch('http://127.0.0.1:8000/api/remove-tag/', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({'project': projectId, 'tag': tagId})
    })
    .then(response => response.json())
    // removing the tag (the physical HTML element) from DOM
    .then(data => {
      e.target.remove()
    })

  })
}
