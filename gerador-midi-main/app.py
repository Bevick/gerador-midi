from flask import Flask, request, send_file
from midiutil import MIDIFile

app = Flask(__name__)

@app.route('/gerar_midi', methods=['POST'])
def gerar_midi():
    # Recebe os dados enviados pelo ChatGPT
    data = request.json
    bpm = data.get("bpm", 120)
    notas = data.get("notas", [])

    # Criar o arquivo MIDI
    midi = MIDIFile(1)
    track = 0
    midi.addTrackName(track, 0, "Generated Track")
    midi.addTempo(track, 0, bpm)

    for nota in notas:
        pitch, start_time, duration = nota
        midi.addNote(track, 0, pitch, start_time, duration, 100)

    # Salvar o arquivo MIDI
    file_name = "musica.mid"
    with open(file_name, "wb") as file:
        midi.writeFile(file)

    # Retornar o arquivo gerado
    return send_file(file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
