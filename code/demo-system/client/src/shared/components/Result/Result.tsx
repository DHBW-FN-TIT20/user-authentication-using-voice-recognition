/**
 * @file Result.tsx
 * @author Henry Schuler
 */
import React from 'react'
import './Result.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faClose, faUser, faFile } from '@fortawesome/free-solid-svg-icons'
import { Line } from 'react-chartjs-2'

export interface ResultProps {
  authenticatingUserId: number;
  selectedFile: {speakerId: number, sampleId: number};
  results: {absolute_accuracy_of_selected_speaker: number, is_authenticated: boolean, absolute_accuracy_of_all_speakers: number[]};
  close: () => void;
}

/**
 * A pop-up for displaying the authentication result from the server (text and line chart)
 * @param props Passes required values for displaying the information as well as a function reference for closing the pop-up
 * @returns JSXElement
 */
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
            Mit einer Wahrscheinlichkeit von <b>{(props.results.absolute_accuracy_of_selected_speaker * 100).toFixed(4)} %</b> gehört die angegebene Datei zu dem zu authentifizierenden Benutzer.
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
          <div className="chart">
            <Line 
              data={{
                labels: Array.from(Array(20).keys()),
                datasets: [
                  {
                    label: 'Zuordnungswahrscheinlichkeit',
                    data: props.results.absolute_accuracy_of_all_speakers,
                    pointRadius: 6,
                    pointBackgroundColor: Array(20).fill("").map((color, index) => index === props.authenticatingUserId ? (props.results.is_authenticated ? "#03AC13B0" : "#FF000090") : "#22222240 "),
                  },
                  {
                    label: 'Schwellwert',
                    data: Array(20).fill(0.7),
                    borderColor: 'rgba(255, 0, 0, 1)',
                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                    pointRadius: 0,
                  }
                ],
              }}
              options={{
                maintainAspectRatio: false,
              }}
            />
          </div>
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
