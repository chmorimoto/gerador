
import QtQuick 2.2
import QtQuick.Controls 1.1
import QtMultimedia 5.0

Item {
    id: window
    width: 640
    height: 480

    Rectangle {
        id: root
        anchors.fill: parent
        
        Image { 
		    id: fundo
            anchors.fill: parent
            source: "content/gfx/bateria-completa.png"
		}
    

	ListModel {
		id: myModel

                ListElement {
                        nome: "prato"  
                        px: 163; py: 80
                        wi: 180; he: 100
                        soundSource: "content/audio/prato_conducao1.wav" 
                }
    

                ListElement {
                        nome: "bumbo"  
                        px: 395; py: 365
                        wi: 175; he: 120
                        soundSource: "content/audio/bumbo_medio.wav" 
                }
    

                ListElement {
                        nome: "caixa"  
                        px: 453; py: 200
                        wi: 140; he: 120
                        soundSource: "content/audio/caixa.wav" 
                }
    
	}
 
      Component {
            id: myDelegate
            Rectangle {
                id: wrapper
                x: px ; y: py
                width: wi; height: he
                color: '#ffff00'
                opacity: 0.3
                radius: 35
                Text {
                    anchors.centerIn: parent
                    text: nome
                }
                SoundEffect {
                    id: playSound
                    source: soundSource
                }
                MouseArea {
                    anchors.fill: parent
                    onPressed: {
                        playSound.play()
                    }
                }
            }
        }
                

        PathView {
            id: pathV
            anchors.fill: parent
            model: myModel
            delegate: myDelegate

            preferredHighlightBegin: 0
            preferredHighlightEnd: 0
            highlightRangeMode: PathView.NoHighlightRange

            focus: true
            Keys.onLeftPressed: decrementCurrentIndex()
            Keys.onRightPressed: incrementCurrentIndex()

            Timer{
                id: timer
                interval: 1000; running: false; repeat: true;
                onTriggered: {pathV.incrementCurrentIndex()}
            }
            path: Path {
                startX: myModel.get(0).px 
                startY: myModel.get(0).py           

		PathLine{ x: myModel.get(1).px; y: myModel.get(1).py}
		PathLine{ x: myModel.get(2).px; y: myModel.get(2).py}
		PathLine{ x: myModel.get(0).px; y: myModel.get(0).py}
		}
	}
	}
}
