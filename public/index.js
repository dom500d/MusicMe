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
    const tbody = document.querySelector(".songHolder");
    let data2send;
    searchButton.addEventListener("click", (event) => {
        while (tbody.lastElementChild) {
            tbody.removeChild(tbody.lastElementChild);
        }
        let search = document.getElementById("search");
        if(search.value == "" || search.value == null) {
            alert("Please enter something in the search bar!");
        } else {
            fetch(`/search/${search.value}`).then((response) => response.json())
            .then((data) => {
                console.log(data);
                let i = 0;
                while(i < Object.keys(data).length) {
                    addSong(data[i], i);
                    i++;
                }
            });
        }
    });
    function addSong(data, i) {
        const template = document.getElementById('song');
        const clone = template.content.cloneNode(true);
        let id = i;
        clone.querySelector('.title').innerHTML = data['song'];
        clone.querySelector('.artist').innerHTML = data['artist'];
        clone.querySelector('.link').innerHTML = data['link'];
        clone.querySelector('.id').innerHTML = id;
        clone.children[0].id = `song${id}`;
        tbody.appendChild(clone);
    }
});
