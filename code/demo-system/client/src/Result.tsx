import React from 'react'
import './Result.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faClose, faUser, faFile } from '@fortawesome/free-solid-svg-icons'

export interface ResultProps {
  authenticatingUserId: number;
  selectedFile: {speakerId: number, sampleId: number};
  results: {absulute_accuracy_of_selected_speaker: number, is_authenticated: boolean};
  close: () => void;
}

export default function Result(props: ResultProps) {
  return (
    <div 
      className="resultWrapper"
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          props.close();
        }
      }}
    >
      <div
        className={"resultWindow " + (props.results.is_authenticated ? "authenticated" : "notAuthenticated")}
      >
        <div
          className="content"
        >
          <h2>
            {
              props.results.is_authenticated ?
              "Authentifizierung erfolgreich" : "Authentifizierung fehlgeschlagen"
            }
          </h2>
          <table>
            <tbody>
              <tr>
                <td>
                  Authentifizierung für:
                </td>
                <td>
                  <FontAwesomeIcon icon={faUser} /> {props.authenticatingUserId}
                </td>
              </tr>
              <tr>
                <td>
                  Ausgewählte Datei:
                </td>
                <td>
                  <FontAwesomeIcon icon={faUser} /> {props.selectedFile.speakerId} <FontAwesomeIcon icon={faFile} /> {props.selectedFile.sampleId}
                </td>
              </tr>
            </tbody>
          </table>
          <p>
            Mit einer Wahrscheinlichkeit von <b>{(props.results.absulute_accuracy_of_selected_speaker * 100).toFixed(4)} %</b> gehört die angegebene Datei zu dem zu authentifizierenden Benutzer.
          </p>
          <p>
            {
              props.results.is_authenticated ?
              <span>
                Der definierte Schwellwert von <b>70 %</b> wurde somit überschritten und die Authentifizierung war <b>erfolgreich</b>.
              </span>
              :
              <span>
                Der definierte Schwellwert von <b>70 %</b> wurde somit nicht überschritten und die Authentifizierung war <b>nicht erfolgreich</b>.
              </span>
            }
          </p>
        </div>
        <div
          className="navigation"
        >
          <FontAwesomeIcon 
            icon={faClose} 
            size={"lg"} 
            className="closeIcon"
            onClick={() => {
              props.close();
            }}
          />
        </div>
      </div>
    </div>
  )
}
