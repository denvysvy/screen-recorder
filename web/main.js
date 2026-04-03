

const stateMain = {
  isVolumeOn: true,
  isMicroOn: true,
  isTimeOn: true,
    stopTimeSec: 0,
    stopTimeMin: 0,
    stopTimeHour: 0,
  isec: 0,
  imin: 0,
  ihour: 0,
  screen: 'full',
  fps: 24,
  resolution: '1080p'
}

let stopTime = 0;


let countDown = 3;
let interval;

let seconds = 0;
let remainingSeconds;
let timeInterval;
let dots = 0;

let fileName ='defult';
let fileType = 'mp4';


renderMainPage();



// -------------------------------------------- Main page -----------------------

function renderMainPage(){
  
  const main = document.querySelector(".main");

  main.innerHTML = `
    <header class="header">
      <label for="FPS" class="hint">FPS</label>
      <input  id="FPS" name="choice" class="FPS-input" placeholder="${stateMain.fps}" value="${stateMain.fps}" type="number" min="1" max="80" step="1" >

      <label for="resolution" class="hint">Resolution</label>
      <select id="resolution" class="Resolution-input">
        <option value="480p" ${stateMain.resolution === '480p' ? 'selected' : ''}>480p </option>
        <option value="720p" ${stateMain.resolution === '720p' ? 'selected' : ''}>720p </option>
        <option value="1080p" ${stateMain.resolution === '1080p' ? 'selected' : ''}>1080p</option>
        <option value="1440p" ${stateMain.resolution === '1440p' ? 'selected' : ''}>1440p </option>
      </select>
    </header>

    <div class="up-section">
      <button class="screen-size-button js-screen-size-button">
        ${renderScreenIcon()}

      </button>
      <button class="sound-button js-sound-button">
        ${renderVolume()}
      </button>
        <button class="micro-button js-micro-button">
          ${renderMicro()}
        </button>
        <div class="time-container js-time-container">
          ${renderTime()}
        </div>
    </div>

    <div class="down-section">
      <div class="record-button js-record-button" role="button">
        <img src="svg/record.svg" alt="Record icon">
      </div>
    </div>
  `;

  addTimeButtonListener();

  const sizeButton = document.querySelector('.js-screen-size-button');
    sizeButton.addEventListener("click", () => {
    selectScreenSize();
  });
  window.addEventListener("render-size-icon",  e=>{
    stateMain.screen = e.detail.screen;
    renderScreen();
  });

  const microButton = document.querySelector('.js-micro-button');
  microButton.addEventListener("click", () => {
    toggleMicro(microButton);
  });

  const volumeButton = document.querySelector('.js-sound-button');
  volumeButton.addEventListener("click", () => {
    toggleVolume(volumeButton);
  });

  const recordButton = document.querySelector('.js-record-button');
  recordButton.addEventListener("click", () => {
    toggleRecording();
  });

  const fpsInput = document.getElementById("FPS");
  fpsInput.addEventListener("input", (e) => {
    if (e.target.value < 1) {
      e.target.value = 1;
    } else if (e.target.value > 60) {
      e.target.value = 60;
    }     
    stateMain.fps = parseInt(e.target.value);
  });

  const resolutionSelect = document.getElementById("resolution");
  resolutionSelect.addEventListener("change", (e) => {
    stateMain.resolution = e.target.value;
  });
}



// buttons

function toggleVolume(volumeButton) {
  stateMain.isVolumeOn = !stateMain.isVolumeOn;
  const html = renderVolume();
  volumeButton.innerHTML = html;
}
function renderVolume() {
  if (stateMain.isVolumeOn) {
    return '<img src="svg/volume-on.svg" alt="Volume icon" >'
  } else {
    return '<img src="svg/volume-off.svg" alt="Volume icon" >'
  }
}


function toggleMicro(microButton) {
  stateMain.isMicroOn = !stateMain.isMicroOn;
  const html = renderMicro();
  microButton.innerHTML = html;
}
function renderMicro() {
  if (stateMain.isMicroOn) { 
    return '<img src="svg/micro-on.svg" alt="Microphone icon" >'
  } else {
    return '<img src="svg/micro-off.svg" alt="Microphone icon" >'
  }
}


function renderScreen() {
  const screenButton = document.querySelector('.js-screen-size-button');
  const html = renderScreenIcon();
  screenButton.innerHTML = html;
}
function renderScreenIcon() {
  if (stateMain.screen === 'full') { 
    return '<img src="svg/screen.svg" alt="Full size icon" >'
  } else {
    return '<img src="svg/selected.svg" alt="Selected size icon" >'
  }
}


