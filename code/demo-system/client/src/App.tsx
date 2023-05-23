import { useEffect, useState, useRef } from 'react';
import'./App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faFile } from '@fortawesome/free-solid-svg-icons'
import Result from './Result';

async function login(userId: number, selectedUserId: number, selectedFileIndex: number) {
  // get the current url and remove everything after the main url and remove the port if exists
  const url = window.location.href.replace(/\/[^\/]*$/, "").replace(/:\d+$/, "");
  const response = await fetch(`${url}:5500/?speaker_id=${userId}&sample_id=${selectedFileIndex}&selected_speaker_id=${selectedUserId}`);

  if (!response.ok) {
    return { 
      absulute_accuracy_of_selected_speaker: 0,
      is_authenticated: false
    };
  }

  const json = await response.json();
  
  return json;
}

function App() {
  const [loginDisabled, setLoginDisabled] = useState<boolean>(true);
  const [userId, setUserId] = useState<number>(NaN);
  const [selectedUserId, setSelectedUserId] = useState<number>(NaN);
  const [selectedFileIndex, setSelectedFileIndex] = useState<number>(NaN);
  const [showResults, setShowResults] = useState<boolean>(false);
  const [results, setResults] = useState<any>({absulute_accuracy_of_selected_speaker: 0, is_authenticated: false});
  const [fetching, setFetching] = useState<boolean>(false);
  
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
              setUserId(NaN);
              setSelectedUserId(NaN);
              setSelectedFileIndex(NaN);
              setShowResults(false);
            }}
          />
      }
    </div>
  );
}

export default App;
