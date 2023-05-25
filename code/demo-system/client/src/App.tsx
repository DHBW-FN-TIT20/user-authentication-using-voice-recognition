import { useEffect, useState, useRef } from 'react';
import'./App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faFile, faInfoCircle } from '@fortawesome/free-solid-svg-icons'
import Result from './Result';
import Info from './Info';

async function login(userId: number, selectedUserId: number, selectedFileIndex: number) {
  try {
    // get the current url and remove everything after the main url and remove the port if exists
    const url = window.location.href.replace(/\/[^\/]*$/, "").replace(/:\d+$/, "");
    const response = await fetch(`${url}:5500/?speaker_id=${selectedUserId}&sample_id=${selectedFileIndex}&selected_speaker_id=${userId}`);
  
    if (!response.ok) {
      return { 
        absolute_accuracy_of_selected_speaker: 0,
        is_authenticated: false,
        absolute_accuracy_of_all_speakers: []
      };
    }
  
    const json = await response.json();
    
    return json;
  } catch (e) {
    console.error(e);
    return {
      absolute_accuracy_of_selected_speaker: 0,
      is_authenticated: false,
      absolute_accuracy_of_all_speakers: []
    }
  }
}

function App() {
  const [loginDisabled, setLoginDisabled] = useState<boolean>(true);
  const [userId, setUserId] = useState<number>(NaN);
  const [selectedUserId, setSelectedUserId] = useState<number>(NaN);
  const [selectedFileIndex, setSelectedFileIndex] = useState<number>(NaN);
  const [showResults, setShowResults] = useState<boolean>(false);
  const [results, setResults] = useState<any>({absolute_accuracy_of_selected_speaker: 0, is_authenticated: false, absolute_accuracy_of_all_speakers: []});
  const [fetching, setFetching] = useState<boolean>(false);
  const [showInfo, setShowInfo] = useState<boolean>(false);
  
  const audioRef = useRef<HTMLAudioElement>(null)

  const updateSong = () => {
    if(audioRef.current){
        audioRef.current.pause();
        audioRef.current.load();
    }
  }

  useEffect(() => {
    const updateLoginStatus = () => {
      if (!isNaN(userId) && userId >= 0 && userId < 20 && !isNaN(selectedUserId) && !isNaN(selectedFileIndex)) {
        setLoginDisabled(false);
      } else {
        setLoginDisabled(true);
      }
    }
    updateLoginStatus();
  }, [userId, selectedUserId, selectedFileIndex])

  useEffect(() => {
    updateSong();
  }, [selectedUserId, selectedFileIndex])

  useEffect(() => {
    // eventlistener on esc -> setShowResults(false);
    const escFunction = (event: KeyboardEvent) => {
      if(event.key === 'Escape') {
        setShowResults(false);
        setLoginDisabled(false);
      }
    }
    document.addEventListener("keydown", escFunction, false);
  }, [])

  return (
    <div className="App">
      <form
        className="loginForm"
        onSubmit={async (e) => {
          e.preventDefault();
          if (!loginDisabled) {
            setFetching(true);
            setLoginDisabled(true);
            setResults(await login(userId, selectedUserId, selectedFileIndex));
            setFetching(false);
            setShowResults(true);
          }
        }}
      >
        <FontAwesomeIcon icon={faInfoCircle} className="infoIcon" size="2x" onClick={() => {
          setShowInfo(!showInfo);
        }} />
        <h2>Login</h2>
        <div
          className='userWrapper'
        >
          <input 
            type="number"
            placeholder="userId" 
            value={userId.toString()} 
            onChange={(e) => {
              const id = parseInt(e.target.value);
              if (id >= 0 && id < 20) {
                setUserId(id);
              } else {
                setUserId(NaN);
              }
            }}
          />
        </div>
        <div
          className='fileWrapper'
        >
          <div className="fileList">
            {
              // create an array with all numbers from 0 to 20
              Array.from(Array(20).keys()).map((id) => {
                return Array.from(Array(9).keys()).map((fileIndex) => {
                  return (
                    <div 
                      key={"speaker" + id + "file" + fileIndex}
                      className={"fileItem " + (selectedUserId === id && selectedFileIndex === fileIndex ? "selected" : "")}
                      onClick={() => {
                        setSelectedUserId(id);
                        setSelectedFileIndex(fileIndex);
                      }}
                    >
                      <span>
                        <FontAwesomeIcon icon={faUser} />
                        &nbsp;{id}
                      </span>
                      <span>
                        <FontAwesomeIcon icon={faFile} />
                        &nbsp;{fileIndex}
                      </span>
                    </div>
                  )
                })
              })
            }
          </div>
          {
            !isNaN(selectedUserId) && !isNaN(selectedFileIndex) &&
            <div className="audioPlayer">
              <audio controls ref={audioRef}>
                <source src={`./audio_dataset/Speaker${String(selectedUserId).padStart(4, '0')}/Validation_Speaker${String(selectedUserId).padStart(2, '0')}_${String(selectedFileIndex).padStart(4, '0')}.wav`} type="audio/wav" />
                Audio files are not supported by your browser.
              </audio>
            </div>
          }
        </div>
        <button 
          disabled={loginDisabled}
        >
          {
            fetching ? 
            "Loading..."
            :
            "Login"
          }
        </button>
      </form>

      {
        showResults &&
          <Result 
            authenticatingUserId={userId}
            selectedFile={{speakerId: selectedUserId, sampleId: selectedFileIndex}}
            results={results}
            close={() => {
              setShowResults(false);
              setLoginDisabled(false);
            }}
          />
      }
      {
        showInfo &&
        <Info 
          close={() => setShowInfo(false)}
        />
      }
    </div>
  );
}

export default App;
