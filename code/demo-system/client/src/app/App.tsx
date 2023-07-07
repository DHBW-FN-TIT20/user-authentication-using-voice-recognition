import { useEffect, useState, useRef } from 'react';
import'./App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faFile, faInfoCircle } from '@fortawesome/free-solid-svg-icons'
import Result from '../shared/components/Result/Result';
import Info from '../shared/components/Info/Info';

import configData from '../config.json'

async function login(authenticatingUserId: number, sampleFileUserId: number, sampleFileIndex: number) {
  try {
    const response = await fetch(`http://${configData.SERVER_URL}:${configData.SERVER_PORT}/?speaker_id=${sampleFileUserId}&sample_id=${sampleFileIndex}&selected_speaker_id=${authenticatingUserId}`);
  
    console.log(response)
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
    alert(`Es konnte keine Verbindung zum Server (${configData.SERVER_URL}:${configData.SERVER_PORT}) hergesetellt werden!`)
    return {
      absolute_accuracy_of_selected_speaker: 0,
      is_authenticated: false,
      absolute_accuracy_of_all_speakers: []
    }
  }
}

function App() {
  const [loginDisabled, setLoginDisabled] = useState<boolean>(true);
  const [authenticatingUserId, setAuthenticatingUserId] = useState<number>(NaN);
  const [sampleFileUserId, setSampleFileUserId] = useState<number>(NaN);
  const [sampleFileIndex, setSampleFileIndex] = useState<number>(NaN);
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
      if (!isNaN(authenticatingUserId) && authenticatingUserId >= 0 && authenticatingUserId < 20 && !isNaN(sampleFileUserId) && !isNaN(sampleFileIndex)) {
        setLoginDisabled(false);
      } else {
        setLoginDisabled(true);
      }
    }
    updateLoginStatus();
  }, [authenticatingUserId, sampleFileUserId, sampleFileIndex])

  useEffect(() => {
    updateSong();
  }, [sampleFileUserId, sampleFileIndex])

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
            const result = await login(authenticatingUserId, sampleFileUserId, sampleFileIndex)
            setResults(result);
            setFetching(false);
            setShowResults(result.absolute_accuracy_of_all_speakers.length > 0);
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
            value={authenticatingUserId.toString()} 
            onChange={(e) => {
              const id = parseInt(e.target.value);
              if (id >= 0 && id < 20) {
                setAuthenticatingUserId(id);
              } else {
                setAuthenticatingUserId(NaN);
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
                      className={"fileItem " + (sampleFileUserId === id && sampleFileIndex === fileIndex ? "selected" : "")}
                      onClick={() => {
                        setSampleFileUserId(id);
                        setSampleFileIndex(fileIndex);
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
            !isNaN(sampleFileUserId) && !isNaN(sampleFileIndex) &&
            <div className="audioPlayer">
              <audio controls ref={audioRef}>
                <source src={`./audio_dataset/Speaker${String(sampleFileUserId).padStart(4, '0')}/Validation_Speaker${String(sampleFileUserId).padStart(2, '0')}_${String(sampleFileIndex).padStart(4, '0')}.wav`} type="audio/wav" />
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
            authenticatingUserId={authenticatingUserId}
            selectedFile={{speakerId: sampleFileUserId, sampleId: sampleFileIndex}}
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
