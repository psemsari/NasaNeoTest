//simple fonction pour avoir un menu déroulant du contenu
function getCookie(name) {
    const cookies = document.cookie.split('; ')
    const value = cookies
        .find(c => c.startsWith(name + "="))
        ?.split('=')[1]
    if (value === undefined) {
        return null
    } 
    return decodeURIComponent(value)
}

const buttons = document.querySelectorAll('button')
buttons.forEach((button) => {
    button.addEventListener('click', async function () {
        content = button.nextElementSibling
        if (content.style.display === "block") { //if tag loaded just no recal
            content.style.display = "none";
        } else {
            content.style.display = "block";
            if (content.getAttribute('load') == "false")
            {
                //requête vers moreinfo
                await fetch('v2/moreinfo', {
                    method: 'POST',
                    //encode le body au format de formulaire pour que django le reconnaisse comme une form
                    headers: {'X-CSRFToken': getCookie('csrftoken'), 'content-type': 'application/x-www-form-urlencoded'},
                    body: 'id='+ button.getAttribute('id') + "&date=" + button.getAttribute('day')
                })
                .then( (res) => {
                    res.json().then((obj) => {
                        //remplace le loader par les informations obtenu
                        const template = document.querySelector('#template')
                        const div = template.content.cloneNode(true)
                        const h4 = div.querySelector('h4')
                        h4.innerText = 'Prochain passage: ' + obj.next_approach_date
                        const ul = div.querySelector('ul')
                        obj.lasts_approachs.forEach(element => {
                            li = document.createElement('li')
                            li.innerText = "Date : " + element.date + " / Distance : " + element.distance + " km"
                            ul.append(li)
                        });
                        content.replaceWith(div)
                    })
                })
                .catch( (err) => {
                    content.innerText = 'Error: ' + err.reason
                })
            }
        }

    })
})
