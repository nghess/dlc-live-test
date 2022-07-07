import mido
from mido.sockets import PortServer, connect

outport = mido.open_output('Microsoft GS Wavetable Synth 0')

server = PortServer('localhost', 21928)

msg = mido.Message('note_on', note=100, velocity=3, time=6.2)

while True:
    outport.send(msg)
    server.send(msg)