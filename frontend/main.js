let loginBtn = document.getElementById('login-btn')
let logoutBtn = document.getElementById('logout-btn')

let token = localStorage.getItem('token')
//if we are logged in, then remove the Login button, we will not need it.
if (token)
{
    loginBtn.remove()
}
//if we are logged out, remove the Logout button.
else
{
    logoutBtn.remove()
}

// when the user logs out, remove the token that's associated with it
logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    localStorage.removeItem('token')
    // Direct the user to the login page
    window.location = 'file:///C:/Users/SK/Desktop/frontend/login.html'
})

// this is the domain or the endpoint we are gonna fetch our data from
let projectUrl = "http://127.0.0.1:8000/api/projects/"

let getProjects = () => {

    // we make a GET request here
    fetch(projectUrl)

    // This is a promise. A promise is kind of like a response to what just happens after excuting the above 'fetch' method
    // It wait for 'fetch' to finish rendering and then we get this response
    // with the 'fetch' api we do need to convert our data to json format.
    .then(response => response.json())
    .then(data => {
        // data here is the list of all projects that we have
        console.log(data)
        buildProjects(data)
    })
}


let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById('project--wrapper')
    // clear its contents to avoid rendering the whole projects everytime we vote a one
    projectsWrapper.innerHTML = ''
    for(let i=0; projects.length>i; i++)
    {
        let project = projects[i]

        let projectCard = `
            <div class="project--card">
                <img src="http://127.0.0.1:8000${project.featured_image}" />
                
                <div>
                    <div class="card--header">
                        <h3>${project.title}</h3>
                        <strong class="vote--option" data-vote="Up" data-project="${project.id}" >&#43;</strong>
                        <strong class="vote--option" data-vote="Down" data-project="${project.id}" >&#8722;</strong>
                    </div>
                    <i>${project.vote_ratio}% Positive Feedback</i>
                    <p>${project.description.substring(0, 150)}</p>
                </div>

            </div>
        `
        // show the project titles inside of 'project--wrapper' section
        projectsWrapper.innerHTML += projectCard
    }

    // Add an event listener 
    addVoteEvents()
}

let addVoteEvents = () => {
    let voteBtns = document.getElementsByClassName('vote--option')
    
    for (let i=0; voteBtns.length > i; i++)
    {
        // (e) here refers to the actual event
        voteBtns[i].addEventListener('click', (e) => {
            let token = localStorage.getItem('token')
            console.log('TOKEN: ', token)
            // vote here is the type of vote. And target is the actual item we just clicked on.
            // dataset enables us to get the custom attributes we have in the html tags
            let vote = e.target.dataset.vote
            // the project the user voted on
            let project = e.target.dataset.project

            // we are gonna send the dynamic value of each click
            // because this is a POST request, we need to specify a few things here.
            fetch(`http://127.0.0.1:8000/api/projects/${project}/vote/`, {
                method: 'POST', 
                headers: {
                    // this is equivalent to selecting the type of form-data (which will be fetched from the body of the request) on Postman
                    'Content-Type': 'application/json',
                    // remember when we were sending a token through Postman, we were setting authorization value (Bearer + {token}). this key is also equivalent to that
                    Authorization: `Bearer ${token}`, 
                },
                // this is equivalent to assigning the body with a value in Postman
                body: JSON.stringify({'value': vote})
             })
             .then(response => response.json())
             .then(data => {
                 console.log('Success!', data)
             })
            
        })
    }
}


getProjects()