function toggleTime() {
  const timeContainer = document.querySelector('.js-time-container');
  stateMain.isTimeOn = !stateMain.isTimeOn;
  const html = renderTime();
  timeContainer.innerHTML = html;
  addTimeButtonListener();
}
function addTimeButtonListener() {
  const timeButton = document.querySelector('.js-time-button');
  timeButton.addEventListener("click", () => {
    toggleTime();
  });
}
function renderTime() {
  if (stateMain.isTimeOn) {
    return `
          <button class="time-button js-time-button" >
            <img src="svg/clock-on.svg" alt="Time icon" >
          </button>
          
          <input id="hours" class="time" value="${stateMain.ihour}" type="number" min="1" max="11" >
          <p>:</p>
          <input id="minutes" class="time" value="${stateMain.imin}" type="number" min="0" max="59" >
          <p>:</p>
          <input id="seconds" class="time" value="${stateMain.isec}" type="number" min="0" max="59" >
          `;
  } else {
    return `
          <button class="time-button js-time-button">
            <img src="svg/clock-off.svg" alt="Time icon" >
          </button>`;
  }
}


function toggleRecording() {
  if (stateMain.isTimeOn) {
    calculateStopTime();
    setParams();  
  }
  if (stopTime  && stateMain.isTimeOn) {
   startCountDown();
  } else {
    !stateMain.isTimeOn && startCountDown();
  }
}
function calculateStopTime() {
  stateMain.stopTimeSec = parseInt(document.getElementById('seconds').value);
  stateMain.stopTimeMin = parseInt(document.getElementById('minutes').value);
  stateMain.stopTimeHour = parseInt(document.getElementById('hours').value);
  stopTime = Math.abs(stateMain.stopTimeSec) + Math.abs(stateMain.stopTimeMin) * 60 + Math.abs(stateMain.stopTimeHour) * 3600;
}
function setParams(){
  stateMain.fps = document.getElementById("FPS").value
  stateMain.resolution = document.getElementById("resolution").value
  stateMain.isec = stateMain.stopTimeSec;
  stateMain.imin = stateMain.stopTimeMin;
  stateMain.ihour = stateMain.stopTimeHour;
  stateMain.stopTimeSec = 0;
  stateMain.stopTimeMin = 0;
  stateMain.stopTimeHour= 0;
}


//-------------------------------------- Waiting page----------------------------- 

function renderWaitingPage(){
  const main = document.querySelector(".main");
  main.innerHTML = `
      <div class="waiting-container">
        <p class="waiting-message">Preparing to record...</p>
        <p class="waiting-time">${countDown}</p>
      </div>
      <div class="cancel-container">
        <button class="cancel-button js-cancel-button">
          <img src="svg/cancel.svg" alt="Cancel icon" >
        </button>
      </div>`;
  const cancelButton = document.querySelector('.js-cancel-button');
  cancelButton.addEventListener("click", () => {
    cancelRec();
  });

}



function startCountDown() {
  clearInterval(interval); 
  renderWaitingPage();
  interval = setInterval(() => {
    countDown--;
    renderCountDown();
    if (countDown <= 0) {
      cleanUpCountDown();       
      renderRecordingPage();      
    }
  }, 1000);
}

function renderCountDown() {
  const timeElement = document.querySelector('.waiting-time');
  timeElement.textContent = countDown;
}

function cleanUpCountDown() {
  clearInterval(interval);
  countDown = 3;
}

// buttons

function cancelRec() {
  cleanUpCountDown();
  renderMainPage();
}


// ----------------------------------------- Recording page --------------------

function renderRecordingPage() {
  
  const main = document.querySelector(".main");
  remainingSeconds = stopTime;
  
  startRecRequest();
  startRecording();
  main.innerHTML = `
    <div class="recording-indicator">
      <p class="title">Recording<p class="title dot-dot-dot"></p></p>
    </div>
    <div class="time-counters-container">
      <div class="recording-time time-container">
        <p class="recording-time-text">Recording time:</p>
        <p class="recording-time-value js-recording-time">${formatTime(seconds)}</p>
      </div>
      ${renderStopTimeContainer()}
    </div>
    <div class="stop-recording-container">
      <button class="stop-recording-button js-stop-recording-button">
        <img src="svg/video-off.svg" alt="Stop icon">
      </button>
    </div>`;

    const stopButton = document.querySelector('.js-stop-recording-button');
    stopButton.addEventListener("click", () => {
      stopRec();
    });
}
function renderStopTimeContainer() {
  if (remainingSeconds && stateMain.isTimeOn){
    return `
      <div class="stop-time time-container">
        <p class="stop-time-text">Stop time:</p>
        <p class="stop-time-value js-stop-time">${formatTime(remainingSeconds)}</p>
      </div>`;
  } 
  return '';
}

