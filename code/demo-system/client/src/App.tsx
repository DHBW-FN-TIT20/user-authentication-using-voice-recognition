import React, { useEffect, useState } from 'react';
import'./App.css';

async function login(userId: number, selectedUserId: number, selectedFileIndex: number) {
  const response = await fetch(`http://127.0.0.1:5500/?speaker_id=${userId}&sample_id=${selectedFileIndex}&selected_speaker_id=${selectedUserId}`);

  if (!response.ok) {
    console.log(response)
    return false;
  }

  const json = await response.json();

  console.log(json)
  
  return true;
}

function App() {
  const [loginDisabled, setLoginDisabled] = useState<boolean>(true);
  const [userId, setUserId] = useState<number>(NaN);
  const [selectedUserId, setSelectedUserId] = useState<number>(NaN);
  const [selectedFileIndex, setSelectedFileIndex] = useState<number>(NaN);
  
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

  return (
    <div className="App">
      <form
        onSubmit={async (e) => {
          e.preventDefault();
          setLoginDisabled(true);
          await login(userId, selectedUserId, selectedFileIndex);
          setUserId(NaN);
          setSelectedUserId(NaN);
          setSelectedFileIndex(NaN);
        }}
        className="loginForm"
      >
        <div
          className="fileList"
        >
          {
            // create an array with all numbers from 0 to 20
            Array.from(Array(20).keys()).map((id) => {
              return (
                <div key={"fileSpeaker" + id}>
                  {
                    Array.from(Array(9).keys()).map((fileIndex) => {
                      return (
                        <div 
                          key={"speaker" + id + "file" + fileIndex}
                          className={"fileItem " + (selectedUserId === id && selectedFileIndex === fileIndex ? "selected" : "")}
                          onClick={() => {
                            setSelectedUserId(id);
                            setSelectedFileIndex(fileIndex);
                          }}
                        >
                          Speaker {id} File {fileIndex}
                        </div>
                      )
                    })
                  }
                </div>
              )
            })
          }
        </div>
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
        <button 
          disabled={loginDisabled}
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default App;
