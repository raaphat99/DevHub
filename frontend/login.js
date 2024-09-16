let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    // by default, the page is refreshing when a user submits a form. we want to prevent that to be able to perform other actions.
    e.preventDefault()
    
    let formData = {
        // we can get the form content by the help of 'name' attribute's value that we assigned in the associated input tag
        'username': form.username.value,
        'password': form.password.value,
    }
    // we will send the form data to this url
    fetch('http://127.0.0.1:8000/api/users/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // this form data is gonna be sent to the backend to the above url with a POST request
        body: JSON.stringify(formData)
    })
    .then(respone => respone.json())
    .then(data => {
        // access refers to the token we want to catch
        console.log('DATA: ', data.access)
        if (data.access)
        {
            // assign the token to the Local Storage in the browser
            localStorage.setItem('token', data.access)
            // Direct the user to this path 
            window.location = 'file:///C:/Users/SK/Desktop/frontend/projects_list.html' 
        } 
        else
        {
            alert('username or password did not work!')
        }
    })
})