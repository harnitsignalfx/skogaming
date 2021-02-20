async function getUsers() {
    let url = '//skogaming.com/api/leaders/starship';
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function renderUsers() {
    let users = await getUsers();
    let html = '';

    users.map(user => {
        let htmlSegment = `<div class="user">
                             <h2>${user.member} ${user.rank} ${user.score}</h2>
                           </div>`;
        html += htmlSegment;
    });

    let container = document.querySelector('.container');
    container.innerHTML = html;
}

renderUsers();
