import React from 'react'
import './Info.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClose } from '@fortawesome/free-solid-svg-icons';

export interface InfoProps {
  close: () => void;
}

export default function Info(props: InfoProps) {
  return (
    <div className='infoWrapper'
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          props.close();
        }
      }}
    >
      <div className='infoWindow'>
        <h2>Info</h2>
        <div className='content'>
          <h3>Studienarbeit</h3>
          <p>
            Im Rahmen unserer Studienarbeit haben wir uns mit der Thematik der Sprachauthentifizierung beschäftigt.
            Dafür haben wir verschiedene Features aus Sprachaufnahmen extrahiert mit denen wir anschließend ein neuronales Netz trainiert haben.
            Aus einer Vielzahl an Features haben wir in einer ausführlichen Auswertung die besten Features ausgewählt (20 MFCC + 20 delta MFCC bei 15000 Frames a 600 Samples).
          </p>
          <h3>Applikation</h3>
          <p>
            Mit diesen Features wurde ein neuronales Netz mit 20 verschiedenen Sprechern trainiert, welches im Backend dieser Applikation zum Einsatz kommt.
            In der Oberfläche können Sie sich nun als eine der 20 Personen authentifizieren.
            Dazu geben Sie die zu authentifizierende <b>userId</b> (0-19) in das Eingabefeld ein.
            Anschließend können Sie aus einer Vielzahl an Sprachaufnahmen für die verschiedenen Sprecher eine Aufnahme auswählen die für die Authentifikation verwendet werden soll.
            Nachdem Sie auf <b>Login</b> geklickt haben, wird die Authentifikation durchgeführt und das Ergebnis angezeigt.
          </p>
          <h3>Fragen</h3>
          <p>
            Bei Fragen wenden Sie sich bitte direkt an uns.
          </p>
        </div>
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
  )
}
