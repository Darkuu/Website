window.addEventListener("load", function(){
    getPosts();
})

async function getPosts(){
    let response = await fetch('/data')
    let data = await response.json()

    let posts = document.getElementById('posts')
    posts.innerHTML = ""

    for(let post of data){
            /* Jaunu produktu paradīšana. */
            
        postsHTML = `<div><h2 id="text"><b>Name: </b>${post.name}</h2><h2 id="text"><b>Surname: </b>${post.surname}</h2><h2 id="text"><b>Number Plate: </b>${post.numberplate}</h2><div class="button" id="text"><a class="delete" href="/create/delete/${post.id}">Delete</a></div>`
        posts.innerHTML = posts.innerHTML + postsHTML
    }
}