function startRecording() {
  clearInterval(timeInterval);
  timeInterval = setInterval(() => {
    seconds++;
    rerenderRecordingTime();
    remainingSeconds--;
    updateStopTime();
    renderDots();
  }, 1000);
}

function rerenderRecordingTime() {
  const recordingTimeElement = document.querySelector('.js-recording-time');
  recordingTimeElement.textContent = formatTime(seconds );
}

function updateStopTime() {
  if (stateMain.isTimeOn) {
    renderStopTime(remainingSeconds);

    if (remainingSeconds <= 0){
      stopRec();
    }
  } 
}
function renderStopTime(remainingSeconds) {
  const stopTimeElement = document.querySelector('.js-stop-time');
  stopTimeElement.textContent = formatTime(remainingSeconds);
}


function renderDots(){
  const dotsElement = document.querySelector('.dot-dot-dot');
  const dotsText = updateDots();
  dotsElement.textContent = dotsText;
}

function updateDots() {
  dots = (dots + 1) % 4;
  let dotsText = '';
  for (let i = 0; i < dots; i++) {
    dotsText += '.';
  }
  return dotsText;
}

function formatTime(totalSeconds) {
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  const h = String(hours).padStart(2, '0');
  const m = String(minutes).padStart(2, '0');
  const s = String(seconds).padStart(2, '0');
  return `${h}:${m}:${s}`;
}

// buttons

function stopRec() {
  cleanUpRecording()
  stopRecRequest();
  renderSavingPage();
}
function cleanUpRecording() {
  clearInterval(timeInterval);
  seconds = 0;
  remainingSeconds = stopTime;
  dots = 0;
}




// ----------------------------------------- Saving page --------------------


function renderSavingPage() {
  
  const main = document.querySelector(".main");
  main.innerHTML = `
    <header class="saving-header">
      <p class="title saving-title">Save file</p>
    </header>
    <div class="saving">
      <div class="saving-container">
        <div class="aliner"><p class="saving-hint-text">File name</p></div>
        
        <div class="aliner"><p class="saving-hint-type">File type</p></div>
        <div class="aliner">
          <button class="directory-button">
            <img src="svg/folder.svg" alt="File directory">
          </button>
          <input type="text" maxlength="30"  class="saving-input-name js-saving-input-name" placeholder="Enter file name">
        </div>
        <div class="aliner">
          <div class="file-icon-container js-preview-button">
            <img src="svg/file.svg" alt="File type">
          </div>
          <select class="saving-input-type js-saving-input-type">
            <option value="mp4" selected>mp4</option>
            <option value="webm">webm</option>
            <option value="ogg">ogg</option>
          </select>
        </div>
      </div>
    </div>
    
    <div class="saving-button-container">
      <button class="saving-button js-saving-button">
        <img src="svg/file-export.svg" alt="Save icon">
      </button>
    </div>`;

    const directoryButton = document.querySelector('.directory-button');
    directoryButton.addEventListener("click", () => {
      configureDirectory();
    });
    const saveButton = document.querySelector('.js-saving-button');
    saveButton.addEventListener("click", () => {
      saveRec();
    });
    const previewButton = document.querySelector('.js-preview-button');
    previewButton.addEventListener("click", () => {
      previewFile();
    });
    
}



// buttons

function saveRec() {
  const nameInput = document.querySelector('.js-saving-input-name');
  const typeSelect = document.querySelector('.js-saving-input-type');
  fileName = nameInput.value.trim() || 'defult';
  fileType = typeSelect.value;
  saveRecRequest(fileName, fileType);
  renderMainPage();
}


// API calls

async function startRecRequest() {
  const settings = {
    fps: stateMain.fps,
    resolution: stateMain.resolution,
    volume: stateMain.isVolumeOn,
    micro: stateMain.isMicroOn
  };
  await window.pywebview.api.start_record(settings);
}

async function stopRecRequest() {
  await window.pywebview.api.stop_record()
}

async function saveRecRequest(fileName, fileType) {
  await window.pywebview.api.save_file(fileName, fileType);
}

async function selectScreenSize() {
  stateMain.screen = 'selected';
  renderScreenIcon();
  await window.pywebview.api.screen_size_selector();
}

async function configureDirectory() {
  await window.pywebview.api.get_directory();
}

async function previewFile() {
  await window.pywebview.api.open_preview();
}


function closeApp() {
    window.pywebview.api.close()
}

function minimize() {
    window.pywebview.api.minimize()
}