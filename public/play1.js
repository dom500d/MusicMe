document.addEventListener("DOMContentLoaded", function(event){
  // your code here
window.onSpotifyWebPlaybackSDKReady = () => {
  const token = 'BQDX5FQoD36VJmHNaFRfjKlOV5yrY7TRhSIrw34kFr65uwWbVtPsh2arpIbV_XrDoEmuu-iuHmWXI8EMdfjb-1qWcA5SAZLflJKcisqSBrI6ypZFdiPZP9Tfqs7HdKz4B0bNV6FfGrlvTzwainVmJjomMwB2rYJ-GP4KHg3gK-V64qksItX1Rwb6Y6pMYthVShvtpxxclwCc';
  const player = new Spotify.Player({
    name: 'Web Playback SDK Quick Start Player',
    getOAuthToken: cb => { cb(token); },
    volume: 0.5
  });
  // Ready
   player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);
  });

  // Not Ready
  player.addListener('not_ready', ({ device_id }) => {
    console.log('Device ID has gone offline', device_id);
  });
  player.addListener('initialization_error', ({ message }) => { 
    console.error(message);
  });

  player.addListener('authentication_error', ({ message }) => {
    console.error(message);
  });

  player.addListener('account_error', ({ message }) => {
    console.error(message);
  });
  player.connect();
  } 
});