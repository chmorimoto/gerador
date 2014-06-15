#!/usr/bin/env python3

############################################################

## Copyright (c) 2008, Universidade de Sao Paulo
## All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions 
## are met:

##  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer 
##    in the documentation and/or other materials provided with the distribution.
##  - Neither the name of the Universidade de Sao Paulo nor the names of its contributors may be used to endorse or promote products 
##    derived from this software without specific prior written permission.


## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT 
## NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
## THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
## (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
## HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

############################################################

import sys
import os.path
import json

# ============================================================

class Fundo:
    def __init__(self, w, h, img):
        self.w = w
        self.h = h
        self.sourceImg = img

# ============================================================

class Objeto:
    def __init__(self, idNome, x, y, w, h, t="", som=""):
        self.id = idNome
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = t
        self.sourceSom = som

# ============================================================

def main (arqEntrada = None, arqSaida = None):
    '''
    modo V -> varredura
    '''
    if arqEntrada is None:
        arqEntrada = input("Nome do arquivo de entrada: ")
    if arqSaida is None:
        arqSaida = input("Nome do arquivo de saida: ")
        
    qml = []
    # fundo: size, imagem.source
    fundo, objs = le_configuracao(arqEntrada)

    monta_cabecalho(qml, fundo)
    monta_ListModel(qml, objs)
    monta_Delegate(qml)
    monta_View(qml, objs)
        
    qml.append("\t}")
    qml.append("}")
    grava_jogo(arqSaida, qml)

        
# ============================================================
# ============================================================

def grava_jogo(nome_arquivo, jogo_qml):
    '''
    '''
    arq = open(nome_arquivo, 'w')
    for lin in jogo_qml:
        arq.write(lin + "\n")

    arq.close()

# ============================================================

def monta_View(qml, objs):
    view = """
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
"""
    qml.append(view)
    for i in range(len(objs)):
        qml.append("\t\tPathLine{ x: myModel.get(%d).px; y: myModel.get(%d).py}"%((i+1)%len(objs),(i+1)%len(objs)))
    qml.append("\t\t}")
    qml.append("\t}")
                   
    
# ============================================================

def monta_ListElement(qml, obj):
    '''
    '''
    elem = """
                ListElement {
                        nome: "%s"  
                        px: %s; py: %s
                        wi: %s; he: %s
                        soundSource: "%s" 
                }
    """%(
        str(obj.id),
        str(obj.x), str(obj.y),
        str(obj.w), str(obj.h),
        obj.sourceSom
        )
    qml.append(elem)

# ============================================================

def monta_ListModel(qml, objs):
    qml.append("\n\tListModel {")
    qml.append("\t\tid: myModel")
    for obj in objs:
        monta_ListElement(qml, obj)
    qml.append("\t}")

# ============================================================

def monta_Delegate(qml):
    delegate = """ 
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
                """
    qml.append(delegate)
        
# ============================================================

def monta_cabecalho(qml, fundo):
    ''' 
    Coloca no doc qml:
    - imports 
    - cria uma janela
    - carrega a imagem de fundo
    '''
    # monta cabecalho
    cab = """
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
            source: "%s"
		}
    """ %(fundo.sourceImg)
    
    qml.append(cab)
    
# ============================================================

def le_configuracao(arqEntrada):
    arq_json = open(arqEntrada, "r")
    json_str = arq_json.read()
    decoder = json.JSONDecoder()
    json_obj = decoder.decode(json_str)
    fundo_json = json_obj["fundo"]

    # le fundo do arquivo
    f = Fundo(fundo_json["width"], fundo_json["height"], fundo_json["source_img"])

    # le objetos
    objs_json = json_obj["objs"]
    objs = []
    for obj_json in objs_json:
        # cria objeto 
        new_obj = Objeto(obj_json["id"], obj_json["x"], obj_json["y"], obj_json["width"], obj_json["height"], som=obj_json["source_sound"])
        objs.append(new_obj)
            
    return f, objs

# ============================================================

if __name__=="__main__":
    main()
