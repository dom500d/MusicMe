// window.onSpotifyWebPlaybackSDKReady = () => {
//     const token = '[My access token]';
//     const player = new Spotify.Player({
//       name: 'Web Playback SDK Quick Start Player',
//       getOAuthToken: cb => { cb(token); },
//       volume: 0.5
//     });
// }
//Wait for the documenmt to load
document.addEventListener("DOMContentLoaded", (event) => {
    const searchButton = document.querySelector('#search-button');
    let data2send;
    let tbody1 = document.querySelector('.spotify');
    let tbody2 = document.querySelector('.soundcloud');
    searchButton.addEventListener("click", (event) => {
        while (tbody1.lastElementChild) {
            tbody1.removeChild(tbody1.lastElementChild);
        }
        while (tbody2.lastElementChild) {
            tbody2.removeChild(tbody2.lastElementChild);
        }
        let search = document.getElementById("search");
        if(search.value == "" || search.value == null) {
            alert("Please enter something in the search bar!");
        } else {
            fetch(`/search/${search.value}`).then((response) => response.json())
            .then((data) => {
                console.log(data);
                let c = 0;
                console.log(Object.keys(data['spotify']).length);
                console.log((data['spotify'][1]));
                while(c < Object.keys(data['spotify']).length) {
                    console.log(c);
                    addSong(data['spotify'][c], c, 'spotify');
                    c++;
                }
                c = 0;
                while(c < Object.keys(data['soundcloud']).length) {
                    addSong(data['soundcloud'][c], c, 'soundcloud');
                    c++;
                }
            });
        }
    });
    function addSong(data, i, service) {
        let tbody = document.querySelector(`.${service}`);
        const template = document.getElementById('song');
        const clone = template.content.cloneNode(true);
        let id = i;
        clone.querySelector('.title').innerHTML = data['title'];
        clone.querySelector('.artist').innerHTML = data['artist'];
        clone.querySelector('.link').innerHTML = data['link'];
        clone.querySelector('.id').innerHTML = id;
        clone.children[0].id = `song${id}`;
        tbody.appendChild(clone);
    }
});
